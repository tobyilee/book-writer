
## 05장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- 스택 PR "2026년 9월 기준으로는 아직 preview" — 원고에 이미 시점 명기. GitHub Changelog(2026-07-30 public preview)·Docs 검색으로 2026-09 현재 GA 공지 없음 확인, 유지
### ✅ 확인 (요약)
- `(사실 확인 필요)` 해소: Draft PR의 CODEOWNERS 알림 억제·"Ready for review" 전 머지 불가 — GitHub Changelog 2019-02-14 원문("Draft pull requests suppress notifications to CODEOWNERS reviewers", "cannot be merged until they are marked as 'Ready for review'") 대조 일치. 주석만 제거
- Sadowski 2018 수치 7건(24줄·35%·90%·10%·900만 건·1h/5h·4시간 미만), Google small CLs 인용 2건·30분/5분·200줄/50파일, Bosu 150만, Kudrjavets 845,316/401,790/100개·10개 언어·인용문, di Biase 28명, Gousios 13%/53%(2012~2013 데이터 명기), Bacchelli 인용, Draft PR 2019-02·2025-05-01, gh-stack 명령·머지 동작·merge queue 점진 배포, TWICE·jenadine·GeekNews 재승인 불만, DEVOCEAN 인용·템플릿 3칸 — 01_reference.md §1.5·1.6·2.1·2.2·2.4·4.2·4.5와 일치
### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- 자동 머지 전제 보완: "PR에 자동 머지를 켜 두면" → "저장소 설정에서 자동 머지를 허용해 두고 PR에 자동 머지를 켜 두면" — GitHub Docs "Automatically merging a pull request"("Before you use auto-merge, it must be enabled for the repository.")
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 2건 해소: (1) 자동 머지 동작 — Docs "Auto-merge merges a pull request automatically after all required reviews and status checks pass." 일치(위 전제 보완 외 유지). (2) 토스페이먼츠 성과 — toss.tech/article/25431(2024-02-07) 원문 "평균적으로 PR 리뷰가 되는 시간이 하루 내외로 짧아졌고", "코멘트 수도 평균적으로 2배 이상 많아졌어요", 평일 오후 2시 리마인더 일치. "보고했다" 귀속 유지
- Bacchelli & Bird 수치 6건·인용, Mäntylä 75%, Beller 1,400건·75:25·7~35%·10~22%, Sadowski 도입 동기 인용·리뷰어 중앙값 1명·25%·Finding 4 인용·승인 시간 비교 5건·80%, Rigby & Bird 66~150%·2명 수렴, McIntosh 2/5개, Bosu 첫해, Tsay 2014, Kudrjavets 2022b 29~63%·인용, Nudge 147/8,500/60%/73%/8,000/210,000, Shan 84.7%·p75 24시간, 코멘토 2024, DEVOCEAN 인용·Pn/D-n·09시, HN Theatre(2025-09경)·nitwit005 인용, Gousios 2015 749명, 우아한테크세미나 2022 — 01_reference.md §2.1·2.2·2.3·2.4·3·4.4·4.6과 일치
### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — Travis 시대 데이터 한계는 원고에 이미 명기)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 해소: Google 블로그 flaky 16% — Micco 2016-05-27 원문(Blogger 피드로 본문 추출) "Almost 16% of our tests have some level of flakiness associated with them!" 일치. 2차 인용이 아니라 원문 확인됨. 원고는 16%(테스트 중 flaky 비율)와 Luo 재인용 4.56%(실패 중 flaky 비율)를 분모가 다르다고 분리 서술하고 1.5%는 쓰지 않아 집필 규율 준수. 주석만 제거
- Vasilescu 246/20.5%/42.3%·인용, Hilton 2016 34,544/1,529,291/442·0.54 대 0.24·5.2/6.8/1.6시간·87.71/79.61/47.00/44.12%·디버깅 인용, Bernardo 2018 87/162,653/51.3%·2023 확장판 450건·인용, Kinsman 2021·Wessel 2023 방향, Release Flow 60,000/5분·200건 PR, Hilton 2017 Assurance 축, Memon 2017 13,000/1억 5천만/초당 1건/45분/550만 중 91.3%·인용, Machalica 2019 절반/95%/99.9%, Luo 51/201·45/20/12%·54%·78%·96%·4.56%(160만 중 7.3만, 10회 재실행 기준)·인용, Parry 2022, HN smarterclayton·mdoms·hinkley·l0b0·"painkiller"(2026-02경), Shopify 실패 허용 임계값, Discussion #168145, Henderson 2023 13,000건 — 01_reference.md §2.5·2.6·2.7·3·4.3·research/web.md와 일치
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — 시점 명기 이미 충분)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: 2026-04-23 스쿼시 사고 "커밋은 Git에 남아 데이터 손실 없음" — GitHub Blog "An update on GitHub availability"(Vlad Fedorov, 2026-04-28) 원문 "There was no data loss: all commits remained stored in Git." 확인. 주석 삭제, "닷새 뒤 블로그에서 설명했다"로 출처 시점 명기. 시간창(16:05~20:43 UTC)·조건(squash + 그룹 2개 이상)·원인(feature flag 게이팅 누락된 머지 베이스 계산 경로)·비영향 범위(merge/rebase 그룹, 큐 밖 PR)는 Discussion #193645 인시던트 요약과 일치. 규모 수치는 블로그 658 repos/2,092 PRs vs 스레드 요약 230 repos vs HN 인용 2,804 PRs로 여전히 엇갈려 본문의 생략 판단 유지.
- GitHub 사내 train(최대 15개, 8+ hours)·30,000+ PR/450만 CI·33%·30개 이상 동시 배포·인용문 — 01_reference §3.1, research/web.md와 일치.
- Shopify 2018(90% 이상, 인용문)·2019(predictive branch, batch size 8, "Master must always be green") — 일치.
- Block 인용, Lobsters 2026-07-27 두 인용(elijahpotter·byroot) — 일치.
- Not Rocket Science Rule 2014 2차 인용 고지, bors-ng 2023-04-30 "feature frozen and deprecated" — 일치.
- SubmitQueue EuroSys 2019, 5%→40%(슬라이드), 2^n, iOS 52%("Uber 보고에 따르면" 귀속 유지) — 일치.
- GitHub Docs 정의문, GA 공지 인용(2023-07), 큐 제거 사유 4가지, `gh-readonly-queue/`, `merge_group` — 일치.
- Kudrjavets 2022b 29~63%·자동 머지 권고 — 일치.
### 미해소
- (없음)

## 13장 (라운드 1)

### ❌ 정정
- "Team 플랜 private 저장소 가용 여부는 공식 문서로 확인하지 못했다(사실 확인 필요) … 아직 지원하지 않는 것으로 보이지만" → "2026년 9월 기준 GitHub Docs도 같은 범위(조직 소유 public 저장소, GitHub Enterprise Cloud 조직의 private 저장소)를 적는다. Team 플랜의 private 저장소는 여기에 들지 않는다" — 근거: GitHub Docs "Managing a merge queue" 가용성 문구 "Pull request merge queues are available in any public repository owned by an organization, or in private repositories owned by organizations using GitHub Enterprise Cloud." (2026-09-26 조회)
- "룰셋에서 같은 규칙을 켠다(사실 확인 필요)" → 룰셋 "Require merge queue" 규칙 존재 확인 + "저장소 수준 룰셋에만 있고 조직 수준 룰셋에서는 쓸 수 없다" 제약 추가 — 근거: GitHub Docs "Available rules for rulesets" (enterprise-cloud@latest) "Require merge queue … This rule is not available for rulesets created at the organization level."
- #168145 오귀속: flaky 테스트 증폭의 사례로 인용됐으나, 토론 원문은 워크플로가 `merge_group`과 `gh-readonly-queue/` 브랜치 push 양쪽에 반응해 중복 런이 서로를 취소한 사례(해법: `branches-ignore`에 `gh-readonly-queue/**`). flaky 문단에서 인용을 빼고 일반 서술로, 해당 토론은 concurrency·트리거 문단으로 옮겨 실제 내용대로 서술 — 근거: github.com/orgs/community/discussions/168145
- #151100 "공식적으로 확인된 동작은 아니다(사실 확인 필요)" → 2025-02 보고 내용(머지 큐가 pull_request 이벤트의 `ci_done`을 보고 머지), 참여자가 전한 GitHub 지원팀 답변(CI 실행을 줄이려던 변경의 부작용, 롤백), 이후 재발 보고까지 사실대로 서술 — 근거: discussions/151100 원문 (2025-02-10 원글, 02-14 지원팀 답변 전달, 02-25~26 재발 댓글)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- GitLab 머지 트레인: "커뮤니티에서는 Premium 이상 전용이라는 이야기(사실 확인 필요)" → "GitLab 문서 기준 Premium·Ultimate 티어에서만 쓸 수 있는 기능이니(2026년 9월 기준)" — 근거: docs.gitlab.com/ci/pipelines/merge_trains "Tier: Premium, Ultimate"
### ✅ 확인 (요약)
- `(사실 확인 필요)` 6건 모두 해소 (위 4건 + 아래 2건).
- 머지 큐 설정에서 머지 방식 선택: GitHub Docs "Merge method: Select which method to use when merging queued pull requests: merge, rebase, or squash." 확인 — 주석 삭제, "(merge·rebase·squash)" 병기.
- concurrency `group: ${{ github.head_ref || github.run_id }}`와 merge_group: Docs contexts "github.head_ref … only available when the event … is either pull_request or pull_request_target" 확인 — 원고 논리 맞음. 근거 한 문장 추가, 주석 삭제.
- 표 1 설정 4항목·범위 1~100·Merge limits 대기 시간 의미·Only merge non-failing 의미 — Docs와 일치. 기본값 미기재 유지(집필 규율).
- #15254 원글 인용·2026년 AWAITING_CHECKS ~23 PRs, #14801 인용 2건과 처리량 예(8 PRs/30분/2-build → 2시간), HN 36707239 "doubly expensive", Mergify two-step·배치 분할, jump-to-front 경고·관리자 기본값, `merge_group` 활동 유형 `checks_requested`, 서드파티 CI `gh-readonly-queue/{base_branch}`, 스택 PR 2026-07-30 public preview 인용 — 01_reference·research와 일치.
- YAML 예제: 문법 유효, SHA 자리표시 규약 준수.
### 미해소
- (없음)

## 14장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — "2026년 9월 기준"·"2026년 1월 갱신판 기준" 이미 명기)
### ✅ 확인 (요약)
- 배포 환경 required reviewers·wait timer의 Free/Pro/Team public 한정, 머지 큐 GA 시점 조직 소유 public 저장소 가용 — 01_reference §2·§2.11, GitHub Docs(13장 확인분)와 일치.
- Driessen 2020 노트("explicitly versioned", "panaceas don't exist"), Release Flow 핫픽스 main 우선·cherry-pick — 일치.
- DORA 5지표 명칭·2026-01 갱신판 — 01_reference §1.9와 일치.
- concurrency `queue` 2026-05, `pull_request_target` 2025-12-08 동작 변경, 2025-12 셀프호스트 러너 요금 발표·연기 — 일치.
- 에이전트 PR 프리프린트: arXiv:2607.04697(Xu·Subramanian·Karthik, 2026-07-06 제출) 실재 확인, 본문은 식별자·수치 없이 방향만 서술하고 동료 심사 미확인 고지 — 적절. carlana(Lobsters) 인용 일치.
### 미해소
- (없음)

## 01장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — DORA 표는 이미 "2026-01 갱신판" 명시)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 해소: 실패 배포 복구 시간 = **처리량** 분류 맞음. dora.dev/guides/dora-metrics (Last updated 2026-01-05) "DORA uses three factors to measure software delivery throughput: … Failed deployment recovery time" — 처리량 3(리드 타임·배포 빈도·복구 시간) + 불안정성 2(변경 실패율·재작업률). 주석만 제거.
- 인용 5건(Shopify 2018, Fowler 2020 ×3, Bird & Zimmermann 8.9일/0.04건, Shihab 2012) — research/web.md 자료 48·papers.md·01_reference §2.10과 일치. Ghiotto 10~20%는 재인용 표기 유지.
- DORA 정의문 5건 — 01_reference §1.9와 일치.
### 표시 보강
- 오프닝 calculateFee 장면이 실제 사고처럼 읽혀 "가상의 장면이지만 어느 팀에서나 일어날 수 있는 일이다." 한 문장 추가.
### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- 비교표 TBD 핫픽스 경로 "트렁크에서 고쳐 릴리스 브랜치로 (사실 확인 필요)" → "트렁크에서 먼저 고친 뒤 릴리스 브랜치로 체리픽" — 근거: trunkbaseddevelopment.com/branch-for-release "reproduce the bug on the trunk, fix it there with a test … then cherry-pick that to the release branch" (웹 2차 확인)
- 비교표 OneFlow 핫픽스 경로 "릴리스 태그 기준 브랜치에서 (사실 확인 필요)" → "최신 버전 태그에서 핫픽스 브랜치 → 태그 후 영원한 브랜치로 머지" — 근거: Adam Ruka, endoflineblog.com OneFlow 원문 "Hotfix branches are cut from the commit that the latest version tag points to." 마무리는 tag → merge to master (웹 2차 확인)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — GitHub Docs 인용은 "2026년 9월 조회 기준" 명시)
### ✅ 확인 (요약)
- Driessen 2020-03 노트 인용 2건·요지 2건, 2010 원문 master/develop 정의·`--no-ff` — research/web.md 자료 32와 일치. "열여섯 살이 넘었다"(2010-01→2026-09) 맞음.
- GitHub Flow 6단계·브랜치 삭제 인용, Microsoft "often overlooked part of GitHub Flow" — web.md 자료 14·01_reference §1.7과 일치.
- GitLab Flow 인용 2건, TBD 정의·단기 브랜치·릴리스 브랜치·DORA 기준 인용, OneFlow 인용 3건, Release Flow 인용, Fowler 2건 — 01_reference §1.7·§2.10과 일치.
- 커뮤니티 인용 3건(Lobsters bkircher·skade 2020, HN SAI_Peregrinus "two weeks") — research/community.md와 일치.
### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- 배민 안드로이드 인용 "2016년 1월에 Github로 … 사용하기 시작했으나, 2017년 6월부터 Git-flow로 … 되었습니다." (요약 발췌를 한 문장으로 합친 비원문) → 원문 문장 "2016년 1월, Github로 소스코드를 이전하면서 Github-flow를 사용하기 시작했습니다." 인용 + "2017년 6월부터 Git-flow로 브랜치 전략을 바꿨다" 서술로 분리 — 근거: techblog.woowahan.com/2553 원문 대조. 팀 2~3명→5명, Upstream/Origin/Local, squash·rebase, 작성자 직접 머지도 원문 확인.
- 맘시터 수치 "하루 5회 이상 배포 … 300줄 미만(사실 확인 필요)" → "하루 평균 5건 안팎의 배포 … PR은 대개 300줄 이하" — 근거: tech.mfort.co.kr 원문 "일반적으로는 하루 평균 5건 내외의 배포가 발생합니다", "PR은 일반적으로 300줄 이하의 변경사항을 가져" (웹 2차 확인). "이상"은 원문과 불일치.
- 맘시터 "주 단위의 작은 증분" → "한 달 걸릴 작업이라도 일주일에 한 번씩 나눠 배포하는 식" — 원문은 예시("한 달이 걸릴 작업 하나를 일주일에 한번 배포하는 방식으로 쪼개서")로 제시.
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음)
### ✅ 확인 (요약)
- Release Flow 인용 3건·"하루 200개가 넘는 PR" — web.md 자료 14와 일치.
- Hodgson 2017 토글 4분류·인용 2건, Rahman 2016(Chrome 릴리스 39개·5년) — web.md 자료 39·papers.md와 일치.
- 오프닝 앱 팀·코드·YAML은 "해보자"/"예시 형식"으로 가상임이 드러나 있어 보강 불요.
### 미해소
- (없음)

## 04장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- 룰셋 정의 뒤 "조직 단위로 걸 수 있는 범위는 플랜에 따라 다르니" → 플랜 조건이 조직 단위 룰셋에 걸린다는 점과 저장소 룰셋 가용성(Free=공개 저장소만, Pro·Team·Enterprise Cloud=비공개 포함)을 명시 — 근거: GitHub Docs managing-rulesets 페이지 "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." (웹 2차 확인). 정의문만으로는 룰셋 자체가 Team 이상 전용으로 읽힐 위험.
### 🕒 신선도
- 평가 모드 "이것은 Enterprise Cloud 전용이다" → "발표 당시 기준으로 Enterprise Cloud 전용이었다" (근거가 2023 GA 체인지로그)
- 룰셋 가용성 서술에 "2026년 9월 GitHub Docs 기준" 부기
### ✅ 확인 (요약)
- 보호 규칙 설정 항목 12개, stale 승인·선형 이력·관리자 포함·strict/loose 인용 — 01_reference §1.1과 일치.
- 룰셋 정의문(원문 그대로 재확인), 75/75 한도, 겹침·최엄격 규칙, enforcement 변경, read 권한 열람, 2023-04-17 beta / 07-24 GA, required reviewer rule 2026-02-17 GA·`!` 지원·CODEOWNERS 공존 인용 — 01_reference §1.2·web.md 자료 2와 일치.
- CODEOWNERS 위치·탐색 순서·마지막 패턴 우선·미지원 문법·3MB·쓰기 권한·any owner 승인, workflows 디렉터리 권고 — §1.3과 일치. "코드 오너 리뷰 요구" 설정(Require review from Code Owners)이 리뷰 필수 규칙의 하위 옵션이라는 서술 맞음.
- 머지 방식 3종 인용·리베이스 머지 SHA/서명 함정 — §1.4와 일치.
- HN·커뮤니티 인용 5건(JoshTriplett, William_BB, cj 요지, burntsushi, kdmccormick) — research/community.md 논쟁 B와 일치. 12장 squash 머지 그룹 사고 교차 참조(2026-04-23) 원장과 일치.
### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- 예제 액션 메이저 버전 `actions/checkout@v5`·`actions/setup-node@v5` → `@v7` (7곳) — 근거: GitHub 릴리스 페이지 1차 확인(2026-09-26 조회). **확인값: actions/checkout 최신 v7.0.1(2026-07-20), actions/setup-node 최신 v7.0.0(2026-07-14).** 8~9장 예제도 같은 값 사용 권장. 참고: checkout v7은 pull_request_target·workflow_run에서 fork PR 체크아웃을 차단하는 변경 포함(릴리스 노트)
### ⚠️ 약화·삭제
- 맺음말 tj-actions "2만 개가 넘는 저장소" → "2만 개가 넘는 저장소(보안 업체 추정)" — 01_reference §3.3 "23,000개 이상(보안업체 추정)"에 맞춰 귀속 명기
### 🕒 신선도
- OIDC subject 예시 뒤에 신형식 고지 추가: 2026-07-15 이후 생성 저장소의 기본 sub가 `repo:octo-org@123/octo-repo@456:ref:refs/heads/main`(불변 ID 포함), 기존 저장소는 opt-in — 근거: GitHub Changelog 2026-04-23 "Immutable subject claims for GitHub Actions OIDC tokens"(2026-06-10 editor's note로 구분자 `@` 확정). 11장 검증 중 발견해 10장 final에 소급 반영
- 그 외 시점 명기는 원고에 이미 충분(비교표·environments "2026년 9월 GitHub Docs 기준", queue "2026년 5월")
### ✅ 확인 (요약)
- `(사실 확인 필요)` 5건·HTML 메모 전부 해소, 메모 삭제:
  - 복합 액션 `run` 스텝 `shell` 필수 — Docs metadata syntax "`runs.steps[*].shell` … required if `run` is set", composite에 defaults 미지원. 근거 한 문장 보강
  - 복합 액션 시크릿 — Docs "Reusing workflow configurations" 비교표 composite "Cannot use secrets" 원문 대조. 표 문구를 "시크릿을 직접 쓰지 못하고 입력값으로 전달"로, 본문에 원문 인용 추가
  - 재사용 워크플로 체크 이름 "호출자 잡 / 호출된 잡" — Docs 본문에 명시 문장은 없으나 Community Discussion #46752·#72708 등 보고와 일치(동작 서술로 유지, 인용 없음)
  - 호출된 워크플로 권한이 호출자 범위를 넘지 못함 — Docs "Reuse workflows" "permissions can only be maintained or reduced—not elevated—throughout the chain." 인용 추가
  - OIDC `id-token: write` — Docs OIDC reference "The job or workflow must grant the `id-token: write` permission…", "Without `id-token: write`, the OIDC JWT ID token cannot be requested." 확인. 잡 수준 `permissions`가 워크플로 수준을 대체한다는 점 한 문장 보강(예제가 잡에 `contents: read`를 반복하는 이유)
  - 잡 수준 `concurrency`의 `queue: max` — Changelog 2026-05-07 "up to 100 queued jobs or workflow runs per concurrency group", `cancel-in-progress` false/미설정 조건. 예제(잡 수준, cancel-in-progress 없음) 유효
- 재사용 워크플로 `workflow_call`·잡 수준 호출·`inherit` 인용, 10단계·순환 금지, 복합 액션 10개 중첩·한 스텝 로깅·Marketplace, environments(승인자 6·자기 승인 금지 인용·wait timer 1~43,200분·보호 규칙 6개·환경 시크릿 잠금 인용·Free/Pro/Team public 한정), OIDC 인용 2건·subject 예 2개, Valenzuela-Toledo 2024 약 200개, Rostami Mazrae 2026(arXiv:2602.14572, 프리프린트 고지) 49K·2019-11~2025-08·중앙값 3·7.3%, queue 기본 동작·최대 100, GitHub Flow 배포 시점 Microsoft 귀속 — 01_reference §2.8·2.9·research/web.md와 일치. 재사용 워크플로 파일당 호출 한도 수치는 원고에 없음(규율 준수)
### 미해소
- (없음)

## 08장 (라운드 1)

**액션 메이저 버전 확인값 (2026-09-26, GitHub API `repos/actions/*/releases/latest` 1차 확인 — 10~11장과 공유):** `actions/checkout` v7 (v7.0.1, 2026-07-20) · `actions/setup-node` v7 (v7.0.0, 2026-07-14) · `actions/cache` v6 (v6.1.0, 2026-06-26) · `actions/upload-artifact` v7 (v7.0.1, 2026-04-10) · `actions/download-artifact` v8 (v8.0.1, 2026-03-11). 업로드·다운로드 아티팩트의 메이저가 서로 다르다는 점 주의. 참고(11장용): checkout v7 릴리스 노트에 "block checking out fork pr for pull_request_target and workflow_run"(PR #2454)이 포함됨.

### ❌ 정정
- 예제 YAML 5곳 `actions/checkout@v5`·`actions/setup-node@v5` → `@v7` — 근거: 위 GitHub 릴리스 1차 확인.
- "cron 시각은 … UTC 기준으로 해석되니" → "따로 지정하지 않으면 … UTC 기준" + "2026년 9월 GitHub Docs 기준 `timezone` 키로 IANA 시간대 지정 가능" 부기 — 근거: GitHub Docs events-that-trigger-workflows "By default, scheduled workflows run in UTC. You can optionally specify a timezone using an IANA timezone string" (웹 2차).
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- 액션 버전 안내문에 "2026년 9월 기준 최신값(checkout·setup-node 모두 v7)" 명기.
### ✅ 확인 (요약)
- 저술가 메모 문법·동작 6건: `$GITHUB_OUTPUT` 스텝 출력, 잡 기본 병렬("run in parallel by default"), `if: always()` 상태 함수, 잡 수준 `permissions`(명시하면 나머지는 `none` — 본문에 한 문장 보강), 필수 체크 이름=잡 이름("대개"로 헤지돼 있어 유지), schedule UTC 기본 — GitHub Docs workflow-syntax 대조(웹 2차). HTML 메모 삭제.
- 한도 표 6행(6시간·35일·256개·24시간·동시 잡 20/40/60/500·토큰 1,000/15,000), 브랜치 글롭 필터, fork PR 시크릿 인용, `workflow_run` 인용, permissions 키 "열 개가 넘는다"(원장 16개), 2023-02 기본 read-only 전환 — 01_reference §2.8·§2.9와 일치.
- Saroar & Nayebi 2023(90명, 60.87%), HN "진짜 프로그래밍 언어를 쓰라"(tcoff91) — §2.8·§4.9와 일치. 토스 평일 오후 2시 리마인더 — §3.5와 일치.
### 미해소
- (없음)

## 09장 (라운드 1)

(액션 버전 확인값은 08장 섹션 참조 — checkout v7 · setup-node v7 · cache v6 · upload-artifact v7 · download-artifact v8, 2026-09-26 GitHub API 1차 확인)

### ❌ 정정
- 예제 YAML `actions/checkout@v5`·`setup-node@v5` → `@v7`, `actions/cache@v4` → `@v6`, `upload-artifact@v4` → `@v7`(2곳), `download-artifact@v4` → `@v8` — 근거: GitHub 릴리스 1차 확인. download v8은 해시 불일치 시 기본 `error`로 바뀌었으나 예제 입력(`name`·`path`)은 그대로 유효.
- "GitHub는 며칠 만에 … 연기" → "이틀 만에" — 근거: 01_reference §2.8·§3.4, research/community.md (2025-12-16 발표 → 12-17~18 연기).
- "용량이 차면 오래된 항목부터" → "마지막으로 쓰인 지 오래된 항목부터" — 근거: GitHub Docs dependency-caching "deleting the caches in order of last access date, from oldest to most recent" (웹 2차).
- 건너뛴 잡의 필수 체크 취급(사실 확인 필요, 조건문) → 단정으로 교체: "GitHub Docs에 따르면 건너뛴 잡은 상태를 'Success'로 보고하고, 필수 체크여도 머지를 막지 않는다" — 근거: Docs control-jobs-with-conditions·status-checks "A job that is skipped will report its status as 'Success'. It will not prevent a pull request from merging, even if it is a required check." (웹 2차). 앞 문장은 "`needs`의 눈으로 보면 건너뛴 잡은 성공이 아니다"로 범위 한정(두 서술 충돌 방지).
### ⚠️ 약화·삭제
- 셀프호스트 요금 재도입 여부(사실 확인 필요) → "2026년 중반까지 시행되지 않은 상태로 알려져 있지만, 재도입 여부는 GitHub 공지를 직접 확인하자" — 근거: research/community.md "2026년 중반 기준 미시행", 2차 보도(samexpert 등 "shelved") 일치. 공식 철회 공지는 미확인이라 "알려져 있다" 수준 유지.
### 🕒 신선도
- 아티팩트 액션 문단에 "2026년 9월 기준 최신은 upload-artifact v7, download-artifact v8"과 두 메이저가 짝이 아니라는 점 명기.
- `queue: max`는 원고에 이미 "2026년 5월에 새 옵션"으로 시점 명기 — Docs workflow-syntax(`single` 기본, `max` 최대 100) 및 Changelog 2026-05-07과 일치.
### ✅ 확인 (요약)
- 저술가 메모 문법 3건: `setup-node`의 `cache` 입력(npm·yarn·pnpm, action.yml 확인), `if: always()`·`contains(needs.*.result, …)`, 건너뛴 잡 보고 방식(위 정정). `retention-days` 입력 실재(upload-artifact action.yml, 최소 1일). HTML 메모 삭제.
- Bouzenia & Pradel 2024(32.9%·91.2%·연 $504·50.7/30.9/15.5%·1.1~31.6%), 뱅크샐러드 인용·1분 8초→21초·약 40초, 캐시 스코프 인용 2건·매칭 순서·7일·10GB·증설 주체, pull_request_target 캐시 오염, v3 차단 2025-01-30·v4 90%·500개, 아티팩트 저장 한도 4플랜, concurrency 기본 대기 인용·`queue: max`+`cancel-in-progress` 검증 오류, Discussion #13690(2022-03·👍101·joegaudet 인용·2026-08 joshuat), HN ZuoCen_Liu·jjgreen 인용, 2025-12-16 가격 공지(39%·$0.002·2026-03-01)·연기 인용 요지, woodruffw·danpalmer·sebastien 인용 — 01_reference §2.8·§3.4, research/community.md와 일치.
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- 예제 SHA 고정 주석의 메이저 버전: checkout `# v5` → `# v7`, upload-artifact `# v4` → `# v7`, download-artifact `# v4` → `# v8` — GitHub 릴리스 API 1차 확인(2026-09-26): checkout v7.0.1(2026-07-20), upload-artifact v7.0.1(2026-04-10), download-artifact v8.0.1(2026-03-11). v8의 `run-id`·`github-token` 입력과 다른 런에서 받을 때 `actions: read` 필요는 README와 일치, 예제 유효
- `GITHUB_TOKEN` "워크플로마다 새로 발급" → "잡이 시작될 때마다 새로 발급되고 잡이 끝나면 만료", 호스트 러너 최대 6시간 보강 — Docs "GITHUB_TOKEN"(잡 종료 또는 최대 수명 시 만료)
- 2025-12-08 이전 `pull_request_target` 동작: "PR의 base 브랜치 워크플로가 쓰였다" → "base로 지정된 어느 브랜치든 워크플로 출처가 될 수 있었다" — Changelog 2025-11-07 원문 "any branch within the parent repository set as the base branch of a pull request could have been used as the source of the executed workflow"
- 218개 귀속: "국내 보도에서 최소 218개 집계(사실 확인 필요)" → "Endor Labs가 218개로 추산, 국내 보도도 전함" — 데일리시큐 원문("218개 저장소는 콘솔 로그에 비밀정보를 출력한 것으로 확인"), BleepingComputer·The Hacker News(Endor Labs 추정) 확인
### ⚠️ 약화·삭제
- 악성 커밋 "3월 12일설" 문장 삭제 — 1차 확인 불가, 데일리시큐는 3월 14일로 기술
- SHA 고정 강제 정책(2025-08-15) "tj-actions 사건에 대한 대응이다" → "공지가 특정 사건을 거론하지는 않지만, tj-actions 사건 다섯 달 뒤에 나온 장치" — Changelog 원문에 tj-actions 언급 없음 확인
- immutable releases "액션 생태계 전체 적용은 확인 못 함(사실 확인 필요)" → 배포자가 켜야 작동한다는 확인된 사실만 남김
- 오프닝 "수만 개 저장소" → "2만 개가 넘는 저장소"(23,000+ 추정치와 정합)
### 🕒 신선도
- AI 에이전트 액션 프롬프트 인젝션: "보도 수준(사실 확인 필요)" → "2026년에도 여럿 보고되고 패치됐다" — The Hacker News 2026-06 보도(Claude Code GitHub Action, 2026-01 보고·패치, CVSS v4 7.8)와 Cline 2026-02 사례 언급 확인. 특정 제품명은 원고에 넣지 않음
### ✅ 확인 (요약)
- HTML 메모·`(사실 확인 필요)` 5건 전부 해소, 메모 삭제
- CVE-2025-30066·CISA 2025-03-18 경보(reviewdog/action-setup 병기)·2025-03-14~15 v1~v45.0.7 태그 재지정·Advisory 제목 인용·23,000+(보안업체 추정)·v46.0.1 해소 — 01_reference §3.3 일치. 봇 PAT 발단·reviewdog 연쇄 — 데일리시큐·The Hacker News(CVE-2025-30154 경유 PAT 획득) 확인, "분석이 나왔다" 귀속 유지. 2025-03-14 금요일 맞음
- SHA 고정 강제·`!` 차단(2025-08-15), immutable releases GA(2025-10-28, 자산·태그 불변·attestation) — §2.9·Changelog 일치
- SHA 고정 Docs 인용 2건, GITHUB_TOKEN 권고 인용, Koishybayev 2022(213,854/447,238/99.8%·99.7/97/18%·7,485개 3.5%, 전환 이전 데이터 고지), 2023-02-02 기본 read-only 전환, Security Lab 2021 인용 3건, pull_request_target 변경 인용 2건·GITHUB_REF/SHA, "must not explicitly check out untrusted code", 중간 환경 변수 권고 인용, ARGUS 2023(2,778,483/31,725/4,307/80/7배·인용), 셀프호스트 인용, HN 인용 2건(srvaroa·remram) — 01_reference·research와 일치. rarkins 인용 없음(규율 준수)
- Dependabot `package-ecosystem: github-actions`, `directory: /` — 표준 설정
### 미해소
- (없음)

## 07장 (라운드 2)
- 수락 게이트 라우팅 재검 (2026-09-26)
- ❌ 라운드 1의 "Discussion #168145 — 01_reference.md 일치" ✅ 판정 철회: 원장 자체가 오귀속. 토론 원문은 flaky 테스트 증폭 사례가 아니라, 워크플로가 `merge_group`과 `gh-readonly-queue/` 브랜치 push 양쪽에 반응해 같은 concurrency 그룹의 런이 서로를 취소한 사례 — 근거: github.com/orgs/community/discussions/168145
- 7장 처리: #168145 언급 삭제, 머지 큐에서 flaky 하나가 그룹 전체를 떨어뜨린다는 내용은 출처 없는 일반 서술로 유지
- 원장 주석: 01_reference.md·research/community.md의 #168145 해석 줄에 오귀속 주석 추가
### 미해소
- (없음)

## 11장 (라운드 2)
- 수락 게이트 라우팅 재검 (2026-09-26): `pull_request_target`·cache poisoning 새 문단
- ✅ "GitHub Docs는 ... 쓰기 권한·시크릿 노출과 함께 캐시 오염(cache poisoning)을 꼽는다" — 01_reference.md §2.8 인용 및 Docs 원문("may lead to security vulnerabilities. These vulnerabilities include cache poisoning and granting unintended access to write privileges or secrets.")과 일치
- ⚠️ 약화: 마지막 문장 "…캐시를 써 넣을 수 있다면, 이후의 실행은 그 오염된 캐시를 제 것인 양 되살린다" — Docs는 가능성("may lead to")만 말하고 후속 실행이 반드시 복원한다는 메커니즘은 단정하지 않음 → "…캐시에 손을 댈 수 있다면, 그 캐시를 되살리는 이후의 실행까지 오염될 수 있다는 뜻이다."로 약화 (11_final.md·04_manuscript.md 동일 반영)
### 미해소
- (없음)
