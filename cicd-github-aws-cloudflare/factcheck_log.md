
## 10장 (라운드 1)

### ❌ 정정
- Mini Shai-Hulud "(사실 확인 필요)" 문장 → 재작성. 웹 2차 확인: THN(2026-09-25) — actions-cool/issues-helper·maintain-one-comment가 2026-09-16 다시 접근 가능해짐, 2026-05-18 최초 침해(Mini Shai-Hulud 클러스터). SafeDep(2026-09-24) — 페이로드가 `.claude/settings.json`·`.vscode/tasks.json` 훅을 저장소에 커밋. **"Dependabot으로 위장한 워크플로 주입"은 SafeDep 원문에 없음 → 삭제** (research/community.md 패턴 9의 요약이 부정확). 날짜 표현은 "2026년 5월 침해 → 9월 중순 재활성화 보도"로 교체.
### ⚠️ 약화·삭제
- "Greshake 등이 간접 프롬프트 인젝션을 처음 체계적으로 보여준 논문" → "체계적으로 보여준 대표 논문" — '처음' 단정 근거 없음(레퍼런스는 '원전/seminal'까지만).
- Clinejection 공격 경로 → "커뮤니티 토론과 보안 연구 노트가 전하는 경로" — 출처가 HN 스레드·CSA 연구 노트(C-패턴12, C-휴7)뿐이므로 보고된 경로로 귀속. 대상 프로젝트명·피해 규모(~4,000대)는 원고에 없음(유지).
### 🕒 신선도
- (해당 없음 — claude-code-action `v1.0.235` 주석은 W-0 2026-09-26 조회값과 일치)
### ✅ 확인 (요약)
- s1ngularity: 2025-08, Claude·Gemini·Q CLI, `--dangerously-skip-permissions`/`--yolo`, Wiz 수치(GitHub 토큰 1,000+·클라우드 자격증명·npm 토큰 수십·파일 약 2만) — W-22.
- Greshake 인용(P-54), PromptPwnd 2025-12(2026-03 갱신)·대상 4종·포춘 500 최소 5곳·권고 인용(W-41), Comment and Control 4,714·8·15개 액션·책임 공개 대상(P-55), Clinejection `allowed_non_write_users: "*"`·yread 인용·`contents: read` 주석(C-패턴12), "RISKY"(W-39), CodeRabbit RCE 2025-08·1M 저장소 주장·1월 수정(C-패턴12).
- codex-action 인젝션 벡터·쓰기 권한자 기본값(W-40), claude-code-action 쓰기 권한자 기본값(W-38), 정제 항목 5종·"new bypass techniques may emerge"·`ACTIONS_STEP_DEBUG`(W-39), C-휴7 체크 항목.
- gh-aw 1,248개(276 저장소)·556.5단어·62.1%·78.2%·9.4%·2026-09-23 게시(P-56). Copilot cloud agent `copilot/`·"Approve and run workflows"(W-42).
### 미해소
- (없음)

## 04장 (라운드 1)

### ❌ 정정
- "한 블로그는 2026년 7월 이후 immutable subject claim에 옵트인한 저장소는 … 실패한다고 주장한다(사실 확인 필요). GitHub 공식 changelog로 확인되지 않은 내용" → 확인된 사실로 교체: 2026-04 발표, `repo:org@<조직ID>/repo@<저장소ID>:...` 형식, 2026-07-15 이후 새 저장소·이름 변경·이전 저장소는 자동 적용, 기존 저장소는 옵트인해야 적용, github.com 한정. 새 저장소는 이 장의 이름 기반 `sub` 조건으로는 실패한다고 명시 — 근거: GitHub Changelog "Immutable subject claims for GitHub Actions OIDC tokens" (2026-04-23, 2026-06-10 갱신), 웹 2차 확인. 레퍼런스 4.3 #12의 "공식 changelog 미확인"은 리서치 누락이었음
- 신뢰 정책 JSON 직후에 "이 `sub`는 이름 기반 형식이며, 2026-07-15 이후 만든 저장소는 형식이 다르다" 한 문장 추가 (위 정정의 연쇄)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- immutable `sub` 문단에 "2026년 9월 기준 github.com" 명시
### ✅ 확인 (요약)
- 수치 5건(NDSS 2019 약 6개월·10만+ 저장소·매일 수천 개 / ICSE 2019 98개월·중앙값 20개월) — P-23, P-36
- 버전·날짜 6건(configure-aws-credentials v6.3.0, checkout v7, custom properties 클레임 GA 2026-04, `deployment: false` 2026-03 및 커스텀 보호 규칙 제약, Cloudflare Worker 권한 2026-09-15, 역할 4종·Editor 삭제 불가·Specified Workers 인용) — W-0, W-4, W-5, W-34
- API·입력 5건(`role-duration-seconds` 기본 3600·900~43,200, `role-session-name` 기본 `GitHubActions`, `aud` `sts.amazonaws.com`, 공급자 URL, wrangler-action `apiToken`·`accountId`) — W-13, W-14, W-33
- 인용 4건(Lobsters insanitybit·ashishb, claude-code-action PAT 경고·워크로드 아이덴티티 페더레이션, HN adzicg) — C-휴3, C-휴6, W-38, W-39
- Cloudflare의 GitHub OIDC 미지원은 원고가 이미 "공식 문서에서 확인하지 못했다, 2026년 9월 기준"으로 약화해 둠 — 레퍼런스 4.3 #11 방침과 일치
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- "Beko의 22개 저장소에 Qodo PR-Agent를 적용한 사례 … 73.8%" → "한 기업이 오픈소스 Qodo PR-Agent 기반 자동 리뷰를 도입한 ICSE 2025 사례 연구 … 세 프로젝트의 PR 4,335건(자동 리뷰 1,568건) … 73.8% 해결 처리" — 웹 2차 확인: arXiv 2412.18531 초록(v2, ICSE 2025 SEIP). **"22"는 저장소 수가 아니라 광범위 설문 응답 실무자 수(22명)**, 도구 접근 인원은 10개 프로젝트 약 238명. 초록에 기업명(Beko) 없음 → 기업명 삭제. 73.8%는 확인.
- PR 종료 시간 "(사실 확인 필요)" → "평균 5시간 52분에서 8시간 20분으로 늘었다" + "프로젝트마다 추세는 달랐다·잘못된 리뷰·불필요한 수정 요구" 병기 — 초록 원문과 일치.
- "병합되지 못한 에이전트 PR 약 3만 3천 건을 분석한" → "에이전트 PR 약 3만 3천 건을 분석해 병합되지 못한 PR의 특징을 살핀" — P-50·P-52 기준 33k는 분석 대상 에이전트 PR 전체(AIDev)이며 실패 PR만의 수가 아님.
- ※ 01_reference.md 3.5 "Beko 22개 저장소"와 research/papers.md 논문 47의 "10개 프로젝트·22개 저장소"는 초록과 어긋남 — 다른 장이 P-47을 인용하면 같은 정정 필요 (수락 게이트 참고).
### ⚠️ 약화·삭제
- "도구 대부분이 비용 때문에 diff만 컨텍스트로 본다는 지적" → "…때문일 거라는 추측" — 원문(storystarling)은 "I suspect"로 추측 표현.
- "커뮤니티에서 자주 언급되는 규칙(400줄 PR 상한)" → "커뮤니티에서 공유된 경험칙" — 출처는 GeekNews 스레드 안의 Lobsters 요약 1건(C-패턴11)으로 빈도 근거 없음. 규약 초안의 "400줄 안팎"·"출발점일 뿐" 프레이밍은 유지.
### 🕒 신선도
- (해당 없음 — Copilot code review GA 2026-03·6,000만 건은 시점 명기됨)
### ✅ 확인 (요약)
- GeekNews 인용 2개는 동일 글(C-패턴11), danpalmer·koh3276 발언(C-패턴11). P-44 802명·196,212건·2024-01~2026-04·2.09배·인용문.
- P-51 82.1%/66.1%/16%p·MSR 2026, P-49 567개·83.8%·54.9%, P-43 정성 결론, P-46 과신 인용, W-43 2026-03·6,000만, W-44 Bugbot `neutral` 인용·`.cursor/BUGBOT.md`, W-47 kt cloud 인용, W-48 57건 중 32건·Evidence/Mitigation·인용, W-49 스위스 치즈 인용, zmmmmm 80%·신호 대 잡음 인용·marginalia_nu·jjmarr(C-패턴10·휴5), C-논쟁E 세 관점, W-42 공동 저자.
- P-41 55.8%, P-42 16명·246개·19%·24%·20%, P-39 처리량·안정성 감소, P-40 처리량 양(+)·안정성 음(−), DORA 5지표(W-46), wrangler-action `gitHubToken`(W-33), `deployment: false`(W-4).
### 미해소
- (없음)

## 01장 (라운드 1)

### ❌ 정정
- "십 년 가까이 쌓인 연구" → "십 년 넘게 쌓인 연구" — 인용 연구가 2015(Vasilescu)~2026년에 걸침

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (없음 — 장 말미에 "2026년 9월 기준" 명시돼 있음)

### ✅ 확인 (요약)
- `(사실 확인 필요)` 배포 재작업률 정의: dora.dev "The ratio of deployments that are unplanned but happen as a result of an incident in production", 2024년 도입(dora.dev/insights/dora-metrics-history) — 원고 서술과 일치, 주석 제거
- DORA 2025 수치(약 5,000명·90%·80%+·30%)·인용 2건, DORA 2024(1.5%·7.2%) — 01_reference §1.2·research/papers.md 39·40, web.md 자료 46
- Vasilescu 2015, Hilton 2016(34,544·1,529,291·442·folklore), Hilton 2017(세 축 인용), Felidre 2019(1,270·약 60%·85%·4일·10분 규칙), 에이전트 PR 실패 연구(MSR 2026, P-50) — papers.md 초록과 일치
- 토스 SLASH 23 인용·날짜, Flowkater·GeekNews 인용, Accelerate 2018·4지표, dora.dev 현행 5지표 — 01_reference와 일치

### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- cron `timezone:` 필드 위치 `(사실 확인 필요)` → 공식 문서(workflow-syntax `on.schedule`) 예제가 `- cron: ...` 항목 안에 `timezone:`을 형제 키로 두는 형태임을 확인. YAML 주석 "필드 위치는 공식 문서와 대조할 것"과 대조 권유 문장을 확인된 서술("`timezone`은 `cron`과 같은 항목 안에 나란히 둔다. 공식 문서의 예제도 이 형태다.")로 교체

### ⚠️ 약화·삭제
- "두 문장이 유독 많이 회자됐다" → "두 문장이 이 스레드의 요지를 잘 담고 있다" — 회자 정도에 대한 근거 없음(community.md 패턴 1)
- action-tmate "종료 예정이라는 이야기가 커뮤니티에서 나온다(사실 확인 필요)" → "기반 서비스인 tmate.io의 공식 중계 서버가 종료를 예고하면서, upterm 쪽으로 옮겨 가는 프로젝트가 늘고 있다(2026년 9월 기준)" — action-tmate 저장소 자체에는 폐기 공지 없음, 종료 대상은 tmate.io 공식 서버(nixpkgs#457502, 2025-11; 다수 프로젝트의 action-upterm 이전 PR). 종료 일자는 1차 출처로 확정 못 해 기재하지 않음

### 🕒 신선도
- action-tmate 서술에 "2026년 9월 기준" 부착

### ✅ 확인 (요약)
- HN 인용 4건(iamcalledrob·1a527dd5·physicsguy·mlrtime)·스레드 날짜 2026-01 — community.md
- 재사용 워크플로 한도 10단계/50개(2025-11), concurrency 큐 100개 FIFO(2026-05)·`queue: max`와 `cancel-in-progress: true` 병용 불가, cron 타임존(2026-03) — web.md 자료 2·3·4
- 워크플로 파일 7.3% 매주 변경(P-9), 재시도·대기 조치 연구(P-29), `act` 80%·services 컨테이너 이슈(C-패턴2)
- Copilot 에이전트 AGENTS.md 지원 2025-08·인용문, 보안 가이드(중간 환경 변수·CODEOWNERS), 토스 템플릿 인용 — web.md 자료 15·45·50
- `actions/checkout@v7` 최신 메이저(v7.0.1) — 01_reference §0

### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- 레몬베이스 "다른 방식으로 바꿨다" → "개발자가 배포 대상을 워크플로 옵션으로 직접 고르는 방식으로 바꿨다" — GeekNews 소개글 원문 "개발자가 배포 대상을 선택할 수 있도록 Workflow 옵션으로 제공"
- 레몬베이스 롤백 사유: "구체적인 상황은 원문을 확인해야 하지만, 이유를 추측해볼 수는 있다" → "소개글에는 어떤 상황이었는지까지는 나오지 않는다. 그러니 여기서부터는 추측이다." — 뒤따르는 원인 설명이 저자 추측임을 명시(소개글에 구체 사유 없음 확인)

### ⚠️ 약화·삭제
- self-hosted 과금 "재개 여부는 정해지지 않았다" → "재개 여부는 공식적으로 확인되지 않는다" — 1차 소스는 "postponing"까지만, 결정 부재 자체는 확인 불가(web.md 자료 8 주의)

### 🕒 신선도
- (없음 — 가격표·과금 서술에 "2026년 9월 기준" 이미 명시)

### ✅ 확인 (요약)
- `(사실 확인 필요)` 경로 필터 + 필수 체크 Pending: GitHub 공식 workflow-syntax 문서 "checks associated with that workflow will remain in a 'Pending' state. A pull request that requires those checks to be successful will be blocked from merging" — 주석 제거하고 공식 문서 근거 한 문장 추가
- Bouzenia & Pradel(ICSE 2024: $504·91.2%·50.7/30.9/15.5%·32.9%), Kotinos(14,364·87.9%·74%), 캐시 프리프린트(952·17,185·9.37 — arXiv 2604.13129 초록으로 캐시 도입 저장소 기준임 확인), Memon 2017, 플레이키(59%·22,352·876,186·170회), 빌드 깨짐(588·924,616) — papers.md
- 러너 가격표 7종·최대 39% 인하·$0.002 플랫폼 요금·96%·대형 러너 조건, arm64 러너(2025-08 퍼블릭 4 vCPU, 2026-01-29 프라이빗 2 vCPU, 라벨 3종), 버즈빌 ARC(2024), Runner Scale Set Client(2026-02), self-hosted 과금 연기 문구, 캐시 10GB·종량 과금(2025-11), 머지 큐 `merge_group` must·1~100, F-Lab, 레몬베이스 27→12분 55%, Copilot cloud agent "Approve and run workflows" — web.md 자료 5·6·7·8·9·10·11·12·42
- 벤더 캐시 수치(1.2GB·38초·6초)는 원고가 이미 이해관계 단서와 함께 제시 — 유지

### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "claude-code-action도 같은 워크로드 아이덴티티 페더레이션으로 Claude API에 접근하므로" → "GitHub OIDC 토큰을 교환하는 같은 방식의 워크로드 아이덴티티 페더레이션으로 … 접근할 수 있으므로" — W-38 기준 신뢰 대상은 AWS가 아닌 Claude Console 서비스 계정이고 선택 기능이므로 '같은 방식'·'할 수 있다'로 정밀화.
### 🕒 신선도
- 신선도 감시 표 확인: `pull_request_target` 기본 차단은 "평가 모드, 2026-11-02 강제 예정, 프라이빗·내부 미적용"으로 "예정" 표기 유지(W-21, 4.3 #6) — 본문의 "출간 시점에 '시행'으로 바뀌어 있을 수 있다" 경고도 유지. 보안 로드맵은 "2026년 3월 발표·출시 여부 미확인"(W-20), Worker Previews 4.135.0+(W-32), self-hosted 과금 "연기·재개 불확실"(W-8), Cloudflare OIDC "확인하지 못함"(W-33), 버전 v6.3.0·v4.1.3·v1.0.x(W-0) 모두 2026년 9월 기준 명기됨.
### ✅ 확인 (요약)
- Hilton 세 축 정의(P-3), Copilot cloud agent "Approve and run workflows"·Ready/승인 불가(W-42), `wrangler versions upload/deploy`(W-35), Specified Workers·Editor(W-34), Ian Duncan 2026-02 "CI의 Internet Explorer"·비판 항목·Buildkite/Concourse(C-논쟁A), 2026년 장애 횟수 푸념·비공식 가동률 수치 미사용(C-패턴4), sebastien(Lobsters)·카카오엔터프라이즈·GeekNews "대안은 있지만 대체재는 없다"(C-논쟁A), W-49 검증 이동 인용.
- 편집자용 HTML 주석(3행)은 지시대로 유지.
### 미해소
- (없음)

## 05장 (라운드 1)

### ❌ 정정
- "base64로 인코딩된(사실 확인 필요)" → "base64로 두 번 인코딩된" — 근거: memdump.py가 시크릿을 이중 base64로 로그에 출력(Wiz·StepSecurity·Semgrep 분석, 웹 2차 확인)
- "그 액션이 수만 개 저장소의 러너 안으로" → "2만 개가 넘는 저장소의" — 23,000개 수치(W-16·4.3 #4)와 일치시킴
- "그 뒤 GitHub가 기본값을 일부 조정했다는 이야기도 있다(사실 확인 필요)" → "GitHub는 2023년 2월부터 새로 만드는 조직·저장소의 `GITHUB_TOKEN` 기본 권한을 읽기 전용으로 바꿨다. 다만 이미 있던 조직·저장소의 설정은 그대로 두었다" — 근거: GitHub Changelog 2023-02-02 "Updating the default GITHUB_TOKEN permissions to read-only" (웹 2차 확인)
### ⚠️ 약화·삭제
- "tj-actions 사고에서 가장 심하게 당한 프로젝트 중에는 SHA 고정을 하고 봇으로 해시를 갱신하던 곳들도 있었다"(서술자 단정) → "Lobsters의 한 개발자에 따르면 …"으로 귀속 — 근거가 alerque 개인 발언뿐(C-패턴9)
### 🕒 신선도
- (원고가 이미 처리: pull_request_target 강제 2026-11-02 "예정"+출간 시점 경고, 보안 로드맵 `dependencies:` "2026년 9월 기준 출시 여부 미확인", `actions/attest` v4.2.2 "2026년 9월 기준")
### ✅ 확인 (요약)
- tj-actions 7건(v1~v45.0.7, 러너 워커 메모리→로그, 2025-03-14~15, CVE-2025-30066, CVSS 8.6, v46.0.1, 23,000 vs 218 구분·데일리시큐 2025-03-23, reviewdog CVE-2025-30154, 봇 PAT) — W-16, W-17
- s1ngularity 6건(2025-08, 워크플로 추가 2025-08-21, Wiz 2025-08-27, 1,000+ 토큰·수십 개 자격증명·약 2만 파일, 400+ 사용자·조직, 5,500+ 저장소) — W-22 (THN 오기 날짜 미사용 확인)
- 논문 수치 12건(USENIX 2022 4속성·447,238·99.8%·97%·18% / EASE 2026 95개·30기준·28%·4%·κ=0.28·81% / ARGUS 약 278만·약 3만 2천·4,307·80 / ACM REP 2026 3억 2,840만·1,020만·18.9만·32 중 7 / 스캐너 9종·2,722개 / SCORED '22 3속성) — P-11~P-18, P-21
- 정책·기능 8건(SHA 고정 정책 2025-08·`!` 차단 목록 최후 평가, Dependabot 쿨다운 2026-07·3일·보안 업데이트 예외, 보안 로드맵 2026-03, checkout v7 2026-06-18·백포트 2026-07-16·`allow-unsafe-pr-checkout`, attestation SLSA L2/L3, immutable releases 2025-10, CodeQL 2025-04·158,000·80만·15%) — W-15, W-18, W-19, W-20, W-21, W-23, W-24, W-25
- 커뮤니티 인용 5건(AlecBG·koolba·maxloh·mmarian HN, alerque Lobsters, immutable releases HN 반응) — C-패턴9, C-휴2
### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- "65,535자로 알려져 있다, 사실 확인 필요" → "GitHub API의 오류 메시지 기준 최대 65,536자" — 근거: API 오류 "Body is too long (maximum is 65536 characters)"가 다수 액션 이슈(renovate #14551, add-pr-comment #93 등)에 동일하게 기록됨. 레퍼런스의 65,535는 2차 소스
- "CDKTF는 HashiCorp가 개발을 종료했다는 이야기가 2025년 말 커뮤니티에서 돌았다(사실 확인 필요)" → "HashiCorp가 2025년 12월 10일부로 개발·유지보수를 끝내고 저장소를 보관 상태로 돌렸다 … 새로 도입할 선택지는 아니다" — 근거: hashicorp/terraform-cdk README 공지(웹 2차 확인)
- verify-ecs-deploy.sh의 네이티브 blue/green 조회 필드 "(사실 확인 필요)" → 스크립트가 롤링 배포 기준임을 명시하고, 네이티브 blue/green·linear·canary는 `aws ecs list-service-deployments`·`describe-service-deployments`로 상태·대상 리비전을 조회하라고 구체화 — 근거: ECS API Reference(ListServiceDeployments·DescribeServiceDeployments·DescribeServiceRevisions), 웹 2차 확인
- PR plan 역할 `sub`(`repo:ticketbox-org/ticketbox:pull_request`)에 "2026년 7월 15일 이후 만든 저장소라면 ID가 붙은 형식" 괄호 추가 — 04장 immutable `sub` 정정의 연쇄
### ⚠️ 약화·삭제
- containers-roadmap #1488 "태스크가 하나뿐인 서비스는 실패 감지에 약 100분" 삭제 — 이슈 본문에서 확인되지 않음. "자동 롤백을 켜두었는데도 FAILED에 머문 채 롤백하지 않았다"는 보고만 남김(이슈 본문 확인)
- aws-lambda-deploy 입력 이름 "(사실 확인 필요)" 해소 — `function-name`·`code-artifacts-dir`는 공식 README와 일치(웹 확인), 확인 요청 문장을 "2026년 9월 기준 공식 README를 따랐다"로 교체
### 🕒 신선도
- aws-lambda-deploy 입력 이름에 "2026년 9월 기준" 부착
### ✅ 확인 (요약)
- 버전 5건(checkout v7.0.1, configure-aws-credentials v6.3.0, amazon-ecr-login v2.1.7, amazon-ecs-deploy-task-definition v2.6.3, setup-terraform v4.0.1) — W-0
- 액션 입력·출력·CLI 필드 6건(`wait-for-service-stability`, `task-definition`/`cluster`/`service`, `steps.ecr.outputs.registry`, `deployments[?status==PRIMARY]`, `rolloutState` COMPLETED, `ubuntu-24.04-arm`) — 공식 액션 README·ECS API 기준
- 날짜 9건(arm64 2025-08/2026-01, ECS blue/green 2025-07-17, linear/canary 2025-10-30, NLB 2026-02, 이관 블로그 2025-09 "all-at-once" 구버전 처리, App Runner 2026-04-30, ECS Express Mode 2025-11·Graviton 2026-09, Lambda 액션 2025-08) — W-9, W-26~W-29
- 인용·수치 5건(#191 성공 보고, TaskSet vs ServiceRevision, ICSE 2019 293·15,232·21,201·1,326, CCS 2023 과신, danw1979 HN) — C-패턴7, W-27, P-36, P-46, C-논쟁B
### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- Worker Previews 격리: "대부분의 바인딩이 프리뷰마다 격리된 사본으로 붙는다" → Durable Objects만 자동 격리이고, D1·KV·R2는 같은 `database_id`/`id`면 프로덕션과 공유하므로 `previews.d1_databases` 등으로 따로 바인딩해야 격리된다(문서가 권하는 공용 스테이징 D1 패턴 추가). 그림 1 라벨("D1 사본"→"프리뷰용 D1", "previews 설정"), 비교표, 핵심 요약 불릿도 함께 고침 — 근거: developers.cloudflare.com/workers/previews/resources/ (2026-09-26 조회). 참고: 01_reference.md §3.3의 "대부분 바인딩은 Preview별 격리 사본"은 원문을 과하게 요약한 것
- Preview URLs: 별도 기능이 아니라 `wrangler versions upload --preview-alias`로 붙이는 별칭 Version URL이며, 현행 문서는 "preview URLs"를 Version URLs의 옛 이름으로 소개한다 → 본문 단락과 표 행을 고침(격리 "없음, 프로덕션 리소스 사용", PR 테스트 "부적합"). "기능이 셋" → "이름에 preview가 들어간 것이 셋" — 근거: developers.cloudflare.com/workers/configuration/previews/, compare-workflows/, wrangler commands 문서(`--preview-alias`는 `versions upload`의 옵션)
- D1 `--remote` 함정과 #221: #221의 실제 내용은 토큰에 D1 편집 권한이 없어 잡이 **실패**했는데 로그에 쓸 만한 오류가 없었다는 것(2023-12, CLOSED)이고, `--remote` 누락 이야기가 아니다 → `--remote` 누락 위험은 "문서상 기본 대상이 로컬 DB"라는 근거로 따로 서술하고, #221은 "권한 부족으로 오류 메시지 없이 실패한 사례"로 바로잡음 — 근거: gh issue view 221, developers.cloudflare.com D1 로컬 개발 문서(`--local` 기본)
- 버전에 담기는 것: "D1, KV, 시크릿은 버전 안에 들어 있지 않다" → 버전은 코드·정적 에셋·바인딩 설정·호환성 설정을 담고, D1·KV의 **데이터**가 버전 밖에 있다. 시크릿 언급은 삭제(`wrangler versions secret put`이 새 버전을 만들기 때문). 핵심 요약 불릿도 "D1·KV의 데이터"로 고침 — 근거: Workers "Versions & deployments" 문서, secrets 문서

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도 / 사실 확인 필요 해소
- `not_found_handling: "single-page-application"` ✅ — 공식 SPA 라우팅 문서의 예제. 주석 제거
- wrangler-action `workingDirectory` ✅ — 액션 README 입력 목록. 주석 제거
- Workers 커스텀 도메인이 Cloudflare 존 밖에서 안 되는 문제 → 2026년 9월 기준 공식 문서가 "active Cloudflare zone"을 전제 조건으로 요구한다는 확인 문장으로 교체
- AWS는 Bandwidth Alliance 비회원 ✅(Cloudflare 블로그 "AWS's Egregious Egress" 등). 송신 요금 효과는 커뮤니티 지적으로 남기고 "~ㄹ 수 있다"로 표현
- `wranglerVersion: "4.141.0"` ✅ — npm 최신이며 2026-09-25T19:24Z 게시("전날 나온 최신"과 일치). wrangler-action v4.1.3 ✅ (2026-09-24), actions/checkout v7.0.1 ✅

### ✅ 확인 (요약)
- 버전·날짜 8건(4.135.0=2026-09-18 게시, 4.136.3, 4.21.0=2025-06-23 게시/2025-07 공지, 2025-08-10 HN, 2025-11-18 장애, 2026-09-15 changelog, 3.114.x/4.x #8851, pages-action 저장소 404)
- 인용 6건(마이그레이션 가이드의 "broader set of features", "Do not use Version URLs…", "recommended way…", 서비스 바인딩 예외, Tunnel "without a publicly routable IP", IP 허용 목록 "Vulnerable to IP spoofing") — W-31~W-37
- 설정·옵션 7건(`pages_build_output_dir`→`assets.directory`, `run_worker_first`, `apiToken`/`accountId`/`gitHubToken`/`deployment-url`, `command: preview --name …`, AOP의 Full/Full(strict) 조건, D1 비대화형 백업·롤백·`d1_migrations`)
- Cloudflare의 GitHub OIDC 수용 여부는 본문이 이미 "확인하지 못했다"로 쓰고 있어 그대로 둠

### 미해소
- (없음)

## 08장 (라운드 1)

### ❌ 정정
- 롤백이 되돌리지 않는 것: "바인딩 설정, D1의 데이터, 시크릿은 롤백과 함께 돌아오지 않는다" → "D1과 KV에 쌓인 데이터와 D1의 스키마는 롤백과 함께 돌아오지 않는다". 공식 문서는 버전이 "bundled code, static assets, bindings, and compatibility settings"를 담는다고 하고, 시크릿 변경도 새 버전을 만든다(`wrangler versions secret put`). 롤백 문서의 "Resources connected to your Worker will not be changed"는 자원(저장소)을 말하는 것으로 읽는다. 그림 2의 "Worker 바인딩·시크릿" → "KV·R2에 쌓인 데이터", 런북 3단계의 "바인딩·시크릿·환경 변수를 바꿨나?" → "버전 밖에서 바꾼 설정(콘솔에서 바꾼 WAF 규칙·대기열 기준 등)이 있었나?" — 근거: Workers "Versions & deployments"·Rollbacks·Secrets 문서(2026-09-26 조회). 01_reference.md §3.3의 "(바인딩·D1 데이터·시크릿 미복원)"은 레퍼런스 쪽의 해석 오류
- ECS 사용자 고정(표): "확인 안 됨(사실 확인 필요)" → "ECS 점진 배포 기능 자체에는 없음. ALB 가중 타깃 그룹의 타깃 그룹 고정(target group stickiness) 설정 영역" — 근거: AWS ECS "ALB resources for blue/green, linear, and canary" 문서(가중 타깃 그룹 사용), ALB weighted target groups 공지(2019-11)

### ⚠️ 약화·삭제
- "자동 롤백 장치가 레퍼런스에서 확인되지 않는다"(본문·표) → "2026년 9월 기준 공식 문서에서 찾을 수 없다". 독자에게 보이는 문장에 내부 용어 "레퍼런스"가 섞인 것을 사실 근거 표현으로 바꿈

### 🕒 신선도 / 사실 확인 필요 해소
- `wrangler versions deploy "<id>@10%" "<id>@90%"` ✅. 위치 인자 `[<version-id>@<percentage>..]`, 비대화형 실행은 `-y/--yes` → 스크립트 두 곳과 런북에 `-y`를 추가하고 주석 정리 — 근거: wrangler commands 문서(versions deploy)
- Workers vars가 새 버전에 담기는지 ✅. 환경 변수는 "a type of binding"이고 버전은 바인딩을 담는다 → 주석 제거, "바인딩의 한 종류라"로 근거를 드러냄

### ✅ 확인 (요약)
- 날짜 6건(ECS 블루/그린 2025-07, 선형·카나리 2025-10-30, NLB 2026-02, AWS 블로그 2025-09-16 "all-at-once", Cloudflare 장애 2025-11-18, Metrics changelog 2026-09-25) — W-26, W-27, W-35
- 수치 7건(Gandalf 18개월·92.4%·100%, SOSP 2015 매일 수천 건, 최대 2개 버전, 최근 100개 버전 두 곳, HN 916 댓글 → "900개가 넘는") — P-32, P-33, W-35, C-논쟁G
- 인용·주장 5건(abalone 봇 관리 발언, DORA 2024/2025 안정성 음(−)·2025 처리량 양(+)·방법론 차이, "2026년 들어 셀 수 없이" 장애 불만, 한국 저장소 롤백 실패 시 파이프라인 실패 패턴 B-TING #328·assistudy-toy #39, `Cloudflare-Workers-Version-Key`) — P-39, P-40, C-패턴7, W-35

### 미해소
- (없음)

## 09장 (라운드 1)

### ❌ 정정
- 최소 안전 설정 템플릿의 권한: 트리거에 `issue_comment`(이슈 코멘트 포함)가 있는데 `issues: write`가 빠져 있었음 → `issues: write` 추가. 공식 예제(examples/claude.yml)의 권한 조합(contents·pull-requests·issues: write, id-token: write, actions: read)을 주석으로 밝히고, 템플릿이 쓰기 권한을 일부러 좁혔다는 점을 적음 — 근거: anthropics/claude-code-action examples/claude.yml (2026-09-26 조회)
- 자동 리뷰(codex) 결정표의 "봇: 해당 없음" → "`allow-bots` 기본값(false) 유지". codex-action에는 `allow-bots`(기본 false)·`allow-bot-users` 입력이 있다 — 근거: openai/codex-action action.yml
- codex 워크플로 발췌에 모델 자격증명 입력이 빠져 있었음(결정표는 "API 키 시크릿(에이전트 잡에만)") → `openai-api-key: ${{ secrets.OPENAI_API_KEY }}` 한 줄 추가 — 근거: codex-action action.yml

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도 / 사실 확인 필요 해소
- codex-action 입력 `prompt-file` ✅, 출력 `final-message` ✅, `safety-strategy` 기본값 `drop-sudo` ✅ — action.yml. 주석 제거(`drop-sudo`에는 "기본값이지만 명시" 주석)
- claude-code-action 도구 제한 옵션 → `claude_args`의 `--allowedTools`(허용)·`--disallowedTools`(차단) — docs/configuration.md. 워크로드 아이덴티티 페더레이션 입력명 `anthropic_federation_rule_id` 등을 주석에 명시 — action.yml
- claude-code-action v1.0.235 ✅ (저장소 최신 태그), codex-action은 "버전은 릴리스에서 확인" 유지(태그 v1.12가 최신, GitHub Releases 없음)

### ✅ 확인 (요약)
- 기본값·옵션 9건(쓰기 권한자만 트리거(claude·codex), `allowed_non_write_users` "RISKY", `allowed_bots` 루프 방지, `prompt` 유무로 interactive/automation, `/install-github-app`, `--max-turns` in `claude_args`·concurrency, `ACTIONS_STEP_DEBUG` → full output, `drop-sudo`/`unprivileged-user`, permission profiles ≠ `safety-strategy`) — W-38~W-40, action.yml
- 인용·동작 6건("GITHUB_TOKEN 커밋은 워크플로를 트리거하지 않는다", PAT 금지 사유, 기본 설정에서 PR 자동 생성 안 함, 포크 PR 시크릿 미전달, 느슨한 권한 시 호스트 상태 보장 없음, HN avree "doesn't 'prevent'…") — W-38~W-40, C-휴6
- Copilot 7건(2025-09-25 GA·coding agent 명칭, 2026 cloud agent 개칭, 2025-11 Actions 없이 사용, 쓰기 권한자만 할당, Approve and run workflows, Ready/승인/머지 불가, Copilot 작성·할당자 공동 작성) — W-42, W-2
- 지시 파일 3건(AGENTS.md AAIF 2025-12-09·6만 개 이상, Copilot이 읽는 지시 파일 목록, CLAUDE.md 권고) — W-45, W-38
- 퍼블릭 저장소 self-hosted 러너 "should almost never be used" — W-15

### 미해소
- (없음)
