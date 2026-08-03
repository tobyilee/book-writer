# OpenAI Codex 사용법 완전 정리 — 저술 계획

> **장르:** tech-book (활성 프로필: `profiles/tech-book/`)
> **슬러그:** `codex-guide`
> **레퍼런스:** `codex-guide/01_reference.md` (148 URL / 고유 문서 약 140개, 2026-08-02 문서 기준)
> **계획 작성일:** 2026-08-02 · **개정:** 라운드 1 리뷰 반영 (Critical 7 / Major 12 / Minor 14 전건 반영)

---

## 제목 후보

1. **『Codex로 갈아타는 개발자』** — 톤: 담백한 실무 안내서. 포지셔닝: 마이그레이션 가이드. Claude Code에서 Codex로 이동하는 여정 자체를 상품으로 내세운다. 장점은 명확한 타깃, 단점은 "완전 정리"라는 레퍼런스 가치가 제목에 드러나지 않는다는 것.

2. **『같은 이름, 다른 동작 — Claude Code 사용자를 위한 OpenAI Codex 완전 정리』** — 톤: 함정 경고 + 레퍼런스 병행. 포지셔닝: 대상 독자의 가장 아픈 지점(`/clear`가 chat을 날리고, Esc 두 번이 파일을 되돌리지 않고, 중첩 `AGENTS.md`가 로드되지 않는다)을 제목에 그대로 박는다. 부제가 커버리지 약속을 담당한다.

3. **『두 번째 하네스』** — 톤: 개념적·에세이형. 포지셔닝: "모델이 아니라 하네스가 성능을 만든다"(Gorinova et al., arXiv:2606.17799)는 논지를 제목으로 세우고, Codex를 두 번째 하네스로 배우는 책이라고 규정한다. 가장 세련되지만 검색·서점 진열에서 무엇에 관한 책인지 즉시 읽히지 않는다.

**추천: 2번.** 이 책의 독자는 "Codex가 뭐냐"를 묻지 않는다. 이미 Claude Code로 에이전틱 코딩을 해봤고, 두 번째 도구를 손에 쥔 사람이다. 그에게 가장 잘 팔리는 약속은 **"내가 알던 것과 무엇이 다른지, 그리고 빠짐없이"**다. 주제목이 관점(대응·차이)을, 부제가 커버리지(완전 정리)를 각각 책임지므로 이 책의 두 제약 조건이 제목 한 줄에 모두 들어간다.

> **주제목 전용 규칙 (M10 반영).** 『같은 이름, 다른 동작』은 **책 전체의 소유**다. 어떤 챕터도 이 문구를 제목·소제목으로 쓰지 않는다 — 3장이 이 문구를 가져가면 나머지 11개 장이 부제 밑으로 밀리고, 목차를 펼친 독자는 "3장이 이 책의 본체인가"로 읽는다. 3장 제목은 **「손이 먼저 기억한다 — 첫 주에 나는 사고들」**로 확정한다.

---

## 책 특성

- **장르:** tech-book — 레퍼런스 성격이 강한 실무 기술서 (에세이형 서술 + 원장형 표 병행)
- **분량:** 12장 / 약 **108,000자**(한글, 순수 산문 기준). 부속(머리말·에필로그·참고문헌) 포함 시 약 118,000자
- **난이도:** 중급~고급. AI 에이전틱 코딩 경험을 **전제**한다. 에이전트·MCP·훅·샌드박스 같은 용어를 처음부터 설명하지 않는다
- **독자 여정:**
  - **진입 상태** — Claude Code로 실무를 해봤고, `CLAUDE.md`·훅·스킬·MCP를 자기 손에 맞춰 세팅해둔 **개인 개발자**. Codex를 깔아봤거나 깔 예정이며, "설정을 다시 다 해야 하나", "내 습관 중 뭐가 위험한가", "요금은 어떻게 되나"가 머릿속에 있다.
  - **각성 지점** — 3장. 손이 기억하는 동작이 Codex에서 다른 결과를 낸다는 것을 확인하는 순간. 특히 **Esc 두 번은 대화만 되감고 파일 수정은 워킹 트리에 남는다**는 사실.
  - **배움** — 4~8장. 지침·설정·권한·확장·프롬프팅·비용이라는 여섯 축을 Claude Code 대응 관계로 재구성해 익힌다.
  - **적용** — 9~11장. 위임(로컬·클라우드·비대화형), 리뷰·보안, 부품화·조직 종속으로 자기 업무 형태에 맞춰 붙인다.
  - **출구 상태** — Codex를 **Claude Code의 대체재가 아니라 다른 성질의 두 번째 하네스**로 다룰 수 있다. 구체적으로: 임포트로 30분 만에 이주하고, 승인·샌드박스 3축을 구분해 설정하고, 모델 선택을 비용 설계로 이해하고, 어떤 작업을 어느 도구에 맡길지 스스로 판단한다.
  - **시점 고정 (C7·판정 3 반영):** 이 책의 서술 시점은 **끝까지 개인 개발자**다. 11장 엔터프라이즈 절에서도 독자를 관리자 대리인 자리에 세우지 않는다 — "관리자가 무엇을 정하는가"가 아니라 **"내 설정이 왜 안 먹히는가"**로 쓴다.

---

## 저술 규율 (전 챕터 공통 제약 — 저술가·fact-checker 필독)

계획 단계에서 못 박는다. 이 규율은 챕터별 지시보다 우선한다.

1. **시점 병기 의무 — 문안은 `(2026-08-02 문서 기준)` 하나로 고정한다** (m7 반영). "2026년 8월 기준"·"2026-08 기준" 등 변형 표기를 쓰지 않는다. 공식 문서에 발행일 표기가 없으므로 시점 앵커는 이것 하나뿐이다.
   - **남발 방지:** **장당 첫 등장 1회 + 수치 표 캡션에만** 붙인다. 매 문단 반복하면 스타일 체크리스트의 tic 과포화에 걸린다.
2. **권한 프로필은 Beta다.** 정전처럼 서술하지 않는다. 논지는 **"구 체계(`sandbox_mode`/`approval_policy`)가 기본이고, 신 체계(권한 프로필)가 Beta로 병행한다"**이며, 폴백 규칙("구 설정이 어디에라도 있으면 구 체계가 이긴다")을 반드시 함께 쓴다.
3. **승인 축은 셋이다.** ⓐ `sandbox` ⓑ `approvals` ⓒ `approvals_reviewer` + `granular` 하위 토글 5개. **Claude Code 대응표는 3축 기준으로 작성한다.** 2축으로 뭉개면 5장 전체가 틀린다.
4. **요금·한도는 최고 위험 영역이다.** 범위값(`10-100` 등)을 단일 수치로 뭉개지 않는다. 커뮤니티의 한도 급등 주장(#28879)은 **"커뮤니티 관측 / 공식 문서로 확인·반박 불가"**로 귀속해서만 쓴다.
5. **🕒 모델 은퇴는 미래 시제로 쓴다 (C1 — 레퍼런스 오류 정정).**

   > `gpt-5.4`·`gpt-5.4-mini`는 **2026-08-31 은퇴 예정**이다(ChatGPT 로그인 사용자 한정 — API 키 인증은 영향 없음). 대체는 각각 Terra·Luna. **2026-08-02 문서 기준으로는 아직 은퇴 전이다.** 이 책을 읽는 시점에는 이미 지난 날짜일 가능성이 높으므로, 은퇴 여부가 아니라 **대체 경로**를 기준으로 읽어라.

   - **서술 시제를 미래형으로 고정한다** — "은퇴했다" 금지, "은퇴 예정이다" 사용. **8장과 12장 양쪽에 위 문안을 그대로 적용**한다.
   - ⚠️ **레퍼런스 §3-1·§7-4 #1의 "이 책이 나오는 시점엔 이미 지난 날짜다"는 무효다.** 레퍼런스 작성자가 집필 시점을 뒤로 가정한 오류이며, 계획 라운드 1에서 오류로 확정·정정했다(오늘 2026-08-02 기준 은퇴일은 29일 뒤 미래다). **저술가는 레퍼런스를 직접 읽고 이 정정을 되돌리지 않는다.** 동일 내용이 `codex-guide/fact_rules_active.md`에 시드돼 있다.
   - **그 밖의 🕒 재확인 항목:** `/rewind` #11626, 중첩 AGENTS.md #12115, 60초 자동 응답 #28969, 요금·한도 #28879/#34035, 권한 프로필 Beta 딱지, Codex Security(출시 4일 차 관측), 모델 라인업, 컨텍스트 창 #32806.
6. **인용 금지 판정 준수 — 9건** (`01_reference.md` §7-3의 8건 + m10 추가 1건). dev.to 65% 설문 / "2.2배" 벤치마크 / 세션 6,852건 통계 / SWE-Lancer 모델별 수치 / Terminal-Bench **구체 순위** / Threads(qjc.ai) / SEO성 정리 콘텐츠 4곳 / velog 토큰 비교 / **`/codex/overview`의 UI 삽화 속 문자열**("5.6 Sol Extra High" vs "5.6 Sol Extended" — 리서처 2인이 서로 다르게 판독, §3-1) — **어느 챕터에서도 쓰지 않는다.**
7. **문서 내부 불일치 6건**(§3-11)은 정전 페이지 하나만 인용한다. WSL 경로 성능 권고는 **아예 쓰지 않는다**(확정 불가).
8. **명칭 주의:** `/codex/artifacts-viewer`의 실제 제목은 **"Work with files"**다. "Artifacts viewer"를 용어·소제목으로 쓰지 않는다. 성숙도도 "Codex는 4단계 체계를 쓴다"로 일반화하지 않는다(정의표만 있고 기능별 등급 목록이 없다).
9. **커뮤니티 인용은 진영을 밝힌다.** r/codex·r/ClaudeAI 출신 자료는 출신 서브레딧을 명시하고, 게시일을 붙인다.
10. **"Codex는 오픈소스다"라고 쓰지 않는다.** CLI·SDK·app-server·skills는 오픈소스지만 IDE 확장과 cloud는 명시적으로 "Not open source"다.
11. **경험담을 만들지 않는다 (C5 신설 — 라운드 1 "저자 경험 서술로 메운다" 지시 철회).** 이 책에 등장하는 모든 1인칭 사례·현장 일화·수치는 **레퍼런스에 출처와 게시일이 있는 것뿐**이다. "내가 겪었다", "한 동료가", "어느 팀에서는" 류의 **출처 없는 경험 서술을 쓰지 않는다.** 공감 소재가 필요하면 아래 4종에서 고른다.
    - ⓐ **AWS 한국 기술블로그**(Kyutae Park, Ph.D, AWS AI 스페셜리스트 SA, 2026-06-11 — 실명·소속이 있는 국내 유일 심층 비교 자료)
    - ⓑ **dcinside 특이점갤**(코유키1357, 2026-04-28, 조회 7,507)
    - ⓒ **GitHub 이슈 댓글**(#12115 전환 포기 사유 2건: anrooo 2026-05-15, leonardo-panseri 2026-06-04)
    - ⓓ **HN·r/codex 인용**(진영·게시일 병기), GeekNews 한국어 댓글
    - 국내 사례가 부족한 것은 **결함이 아니라 사실**이며, 필요하면 "한국어 1차 후기가 거의 없다"는 것 자체를 서술한다(레퍼런스 §7-2 #3이 확정 보고한 발견이다).
    - **3장 오프닝('실패 장면')은 인용된 실패로 연다** — #11626 댓글 또는 dcinside 증언. **지어낸 새벽 3시로 열지 않는다.**
12. **Claude Code 쪽 사실 주장은 화이트리스트 안에서만 쓴다 (C6 신설).** 이 책의 레퍼런스는 Claude Code 문서를 1차 수집하지 않았다. 따라서 Claude Code에 대한 구체 주장은 레퍼런스 **§1-5(용어 대응 빠른 지도) · §4-2(같은 이름 다른 동작 6행) · §4-4(Claude Code에만 있는 것 6항목)**에 명시된 것으로 한정한다. 그 밖의 주장(버전·플래그명·기본값·이벤트 개수·요금·모델 라인업)은 쓰지 않는다. 꼭 필요하면 `(사실 확인 필요)` 주석을 달고 **fact-checker에게 에스컬레이션**한다 — **저술가 재량으로 덮지 않는다.**
    - 특히 훅 이벤트 "29+"(§4-2)는 레퍼런스가 Codex 문서·이슈 경유로 확보한 수치이므로, "Claude Code는 29개 이벤트를 지원한다"가 아니라 **"Codex 측 이슈(#21753)가 대조군으로 제시한 수치"**로 귀속해서 쓴다.
    - 대응 관계 서술의 안전한 문형: **"Codex는 X다. Claude Code 사용자에게 익숙한 Y와는 여기서 갈린다."** Claude Code 쪽을 새로 정의하지 말고 독자가 이미 아는 것으로 취급한다.

---

## 분량 규약 (프로필 기본값 오버라이드)

`profiles/tech-book/scaffolds.md`의 기본값은 챕터당 3,000~6,000자다. 이 책은 140개 문서를 커버해야 하므로 **오버라이드한다.**

- **챕터 목표:** 7,000~10,000자 (한글, **표·코드 블록·mermaid·인용 블록을 제외한 순수 산문 기준**)
- **스케일 규칙 적용:** 문단을 늘리지 말고 **소절(`###`) 수를 늘린다.** 챕터당 소절 **6~7개**, **소절당 순수 산문 3,000자 상한**
- **표는 분량이 아니라 밀도다.** 이 책은 원장형 표가 많다 — 표를 넣었다고 산문 몫을 줄이지 않는다. 표는 항상 산문 해설과 짝을 이룬다. **10장 소절 4·6, 11장 소절 5, 12장 소절 2는 "표 1개 + 산문 해설" 짝을 의무화**한다(표가 페이지 수를 흡수하고 산문은 흐름만 설명한다)
- **mermaid 다이어그램:** 구조·관계·흐름은 산문으로 늘어놓지 말고 도식으로 그린다. 챕터마다 그림 번호는 1부터. 장별 배정은 **통권 변주 배정표의 "그림" 열이 단일 출처**다(총 7개)
- **`### 이 장의 핵심` 박스:** 개념 밀도가 높은 **4·5·6·8장에만** 둔다. 형식은 전 책에서 통일(3~5 불릿)
- **총량:** **108,000자** (장별: 1장 8,000 · 2장 7,000 · 3장 9,000 · 4장 9,000 · 5장 10,000 · 6장 9,000 · 7장 9,000 · 8장 10,000 · 9장 9,000 · 10장 10,000 · 11장 10,000 · 12장 8,000)

---

## 내러티브 아크

이 책은 **"낯선 제품을 배우는 순서"가 아니라 "이미 아는 것을 다시 배우는 순서"**로 흐른다.

**1장**은 전제를 교정한다. Claude Code 사용자는 Codex를 "OpenAI가 만든 Claude Code"로 상상하고 들어오는데, Codex는 단일 CLI 도구가 아니라 ChatGPT 우산 아래의 표면 집합이다. 여기서 제품 지도를 펼치고, **2026년 상반기에 표면이 어떻게 늘어났는지 연표로 심고**, 오픈소스 경계가 CLI 층에서 정확히 뒤집혀 있다는 사실로 두 제품의 전략 차이를 먼저 각인시킨다. **2장**은 곧바로 손을 움직이게 한다 — `/codex/import`가 `CLAUDE.md`→`AGENTS.md`, `settings.json`→`config.toml`, 슬래시 명령→스킬까지 이주 경로를 문서와 프로토콜 양쪽에 구현해뒀기 때문이다. 배우기 전에 옮겨놓고 시작하는 편이 이 독자에게 자연스럽다. **다만 임포트에는 알려진 사고가 있으므로, 되돌릴 수 있게 만들어두는 5분 절차를 먼저 세우고 옮긴다** — 독자는 승인·샌드박스를 5장에서야 배우기 때문이다.

**3장**이 이 책의 각성 지점이다. 임포트가 끝났으니 이제 손이 움직이는데, 같은 이름의 명령이 다른 일을 한다. `/clear`, Esc 두 번, 중첩 지침 파일, `$` 접두사, 위험 플래그 이름 — 여기서 독자는 "설정을 옮겼다고 이주가 끝난 게 아니구나"를 몸으로 안다. 그 충격을 동력 삼아 **4~6장**에서 통제 장치를 하나씩 다시 세운다. 지침과 설정(4장) → 승인과 샌드박스(5장) → 확장 모델(6장) 순서인 이유는 명확하다. 설정 파일이 어디 있는지 알아야 권한을 걸 수 있고, 권한 경계를 알아야 훅·스킬·execpolicy가 무엇을 막는지 이해된다.

**7·8장**은 매일의 운용이다. 프롬프트와 chat 단위 관리(7장), 그리고 모델 선택이 곧 비용 설계라는 사실(8장). 8장을 7장 뒤에 둔 것은 의도적이다 — 어떤 작업을 어떻게 시키는지 알기 전에 요금표부터 보면 숫자가 추상으로 남는다. **9~11장**은 확장 반경을 넓힌다. 내 노트북 밖으로(9장 위임), 내 코드 밖으로(10장 리뷰·보안), 내 손 밖으로(11장 SDK·MCP·조직 종속). 이 세 장이 **"내 손 밖에서 내 환경이 결정된다"**는 공통 논지를 완성한다 — 11장 후반의 엔터프라이즈 절이 "관리자 매뉴얼"이 아니라 "내 설정이 왜 안 먹히는가"인 이유가 여기 있다.

**12장**은 갈라진 진화를 정면으로 다룬다. 2026년 상반기 Codex는 터미널 도구에서 데스크톱 앱·브라우저·컴퓨터 조작·음성·전용 하드웨어로 뻗어나갔고, 같은 기간 Claude Code는 CLI/SDK 중심을 지켰다. **1장에서 심은 연표를 여기서 회수**하면, Codex 고유 표면 소개가 단순한 잔여 처리도 나열도 아니라 **앞 장에서 심어둔 사실의 회수이자 논지의 증거 제시**가 된다. 그리고 마지막 절에서 "둘 중 하나를 고르라"가 아니라 "성질이 다른 두 하네스를 어떻게 함께 쓰는가"로 책을 닫는다. 이것이 대상 독자에게 정직한 결론이다 — 그들은 이미 Claude Code를 쓰고 있고, 앞으로도 버리지 않을 것이기 때문이다.

---

## 설계 근거

### 채택한 구조의 이유

1. **"이주 → 각성 → 재구축 → 운용 → 확장 → 종합" 6단 흐름이 대상 독자의 실제 시간 순서와 일치한다.** 이 독자는 Codex를 백지에서 배우지 않는다. 이미 있는 세팅을 옮기고(2장), 손버릇에 데이고(3장), 다시 세우는(4~6장) 순서로 겪는다. 학습 순서를 독자의 실제 겪는 순서에 맞추면 각 장의 동기가 저절로 생긴다.
2. **Claude Code 대응 관점을 "비교 챕터"로 분리하지 않고 전 장에 분산했다.** 대응 관점을 한두 장에 몰면 나머지 장이 일반 매뉴얼이 되고, 그 순간 "공식 문서를 한국어로 옮긴 책"과 구별되지 않는다. 각 장에 **Claude Code 대응 포인트**를 필수 항목으로 박아 축이 끊기지 않게 했다. 다만 이 결정에는 대가가 따르므로 **규율 12(Claude Code 사실 주장 화이트리스트)**로 봉인했다 — 레퍼런스가 Claude Code 문서를 1차 수집하지 않았기 때문에, 12개 장 전부가 1차 소스 없는 사실 주장을 생산할 구조적 위험을 안고 있었다.
3. **커버리지를 "챕터 배정"이 아니라 "쓸 자리"로 증명한다.** 148개 URL에 담당 챕터를 지정하는 것만으로는 부족하다는 것이 라운드 1의 판정이었다 — 매핑표는 "어느 장이 맡는가"만 보여줄 뿐 "그 장에 그 문서를 쓸 자리가 있는가"는 보여주지 않는다. 그래서 형식적 배정이 있던 5개 장(1·4·9·10·11)에 **소절을 신설하거나 표를 의무화**했고, 각 장에 **필수 산출 아티팩트**를 행·열 구성까지 명세했다. 커버리지 점검 대상도 공식 문서 148개에서 **커뮤니티 이슈 16건 + 학술 문헌 11건 + 국내 1차 소스 3종**으로 확장했다(아래 "커뮤니티·학술 소스 배정 표").

### 기각한 대안 1 — 공식 문서 트리 미러링 (A~F 그룹을 그대로 6부로)

레퍼런스 §6-1의 문서 그룹 A(기초·표면) B(설정) C(개발자 도구) D(보안) E(엔터프라이즈) F(추가)를 그대로 6부 구조로 삼는 안.

**기각 사유:** 커버리지는 100% 자동 달성되지만 독자 여정이 없다. 문서 트리는 "찾아보는 사람"을 위한 배열이지 "처음부터 읽는 사람"을 위한 배열이 아니다. 더 결정적으로 **Claude Code 대응 축이 통째로 사라진다** — 이 축이 없으면 대상 독자에게 이 책의 존재 이유가 없다. 또한 별칭 중복 6쌍(`/codex/cli/reference` ≡ `/codex/cli/slash-commands` 등)과 문서 내부 불일치 6건을 구조가 그대로 물려받아, 같은 내용을 두 곳에서 다르게 서술할 위험이 구조적으로 생긴다.

### 기각한 대안 2 — 태스크 기반 쿡북 (설치 → 첫 작업 → 리뷰 → 배포 → 팀 확산)

"이런 일을 하고 싶을 때"로 목차를 세우는 실전 쿡북 안. 실용서 감각으로는 가장 잘 읽힌다.

**기각 사유:** **"빠짐없이"라는 제약과 정면 충돌한다.** 태스크에 걸리지 않는 문서가 대량으로 탈락한다 — `/codex/feature-maturity`, `/codex/open-source`, `/codex/enterprise/compliance-api`, `/codex/security/threat-model`, `/codex/hipaa-configuration` 같은 것들은 어떤 태스크의 단계로도 자연스럽게 들어가지 않는다. 억지로 부록에 몰아넣으면 "완전 정리"가 아니라 "쿡북 + 잡동사니 부록"이 된다. 게다가 태스크 서술은 UI·플래그 변화에 가장 먼저 낡는데, 이 주제는 **주 단위로 변한다**(§7-4).

### 기각한 대안 3 — 전면 대조 구조 (매 장을 Claude Code vs Codex 표 대결로)

모든 장을 좌우 2열 비교로 구성하는 안. 대상 독자 관점을 극한까지 밀어붙인 형태다.

**기각 사유:** **Codex 고유 기능이 "대응 없음"이라는 빈칸으로만 처리된다.** Codex cloud, Computer Use, Chronicle, Appshots, Auto-review, execpolicy 테스트 하네스, Sites, Micro — 레퍼런스 §4-3이 열거한 이 목록은 책의 상당 부분을 차지하는데, 대조 표에서는 전부 한쪽이 비어 있는 행이 된다. 대조는 **관점**으로 유지하되 **골격**은 Codex 자신의 구조를 따르는 편이, 고유 기능을 정당한 분량으로 설명하면서 대응 관계도 놓치지 않는 유일한 길이다. 부수적으로, 전면 대조는 Claude Code 쪽 사실 주장이 챕터마다 늘어나 fact-check 부담이 두 배가 된다(이 책의 레퍼런스는 Codex 문서 기반이며 Claude Code 문서를 1차 수집하지 않았다 — 이 제약이 규율 12의 근거다).

### 기각한 대안 4 — 13장 분리 (11장을 "부품화"와 "조직 배포"로 쪼개기)

라운드 1 제출본의 열린 위험 3에서 planner 자신이 제기한 안. 리뷰 판정 3에서 **기각**으로 결론났고, 그 판단을 수용한다.

**기각 사유:** ⓐ 12장 구조에 맞춰 짜인 **통권 변주 배정표가 무효**가 된다 — 13장이면 오프닝·클로징·스캐폴드를 전면 재배정하고 인접 중복 0을 다시 만들어야 한다. ⓑ 분리하면 "조직 배포" 장이 독립적으로 서는데, **개인 개발자 독자에게 그 장 전체가 건너뛰기 대상**이 된다. 이질성이 해소되는 게 아니라 한 장이 통째로 버려진다. ⓒ 이질성의 진짜 원인은 장의 크기가 아니라 **독자 시점이 장 중간에서 개인 → 관리자로 바뀌는 것**이었다. 시점을 개인에 고정하는 리프레임(C7 — "내 설정이 왜 안 먹히는가")으로 원인을 제거했으므로 분리가 불필요해졌다. 시점이 끝까지 개인 개발자에 머물면 SDK·MCP 절과 엔터프라이즈 절이 같은 논지("내 손 밖에서 내 환경이 결정된다") 아래 묶인다.

---

## 통권 변주 배정표

저술가는 자기 장만 보므로 통권 수렴은 계획에서만 막을 수 있다. 아래 배정은 **구속력이 있다.**

| 장 | 오프닝 기법 | 클로징 기법 | 클로징 정의 (m8) | 스캐폴드 유형 | 그림 (m12) |
|---|---|---|---|---|---|
| 1 | 정의 뒤집기 | 되묻고 닫기 | 서두에 던진 전제를 독자에게 되돌려 묻고, 답은 다음 장에 맡긴다 | 개념 도입형 | 표면 지도 / 연표 (2) |
| 2 | 인용·일화 | 체크리스트 착지형 | 장에서 흩어진 절차를 번호 목록 하나로 모아 닫는다 | 문제-해결형 | 임포트 흐름 (1) |
| 3 | 실패 장면(in medias res) | 대가 명시형 | 이 장에서 배운 편의가 무엇을 대가로 요구하는지 밝히고 닫는다 | 사례 분석형 | — |
| 4 | 충격적 수치·사실 | 적용 과제형 | 독자가 오늘 자기 환경에서 실행할 한 가지를 지정한다 | 문제-해결형 | — |
| 5 | 정의 뒤집기 | 스키마로 착지형 | 장에서 세운 개념을 설정 스키마·표 하나로 압축해 닫는다 | 개념 도입형 | 3축 분리 / 폴백 결정 흐름 (2) |
| 6 | 상황 가정 | 방법 제시형 | 마지막 문단을 재현 가능한 절차로 바꿔 닫는다 | 비교 대조형 | — |
| 7 | 수사적 질문 | 한 문장 여운형 | 요약 없이 한 문장으로 매듭짓는다 | 문제-해결형 | — |
| 8 | 충격적 수치·사실 | 미해결 고지형 | 확인 불가·판정 유보 항목을 명시하고 독자에게 넘기며 닫는다 | 비교 대조형 | — |
| 9 | 상황 가정 | 사례의 결말 | 장 도입에 꺼낸 사례가 어떻게 끝났는지 알려주며 닫는다 | 사례 분석형 | 위임 결정 흐름 (1) |
| 10 | 인용·일화 | 원문 인용으로 닫기 | 해설을 붙이지 않고 1차 소스 문장 하나로 끝낸다 | 문제-해결형 | — |
| 11 | 수사적 질문 | 선택지 제시형 | 상황별 갈림길 2~3개를 제시하고 선택을 독자에게 남긴다 | 비교 대조형 | SDK·app-server·MCP 3경로 (1) |
| 12 | 앞 장 콜백 | 여정 회수형 | 책 전체가 지나온 축을 회고하고 가져갈 관점을 분명히 한다 | 종합 정리형 | — |

**검증:**
- 인접 장 오프닝 중복 **0건** (1정의뒤집기 → 2인용 → 3실패장면 → 4수치 → 5정의뒤집기 → 6상황가정 → 7수사질문 → 8수치 → 9상황가정 → 10인용 → 11수사질문 → 12콜백)
- 오프닝 분포 균등 — 프로필 메뉴 **7종 전부 사용**, 정의뒤집기 2 / 인용 2 / 수치 2 / 상황가정 2 / 수사질문 2 / 실패장면 1 / 콜백 1
- '상황 가정' 오프닝 **2/12 = 17%** (상한 1/3 이하 충족)
- 클로징 기법 **12개 전부 상이** + 프로필 `scaffolds.md`에 없는 기법명 전부에 **한 줄 정의 부여**(m8 반영 — 저술가가 해석할 근거를 제공)
- 스캐폴드 유형 인접 중복 **0건**. 분포: 문제-해결형 4 / 비교 대조형 3 / 개념 도입형 2 / 사례 분석형 2 / 종합 정리형 1
- **그림 총 7개** — 1장 2 / 2장 1 / 5장 2 / 9장 1 / 11장 1. **이 표가 그림 배정의 단일 출처**이며, 장 항목의 그림 언급은 이 표를 따른다(m12 반영)

> **⚠️ M6 반영의 부수 효과 고지.** 리뷰 M6은 3장(비교대조→사례분석)·10장(개념도입→문제해결) 교체 시 "비교 대조형이 33%→25%로 완화된다"고 평가했으나, 재계산 결과 **문제-해결형이 3→4(33%)로 올라가 최대 쏠림 수치는 33%로 동일**하다. 그럼에도 M6을 반영한 이유는 **"장의 실제 진행과 스캐폴드의 일치"가 "유형 분포 균등"보다 상위 기준**이기 때문이다 — 3장은 선택지 비교가 아니라 사고 사례이고(오프닝 '실패 장면'과의 궁합도 사례 분석형이 낫다), 10장은 통념 제시 → 반증 → 재조정이다. 분포를 맞추려 4장·7장을 억지 유형으로 바꾸면 같은 문제를 다른 장으로 옮기는 것에 불과하다.

---

## 챕터 목록

각 장의 **필수 산출 아티팩트**(M8)는 저술에서 반드시 생산해야 하는 물건이다. 산문으로만 풀면 약속이 이행되지 않고, Phase 4.5 통권 수락 게이트의 "약속 이행 무결성" 검사에서 BLOCK이 난다.

### 1장. Codex는 제품이 아니다 — 표면의 집합을 먼저 이해하기

- **핵심 질문:** 내가 아는 "CLI 하나로 시작해서 CLI 하나로 끝나는 도구"라는 전제는 Codex에 얼마나 통하는가?
- **소절 구성 (6개 — M1 반영):**
  1. 공식 문서의 **3분법**(Chat / ChatGPT Work / Codex) — Claude Code에는 대응 개념이 없는 제품 전략. 원문 표 그대로 인용
  2. 표면 전수 지도 — ChatGPT 데스크톱 앱(1급 표면) · 웹 · CLI · IDE 확장 · Codex cloud(개괄, 심화는 9장) · 주변부. **그림 1(mermaid 표면 지도)**. `/codex/features`가 이 지도의 캡션 근거, `/codex/glossary`는 2장 용어 정전 표의 근거로 앵커링
  3. **오픈소스 경계 비대칭** — CLI·SDK·app-server·skills는 오픈소스, IDE 확장과 cloud는 "Not open source". Claude Code는 CLI 층이 비공개이므로 **CLI 층에서 정확히 뒤집힌 구도**. `/codex/community/codex-for-oss`를 여기에 배치(⚠️ 본문의 "GPT-5.4" 언급은 단독 근거 금지)
  4. **2026년 상반기에 무슨 일이 있었나 — 표면이 늘어난 연표** (M1 신설). `whats-new`·`changelog`(**95개 항목** 전수 색인)에서 굵은 마디만: 앱 macOS 출시(2026-02-02~06) → Windows 네이티브(2026-03-02~06) → 임포트의 Claude Code 지원 명시(changelog 2026-06-09, **2장 예고**) → **Codex 앱이 ChatGPT 데스크톱 앱으로 병합(2026-07-09)** → ChatGPT Work 출시(2026-07-09) → Codex Micro(2026-07-15) → 다중 폴더(2026-07-20~24) → Codex Security(2026-07-28). **그림 2(mermaid timeline)** — **12장이 이 연표를 콜백해 "진화 방향이 갈렸다"의 증거로 재사용한다**
  5. 성숙도 라벨을 다루는 법 — 4등급 정의표는 있으나 **기능별 등급 목록이 없다.** "Codex는 4단계 성숙도 체계를 쓴다"는 **과잉 일반화**다. ⚠️ `experimental` 명령 **목록 전수는 9장 단독**이며(m5), 1장은 개념 경고만 한다
  6. 이 책의 존재 이유 — 하네스 요소 하나가 모델 세대를 통째로 올리는 것만큼 점수를 바꾼다(Gorinova et al., arXiv:2606.17799, 2026 📄 preprint), 인터페이스가 성능이다(Yang et al., SWE-agent, NeurIPS 2024 ✅)
- **독자가 얻는 것:** "Codex = OpenAI판 Claude Code"라는 오해를 버리고, 자기가 쓸 표면을 먼저 고르는 판단 기준
- **필수 산출 아티팩트:** ① 표면 지도 mermaid(그림 1) ② **표면 확장 연표 mermaid timeline(그림 2 — 12장 콜백 대상)**
- **Claude Code 대응 포인트:** 단일 표면(CLI) vs 표면 집합 / cwd 암묵 vs 온보딩에서 폴더를 명시적으로 고르는 절차 / 오픈소스 경계 역전
- **커버 문서:** `/codex`, `/codex/overview`, `/codex/use-chatgpt`, `/codex/get-started-with-work`, `/codex/app`, `/codex/web`, `/codex/cli`, `/codex/ide`, `/codex/cloud`(보 — 개괄), `/codex/features`, `/codex/feature-maturity`, `/codex/open-source`, `/codex/glossary`, `/codex/whats-new`, `/codex/changelog`, `/codex/community/codex-for-oss`, `/codex/guides/build-ai-native-engineering-team`(보)
- **오프닝:** 정의 뒤집기 / **클로징:** 되묻고 닫기 / **스캐폴드:** 개념 도입형
- **예상 분량:** 8,000자 (소절 6개)

---

### 2장. 이주는 이미 구현돼 있다 — `/codex/import`가 말해주는 것

- **핵심 질문:** 내 `CLAUDE.md`·훅·스킬·MCP 설정을 처음부터 다시 만들어야 하는가?
- **소절 구성 (6개 — M3·M2 반영):**
  1. **임포트 전 5분 — 되돌릴 수 있게 만들어두기** (M3 신설, 순서상 맨 앞). 이 장은 "배우기 전에 옮겨놓고 시작하라"고 권하는데, 독자는 승인·샌드박스를 5장에서야 배운다. 절차 없이 따라 하면 3장 전에 사고가 난다. ① `~/.codex/config.toml` **백업**(#24515가 덮어쓰는 바로 그 파일) ② **깨끗한 git 트리에서 시작**(§5-8 #4) ③ 첫 실행은 **`--sandbox read-only`** — 5장에서 제대로 배우기 전까지의 안전 기본값 ④ 임포트 직후 **`/debug-config`**로 레이어 순서·정책 출처 확인(4장 예고) ⑤ 원문 "임포트 후 반드시 검토할 것" 5항목 대조
  2. 임포트 매핑 표 10행 원문 그대로 — `CLAUDE.md`→`AGENTS.md`, `settings.json`→`config.toml`, **슬래시 명령→스킬**, 서브에이전트→Codex agents, 최근 30일 chat→ChatGPT chats
  3. 프로토콜 수준 구현 — `externalAgentConfig/detect`·`import`, `"source": "claude-code"`, 마이그레이션 `itemType` **9종**(`AGENTS_MD`·`CONFIG`·`SKILLS`·`PLUGINS`·`MCP_SERVER_CONFIG`·`SUBAGENTS`·`HOOKS`·`COMMANDS`·`SESSIONS`), 경로 매핑 예시(`/Users/me/project/CLAUDE.md` → `AGENTS.md`, `~/.claude/skills` → `~/.agents/skills`). **그림 1(mermaid 임포트 흐름 — 감지 → itemType 9종 → 대상)**
  4. 비파괴 보장과 그 한계 — "Importing doesn't change or delete your existing agent setup" / 중복 방지 규칙(비어 있지 않은 `AGENTS.md`는 건너뛰고, 스킬 임포트는 기존 디렉터리를 덮어쓰지 않는다) / ⚠️ **Standard Claude Chat data는 임포트 불가** / 최근 **30일** chat만 / 마켓플레이스 추론(`extraKnownMarketplaces` 부재 시 `anthropics/claude-plugins-official` 유추). 알려진 사고 [#24515](https://github.com/openai/codex/issues/24515)(프로젝트 설정이 없을 때 **사용자 레벨** `~/.codex/config.toml`을 덮어써 승인 폭탄)는 **"커뮤니티 보고, open"으로 귀속**하되 소절 1의 백업 절차와 짝을 이룬다
  5. 인증 정리 — `codex login` 계열 6종(`--with-api-key` / `--with-access-token` / `--device-auth`(beta) / `status` / `logout`), `~/.codex/auth.json`, `CODEX_HOME` 기본값 `~/.codex`, `cli_auth_credentials_store`, 환경 변수 3종(`OPENAI_API_KEY`·`CODEX_ACCESS_TOKEN`·`CODEX_CA_CERTIFICATE`), 콜백 포트 **`localhost:1455`**와 SSH 포워딩(`ssh -L 1455:localhost:1455`), ⚠️ API 키 로그인 시 기능 제약("Some features might not be available")
  6. **용어 대응 빠른 지도 — 이 책의 정전** (M2 신설). 레퍼런스 §1-5의 10행 대응표(`AGENTS.md`↔`CLAUDE.md` / `config.toml`↔`settings.json` / Skills↔Skills / `$skill`↔`/skill` / execpolicy `.rules`↔`permissions.allow/deny/ask` / Hooks↔Hooks(부분) / Subagents↔Subagents / Custom prompts↔커스텀 슬래시 명령(Codex 쪽 deprecated) / `codex exec`↔`claude -p` / Codex cloud·Chronicle·Computer Use·Appshots↔대응 없음)를 통째로 싣는다. 임포트 매핑 표(소절 2)와 나란히 놓여 **"문서가 보증하는 이주 경로"와 "개념 대응"의 대비**를 만든다. **이 표를 전 책 용어 정전으로 선언한다** — 이후 장에서 대응 관계를 서술할 때 이 표의 용어·표기를 벗어나지 않으며, editor의 용어 통일 검수 기준이 된다
- **독자가 얻는 것:** 30분 안에 기존 세팅을 옮기고, **옮기기 전에 되돌릴 수 있게 만들고**, 옮긴 뒤 손으로 확인해야 할 항목 체크리스트
- **필수 산출 아티팩트:** ① **임포트 전 5단계 체크리스트**(번호 목록 — 클로징 '체크리스트 착지형'의 실제 내용물) ② 임포트 매핑 표 10행 ③ **용어 대응 정전 표 10행** ④ 임포트 흐름 mermaid(그림 1)
- **Claude Code 대응 포인트:** 이 장 전체가 대응이다. 특히 **슬래시 명령이 스킬로 접힌다**는 사실이 두 제품 확장 모델 차이의 압축판
- **커버 문서:** `/codex/import`, `/codex/quickstart`, `/codex/auth`, `/codex/enterprise/access-tokens`(보 — 인증 부분), `/codex/app-server`(보 — `externalAgentConfig` 부분), `/codex/reference/troubleshooting`, `/codex/glossary`(보 — 용어 정전 표 근거)
- **오프닝:** 인용·일화 / **클로징:** 체크리스트 착지형 / **스캐폴드:** 문제-해결형
- **예상 분량:** 7,000자 (소절 6개)

---

### 3장. 손이 먼저 기억한다 — 첫 주에 나는 사고들

> **제목 변경 (M10):** 라운드 1의 「같은 이름, 다른 동작 — 손이 먼저 기억하는 것들」에서 개칭. 그 문구는 책 주제목의 소유다.

- **핵심 질문:** 설정을 다 옮겼는데 왜 여전히 사고가 나는가?
- **소절 구성 (6개):**
  1. **위험도 최고 3종** — ⓐ `/clear`가 컨텍스트 초기화가 아니라 **터미널을 지우고 새 chat 시작**(뷰만 지우려면 <kbd>Ctrl</kbd>+<kbd>L</kbd>) ⓑ **Esc 두 번은 대화만 되감고 파일 수정은 워킹 트리에 그대로 남는다** — `/rewind` 부재([#11626](https://github.com/openai/codex/issues/11626), 2026-02-12, 👍192, open) ⓒ **중첩 `AGENTS.md`를 자동 로드하지 않는다**([#12115](https://github.com/openai/codex/issues/12115), 👍102, open)
  2. **중첩 `AGENTS.md` — 이 장이 주 서술이다** (M9 분담). 현상 + 사고 + 증언까지. 전환 포기 사유로 직접 언급된 댓글 2건(anrooo 2026-05-15 "This is keeping me from switching from Claude Code, it's really tough to have pretty well-configured AGENTS.md files everywhere only to have Codex ignore them entirely" / leonardo-panseri 2026-06-04 "Will be staying on Claude Code until this is fixed"), 그리고 **한국어 1차 증언**: 코유키1357(dcinside 특이점갤, 2026-04-28, 조회 7,507 — "코덱스의 경우 hook은 있는데 rules가 없어 **각 폴더 루트마다 AGENTS.md를 작성해야하고** 이로 인해 프롬프트 관리가 까다로워지는 문제가 있음"). ⚠️ **AWS 한국 기술블로그를 이 소절에 인용하지 마라**(V3) — 그 블로그에 귀속된 내용은 §5-4 실행 스타일 비교와 §5-8 #6 교차 리뷰뿐이며, **중첩 `AGENTS.md`에 관한 진술은 없다.** 출처가 말하지 않은 것을 그 출처에 귀속하는 것은 규율 12가 막으려는 사고와 같은 종류이고, 이 책에서 가장 신뢰도 높은 국내 소스에 발생하면 손실이 가장 크다. ⚠️ **메커니즘(`project_doc_max_bytes`·`project_doc_fallback_filenames`)은 4장에 넘긴다**
  3. **전환 마찰 원장** (m11 반영). 도입부에 국내 소스의 **존재만** 한 문장으로 알린다(V3 재배치): "국내에 실명·소속을 밝힌 심층 비교가 하나 있다 — Kyutae Park, AWS 한국 기술블로그, 2026-06-11. **실행 스타일 비교는 7장에서 본격적으로 다룬다.**" 이어서 §5-2의 7건 + [#28190](https://github.com/openai/codex/issues/28190)(macOS가 `rg` 차단, 👍79, 해결책 재현됨) **전수 표**. 열 = 마찰 / 이슈 번호 / 개설일 / 👍 / 상태 / **주 서술 장**. 담당 배정: **#11626·#12115·#28969 → 3장, #21753·#19679 → 6장, #13942 → 7장, #24515 → 2장, #28190 → 9장.** 이 표 하나가 원장이자 목차 역할을 한다
  4. 접두사·플래그 차이 — **스킬 호출 접두사 `$`(ChatGPT 표면은 `@`) vs `/`는 이 장이 주 서술**(m3 — 6장은 한 구절 콜백만), `--dangerously-bypass-approvals-and-sandbox`(별칭 `--yolo`) vs `--dangerously-skip-permissions`, **`--full-auto`는 deprecated**("Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used")
  5. **Steering vs Queuing** — 실행 중인 턴에 추가(<kbd>Enter</kbd>) vs 다음 턴 저장(<kbd>Tab</kbd>), 데스크톱 기본값은 Settings > General > Follow-up behavior. Claude Code에는 이 2모드 구분이 없다. [#28969](https://github.com/openai/codex/issues/28969)(질문이 60초 뒤 자동 응답됨, 👍**186**, open — 마찰 3위)를 여기에 붙인다: 사람이 답하기 전에 모델이 답해버리는 것은 steering 감각을 정면으로 배신한다
  6. Codex에만 있는 조작 — `/fork`(전사 복제) · `/side`·`/btw`(임시 곁가지) · `/goal`(지속 목표, 최대 **4,000자**) · `/personality`(friendly/pragmatic/none) · `/raw` · `/keymap` · `/statusline` · `/title` · `/theme` · `/vim`. ⚠️ **여기서는 "있다는 사실과 문법"까지만**(m4) — **언제 쓰는가는 7장 chat 단위 원칙**에서 다루고, **12장에서는 다시 꺼내지 않는다**(12장은 표면만). 명령 지도 개요(전역 플래그 20개 + 서브커맨드 28개 + 내장 슬래시 명령 약 60개가 한 페이지에) + 표면별 명령 페이지가 별칭으로 중복돼 있다는 주의
- **독자가 얻는 것:** 첫 주에 사고를 내지 않을 손버릇 교정표. "커밋은 하되 푸시는 하지 마"를 컨텍스트에 박는 실무 대응(suparious, #11626 — "That way I am always the gatekeeper")
- **필수 산출 아티팩트:** ① **손버릇 교정표**(행: `/clear`·되돌리기·중첩 지침·스킬 접두사·위험 플래그·훅 커버리지 / 열: Claude Code에서의 결과 · Codex에서의 결과 · 위험도 · 대응) ② **전환 마찰 원장 표**(8행 — 주 서술 장 열 포함)
- **Claude Code 대응 포인트:** §4-2 위험 대응표 6행이 이 장의 뼈대. **규율 12에 따라 Claude Code 쪽 서술은 §1-5 · §4-2 · §4-4를 벗어나지 않는다**
- **커버 문서:** `/codex/reference/commands`(≡`/codex/app/commands`), `/codex/reference/slash-commands`, `/codex/cli/reference`(≡`/codex/cli/slash-commands`), `/codex/developer-commands`, `/codex/ide/commands`(≡`/codex/ide/slash-commands`), `/codex/cli-customization`
- **오프닝:** 실패 장면(in medias res) — ⚠️ **인용된 실패로 연다**(#11626 댓글 또는 dcinside 증언). **지어낸 새벽 3시로 열지 않는다**(규율 11) / **클로징:** 대가 명시형 / **스캐폴드:** 사례 분석형 (M6 — 선택지 비교가 아니라 사고 사례이므로)
- **예상 분량:** 9,000자 (소절 6개)

---

### 4장. 지침과 설정 — `AGENTS.md`와 `config.toml`을 다시 세우기

- **핵심 질문:** 내 지침은 정말 다 읽히고 있는가? 설정은 어느 층에서 이기는가?
- **소절 구성 (7개 — m14 반영):**
  1. **`AGENTS.md`는 "에이전트를 위한 README"** — 원문 정의 3구절 인용("Think of `AGENTS.md` as an open-format README for agents" / "A short, accurate `AGENTS.md` is more useful than a long file full of vague rules" / "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`"). `/init`이 스캐폴드를 만든다(Claude Code `/init`과 같은 이름·같은 역할)
  2. ⭐ **바이트 예산이 명시돼 있다** — `project_doc_max_bytes = 32768`. 커뮤니티 이슈([#13386](https://github.com/openai/codex/issues/13386) "AGENTS.md가 조용히 잘린다")의 문서적 근거. 그리고 `project_doc_fallback_filenames`로 **파일명 자체를 바꿀 수 있다** — `CLAUDE.md` 고정과 대비
  3. 계층 로딩과 그 어긋남 — 전역 `~/.codex` → repo → 하위 디렉터리, "가까운 파일이 이긴다". ⚠️ **중첩 미로드는 3장이 주 서술이므로 여기서는 3문장 이내 콜백**(M9 분담): 문서상 규칙과 실제 로딩 동작이 어긋나는 지점임을 한 문장으로 못 박고 곧바로 대응 설정으로 넘어간다
  4. `config.toml` 지형 — 키 **274개** + `requirements.toml` **116개**, 공식 JSON 스키마 `learn.chatgpt.com/docs/config-schema.json`, 3계층 권고(개인 기본값 `~/.codex/config.toml` / 저장소별 `.codex/config.toml` / 일회성 오버라이드), `--profile` 적층(`$CODEX_HOME/profile-name.config.toml`), `-c key=value` 우선순위 원문
  5. **`/debug-config`로 레이어 순서와 정책 출처를 진단하기** — Claude Code에 대응물이 약한 지점. 2장 임포트 직후 절차와 연결. ⚠️ **11장에서 이 3계층이 4계층이 된다는 예고**(관리형 설정)
  6. **개인화 3층** (m14 분리) — memories / Chronicle(macOS·ChatGPT Pro 한정 opt-in 리서치 프리뷰 — **12장 재등장 예고**) / `/codex/personalize`. 무엇이 세션을 넘어 남고 무엇이 안 남는가
  7. **표면별 설정 지형도** (m14 분리) — 데스크톱·IDE·CLI·Windows/WSL 각각 어느 페이지가 무엇을 담당하는가를 표 1개로. ⚠️ **WSL 경로 성능 권고는 쓰지 않는다**(규율 7 — 두 페이지가 정반대이며 확정 불가)
- **독자가 얻는 것:** 지침이 잘리지 않게 관리하는 법, 설정 충돌을 진단하는 절차, 이중 관리를 피하는 현장 노하우(사용자 레벨 `AGENTS.md`가 `CLAUDE.md`를 가리키게 하고 스킬 디렉터리는 스크립트로 동기화 — steve-atx-7600, HN 2026-07-09)
- **필수 산출 아티팩트:** **표면별 설정 지형도 표**(행: 데스크톱 앱·IDE 확장·CLI·Windows/WSL / 열: 담당 문서 · 설정 위치 · 개인화 가능 항목 · 주의)
- **Claude Code 대응 포인트:** `AGENTS.md`↔`CLAUDE.md`(중첩 로딩 동작 다름 — 3장 참조) / `config.toml`↔`settings.json`(형식만 다름) / 파일명 커스터마이즈 가능 vs 고정 / 바이트 예산 명문화 vs 미명문
- **커버 문서:** `/codex/agent-configuration/agents-md`, `/codex/configuration`, `/codex/config-file/config-basic`·`config-advanced`·`config-reference`·`environment-variables`·`config-sample`, `/codex/customization/overview`, `/codex/customization/memories`, `/codex/customization/chronicle`, `/codex/personalize`, `/codex/reference/settings`(≡`/codex/app/settings`), `/codex/ide/settings`, `/codex/developer-settings`, `/codex/windows/windows-app`(≡`/codex/app/windows`), `/codex/windows/wsl`, `/codex/learn/best-practices`(보 — `AGENTS.md` 정의 원문 출처)
- **오프닝:** 충격적 수치·사실(32,768) / **클로징:** 적용 과제형 / **스캐폴드:** 문제-해결형
- **예상 분량:** 9,000자 (소절 7개) + `### 이 장의 핵심`

---

### 5장. 승인은 샌드박스가 아니다 — 세 개의 축과 Beta 딱지

- **핵심 질문:** "승인을 자동으로 넘기면 에이전트가 더 많은 걸 할 수 있게 된다"는 직관은 맞는가?
- **소절 구성 (7개 — V1 확정):**
  1. 원문이 못 박는 분리 — 샌드박스는 **무엇에 닿을 수 있나**, 승인은 **언제 멈추나**. "Changing who reviews a request doesn't expand the sandbox." **Approve for me는 Ask for approval과 같은 워크스페이스 경계를 유지한다**
  2. **통제 축은 셋이다** — ⓐ `sandbox` ⓑ `approvals` ⓒ `approvals_reviewer`(기본 `user` / `auto_review`) + `granular` 하위 토글 5개(`sandbox_approval`·`rules`·`mcp_elicitations`·`request_permissions`·`skill_approval`). **Claude Code 대응표는 3축 기준**
  3. 3층이 겹쳐 있다 — UI 라벨 / 구 설정 값(`approval_policy` × `sandbox_mode`) / `granular` 토글. 섞으면 즉시 틀린다. ⚠️ 권한 모드 개수도 페이지마다 다르다(3종 vs Custom 포함 4종) → **표면별 병기**
  4. **권한 프로필은 Beta다** — "Beta. Permission profiles are under active development and may change." 폴백 규칙 원문 인용: **구 설정이 어느 로드된 config에라도 있으면 구 체계가 이긴다.** 유일한 예외인 관리자 `allowed_permission_profiles`는 Codex **0.138.0** 이상 필요. 내장 프로필 3종과 `extends` 제약(`:danger-full-access` 상속 불가, 순환 거부)
  5. **Auto-review 서킷 브레이커의 정확한 조건** — 3연속 거부 또는 **최근 50건 리뷰 중 10건**. 50건 창을 빼먹으면 틀린 서술
  6. OS별 구현과 경계 — macOS Seatbelt / Linux seccomp+landlock(`0.115`부터 bubblewrap, WSL1은 `0.114`까지) / Windows 네이티브 또는 WSL. **`protected paths`** — `.git`·`.agents`·`.codex`는 writable root 안에서도 읽기 전용이다(에이전트가 자기 통제 장치를 못 고치게 하는 자기참조 방어). 클라우드 네트워크 기본 차단은 한 문장만 언급하고 **9장에 넘긴다**
  7. **왜 이게 중요한가 — 설정으로 안전을 살 수 없다.** 벤더 자체 보고(OpenAI, "Addendum to GPT-5.2 System Card: GPT-5.2-Codex", 2025-12-18, ❌ 벤더 자체 보고): destructive action avoidance가 gpt-5-codex 0.66 → gpt-5.1-codex 0.70 → gpt-5.1-codex-max 0.75 → **gpt-5.2-codex 0.76**. 최신 모델도 **약 4회 중 1회는 파괴적 행동을 피하지 못한다.** ⚠️ **이 애드덤에는 프롬프트 인젝션 정량 평가표가 없다** — "OpenAI가 인젝션 방어율 N%를 보고했다"고 쓰면 거짓이 된다. 그리고 IssueTrojanBench(Singh, Yang, Chen, arXiv:2607.20759, 2026-07-22): 악의적 이슈의 **66.5%가 모든 가드레일 통과**, "rejection is almost entirely from LLMs rather than the agent frameworks" → **CLI 설정으로 안전을 살 수 없다**. ⚠️ **조건 병기 필수(M12):** 66.5%는 **이 벤치마크가 설계한 공격 시나리오 집합 기준**이며 실사용 환경의 침해율이 아니다. 아직 동료 심사를 거치지 않은 📄 preprint이며, **Cursor·Claude Code·Codex Desktop을 이름으로 직접 평가한 유일한 최신 벤치마크**라는 점이 인용 가치의 근거다
     같은 소절 안에서 **현장 노하우로 착지한다** — 샌드박스를 끄지 말고 구멍을 뚫어라(miki123211, HN 2026-07-14: "You can poke specific holes in the sandbox ... You can have explicit deny rules" — `--add-dir` 우선, `danger-full-access` 강제 회피). 이 소절이 클로징 '스키마로 착지형'으로 이어진다
- **독자가 얻는 것:** 3축을 분리해 설정하는 능력. Claude Code 권한 감각을 그대로 옮겼을 때 생기는 오설정을 스스로 잡아낸다
- **필수 산출 아티팩트:** ① **3축 대응표**(행: `sandbox`·`approvals`·`approvals_reviewer`·`granular` 5토글 / 열: 무엇을 통제하는가 · 값 · Claude Code 대응 여부) ② 그림 1·2(mermaid)
- **Claude Code 대응 포인트:** `permissions.allow/deny/ask` 단일 축 ↔ Codex 3축 / Auto-review는 Claude Code에 **대응 없음** / `protected paths`(`.git`·`.agents`·`.codex`가 writable root 안에서도 읽기 전용 — 에이전트가 자기 통제 장치를 못 고치게 하는 자기참조 방어)도 대응물 없음
- **커버 문서:** `/codex/permission-modes`, `/codex/permissions`, `/codex/sandboxing`, `/codex/sandboxing/auto-review`, `/codex/agent-approvals-security`, `/codex/cyber-safety`, `/codex/windows/windows-sandbox`, `/codex/cloud/internet-access`(보 — 한 문장만, 심화는 9장), `/codex/security-administration`(보 — 조직 통제의 존재만 예고, 주 서술은 11장)
- **오프닝:** 정의 뒤집기 / **클로징:** 스키마로 착지형 / **스캐폴드:** 개념 도입형
- **예상 분량:** 10,000자 (소절 7개) + `### 이 장의 핵심`
- **그림 (의무):** 그림 1 = 샌드박스 / 승인 / 리뷰어 3축 분리 도식, 그림 2 = 권한 프로필 폴백 결정 흐름 (mermaid)

---

### 6장. 확장 모델 — 스킬·플러그인·훅, 그리고 테스트되는 규칙

- **핵심 질문:** 내가 쌓아둔 확장 자산은 Codex에서 얼마나 그대로 동작하는가?
- **소절 구성 (6개 — V1 확정):**
  1. 원문 정의 — 스킬은 "특정 작업·워크플로를 위한 지시와 자원의 묶음", 플러그인은 "스킬·커넥터를 담은 설치 가능한 번들"이며 커넥터는 **MCP 서버 기반**. ⚠️ **호출 접두사(`$`/`@`) 차이는 3장이 주 서술**(m3) — 여기서는 한 구절 콜백만
  2. 스킬 경로와 예산 — 개인 `$HOME/.agents/skills`, 팀 공유 `.agents/skills`(저장소 체크인), 스캐폴딩은 `$skill-creator`. **디렉터리명이 벤더 중립**이라는 점의 함의. 스킬 메타데이터 **2% 컨텍스트 예산 하드코딩**([#19679](https://github.com/openai/codex/issues/19679), 👍31, open)과 실측 대응(aldegad: 총 페이로드 15,822자→13,992자로 줄이자 경고 소멸) — **"컨텍스트 예산 3연작"의 첫 번째**(8장 #32806, 11장 MCP 90-91%와 연결)
  3. ⚠️ **Custom prompts는 deprecated** — 원문 첫 문장 "Custom prompts are deprecated. Use skills for reusable instructions that Codex can invoke explicitly or implicitly." 이 기능을 "Codex의 커스텀 슬래시 명령 만들기"로 소개하면 **폐기 예정 기능을 추천하는 셈**이 된다
  4. ⭐ **훅이 `CLAUDE_PLUGIN_ROOT`·`CLAUDE_PLUGIN_DATA`를 호환용으로 설정한다** — 이벤트명·JSON 스키마·exit code 2 관례까지 사실상 동형. **경쟁 제품의 환경 변수를 자기 문서에 박아 넣은 사례**라 인용 가치가 높다. 차이는 **해시 기반 훅 신뢰 검토**와 `--dangerously-bypass-hook-trust`. ⚠️ 커버리지는 **부분** — `PreToolUse`/`PostToolUse`가 Partial, "coverage must be consistent across every tool handler, not only selected paths"([#21753](https://github.com/openai/codex/issues/21753), 👍22, open). 규율 12에 따라 "29+ 이벤트"는 **Codex 측 이슈가 대조군으로 제시한 수치**로 귀속한다
  5. **execpolicy — Codex 고유 강점 3가지:** `justification`으로 규칙에 이유를 문서화 / `match`·`not_match`로 **규칙 자체를 테스트** / `codex execpolicy check --pretty --rules ...`로 **CI에서 규칙을 검증**. 셸 래퍼 처리 규칙(`&&`·`||`·`;`·`|`는 분리 평가, 리다이렉션·변수 치환이 있으면 전체를 하나로). **Claude Code에는 규칙 단위 테스트 하네스가 없다** — 이 책에서 "Codex가 확실히 앞선다"고 말할 수 있는 몇 안 되는 자리
  6. **서브에이전트 — 이슈 3건을 구분하라** (M11 반영). `.codex/agents/*.toml` 구조와 권장 모델 3종. ⚠️ **`subagents` 페이지 원문 표기는 "고난도 `gpt-5.6` / 속도 `gpt-5.6-terra` / 빠르고 좁은 작업 `gpt-5.6-luna`"인데, `gpt-5.6`은 §3-1 정전 모델 ID 목록에 없다** — **원문 표기임을 병기하고 `gpt-5.6-sol`로 임의 해석하지 않는다**(m9). **수치·선택 기준은 8장 단독**(m6)이며 여기서는 "모델을 지정할 수 있는가"라는 구조 문제만 다룬다. 세 이슈를 한 문단으로 구분: **[#14039]** 기능 요구(서브에이전트별 모델 지정, **open**) / **[#31814](https://github.com/openai/codex/issues/31814)** 버그(지정이 먹지 않음, 원인 PR까지 특정, 👍**167**, **closed**) / **[#15250](https://github.com/openai/codex/issues/15250)** 문서 불일치(`spawn_agent`가 일반 `agent_type`만 받아 이름 지정 불가 — "That is not the behavior the docs imply", **open**, CLI 0.144.1 재현). **2026-08-02 문서 기준으로 closed된 것은 특정 버그이고, 기능 요구 자체는 열려 있다**
     - Record & Replay 개요 (한 문단)
- **독자가 얻는 것:** 확장 자산 이식 판단표(그대로 감 / 문법만 바꿈 / 다시 씀). 그리고 Claude Code에서 못 하던 것 하나 — **권한 규칙을 CI에서 테스트하기**
- **필수 산출 아티팩트:** **확장 자산 이식 판단표**(행: 스킬·플러그인·훅·execpolicy 규칙·서브에이전트·커스텀 프롬프트 / 열: 이식 난이도 3등급(그대로 감·문법만 바꿈·다시 씀) · 해야 할 일 · 알려진 함정 이슈 번호)
- **Claude Code 대응 포인트:** 스킬↔스킬(경로·접두사 차이) / 훅↔훅(**부분 대응** + 신뢰 검토 추가) / execpolicy `.rules`↔`permissions.allow/deny/ask`(**Codex만 테스트 하네스 보유**) / 서브에이전트↔서브에이전트(모델 지정에서 Claude Code 우위 — §4-4 근거)
- **커버 문서:** `/codex/skills-and-plugins`, `/codex/build-skills`, `/codex/build-plugins`, `/codex/plugins`, `/codex/hooks`, `/codex/agent-configuration/rules`, `/codex/agent-configuration/subagents`, `/codex/extend/record-and-replay`, `/codex/custom-prompts`, `/codex/enterprise/skills`(보 — 조직 배포는 11장)
- **오프닝:** 상황 가정 / **클로징:** 방법 제시형 / **스캐폴드:** 비교 대조형
- **예상 분량:** 9,000자 (소절 6개) + `### 이 장의 핵심`

---

### 7장. 한 chat, 한 결과 — 프롬프팅과 작업 운영

- **핵심 질문:** Claude Code에서 통하던 프롬프트 습관 중 무엇을 버려야 하는가?
- **소절 구성 (7개 — V1 확정):**
  1. ⚠️ **4요소 프레임이 두 페이지에서 다르다** — `/codex/prompting`은 Goal / Context / Output / Boundaries, `/codex/learn/best-practices`는 Goal / Context / Constraints / Done when. **둘 다 원문이므로 어느 쪽을 쓰는지 밝히고 병기**
  2. 전환의 축을 한 문장으로 — r/codex(2026-05-12) 증언: GPT는 시킨 걸 잘하지만 안 시키면 안 하고, Claude는 알아서 하지만 안 시킨 것도 한다. **"GPT는 능동적이 되게, Claude는 파괴적이지 않게 프롬프트해야 한다"** (r/codex 출신 자료임을 명시)
  3. **흔한 실수 8개** 원문 목록 전량 — 지속 규칙을 프롬프트에 욱여넣기 / 빌드·테스트 실행법을 안 알려주기 / 다단계 작업에 계획 생략 / 워크플로를 이해하기 전에 전권 부여 / 워크트리 없이 같은 파일에 동시 작업 / 수동으로도 불안정한 걸 예약 실행 / 병렬로 쓰지 않고 한 단계씩 감시 / 프로젝트 전체를 한 chat으로
  4. **chat 단위 원칙** — "Keep one chat per coherent unit of work. Fork only when the work truly branches." **`/fork`·`/side`·`/btw`를 언제 쓰는가가 여기다**(m4 — 3장은 있다는 사실과 문법까지). 컨텍스트 공급 차이도 함께: IDE 확장은 열린 파일을 자동 포함하지만 **CLI는 경로를 명시하거나 `/mention`·`@` 자동완성으로 붙여야 한다**
  5. **실행 스타일 논쟁 — 어느 쪽도 단정하지 마라** (C2 신설 소절):
    - **관점 A:** **AWS 한국 기술블로그**(Kyutae Park, Ph.D, AWS AI 스페셜리스트 SA, 2026-06-11 — **실명·소속이 있는 국내 유일 심층 비교 자료**) — Claude는 "단일 패스 작성자"(정찰 없이 700~800줄 한 번에), Codex는 "장인적 접근"(`pwd`/`ls` 정찰 → `apply_patch` → 자가 검증)
    - **관점 B:** chandureddyvari(HN, 2026-02-03) — "Codex feels **lazy** - I have to explicitly tell it to research existing code before it stops giving hand-wavy answers"
    - **관점 C(조건부 반박):** imperfectlyAware(2026-04-24, macOS/Swift/레거시 ObjC) — "Codex ... replicates existing functionality and ignores existing patterns ... produces GitHub tutorial code"
    - **판정: 코드베이스 성격(레거시·자체 프레임워크 여부)이 변수로 보인다. 단정하지 않는다.**
    - **논쟁 C(§5-5) 연결:** 같은 스레드에서 하루 차이로 정반대 증언이 나온다 — NootropicDiary(Sol=경직) vs xoStardustt("Sol tends to go apeshit and refactor half my code ... even with an agents.md that explicitly forbids" cleanup/refactor, 2026-07-09~20). → **"버전 X 시점 기준" 없는 지시 준수 서술 금지**
  6. **작업 운영과 입출력 확장** — 작업 운영 축: Projects, 장시간 작업, Automations(예약 실행 — "수동으로도 불안정한 걸 예약하지 마라"는 문서 자신의 경고와 연결. [#13942](https://github.com/openai/codex/issues/13942) Plan mode 기본 시작 옵션 없음, 👍34, open), 알림
     - 입출력 확장 — 웹 검색(`--search`가 `web_search`를 `"cached"`→`"live"`로), 이미지 입력·생성, Visualizations(⚠️ **CLI·IDE 확장에서는 렌더링되지 않는다**), 파일 작업(문서 제목은 **"Work with files"** — 규율 8)
  7. 실측이 체감과 갈린다 — METR(Becker, Rush, Barnes, Rein, arXiv:2507.09089, 2025 📄): 개발자는 24% 단축을 예상했고 20% 단축됐다고 느꼈으나 **실제로는 19% 느려졌다**. ⚠️ **조건 병기 필수** — 숙련 개발자 **16명** / **246개** 과제 / **평균 5년간 다뤄온 자기 저장소** / 2025년 2~6월 도구 기준. 즉 **AI에게 가장 불리한 조건**이며 **낯선 코드베이스로 일반화할 수 없다**
- **독자가 얻는 것:** chat을 결과 단위로 쪼개는 습관, 예약 실행 전에 통과해야 할 기준, 실행 스타일 논쟁에서 단정하지 않는 태도, 그리고 "빨라진 느낌"을 의심하는 눈
- **필수 산출 아티팩트:** **흔한 실수 8개 대응표**(행: 실수 8개 / 열: 왜 문제인가 · Codex에서의 대응 · 관련 장)
- **Claude Code 대응 포인트:** Plan Mode 기본 시작이 없다(§4-4) / IDE 자동 컨텍스트 vs CLI 명시 지정 / steering·queuing 2모드(3장 연결) / **실행 스타일 논쟁은 양쪽 다 "인용된 관측"이며 규율 12의 화이트리스트 밖 주장을 추가하지 않는다**
- **커버 문서:** `/codex/prompting`, `/codex/learn/best-practices`, `/codex/projects`, `/codex/long-running-work`, `/codex/automations`, `/codex/notifications`, `/codex/web-search`, `/codex/image-inputs`, `/codex/image-generation`, `/codex/visualizations`, `/codex/artifacts-viewer`("Work with files")
- **오프닝:** 수사적 질문 / **클로징:** 한 문장 여운형 / **스캐폴드:** 문제-해결형
- **예상 분량:** 9,000자 (소절 7개)

---

### 8장. 모델 선택이 곧 비용 설계다

- **핵심 질문:** 어떤 모델을, 어떤 추론 강도로, 어떤 표면에서 써야 하는가? 그리고 그 선택은 얼마인가?
- **소절 구성 (7개 — V1 확정):**
  1. **권장 모델 3종 + 프리뷰 1종**(2026-08-02 기준) — `gpt-5.6-sol`(디테일과 완성도) / `gpt-5.6-terra`(일상의 일꾼, "이전에 GPT-5.5에 맡기던 일의 자연스러운 출발점") / `gpt-5.6-luna`(명확하고 반복적인 일) / `gpt-5.3-codex-spark`(텍스트 전용 리서치 프리뷰, ChatGPT Pro 한정). 원문 권고: **"확신이 없으면 Sol로 시작하라"**
  2. **표면별 가용성 표 — cloud 열이 결정적** — Codex cloud에서 쓸 수 있는 모델은 **Sol 뿐**이며 "you can't change the default model for Codex cloud chats"
  3. 추론 강도 — Light(앱·웹·IDE)/Low(CLI) · Medium · High · Extra High. 원칙은 "필요한 결과를 내는 **가장 낮은** 강도". 그리고 결정적 경고: **"GPT-5.5의 추론 강도와 GPT-5.6 사이에 정확한 대응이 없다"** → 익숙한 작업을 낮은 설정에서 먼저 시도하고 조정하라. ⚠️ 값 목록도 페이지마다 다르다(`config-reference`를 정전으로, `subagents`의 `ultra`·`max`는 별도 표기)
  4. 🕒 **모델 은퇴 (예정)** — **규율 5의 문안을 그대로 적용한다.** `gpt-5.4`·`gpt-5.4-mini`는 **2026-08-31 은퇴 예정**이며(ChatGPT 로그인 사용자 한정 — API 키 인증은 영향 없음) 대체는 각각 Terra·Luna. **2026-08-02 문서 기준으로는 아직 은퇴 전이다.** 독자에게는 "은퇴 여부가 아니라 대체 경로를 기준으로 읽으라"고 안내한다. ⚠️ **시제는 미래형으로 고정**("은퇴했다" 금지) — 레퍼런스 §3-1·§7-4 #1의 "이미 지난 날짜다"는 계획 라운드 1에서 **오류로 확정·정정**됐다. 조직 단위 모델 가용성 통제(`workspace-model-availability`)를 여기서 예고하고 **11장에서 회수**
  5. **요금·한도·크레딧 요율 — 한 장의 가격표.** 요금 구조: Free `$0` / Go `$8` / Plus `$20` / Pro `$100`(5x)·`$200`(20x) / Business `$20`(2+ users, **연간 결제 기준**; 월 결제 시 `$25`/user/month)
     - 한도 표 읽는 법 — 플랜 탭 5개 × 모델별 × (Local Messages / Cloud chats / Code Reviews) / 5h. Plus 실측값을 **범위 그대로** 인용. 각주가 핵심: **로컬 메시지와 클라우드 chat이 같은 5시간 창을 공유하며, 주간 한도가 추가로 적용될 수 있다**
     - **크레딧 요율이 곧 설계다** — 입력 Sol/Terra/Luna = 125/50/5, 출력 = 750/300/30. **Sol과 Luna의 입력 요율 차가 25배.** 메시지당 평균 "5-40 credits"
  6. ⚠️ **판정 유보 구간** — 개인 요금제 한도의 1차 소스는 `/codex/pricing` 하나뿐이고 **변경 이력이 없다.** `/codex/enterprise/usage-limits`에는 수치가 전무하며(37줄) "These controls aren't a universal Codex limit system and don't govern OpenAI API Platform billing"이라고 스스로 선을 긋는다. 따라서 커뮤니티의 2026-06 급등 관측([#28879](https://github.com/openai/codex/issues/28879), 2026-06-18, 👍**362**, open — 세션 로그의 `token_count`·`rate_limits` 이벤트 직접 비교, 대안 가설(리즈닝 강도·컨텍스트 팽창·설정 변경·주간 캡) 명시적 배제)과 7월 한도 임시 해제 논의([#34035](https://github.com/openai/codex/issues/34035), 2026-07-18, 👍131, open)는 **"커뮤니티 관측, 1차 확인 불가"로만 서술**한다. 문서의 "5x or 20x higher rate limits"와 실사용이 "materially inconsistent"하다는 보고(§5-11 #3)도 같은 등급. 속도 축(`/codex/agent-configuration/speed`)과 **서브에이전트 권장 모델의 수치·선택 기준도 이 장 단독**(m6)
  7. **벤치마크로 모델을 고르지 마라** (C4 신설 소절 — 라운드 1 미배치 학술 2편의 집):
    - **리더보드 오염:** Aleithan et al., SWE-Bench+, arXiv:2410.06992(2024, 📄 preprint) — 성공 패치의 **32.67%**가 이슈 본문에 답이 적혀 있었고, 해당 인스턴스를 제거하면 해결률이 **12.47% → 3.97%**로 붕괴한다. 저자들은 이 결함이 **SWE-bench Verified에도 남아 있다**고 명시한다
    - **사내 코드베이스는 더 어렵다:** Deng et al., SWE-Bench Pro, arXiv:2509.16941(2025, 📄) — 공개 세트 GPT-5 **23.3%** vs 상업 저장소 세트 **14.9%**. 프런티어 모델도 Pass@1 25% 미만
    - **광고 컨텍스트와 실측** (M4): GPT-5.6 Sol 컨텍스트 **1.05M 광고 vs 실측 353K → 258K** 보고([#32806](https://github.com/openai/codex/issues/32806), **closed**). 회복 여부는 확인 불가이므로 **"2026-08-02 시점에는 재현 보고가 닫혀 있다"까지만** 쓴다. 6장 스킬 2% 예산·11장 MCP 컨텍스트 90-91%와 함께 **"컨텍스트 예산 3연작"**을 완성한다
    - CLI 에이전트를 평가하는 벤치마크는 존재한다 — Merrill et al., Terminal-Bench, ICLR 2026(✅ peer-reviewed), arXiv:2601.11868. ⚠️ **구체 순위는 인용 금지**(규율 6 — 리더보드가 상시 갱신된다). **"그런 벤치마크가 있다"는 사실만**(m13)
    - **결론:** 모델 선택의 근거는 리더보드가 아니라 **표면별 가용성 · 추론 강도 · 크레딧 요율**이다(= 이 장의 나머지 내용)
- **독자가 얻는 것:** 작업 종류별 모델·추론 강도 선택 가이드, 그리고 요금·벤치마크 서술을 읽을 때 무엇이 확정 사실이고 무엇이 관측인지 구분하는 눈
- **필수 산출 아티팩트:** ① **모델·추론 강도 선택 가이드 표**(행: 작업 유형 / 열: 권장 모델 · 추론 강도 · 표면 제약 · 크레딧 부담) ② **표면별 가용성 표**(cloud 열 강조) ③ **Plus 한도 표**(범위값 보존, 캡션에 `(2026-08-02 문서 기준)`)
- **Claude Code 대응 포인트:** Opus/Sonnet/Haiku 3층 감각을 Sol/Terra/Luna에 그대로 매핑하려는 유혹과 그 위험(**정확한 대응 없음**) / cloud 전용 모델 제약은 대응 없음 / 5시간 창 공유 구조. **규율 12 — Claude Code 쪽 요금·모델 라인업은 쓰지 않는다**
- **커버 문서:** `/codex/models`, `/codex/pricing`, `/codex/enterprise/usage-limits`, `/codex/enterprise/workspace-model-availability`, `/codex/agent-configuration/speed`, `/codex/config-file/config-reference`(보 — reasoning effort 값 목록 정전)
- **오프닝:** 충격적 수치·사실(입력 요율 25배) / **클로징:** 미해결 고지형 / **스캐폴드:** 비교 대조형
- **예상 분량:** 10,000자 (소절 7개) + `### 이 장의 핵심`

---

### 9장. 내 노트북 밖으로 — 위임의 세 가지 모양

- **핵심 질문:** 어떤 일을 로컬에 두고, 어떤 일을 클라우드에 보내고, 어떤 일을 사람 없이 돌릴 것인가?
- **소절 구성 (6개 — V1 확정):**
  1. 실행 환경 3종 정리 — 로컬 / 클라우드 / 비대화형. 데스크톱 컴포저의 **Work locally** 토글, 클라우드를 고르는 두 이유(앱을 닫아도 계속 실행 / 웹·모바일에서 이어가기)
  2. 작업 공간 구조 — 다중 폴더(primary가 새 chat·Git 작업·`AGENTS.md`/skills/`config.toml` 자동 탐색을 담당하고 secondary는 파일 검색·읽기·편집만), **Git worktrees가 일급 문서로 있다**(7장 "흔한 실수 8개"의 "워크트리 없이 같은 파일에 동시 작업"과 연결). 로컬 환경 함정으로 [#28190](https://github.com/openai/codex/issues/28190)(macOS가 `rg` 차단, 👍79, **해결책 재현됨**)을 배치(m11)
  3. Codex cloud 실무 — 네트워크 **기본 차단**("Tasks delegated to the cloud run in isolated environments. Internet access is off during the agent phase unless you enable it for the environment"), CLI 접근 경로 `codex cloud`(experimental)·`codex cloud exec --env {ENV_ID} --attempts 1-4`·`codex cloud list --limit 1-20`·`codex apply {TASK_ID}`
  4. **클라우드 고유 리스크** — 실행 환경이 공급자 소유다. ModernMech(HN, 2026-07-26): "same prompting, same model, totally different results because they changed the cloud tool's resource limits". **내 쪽 변경 없이도 어제와 다른 도구가 된다.** 커뮤니티가 확보한 위임 성공 사례는 **전부 커밋~MR 한 개 크기**였다(tunesmith, HN 2026-06-13) — 태스크를 "커밋 하나 크기"로 쪼개라. ⚠️ 레퍼런스 §7-2 #4: **몇 시간짜리 클라우드 위임 후기는 여전히 공백**이라는 사실 자체를 밝힌다
  5. **붙는 자리 표** (M7 신설 — 문서 6개가 한 문장에 뭉개지지 않게 표가 구별을 담당한다). 행 = `codex exec`(↔`claude -p`) / GitHub Action / `@codex` PR / Slack / Linear / SSH·iOS Remote(원격 연결) / 통합 터미널 / Amazon Bedrock. 열 = **트리거 / 인증 / 실행 위치(로컬·클라우드) / 알려진 제약**. 산문은 선택 흐름만 설명한다
  6. **`experimental` 명령을 쓸 때의 규율** (m5 — **목록 전수는 이 장 단독**). `codex app-server` · `codex remote-control` · `codex debug app-server send-message-v2` · `codex debug models` · `codex debug prompt-input` · `codex cloud` · `codex execpolicy` **7개**(2026-08-02 문서 기준, 나머지 21개는 `stable`). 소개할 때 **"실험적 — 예고 없이 바뀔 수 있음"**을 반드시 병기한다(문서 자신이 `codex app-server`에 대해 "may change without notice"라고 못 박는다)
- **독자가 얻는 것:** 위임 결정표(로컬/클라우드/비대화형)와, 클라우드 위임에서 재현성이 깨지는 원인을 미리 아는 것
- **필수 산출 아티팩트:** ① **붙는 자리 표**(8행 × 4열) ② **위임 결정 흐름 mermaid**(그림 1) ③ `experimental` 명령 7개 목록
- **Claude Code 대응 포인트:** **Codex cloud는 대응 없음**(§1-5 — 가장 큰 구조적 차이 중 하나) / `codex exec`↔`claude -p` / 워크트리 운용은 양쪽 공통 권고
- **커버 문서:** `/codex/environments/modes`, `/codex/environments/local-environment`, `/codex/environments/cloud-environment`, `/codex/environments/git-worktrees`, `/codex/cloud`(심화), `/codex/cloud/internet-access`, `/codex/non-interactive-mode`, `/codex/github-action`, `/codex/third-party/github`, `/codex/third-party/slack`, `/codex/third-party/linear`, `/codex/remote-connections`, `/codex/integrated-terminal`, `/codex/amazon-bedrock`, `/codex/long-running-work`(보 — 주 서술은 7장), `/codex/feature-maturity`(보 — `experimental` 목록 근거)
- **오프닝:** 상황 가정 / **클로징:** 사례의 결말 / **스캐폴드:** 사례 분석형
- **그림:** 그림 1 = 위임 결정 흐름 (mermaid)
- **예상 분량:** 9,000자 (소절 6개)

---

### 10장. 두 개의 "검토" — 코드 리뷰와 Codex Security

- **핵심 질문:** Codex가 리뷰를 잘한다는 통념은 어디까지 사실이고, Codex Security는 그것과 무엇이 다른가?
- **소절 구성 (7개 — C3 배분표 확정. 라운드 1의 "12개 주제 한 불릿 나열"을 소절로 못 박는다):**

  | 소절 | 내용 | 커버 |
  |---|---|---|
  | 1 | **리뷰 경로 3종** — CLI `codex review`(비대화형; `--uncommitted`/`--base`/`--commit` 중 **택1 — 서로 충돌한다**), TUI `/review`, GitHub PR `@codex review`(저장소에 Code review 활성화 선행) | `code-review` |
  | 2 | **통념과 자기 반증** — 다수 관점(superfrank HN 2026-05-15 "Codex is far better at code review and catching bugs that actually matter" / bottlepalm HN 2026-07-08 "Codex for code reviews because it is pedantic")과 자기 반증(Ok_Economist3865, **r/codex** 2026-03-17: GPT-5.2로 Opus 코드를 리뷰하면 지적률 90%였는데 **Anthropic 공식 프롬프트 가이드대로 자기 프롬프트를 고치자 25~40%로 떨어졌다**). → "많이 잡는다"의 상당 부분이 **프롬프트 품질 문제**였다(다만 역방향 비대칭은 남는다). + 문서 자신의 경고("models must be trained specifically to identify P0 and P1-level bugs, and tuned to provide concise, high-signal feedback; **overly verbose responses are ignored just as easily as noisy lint warnings**"). OpenAI 자체 주장 **"At OpenAI, Codex reviews 100% of PRs."**는 **출처 표기 없는 자체 주장**임을 밝히고 인용 | `code-review`, `learn/best-practices`(보) |
  | 3 | **경계 긋기 — Codex Security는 별개 제품이다.** 원문이 직접 선을 긋는다(에이전트 실행 안전 ≠ 연결된 GitHub 저장소 스캔 제품). 다만 두 접점: ⓐ CI 실행 시 `codex exec --sandbox workspace-write` ⓑ **Trusted Access for Cyber 인증이 스캔 품질의 전제**("For best results, use an account verified for Trusted Access for Cyber" — 4개 페이지 반복) | `security`, `security/threat-model`, `security/setup`, `agent-approvals-security`(보) |
  | 4 | **스캔 수명주기 — 표 1개 + 산문 해설 (의무).** 워크벤치 → 스캔 → 딥스캔 → 코드 변경 → 트리아지 백로그 → 수정 → 내보내기·취약점 리포트. **표가 8개 페이지를 흡수하고 산문은 흐름만 설명한다** | `security/plugin/*` 8페이지 |
  | 5 | **비결정성과 등급 체계** — 제품이 자기 비결정성을 스스로 명문화한다: "AI-assisted scans can vary, even with the same scan configuration". 스캔 비교 상태 **5종**(`new`·`persisting`·`reopened`·`resolved`·`unknown`), 커버리지 **3등급**(`complete`/`partial`/`unknown`), 보안 하드닝 | `scans`, `deep-scans`, `security-hardening`, `security/faq` |
  | 6 | **자동화 경로 — 표 1개 + 산문 해설 (의무).** CLI · 벌크 스캔 · CI 통합 · SDK. 플러그인 `0.1.15`와 CLI `0.1.3`은 **별개 버전 계열**(모순이 아니다) | `security/cli/*`, `security/sdk`, `plugin/changelog` |
  | 7 | **부품화와 한계** — ⭐ `codex-security mcp`·`codex-security skills`: CLI가 스스로 MCP 서버로 등록되고 스킬을 에이전트에 동기화한다 → **Claude Code를 포함한 다른 에이전트의 부품으로 편입될 수 있다**("경쟁 제품"이 아니라 "조합 가능한 부품"). ⚠️ 벤더 확인(HN 49089755, 2026-07-29): **"this isn't an offline scanner ... code and context ... sent to the hosted model"** — **출시 4일 차 관측**이므로 초기 상태임을 병기. ⚠️ **모델 계열 혼동 금지**: 에이전트 라우팅·사이버 안전 정책은 `GPT-5.3-Codex` 계열(리라우팅 대상 `GPT-5.2`), **Codex Security 스캔 기본이자 유일 권장은 `gpt-5.6-sol`**, CLI 예시에 등장하는 `gpt-5.6-terra`를 권장 모델로 서술하면 **오류** | `security/cli/reference`, `security/faq` |

  > **표 작성 규율 (열린 위험 1 → 라운드 2 판정 반영):** 소절 4·6의 표는 각 행에 "무엇을 하는가"뿐 아니라 **"언제 쓰는가"**를 반드시 담는다. 그리고 **행의 단위는 문서가 아니라 실무 단계다** — 소절 4 표는 **행 수 상한 8행**이며 단계는 워크벤치·스캔·딥스캔·코드 변경·트리아지·수정·내보내기 **7단계**가 기본이다. **페이지 1개 = 행 1개가 되지 않게 하는 것이 이 규율의 핵심**이며, 그래야 "목차를 표로 옮긴 것"이라는 C3 문제가 형태만 바꿔 재발하지 않는다.
- **독자가 얻는 것:** 리뷰 자동화를 도입할 때의 현실적 기대치 조정, 그리고 Codex Security를 자기 에이전트 스택의 부품으로 붙이는 방법
- **필수 산출 아티팩트:** ① **스캔 수명주기 표**(소절 4 — 행: 단계 / 열: 무엇을 하는가 · 언제 쓰는가 · 산출물 · 주의) ② **자동화 경로 표**(소절 6 — 행: CLI·벌크·CI·SDK / 열: 명령 · 인증 · 출력 형식 · 제약)
- **Claude Code 대응 포인트:** `@codex review`↔PR 리뷰 관행 / **Codex Security는 대응 제품 없음** — 다만 MCP로 노출되므로 **Claude Code에서 그대로 쓸 수 있다**(경쟁이 아니라 조합)
- **커버 문서:** `/codex/code-review`, `/codex/security`, `/codex/security/plugin`(+`workbench`·`scans`·`deep-scans`·`code-changes`·`triage-backlog`·`fix-findings`·`export-findings`·`vulnerability-reports`·`security-hardening`·`changelog`), `/codex/security/setup`, `/codex/security/threat-model`, `/codex/security/faq`, `/codex/security/cli`(+`bulk-scans`·`reference`·`ci`·`faq`), `/codex/security/sdk`, `/codex/third-party/github`(보), `/codex/learn/best-practices`(보), `/codex/agent-approvals-security`(보 — 경계 긋기)
- **오프닝:** 인용·일화 / **클로징:** 원문 인용으로 닫기 / **스캐폴드:** 문제-해결형 (M6 — 통념 제시 → 반증 → 재조정 구조)
- **예상 분량:** 10,000자 (소절 7개)

---

### 11장. 내 손 밖으로 — SDK·app-server·MCP, 그리고 조직이 개인을 이기는 지점

> **리프레임 (C7·판정 3):** 라운드 1의 "조직에 들이기"는 독자를 **관리자 대리인** 자리에 세웠다 — 이 책의 독자가 아니다. 서술 시점을 **끝까지 개인 개발자**에 고정한다. 13장 분리는 하지 않는다(기각 대안 4 참조).

- **핵심 질문:** Codex를 "내가 쓰는 도구"가 아니라 "내 시스템의 한 부품"으로 만들 수 있는가? 그리고 조직 워크스페이스에 들어간 순간 **내 설정은 어떻게 되는가**?
- **공통 논지:** **내 손 밖에서 내 환경이 결정된다.** 앞부분은 내가 Codex를 남의 프로그램에 끼우는 이야기, 뒷부분은 남의 정책이 내 설정을 덮는 이야기다. 방향만 반대일 뿐 같은 축이며, 이것이 9~11장을 묶는 논지다.
- **소절 구성 (7개):**
  1. **SDK는 app-server의 얇은 래퍼다** — "The Python SDK controls the local Codex app-server over JSON-RPC". Python SDK는 **2026-08-02 문서 기준 beta**. **그림 1(mermaid — SDK · app-server · MCP 3경로)**
  2. 문서가 직접 제시하는 선택 기준 — **SDK는 코딩 스레드용, MCP 서버 + Agents SDK는 Codex를 더 큰 워크플로의 한 전문가로 쓸 때.** ⭐ `codex mcp-server`는 Codex 자신을 MCP 서버로 노출한다("Useful when another agent consumes Codex") → **Claude Code가 Codex를 도구로 부르는 구성이 문서상 가능하다.** 10장 소절 7(`codex-security mcp`)과 함께 "부품화" 논지를 완성
  3. **MCP 클라이언트로서의 Codex — 진짜 함정은 문법이 아니라 컨텍스트다.** MCP 8개를 그대로 옮기면 세션이 **컨텍스트 90-91%에서 시작**하고 `[features] search_tool = true`로 99%까지 회복(buildxjordan, 2026-02-11) / 선언 안 된 MCP가 `rg`로 폴백해 **메모리 100GB**(ChoasMaster777, 2026-03-19) / 상주 MCP 서버 하나가 Sol을 **3시간** 멈춤(tokovar, 2026-07-13) / WSL에서 Windows `config.toml`이 쓰여 "MCP etc. not being configured correctly"([#13762](https://github.com/openai/codex/issues/13762), 👍55, open). **"컨텍스트 예산 3연작"의 마지막**(6장 스킬 2%, 8장 #32806과 연결). ⚠️ **MCP 설정 이식 자체는 2장 임포트에서 다뤘다**(m1 — 라운드 1의 "3장" 표기는 오기였다)
  4. **내 설정이 왜 안 먹히는가 — 조직이 개인을 이기는 네 지점** (C7 신설, 이 장의 축):
     1. **관리형 설정이 내 `config.toml`을 이긴다** — `requirements.toml` **116키**·MDM 배포. 우선순위 표현이 두 페이지에서 다르므로 **정전은 `managed-configuration`**(§3-11 #3 — `hipaa-configuration` 쪽 표현은 인용하지 않는다). **4장에서 세운 3계층이 여기서 4계층이 된다**
     2. **`allowed_permission_profiles`가 내 권한 프로필을 제한한다** — Codex **0.138.0** 이상 필요(0.137.0 이하는 무시). **5장에서 배운 폴백 규칙의 유일한 예외가 조직 설정**이라는 사실
     3. **`workspace-model-availability`가 내 모델 목록을 줄인다** — **8장에서 세운 모델·비용 설계가 조직 정책에 종속된다**
     4. **access token 만료가 내 CI를 끊는다** — 최단 **1일**, 권장 **7/30/60/90일**, 지원 플랜은 **Business·Enterprise**(정전은 전용 페이지 `access-tokens`, §3-11 #4 — `auth` 쪽의 "Enterprise만" 표기는 인용하지 않는다)
  5. **관리자에게 물어볼 것 — 표 1개로 압축 (의무).** 나머지 관리 문서(관리 콘솔·admin 셋업 / Work admin FAQ / 그룹·프로비저닝 / 역할·워크스페이스 권한 / 거버넌스 / 워크스페이스 분석 / Analytics API / Compliance API / HIPAA 구성 / Windows 배포 / 앱과 커넥터 / 조직 스킬 배포 / 보안 관리)를 **행 = 문서, 열 = 무엇을 정하는가 / 개인 개발자에게 미치는 영향 / 문서가 위임하는 것**으로 압축한다. **"위임" 열은 세 값으로 세분한다**(라운드 2 판정 2): `Help Center` / `인증된 레퍼런스(Analytics·Compliance API)` / `문서에 없음`. 같은 정직함을 유지하면서 독자가 "어디를 찾아가야 하는가"를 얻는다. ⚠️ 확정 가능한 내장 역할은 **Owner / Admin / Member 3개뿐**이며 나머지는 Help Center 위임(§7-1 #3) — **추측으로 채우지 않는다.** Analytics·Compliance API의 엔드포인트·스키마도 "This page doesn't duplicate that contract"로 위임되므로 **없다는 사실만 쓴다.** 열린 위험 2 대응: "위임" 항목이 여러 행에 반복되는 것은 **문서의 실제 상태를 정직하게 반영한 것**이므로, 표 앞에 그 사실을 알리는 한 문장을 둔다
  6. **AI 네이티브 팀 만들기 — 인용 규율과 함께.** `/codex/guides/build-ai-native-engineering-team`을 다루되 ⚠️ 문서가 인용한 **"2시간 17분 / 약 50% 신뢰도"는 METR 연구이지 OpenAI 측정이 아니며 2025년 8월 기준으로 1년 묵었다**(🕒). **"주당 2~5시간 코드리뷰"는 원문에 출처가 없다.** 둘 다 조건을 붙여서만 인용한다
  7. 학습 자원 — `/codex/developers`, use cases·컬렉션·리소스·비디오. ⚠️ 동적 SPA 목록 페이지라 항목명·URL·날짜는 신뢰 가능하나 **개수를 단정하지 않는다**
- **독자가 얻는 것:** Codex를 프로그램에서 호출하는 세 경로의 선택 기준, MCP 이식 시 컨텍스트 예산 사고를 피하는 법, 그리고 **조직 워크스페이스에서 내 설정 중 무엇이 무력화되는지**를 미리 아는 것
- **필수 산출 아티팩트:** ① **3경로 mermaid**(그림 1) ② **"조직이 개인을 이기는 네 지점" 표**(행: 4지점 / 열: 조직이 설정하는 것 · 내 어느 설정을 덮는가 · 관련 장 · 최소 버전 요구) ③ **관리자에게 물어볼 것 표**(13행 × 3열)
- **Claude Code 대응 포인트:** Agent SDK↔Codex SDK / MCP 설정 이식(**2장** 임포트와 연결 — m1) / **Codex를 Claude Code의 서브 도구로 붙이는 구성**이 이 책에서 가장 실용적인 "함께 쓰기" 레시피 — 12장에서 회수
- **커버 문서:** `/codex/codex-sdk`, `/codex/app-server`, `/codex/mcp-server`, `/codex/extend/mcp`, `/codex/developers`, `/codex/use-cases`, `/codex/use-cases/collections`, `/codex/resources`, `/codex/videos`, `/codex/administration`, `/codex/enterprise/admin-setup`, `/codex/enterprise/work-admin-faq`, `/codex/enterprise/groups-and-provisioning`, `/codex/enterprise/roles-and-workspace-permissions`, `/codex/enterprise/managed-configuration`, `/codex/hipaa-configuration`, `/codex/enterprise/access-tokens`, `/codex/enterprise/apps-and-connectors`, `/codex/enterprise/skills`, `/codex/enterprise/governance`, `/codex/enterprise/workspace-analytics`, `/codex/enterprise/analytics-api`, `/codex/enterprise/compliance-api`, `/codex/enterprise/windows-deployment`, `/codex/security-administration`, **`/codex/guides/build-ai-native-engineering-team`**(M5 — 주담당인데 라운드 1 목록에서 누락됐던 항목), `/codex/enterprise/workspace-model-availability`(보 — 주 서술은 8장)
- **오프닝:** 수사적 질문 / **클로징:** 선택지 제시형 / **스캐폴드:** 비교 대조형
- **그림:** 그림 1 = SDK · app-server · MCP 3경로 (mermaid)
- **예상 분량:** 10,000자 (소절 7개)

---

### 12장. 갈라진 진화 — Codex에만 있는 것, 그리고 두 하네스와 함께 사는 법

- **핵심 질문:** 둘 중 하나를 골라야 하는가? 아니면 성질이 다른 두 하네스를 함께 쓰는 것이 정답인가?
- **분량 규칙 (판정 2 — 증량하지 않는다):** planner의 나열 우려는 정당하지만 증량은 답이 아니다. **"표 1 + 심층 1"**로 푼다 — 고유 표면은 표 하나로 압축하고, 산문 심층은 하나만 쓴다. 8,000자·소절 6개 유지.
- **소절 구성 (6개):**
  1. **앞 장 콜백으로 열기** — **1장 소절 4의 연표를 다시 꺼낸다.** 2026년 상반기 Codex는 터미널 도구 → 데스크톱 앱 → GUI·브라우저·컴퓨터 조작·음성·전용 하드웨어로 뻗었고, 같은 기간 Claude Code는 CLI/SDK 중심을 유지했다. 이렇게 열면 고유 표면 소개가 **나열이 아니라 앞 장에서 심어둔 사실의 회수**가 된다
  2. **고유 표면 9종 — 표 1개로 압축 (의무).** (V5 — 라운드 1의 "8종" 표기는 행 수 9와 어긋났다. **9종·9행으로 통일**하며, 심층 대상인 내장 브라우저·Computer Use도 **표에는 행으로 남기고** 산문 심층만 소절 3에서 다룬다.) 행 = 내장 브라우저 · Computer Use · Chrome 확장 · Appshots(양쪽 Command 키) · 음성(Ctrl+M 받아쓰기 / ChatGPT Voice) · Sites · **Codex Micro**(2026-07-15 출시, OpenAI × Work Louder 한정 생산) · Chronicle(macOS·ChatGPT Pro 한정 opt-in 리서치 프리뷰 — 4장에서 예고한 재등장) · `/pets`. 열 = **출시 시점 / 성숙도 라벨 / 요구 조건 / Claude Code 대응 유무**. **각 행 산문은 최대 1~2문장.** ⚠️ `/fork`·`/side` 등 슬래시 명령은 **여기서 다시 꺼내지 않는다**(m4 — 12장은 표면만)
  3. **심층은 하나만 — 내장 브라우저 + Computer Use.** **"터미널 도구가 GUI를 조작하기 시작했다"가 이 장 논지의 유일한 결정적 증거**이므로 이것만 산문으로 깊게 쓴다. 나머지는 표에 맡긴다
  4. **Claude Code에만 있는 것도 정직하게** — `/rewind`(코드까지 되돌리기) · 중첩 지침 파일 자동 로드 · Plan Mode 기본값 시작 · 상태 표시줄 · 서브에이전트별 모델 지정 · 훅 완전 커버리지(§4-4). **규율 12 — 이 6항목을 벗어난 Claude Code 주장을 추가하지 않는다**
  5. **여정 회수 + 함께 쓰기 레시피** — 1장의 3분법에서 11장의 부품화까지 이 책이 지나온 축을 연결하고, 실제 레시피를 준다: MCP를 통한 상호 편입(`codex mcp-server`·`codex-security mcp` — 11장·10장 회수) / 지침 이중 관리 회피(사용자 레벨 `AGENTS.md`가 `CLAUDE.md`를 가리키게, 스킬 디렉터리는 스크립트 동기화) / 교차 리뷰(다른 모델 계열은 서로 다른 맹점을 가진다 — AWS 블로그. **단 반론도 병기**: BloondAndDoom은 같은 모델에 "check again"을 반복해도 된다고 본다) / 작업 성격별 분배
  6. **남는 것, 그리고 이 책의 유효기간** — 조용한 부채(Liu et al., arXiv:2603.28592, 2026 📄: AI 작성 커밋 **302.6천 건**·저장소 6,299개 분석, 총 484,366건 이슈 중 **89.3%가 코드 스멜**, 추적 이슈의 **22.7%가 최신 버전에도 생존**) / 결국 유지보수의 대부분은 사람 개발자가 한다(Sawada et al., EASE 2026 ✅ peer-reviewed) / **생산성 RCT 3편이 서로 충돌한다는 것은 한계가 아니라 발견이다**(+55.8% 2023 Copilot 그린필드 / +21% 2024 Google 사내 / **−19%** 2025 METR — **평균 내지 마라. 조건이 다르면 결과가 뒤집힌다**). 그리고 🕒 **유효기간 고지** — 이 책은 **2026-08-02 문서 스냅샷 기준**이며, 주 단위로 바뀌는 항목(모델 라인업 · 요금·한도 #28879/#34035 · 권한 프로필 Beta 딱지 · `/rewind` #11626 · 중첩 AGENTS.md #12115 · 60초 자동 응답 #28969 · Codex Security · **`gpt-5.4`·`gpt-5.4-mini` 2026-08-31 은퇴 예정** — **규율 5 문안 그대로, 미래 시제 고정**)을 독자에게 넘긴다. 이것이 신뢰의 마지막 장치다
- **독자가 얻는 것:** 도구 선택 논쟁에서 빠져나와, 두 하네스를 작업 성격에 따라 배분하는 자기 기준
- **필수 산출 아티팩트:** **고유 표면 9종 표**(9행 × 4열 — 산문 나열을 대체하는 장치)
- **Claude Code 대응 포인트:** 이 장 전체가 대응의 종합. §4-3(Codex에만 있는 것)과 §4-4(Claude Code에만 있는 것)를 대칭으로 배치
- **커버 문서:** `/codex/browser`, `/codex/computer-use`, `/codex/chrome-extension`, `/codex/appshots`, `/codex/features/voice`, `/codex/sites`, `/codex/features/codex-micro`, `/codex/customization/chronicle`(보 — 주 서술은 4장), `/codex/pets`, `/codex/guides/build-ai-native-engineering-team`(보 — 주 서술은 11장)
- **오프닝:** 앞 장 콜백 / **클로징:** 여정 회수형 / **스캐폴드:** 종합 정리형
- **예상 분량:** 8,000자 (소절 6개)

---

## 문서 섹션 → 챕터 매핑 표 (커버리지 증명)

레퍼런스 §6-1의 **148개 URL 전부**에 담당 챕터를 배정했다. 번호는 §6-1의 일련번호다. `(주)`는 주 서술 챕터, `(보)`는 보조 등장 챕터.

> **M5 반영 — 단일 출처 규약.** 이 표가 **커버 문서 배정의 단일 출처**다. 각 장 항목의 "커버 문서" 목록은 이 표에서 생성하며, 보조 배정도 `(보)` 표기와 함께 장 목록에 남긴다. 저술가는 자기 장의 목록만 보므로 불일치는 곧 누락이 된다. **라운드 1에서 발견된 양방향 불일치 7건(#148·#138·#94·#89·#128·#80·#26)은 전건 해소했다.**

### A. 기초·개념·제품 표면 (1~33)

| # | URL | 담당 장 |
|---|---|---|
| 1 | `/codex` | 1 |
| 2 | `/codex/quickstart` | 2 |
| 3 | `/codex/use-chatgpt` | 1 |
| 4 | `/codex/get-started-with-work` | 1 |
| 5 | `/codex/import` | **2 (핵심)** |
| 6 | `/codex/prompting` | 7 |
| 7 | `/codex/personalize` | 4 |
| 8 | `/codex/skills-and-plugins` | 6 |
| 9 | `/codex/permission-modes` | 5 |
| 10 | `/codex/whats-new` | 1 |
| 11 | `/codex/models` | 8 |
| 12 | `/codex/pricing` | 8 |
| 13 | `/codex/glossary` | **1(주: 표면 지도 앵커)** · 2(보 — 용어 정전 표 근거) |
| 14 | `/codex/app` | 1 |
| 15 | `/codex/web` | 1 |
| 16 | `/codex/cli` | 1 |
| 17 | `/codex/ide` | 1 |
| 18 | `/codex/cloud` | 1(보) · **9(주)** |
| 19 | `/codex/changelog` | 1 |
| 20 | `/codex/feature-maturity` | **1(주: 개념 경고)** · 9(보 — `experimental` 목록 전수 근거) |
| 21 | `/codex/open-source` | 1 |
| 22 | `/codex/features` | 1 |
| 23 | `/codex/projects` | 7 |
| 24 | `/codex/visualizations` | 7 |
| 25 | `/codex/automations` | 7 |
| 26 | `/codex/long-running-work` | 7(주) · 9(보) |
| 27 | `/codex/notifications` | 7 |
| 28 | `/codex/pets` | 12 |
| 29 | `/codex/features/codex-micro` | 12 |
| 30 | `/codex/browser` | 12 |
| 31 | `/codex/computer-use` | 12 |
| 32 | `/codex/features/voice` | 12 |
| 33 | `/codex/plugins` | 6 |

### B. 기능·레퍼런스·설정·커스터마이징 (34~67)

| # | URL | 담당 장 |
|---|---|---|
| 34 | `/codex/web-search` | 7 |
| 35 | `/codex/image-generation` | 7 |
| 36 | `/codex/image-inputs` | 7 |
| 37 | `/codex/appshots` | 12 |
| 38 | `/codex/chrome-extension` | 12 |
| 39 | `/codex/artifacts-viewer` ("Work with files") | 7 |
| 40 | `/codex/reference/commands` | 3 |
| 41 | `/codex/reference/slash-commands` | 3 |
| 42 | `/codex/reference/settings` | 4 |
| 43 | `/codex/reference/troubleshooting` | 2 |
| 44 | `/codex/configuration` | 4 |
| 45 | `/codex/customization/overview` | 4 |
| 46 | `/codex/customization/memories` | 4 |
| 47 | `/codex/customization/chronicle` | 4(주) · 12(보) |
| 48 | `/codex/config-file/config-basic` | 4 |
| 49 | `/codex/config-file/config-advanced` | 4 |
| 50 | `/codex/config-file/config-reference` | **4(주)** · 8(보 — reasoning effort 값 목록 정전) |
| 51 | `/codex/config-file/environment-variables` | 4 |
| 52 | `/codex/config-file/config-sample` | 4 |
| 53 | `/codex/agent-configuration/agents-md` | **4 (핵심)** |
| 54 | `/codex/agent-configuration/subagents` | 6 |
| 55 | `/codex/agent-configuration/speed` | 8 |
| 56 | `/codex/agent-configuration/rules` | **6 (execpolicy)** |
| 57 | `/codex/extend/record-and-replay` | 6 |
| 58 | `/codex/extend/mcp` | 11 |
| 59 | `/codex/windows/windows-app` | 4 |
| 60 | `/codex/windows/windows-sandbox` | 5 |
| 61 | `/codex/windows/wsl` | 4 |
| 62 | `/codex/cli-customization` | 3 |
| 63 | `/codex/developer-commands` | 3 |
| 64 | `/codex/developer-settings` | 4 |
| 65 | `/codex/hooks` | 6 |
| 66 | `/codex/build-skills` | 6 |
| 67 | `/codex/build-plugins` | 6 |

### C. 개발자 도구·환경·SDK·통합 (68~88)

| # | URL | 담당 장 |
|---|---|---|
| 68 | `/codex/developers` | 11 |
| 69 | `/codex/code-review` | 10 |
| 70 | `/codex/integrated-terminal` | 9 |
| 71 | `/codex/environments/modes` | 9 |
| 72 | `/codex/environments/local-environment` | 9 |
| 73 | `/codex/environments/cloud-environment` | 9 |
| 74 | `/codex/environments/git-worktrees` | 9 |
| 75 | `/codex/codex-sdk` | 11 |
| 76 | `/codex/app-server` | 2(보: `externalAgentConfig`) · **11(주)** |
| 77 | `/codex/mcp-server` | 11 |
| 78 | `/codex/github-action` | 9 |
| 79 | `/codex/non-interactive-mode` | 9 |
| 80 | `/codex/third-party/github` | 9(주) · 10(보) |
| 81 | `/codex/third-party/slack` | 9 |
| 82 | `/codex/third-party/linear` | 9 |
| 83 | `/codex/remote-connections` | 9 |
| 84 | `/codex/amazon-bedrock` | 9 |
| 85 | `/codex/use-cases` | 11 (⚠️ 개수 단정 금지) |
| 86 | `/codex/use-cases/collections` | 11 (⚠️ 개수 단정 금지) |
| 87 | `/codex/resources` | 11 (⚠️ 개수 단정 금지) |
| 88 | `/codex/videos` | 11 (⚠️ 개수 단정 금지) |

### D. 보안·권한·샌드박스·Security 제품 (89~116)

| # | URL | 담당 장 |
|---|---|---|
| 89 | `/codex/security-administration` | 5(보) · 11(주) |
| 90 | `/codex/permissions` | **5 (Beta 규율)** |
| 91 | `/codex/sandboxing` | 5 |
| 92 | `/codex/sandboxing/auto-review` | 5 |
| 93 | `/codex/agent-approvals-security` | **5(주)** · 10(보 — 경계 긋기) |
| 94 | `/codex/cloud/internet-access` | 5(보) · **9(주)** |
| 95 | `/codex/security` | 10 |
| 96 | `/codex/security/plugin` | 10 |
| 97 | `/codex/security/plugin/workbench` | 10 |
| 98 | `/codex/security/plugin/scans` | 10 |
| 99 | `/codex/security/plugin/deep-scans` | 10 |
| 100 | `/codex/security/plugin/code-changes` | 10 |
| 101 | `/codex/security/plugin/triage-backlog` | 10 |
| 102 | `/codex/security/plugin/fix-findings` | 10 |
| 103 | `/codex/security/plugin/export-findings` | 10 |
| 104 | `/codex/security/plugin/vulnerability-reports` | 10 |
| 105 | `/codex/security/plugin/security-hardening` | 10 |
| 106 | `/codex/security/plugin/changelog` | 10 |
| 107 | `/codex/security/setup` | 10 |
| 108 | `/codex/security/threat-model` | 10 |
| 109 | `/codex/security/faq` | 10 |
| 110 | `/codex/security/cli` | 10 |
| 111 | `/codex/security/cli/bulk-scans` | 10 |
| 112 | `/codex/security/cli/reference` | 10 |
| 113 | `/codex/security/cli/ci` | 10 |
| 114 | `/codex/security/cli/faq` | 10 |
| 115 | `/codex/security/sdk` | 10 |
| 116 | `/codex/cyber-safety` | 5 |

### E. 엔터프라이즈·관리·인증 (117~133)

| # | URL | 담당 장 |
|---|---|---|
| 117 | `/codex/administration` | 11 |
| 118 | `/codex/enterprise/admin-setup` | 11 |
| 119 | `/codex/enterprise/work-admin-faq` | 11 |
| 120 | `/codex/auth` | 2 |
| 121 | `/codex/enterprise/access-tokens` | 2(보: 인증) · 11(주: 조직) |
| 122 | `/codex/enterprise/groups-and-provisioning` | 11 |
| 123 | `/codex/enterprise/roles-and-workspace-permissions` | 11 |
| 124 | `/codex/enterprise/managed-configuration` | 11 |
| 125 | `/codex/hipaa-configuration` | 11 |
| 126 | `/codex/enterprise/workspace-model-availability` | **8(주)** · 11(보: 소절 4-③) |
| 127 | `/codex/enterprise/apps-and-connectors` | 11 |
| 128 | `/codex/enterprise/skills` | 6(보) · 11(주) |
| 129 | `/codex/enterprise/governance` | 11 |
| 130 | `/codex/enterprise/workspace-analytics` | 11 |
| 131 | `/codex/enterprise/analytics-api` | 11 |
| 132 | `/codex/enterprise/compliance-api` | 11 |
| 133 | `/codex/enterprise/windows-deployment` | 11 |

### F. 색인 대조로 추가 발견 (134~148)

| # | URL | 담당 장 | 비고 |
|---|---|---|---|
| 134 | `/codex/cli/reference` | 3 | 표 29개 복원본이 명령 지도의 1차 근거 |
| 135 | `/codex/cli/slash-commands` | 3 | **134와 바이트 동일 — 별개 문서로 취급 금지** |
| 136 | `/codex/custom-prompts` | 6 | **deprecated — 권장 기능으로 소개 금지** |
| 137 | `/codex/enterprise/usage-limits` | 8 | 수치 전무(37줄) — "수치 없음" 자체가 서술 근거 |
| 138 | `/codex/learn/best-practices` | **7(주)** · 4(보) · 10(보) | 흔한 실수 8개 · `AGENTS.md` 정의 원문 · "100% PR" 자체 주장 출처 |
| 139 | `/codex/overview` | 1 | 산문 거의 없음(랜딩). ⚠️ **UI 삽화 문자열 인용 금지**(규율 6) |
| 140 | `/codex/app/commands` | 3 | ≡ 40 |
| 141 | `/codex/app/settings` | 4 | ≡ 42 |
| 142 | `/codex/app/windows` | 4 | ≡ 59 |
| 143 | `/codex/ide/commands` | 3 | ≡ 145 |
| 144 | `/codex/ide/settings` | 4 | |
| 145 | `/codex/ide/slash-commands` | 3 | ≡ 143 |
| 146 | `/codex/sites` | 12 | |
| 147 | `/codex/community/codex-for-oss` | 1 | ⚠️ "GPT-5.4" 언급은 단독 근거로 쓰지 말 것 |
| 148 | `/codex/guides/build-ai-native-engineering-team` | 1(보) · **11(주: 소절 6)** · 12(보) | ⚠️ METR 인용 귀속·출처 미표기 수치 주의 |

### 커버리지 집계

| 항목 | 값 |
|---|---|
| 배정 대상 URL | **148 / 148 (100%)** |
| 미배정 | **0** |
| 매핑표 → 장 목록 양방향 일치 (M5) | **148 / 148** — 라운드 1 불일치 7건(#148·#138·#94·#89·#128·#80·#26) 전건 해소 |
| 별칭 중복쌍(같은 장에 배정 완료) | 6쌍 — 134≡135, 40≡140, 42≡141, 59≡142, 143≡145, 63↔134(캐노니컬 관계) |
| 고유 문서 기준 커버리지 | 약 140 / 140 |
| 주/보 이중 배정 URL | 16건 — #13·18·20·26·47·50·76·80·89·93·94·121·126·128·138·148 |

> **집계 각주 (m2 · V4).** 라운드 1에 있던 **"장당 주 담당 문서 수(합계 153)" 행은 삭제했다.** 보조 배정이 늘 때마다 갱신해야 하는 **파생 수치인데 커버리지를 증명하지 않으며**(증명은 "미배정 0"과 "양방향 일치 148/148"이 한다), 검증되지 않는 수치를 계획서에 남겨두는 것은 C4가 지적한 사고(근거 없는 수치 체크)의 재발 경로다. 장별 두께에 대한 설명은 아래 편차 해설이 그대로 담당한다.

> **편차 해설.** 10·11장의 문서 수가 많은 것은 Security 플러그인(16개)과 엔터프라이즈(17개)가 **각각 얇고 반복적인 페이지 묶음**이기 때문이다. 두 장 모두 페이지를 하나씩 훑지 않고 **"표 1개 + 산문 해설" 짝으로 압축**한다(10장 소절 4·6, 11장 소절 5 — C3·C7에서 배분표까지 못 박았다). 반대로 2·8장은 문서 수가 적지만 **한 문서의 밀도가 극도로 높다**(`/codex/import`의 매핑 표, `/codex/pricing`의 플랜 탭 5개 × 모델별 한도표).

---

## 커뮤니티·학술 소스 배정 표 (C4 반영 — 커버리지 점검 확장)

라운드 1의 자기 점검 결함(학술 2편이 미배치인데 "모두 배정"으로 체크)을 구조적으로 막기 위해, **공식 문서 외 소스에도 담당 장을 명시**한다.

### 커뮤니티 1차 소스 (GitHub 이슈 원장)

| 이슈 | 주제 | 👍 | 상태 | 주 서술 장 |
|---|---|---|---|---|
| #28879 | 레이트리밋 단가 급등 (세션 로그·대안가설 배제) | 362 | open | **8** (소절 6) |
| #11626 | `/rewind` 부재 | 192 | open | **3** (소절 1) |
| #28969 | 질문 60초 자동 응답 | 186 | open | **3** (소절 5) |
| #31814 | 서브에이전트 모델 지정 불가(버그, 원인 PR 특정) | 167 | **closed** | **6** (소절 6) |
| #34035 | 5시간 한도 임시 해제 영구화 요구 | 131 | open | **8** (소절 6) |
| #12115 | 중첩 `AGENTS.md` (Wix·Stripe 기업 신호) | 102 | open | **3(주)** · 4(보) |
| #28190 | macOS가 `rg` 차단 (해결책 재현됨) | 79 | open | **9** (소절 2) |
| #13762 | WSL `CODEX_HOME`·워크트리 경로 | 55 | open | **11** (소절 3) |
| #13942 | Plan mode 기본 시작 옵션 없음 | 34 | open | **7** (소절 6) |
| #19679 | 스킬 메타데이터 2% 하드코딩 | 31 | open | **6** (소절 2) |
| #21753 | 훅 패리티 (이벤트 매트릭스) | 22 | open | **6** (소절 4) |
| #15250 | 커스텀 서브에이전트 호출이 문서와 불일치 | 16 | open | **6** (소절 6) |
| #24515 | 마이그레이션이 사용자 config 덮어씀 | 0 | open | **2** (소절 1·4) |
| #32806 | 광고 컨텍스트 1.05M vs 실측 353K→258K | — | closed | **8** (소절 7) |
| #13386 | `AGENTS.md` 조용한 잘림 | — | — | **4** (소절 2) |
| #14039 | 서브에이전트별 모델 지정 (기능 요구) | — | open | **6** (소절 6) |

**국내 1차 소스:** AWS 한국 기술블로그(2026-06-11, 실명·소속) → **7장(주 — 실행 스타일 논쟁 소절, §5-4) · 12장(보 — 교차 리뷰, §5-8 #6) · 3장(존재 고지 한 문장만, V3)**. ⚠️ **이 블로그를 중첩 `AGENTS.md`·요금·권한 등 §5-4/§5-8 밖 주제에 귀속하지 마라** / dcinside 특이점갤(2026-04-28) → **3장(주)** / GeekNews 한국어 댓글 → 3장 보조 후보

### 학술·기술 리포트 (§5-10 ①~⑩ + §6-4)

| # | 문헌 | 등급 | 주 서술 장 |
|---|---|---|---|
| ① | Gorinova et al., arXiv:2606.17799 (하네스가 성능을 만든다) | 📄 | **1** (소절 6) |
| ② | Yang et al., SWE-agent, NeurIPS 2024 (인터페이스가 성능이다) | ✅ | **1** (소절 6) |
| ③ | Becker et al. (METR), arXiv:2507.09089 (체감≠실측 −19%) | 📄 | **7** (소절 7) · 12(보) |
| ④ | 생산성 RCT 3편 (+55.8% / +21% / −19%) | 혼합 | **12** (소절 6) |
| ⑤ | Aleithan et al., SWE-Bench+, arXiv:2410.06992 (벤치마크 오염) | 📄 | **8** (소절 7) — 라운드 1 미배치 해소 |
| ⑥ | Deng et al., SWE-Bench Pro, arXiv:2509.16941 (사내 코드베이스) | 📄 | **8** (소절 7) — 라운드 1 미배치 해소 |
| ⑦ | Singh et al., IssueTrojanBench, arXiv:2607.20759 (66.5%) | 📄 | **5** (소절 7, 조건 병기 M12) |
| ⑧ | OpenAI, GPT-5.2-Codex System Card Addendum (0.76) | ❌ 벤더 | **5** (소절 7) |
| ⑨ | Liu et al., arXiv:2603.28592 (조용한 부채) | 📄 | **12** (소절 6) |
| ⑩ | Sawada et al., EASE 2026, arXiv:2605.06464 (사람이 소유한다) | ✅ | **12** (소절 6) |
| ⑪ | Merrill et al., Terminal-Bench, ICLR 2026 | ✅ | **8** (소절 7 — ⚠️ **존재 사실만**, 순위 인용 금지) |

⏳ **낡음 표시 필수(신선도 원장 §C):** SWE-bench 1.96%(2023) · SWE-agent 12.5%(2024) · Agentless 32%(2024) · Copilot 40% 취약(2021) · Claude 3.7 Sonnet 50분 시간 지평(2025-03) — **역사 서술로만 쓰고 현재 Codex 성능의 근거로 쓰지 마라.**

---

## 자기 점검 체크리스트 (검증 근거 병기 — C4 반영)

라운드 1에서 근거 없는 체크가 거짓으로 판명됐으므로(학술 2편 미배치), 각 항목에 **어떻게 검증했는지**를 함께 남긴다. 체크만 하고 근거를 남기지 않으면 같은 사고가 반복된다.

| # | 항목 | 판정 | 검증 방법 |
|---|---|---|---|
| 1 | 모든 챕터가 하나의 핵심 질문에 답한다 | ✅ | 12개 장 각각 "핵심 질문" 1행 존재, 소절 구성이 그 질문의 하위 답으로 배열됨 |
| 2 | 챕터 순서에 맥이 흐른다 | ✅ | 이주(1~2) → 각성(3) → 재구축(4~6) → 운용(7~8) → 확장(9~11) → 종합(12). 9~11장 공통 논지("내 손 밖에서 내 환경이 결정된다") 명시 |
| 3 | 대상 독자 수준에 맞는다 | ✅ | 에이전틱 코딩 경험 전제, 기초 용어 재설명 없음. **서술 시점이 12장 내내 개인 개발자로 고정**(C7 리프레임으로 11장 시점 이탈 제거) |
| 4 | 공식 문서 커버리지 | ✅ **148/148** | 매핑표 A~F 전수, 미배정 0. **양방향 대조 완료** — 매핑표 → 장 목록 148/148, 장 목록 → 매핑표 일치(라운드 1 불일치 7건 해소) |
| 5 | 커뮤니티 소스 커버리지 | ✅ **16/16 + 국내 3종** | "커뮤니티·학술 소스 배정 표" — §6-3 원장 11건 + §5-2 추가분 + #32806·#13386·#14039 = 16건 전부 주 서술 장·소절 지정 |
| 6 | 학술 소스 커버리지 | ✅ **11/11** | §5-10 ①~⑩ + Terminal-Bench 각각의 담당 장·소절 명시. **라운드 1 미배치였던 ⑤ Aleithan·⑥ Deng은 8장 소절 7 신설로 해소** |
| 7 | 챕터 간 중복이 없다 | ✅ | 중복 위험 8건에 주/보 명시 — 중첩 `AGENTS.md`(3주/4보 3문장), `$` 접두사(3주/6콜백), `/fork`(3=문법/7=용법/12=제외), `experimental` 목록(9단독), 서브에이전트 모델 수치(8단독), `/codex/cloud`(9주/1보), `chronicle`(4주/12보), `access-tokens`(11주/2보) |
| 8 | 예상 분량 합계 | ✅ **108,000자** | 8,000×2(1·12) + 7,000×1(2) + 9,000×5(3·4·6·7·9) + 10,000×4(5·8·10·11) = 16,000+7,000+45,000+40,000 = **108,000** |
| 9 | 설계 근거에 기각 대안 ≥2 | ✅ **4건** | 문서 트리 미러링 / 태스크 쿡북 / 전면 대조 / **13장 분리**(라운드 1 열린 위험 3의 답) 각각 기각 사유 명시 |
| 10 | 통권 변주 배정표 완성 | ✅ | 12장 전부 배정. 오프닝 인접 중복 0, 프로필 메뉴 7종 전부 사용, '상황 가정' 2/12(17%), 클로징 12개 상이 + **전부 한 줄 정의 부여**, 스캐폴드 인접 중복 0, **그림 배정 열 신설**(총 7개) |
| 11 | 필수 산출 아티팩트 명세 | ✅ **12/12 장** | 각 장에 "필수 산출 아티팩트" 행 존재. 표는 **행·열 구성까지 지정** |
| 12 | 사용자 명시 요구 2건 | ✅ | ⓐ 매핑표로 커버리지 증명 + 커뮤니티·학술 배정표로 확장 ⓑ 전 장 "Claude Code 대응 포인트" + §4를 2·3·12장 뼈대로 + `/codex/import` 2장 전용 |
| 13 | 사실 리스크 봉인 | ✅ **규율 12건** | 특히 **규율 5(은퇴일 미래 시제)** · **규율 11(경험담 금지 + 허용 소재 4종)** · **규율 12(Claude Code 화이트리스트)**가 라운드 1이 지적한 구조적 구멍을 막는다. 규율 5는 `fact_rules_active.md`에도 시드 |

---

## 열린 위험 (라운드 2 확인 요청)

> 라운드 1의 열린 위험 1·2·3·4는 각각 리뷰 판정 1·2·3·4로 해소됐다. 특히 **열린 위험 4("저자 경험 서술로 메운다")는 삭제**하고 **규율 11**로 대체했다(C5) — 저술가는 에이전트이고, 그 지시는 허구의 경험담을 생산하며, 그렇게 만들어진 문장은 사실 주장이 아니라 서사여서 fact-checker의 레퍼런스 대조를 통과해버린다.

1. **10장 실행 난이도.** 10,000자·7소절로 상향했고 표 2개를 의무화했지만, Codex Security 16개 페이지를 소절 4·6에 담는 일은 여전히 이 책에서 가장 까다로운 저술이다. 저술가가 표를 기능 나열로 채우면 C3가 지적한 문제가 형태만 바꿔 재발한다 — **표의 각 행에 "무엇을 하는가"뿐 아니라 "언제 쓰는가"를 요구**하는 규율을 10장 항목에 명시했다.
2. **11장 소절 5의 압축 강도.** 13개 관리 문서를 표 1개로 압축한다. "문서가 위임하는 것" 열이 절반 이상 "Help Center로 위임"으로 채워질 가능성이 높은데, 이는 **문서의 실제 상태를 정직하게 반영한 것**이므로 결함이 아니다. 표 앞에 그 사실을 알리는 한 문장을 두기로 계획에 못 박았다.
3. **8장 판정 유보 밀도 (승인됨 — 라운드 2 판정 3).** 「요금·한도·크레딧 요율」 절과 「판정 유보 구간」 절은 확정 사실과 커뮤니티 관측이 번갈아 나오므로 문장마다 귀속이 붙는다. 규율 1의 남발 방지(장당 1회 + 표 캡션)와 충돌할 수 있다 — **이 소절만 예외로 문장 단위 귀속을 허용**하되, **시점 표기가 아니라 출처 등급 표기**(공식 / 커뮤니티 관측)로 처리한다.
4. ~~**`gpt-5.6` 표기 처리.**~~ **→ 종결 (라운드 2에서 원문 확인 완료).** 원문 확인 결과(2026-08-02, `research/codex-docs-raw/codex__agent-configuration__subagents.md` L158 "a higher-effort `gpt-5.6` configuration" · L167 "`gpt-5.6`: Start here for demanding agents") **접미사 없는 `gpt-5.6`은 오탈자가 아니라 `subagents` 페이지의 자체 표기다.** 이 페이지는 `gpt-5.6`을 계열/기본 구성을 가리키는 이름으로 쓰고 있으며, `/codex/models` 정전 ID 목록과의 불일치는 **레퍼런스 §3-11에 없던 7번째 문서 내부 불일치**다. m9·FR-7의 처리(원문 표기임을 병기, `gpt-5.6-sol`로 임의 해석 금지)를 **그대로 유지**하며, fact-checker는 이 확인을 반복하지 않는다(비용 통제 — `fact_rules_active.md` FR-7에 근거 시드).
