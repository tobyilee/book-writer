# 논문 리서치: GitHub·AWS·Cloudflare를 쓰는 개발자를 위한 CI/CD (+ AI 코딩 도구 팀 팁)

- genre: tech-book / 대상: 실무 한국 개발자 (비학문 독자 → 증명·통계 기법은 줄이고 결과와 직관 중심)
- 검색 시점: 2026-09-26
- 메타 확인 방법: DOI·저자·연도·발표처는 Crossref API, OpenAlex API(초록·피인용), arXiv API(ID·저자·코멘트의 발표처), USENIX/Google Cloud 공식 페이지에서 직접 조회한 값만 적었다. 피인용수는 OpenAlex 기준(2026-09-26 조회), OpenAlex에 없으면 Crossref `is-referenced-by-count`.
- "초록 기반"이라 적힌 항목은 전문을 읽지 못했고 공개 초록·공식 요약만으로 정리했다. 페이지 번호는 전문 미확인이라 인용문에 붙이지 않았다 — 인용문은 모두 초록 원문이다.
- 표기: [프리프린트] = 동료 심사 전 arXiv만 확인됨. [그레이] = 학술 논문이 아닌 산업 조사 보고서(방법론은 공개되어 있으나 심사 논문은 아님).

---

## A. CI의 효과와 비용 (고전)

### 논문 1: Quality and productivity outcomes relating to continuous integration in GitHub
- 저자·연도: Bogdan Vasilescu, Yue Yu, Huaimin Wang, Premkumar Devanbu, Vladimir Filkov (2015)
- 발표처: ESEC/FSE 2015 (10th Joint Meeting on Foundations of Software Engineering)
- DOI: 10.1145/2786805.2786850
- 피인용수: 400 (OpenAlex)
- 요약: GitHub 프로젝트의 대규모 이력 데이터로 CI 도입의 효과를 분리해 봤다. 교란 요인이 많은 상황에서 회귀 모델로 CI 도입 전후 생산성·품질 지표를 비교했다. 결론은 CI가 팀 생산성을 높여 외부 기여를 더 많이 통합하게 하면서도 코드 품질 저하는 관측되지 않았다는 것.
- 핵심 수치: 초록에 수치 없음 (전문 미확인).
- 인용할 만한 문장:
  > "Our main finding is that continuous integration improves the productivity of project teams, who can integrate more outside contributions, without an observable diminishment in code quality." (초록)
- 독자 전달 제안: "CI는 속도와 품질의 교환이 아니다"라는 1장 도입 근거. 단, 상관 기반 관측 연구라는 점을 한 줄 덧붙이자.

### 논문 2: Usage, costs, and benefits of continuous integration in open-source projects
- 저자·연도: Michael Hilton, Timothy Tunnell, Kai Huang, Darko Marinov, Danny Dig (2016)
- 발표처: ASE 2016 (31st IEEE/ACM International Conference on Automated Software Engineering)
- DOI: 10.1145/2970276.2970358
- 피인용수: 304 (OpenAlex)
- 요약: 세 가지 방법(저장소 분석·빌드 로그 분석·설문)으로 오픈소스에서 CI를 누가, 어떻게, 왜 쓰는지 조사한 최초의 대규모 연구. CI가 릴리스를 더 자주 하게 돕고 인기 프로젝트일수록 널리 채택됨을 보였다.
- 방법론: GitHub 프로젝트 34,544개, 빌드 1,529,291건, 개발자 설문 442명.
- 핵심 수치: 위 표본 규모. "릴리스 빈도 약 2배" 같은 구체 수치는 본문에 있다고 알려져 있으나 이번 조회에서 초록만 확인 → 본문 인용 시 미확인 처리.
- 인용할 만한 문장:
  > "we show evidence that supports the claim that CI helps projects release more often, that CI is widely adopted by the most popular projects" (초록)
  > "developers, tool builders, and researchers make decisions based on folklore instead of data." (초록)
- 독자 전달 제안: "CI는 민간요법이 아니라 데이터가 있다"는 프레이밍.

### 논문 3: Trade-offs in continuous integration: assurance, security, and flexibility
- 저자·연도: Michael Hilton, Nicholas Nelson, Timothy Tunnell, Darko Marinov, Danny Dig (2017)
- 발표처: ESEC/FSE 2017
- DOI: 10.1145/3106237.3106270
- 피인용수: 207 (OpenAlex)
- 요약: 인터뷰와 두 차례 설문으로 개발자가 CI에서 겪는 장벽을 질적으로 조사. 세 가지 긴장 관계를 도출했다: 속도 vs 확실성(Assurance), 접근성 vs 정보 보안(Security), 설정 자유도 vs 사용 편의(Flexibility).
- 인용할 만한 문장:
  > "developers face trade-offs between speed and certainty (Assurance), between better access and information security (Security), and between more configuration options and greater ease of use (Flexibility)." (초록)
- 독자 전달 제안: 책 전체의 설계 축으로 쓰기 좋다 — 빌드 시간(속도/확실성), 시크릿·OIDC(접근/보안), 재사용 워크플로·컴포지트 액션(자유도/편의).

### 논문 4: Continuous Integration Theater
- 저자·연도: Wagner Felidre, Leonardo Furtado, Daniel A. da Costa, Bruno Cartaxo, Gustavo Pinto (2019)
- 발표처: ESEM 2019 (ACM/IEEE International Symposium on Empirical Software Engineering and Measurement)
- DOI: 10.1109/esem.2019.8870152
- 피인용수: 33 (OpenAlex)
- 요약: CI 도구를 "켜 두기만" 하고 실제 CI 관행은 지키지 않는 상태를 "CI 극장"이라 명명. Travis CI를 쓰는 1,270개 프로젝트에서 드문 커밋·낮은 커버리지·오래 깨진 빌드·긴 빌드를 측정.
- 핵심 수치 (초록): 약 60%(748개)가 드문 커밋, 커버리지 확인 가능한 51개 평균 78%(Ruby 86%, Java 63%), 85%가 4일 넘게 방치된 깨진 빌드를 최소 1회 경험, 대부분은 "10분 규칙" 이내 빌드.
- 인용할 만한 문장:
  > "we observed that 85% of the studied projects have at least one broken build that take more than four days to be fixed." (초록)
- 독자 전달 제안: 챕터 오프닝용 — "초록 배지는 CI가 아니다".

---

## B. GitHub Actions 생태계 실증

### 논문 5: How Do Software Developers Use GitHub Actions to Automate Their Workflows?
- 저자·연도: Timothy Kinsman, Mairieli Wessel, Marco A. Gerosa, Christoph Treude (2021)
- 발표처: MSR 2021 (IEEE/ACM 18th International Conference on Mining Software Repositories)
- DOI: 10.1109/msr52588.2021.00054
- 피인용수: Crossref 75 (OpenAlex 6 — 인덱싱 차이)
- 요약: GitHub Actions 도입 직후 사용 양상과 도입 전후 활동 지표 변화를 본 첫 연구. 인식은 긍정적이지만, 도입 후 월별 거절 PR 수가 늘고 병합 PR의 커밋 수가 줄었다.
- 인용할 만한 문장:
  > "the adoption of GitHub Actions increases the number of monthly rejected pull requests and decreases the monthly number of commits on merged pull requests." (초록)
- 독자 전달 제안: 자동화가 리뷰 문턱을 바꾼다는 사례.

### 논문 6: On the Use of GitHub Actions in Software Development Repositories
- 저자·연도: Alexandre Decan, Tom Mens, Pooya Rostami Mazrae, Mehdi Golzadeh (2022)
- 발표처: ICSME 2022
- DOI: 10.1109/icsme55016.2022.00029
- 피인용수: 70 (OpenAlex)
- 요약: 68K 저장소 중 43.9%가 GHA 워크플로를 사용. 액션 재사용은 흔하지만 소수 액션에 집중되며, 액션을 참조하는 방식(버전 지정)이 보안·버전 관리 문제와 연결됨을 논의.
- 핵심 수치: 68K 저장소, 43.9% 사용.
- 인용할 만한 문장:
  > "reuse of actions is a common practice, even if this reuse is concentrated in a limited number of actions." (초록)

### 논문 7: Resource Usage and Optimization Opportunities in Workflows of GitHub Actions
- 저자·연도: Islem Bouzenia, Michael Pradel (2024)
- 발표처: ICSE 2024 (IEEE/ACM 46th International Conference on Software Engineering)
- DOI: 10.1145/3597503.3623303
- 피인용수: 24 (OpenAlex)
- 요약: GHA 워크플로의 자원 사용을 처음 포괄적으로 측정. 유료 저장소 평균 연 $504 비용, 자원의 91.2%가 테스트·빌드에 쓰임. 캐싱은 효과가 있으나 유료 저장소의 32.9%만 채택.
- 핵심 수치 (초록): 연 $504/유료 저장소, 테스트·빌드 91.2%, 트리거 비중 PR 50.7%·push 30.9%·스케줄 15.5%, 캐싱 채택 32.9%, 비활성 저장소의 스케줄 워크플로 중단만으로 해당 워크플로 실행시간 1.1~31.6% 절감.
- 인용할 만한 문장:
  > "CI/CD imposes significant costs, e.g., $504 per year for an average paid-tier repository." (초록)
- 신선도 주의: 가격 정책은 연구 시점 기준. GitHub Actions 과금 체계는 이후 바뀌었을 수 있으므로 web 리서치의 현행 요금과 병기할 것.
- 독자 전달 제안: 캐싱·경로 필터·concurrency 취소 챕터의 동기 부여 수치.

### 논문 8: The Hidden Costs of Automation: An Empirical Study on GitHub Actions Workflow Maintenance [프리프린트]
- 저자·연도: Pablo Valenzuela-Toledo, Alexandre Bergel, Timo Kehrer, Oscar Nierstrasz (2024)
- 발표처: arXiv 프리프린트 (발표처 미확인)
- arXiv: 2409.02366
- 요약: 10개 언어 약 200개 성숙 프로젝트의 워크플로 파일 진화를 분석. 워크플로도 유지보수 대상이며, 버그 수정과 CI/CD 개선이 주요 유지보수 동인.
- 인용할 만한 문장:
  > "practitioners should be aware of proper resource planning and allocation for maintaining GA workflows, thus exposing the ``hidden costs of automation.''" (초록)

### 논문 9: An Empirical Study of the Evolution of GitHub Actions Workflows
- 저자·연도: Pooya Rostami Mazrae, Alexandre Decan, Tom Mens, Mairieli Wessel (2026)
- 발표처: Journal of Systems and Software, 236, 112824 (2026)
- DOI: 10.1016/j.jss.2026.112824 / arXiv: 2602.14572
- 요약: 49K+ 저장소, 267K+ 워크플로 변경 이력, 3.4M+ 파일 버전(2019-11~2025-08). 저장소당 워크플로 중앙값 3개, 워크플로 파일의 7.3%가 매주 변경, 변경의 약 3/4은 단일 변경. LLM 코딩 도구가 워크플로 생성·유지보수 빈도에 미친 결정적 효과는 발견하지 못함.
- 인용할 만한 문장:
  > "We did not find any conclusive evidence of the effect of LLM coding tools or other major technological changes on workflow creation and workflow maintenance frequency." (초록)
- 독자 전달 제안: "워크플로는 한 번 쓰고 끝나는 파일이 아니다" + AI 시대에도 워크플로 관리 방식은 크게 안 바뀌었다는 근거.

### 논문 10: Catching Smells in the Act: A GitHub Actions Workflow Investigation
- 저자·연도: Ali Khatami, Cédric Willekens, Andy Zaidman (2024)
- 발표처: SCAM 2024 (IEEE International Conference on Source Code Analysis and Manipulation)
- DOI: 10.1109/scam63643.2024.00015
- 피인용수: 10 (OpenAlex)
- 요약: 83개 프로젝트의 빈번한 변경 패턴에서 22개 후보 "워크플로 스멜"을 뽑고, 32개 프로젝트에 수정 PR을 보내 메인테이너 반응으로 검증 → 7개 확정 스멜.
- 핵심 수치: 후보 22 → 확정 7. 확정 스멜의 구체 목록은 전문 미확인(본문 인용 시 원문 확인 필요).
- 독자 전달 제안: "워크플로 코드 리뷰 체크리스트" 박스의 학술 근거.

### 논문 11: An Empirical Study of Complexity, Heterogeneity, and Compliance of GitHub Actions Workflows [프리프린트]
- 저자·연도: Edward Abrokwah, Taher A. Ghaleb (2025)
- 발표처: arXiv 프리프린트 (발표처 미확인)
- arXiv: 2507.18062
- 요약: Java·Python·C++ 저장소의 GHA 워크플로 구조와 모범 사례 준수를 분석. 워크플로는 작고 얕으며 외부 액션 의존이 크다. 준수 격차는 permissions·timeout 설정·SHA pinning에서 특히 크고, 재사용 워크플로는 드물다. 공통 파이프라인 접두어가 39.5%에서 나타남.
- 인용할 만한 문장:
  > "Compliance gaps are widespread, especially in permissions, timeout configuration, and SHA pinning, while reusable workflows remain rare." (초록)
- 주의: web 검색 요약에 "SHA pinning 6.3% vs 태그 93.7%" 수치가 이 논문과 연결되어 나왔으나 초록에는 없다 → 본문 사용 시 전문 확인 필요, 현재 미확인.

### 논문 12: How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing
- 저자·연도: Edward Abrokwah, Taher A. Ghaleb (2026)
- 발표처: EASE 2026 (30th International Conference on Evaluation and Assessment in Software Engineering) — arXiv 코멘트 기준 accepted
- arXiv: 2605.02091
- 요약: 공식 문서 기반 30개 기준 준수 체크리스트를 만들고 LLM 감사를 평가. 95개 Java 워크플로에서 전체 준수율 28%, 권한 통제는 4%. LLM 간 합의는 낮아(Fleiss κ=0.28) 전문가 대체 불가, 다단 판정으로 검증 노력 81% 절감.
- 인용할 만한 문장:
  > "overall compliance is 28%, dropping to 4% for permission controls; Security (26%) lags far behind Clarity (68%)." (초록)
- 독자 전달 제안: `permissions:` 블록 명시가 왜 기본값이어야 하는지 + "LLM에게 워크플로 감사를 맡길 때의 한계" 팁 양쪽에 쓸 수 있음.

### 논문 13: How Developers Adopt, Use, and Evolve CI/CD Caching: An Empirical Study on GitHub Actions [프리프린트]
- 저자·연도: Kazi Amit Hasan, Yuan Tian, Safwat Hassan, Steven H. H. Ding (2026)
- 발표처: arXiv 프리프린트 (발표처 미확인)
- arXiv: 2604.13129
- 요약: 952개 저장소(캐시 도입 266, 미도입 686), 워크플로 1,556개, 설정 변경 17,185건. 저장소당 평균 9.37회 캐시 관련 변경. 캐싱은 표준화된 한 방식이 아니라 다양한 메커니즘으로 쓰이며, 파라미터 수정은 사람이, 버전 업데이트는 봇이 주로 수행.
- 독자 전달 제안: "캐시도 유지보수 비용이 있다" — 캐시 키 설계 절.

---

## C. GitHub Actions / CI 보안

### 논문 14: Characterizing the Security of GitHub CI Workflows
- 저자·연도: Igibek Koishybayev, Aleksandr Nahapetyan, Raima Zachariah, Siddharth Muralee, Bradley Reaves, Alexandros Kapravelos, Aravind Machiry (2022)
- 발표처: USENIX Security 2022
- DOI: 미확인 (USENIX 오픈 액세스, https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev)
- 요약: CI/CD 시스템이 지켜야 할 4개 보안 속성(Admittance Control, Execution Control, Code Control, Access to Secrets)을 정의하고 GitHub CI를 다른 5개 플랫폼과 비교. 447,238개 워크플로(213,854 저장소) 분석. GWChecker 도구 공개.
- 핵심 수치 (공식 초록): 99.8% 워크플로가 과권한(read-write), 23.7%가 pull_request로 트리거되며 저장소 코드를 사용, 99.7% 저장소가 외부 액션 실행, 97%가 검증되지 않은 제작자의 액션을 최소 1개 실행, 18%가 보안 업데이트가 누락된 액션을 실행.
- 인용할 만한 문장:
  > "Our analysis shows that 99.8% of workflows are overprivileged and have read-write access (instead of read-only) to the repository." (초록)
- 신선도 주의: 2022 논문 이후 GitHub는 신규 저장소의 GITHUB_TOKEN 기본 권한을 읽기 전용으로 바꾸는 등 기본값을 조정했다(web 리서치로 현행 기본값 확인 필요). 99.8%는 "당시" 수치로 표기할 것.
- 독자 전달 제안: 보안 챕터 오프닝 수치. 4개 속성은 챕터 뼈대로 그대로 재사용 가능.

### 논문 15: ARGUS: A Framework for Staged Static Taint Analysis of GitHub Workflows and Actions
- 저자·연도: Siddharth Muralee, Igibek Koishybayev, Aleksandr Nahapetyan, Greg Tystahl, Brad Reaves, Antonio Bianchi, William Enck, Alexandros Kapravelos, Aravind Machiry (2023)
- 발표처: USENIX Security 2023
- DOI: 미확인 (https://www.usenix.org/conference/usenixsecurity23/presentation/muralee, 코드: github.com/purs3lab/Argus)
- 요약: GitHub Actions의 코드 인젝션 취약점(예: 이슈 제목 같은 신뢰할 수 없는 입력이 `run:` 스크립트로 흘러가는 경우)을 찾는 최초의 정적 taint 분석.
- 핵심 수치 (USENIX 페이지·검색 요약): 워크플로 2,778,483개·액션 31,725개 분석, 워크플로 4,307개와 액션 80개에서 치명적 인젝션 취약점 발견, 기존 기법 대비 7배 이상 탐지.
- 독자 전달 제안: `${{ github.event.issue.title }}`를 `run:`에 직접 넣지 말고 env로 넘기라는 규칙의 근거. 재현 가능(코드 공개).

### 논문 16: Automatic Security Assessment of GitHub Actions Workflows
- 저자·연도: Giacomo Benedetti, Luca Verderame, Alessio Merlo (2022)
- 발표처: SCORED '22 (ACM Workshop on Software Supply Chain Offensive Research and Ecosystem Defenses)
- DOI: 10.1145/3560835.3564554
- 피인용수: 27 (OpenAlex)
- 요약: GHAST 도구로 50개 오픈소스 프로젝트에서 24,905건의 보안 이슈를 식별해 모두 보고.
- 인용할 만한 문장:
  > "The experimental results are worrisome as they allowed identifying a total of 24,905 security issues" (초록)

### 논문 17: Unpacking Security Scanners for GitHub Actions Workflows [프리프린트]
- 저자·연도: Madjda Fares, Yogya Gamage, Benoit Baudry (2026)
- 발표처: arXiv 프리프린트 (발표처 미확인)
- arXiv: 2601.14455
- 요약: 9개 GHA 워크플로 보안 스캐너를 체계적으로 비교. 10가지 공통 약점 분류를 세우고 2,722개 워크플로에 적용. 스캐너마다 분석 전략이 근본적으로 달라 보고 약점의 종류·수에 큰 격차.
- 인용할 만한 문장:
  > "these scanners implement fundamentally different analysis strategies, leading to major gaps regarding the nature and the number of reported security weaknesses." (초록)
- 독자 전달 제안: "스캐너 하나 돌렸다고 안심하지 말 것" — 도구 비교표 절 (도구명은 전문 확인 후).

### 논문 18: Mutating the "Immutable": A Large-Scale Study of Git Tag Alterations
- 저자·연도: Solal Rapaport, Laurent Pautet, Samuel Tardieu, Stefano Zacchiroli, Théo Zimmermann (2026)
- 발표처: ACM Conference on Reproducibility and Replicability 2026 (arXiv journal_ref 기준)
- arXiv: 2606.31354
- 요약: Software Heritage의 3억 2,840만 저장소에서 1,020만 건의 태그 변경(삭제·force-push)을 찾아냄, 18.9만 저장소 영향. Nixpkgs 교차 분석에서 변경된 태그를 참조하는 32개 패키지 중 7개가 실제 빌드 오류.
- 인용할 만한 문장:
  > "We therefore recommend that build systems and package managers pin dependencies to cryptographic commit hashes" (초록)
- 독자 전달 제안: `uses: foo/bar@v4` 대신 커밋 SHA 고정을 권하는 이유 — "태그는 움직인다"를 대규모 데이터로 증명. (2025년 tj-actions/changed-files 사고는 web 리서치 자료로 연결.)

---

## D. 소프트웨어 공급망 보안

### 논문 19: Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks
- 저자·연도: Marc Ohm, Henrik Plate, Arnold Sykosch, Michael Meier (2020)
- 발표처: DIMVA 2020 (arXiv 코멘트 기준)
- arXiv: 2005.09535 / DOI: 미확인
- 요약: npm·PyPI·RubyGems에서 실제 공격에 쓰인 악성 패키지 174개(2015-11~2019-11)를 수집·분석하고 공격 트리 2개를 제시.
- 독자 전달 제안: 의존성 설치 단계가 공격면이라는 기본 그림.

### 논문 20: SoK: Taxonomy of Attacks on Open-Source Software Supply Chains
- 저자·연도: Piergiorgio Ladisa, Henrik Plate, Matias Martinez, Olivier Barais (2023)
- 발표처: IEEE S&P 2023
- DOI: 10.1109/sp46215.2023.10179304
- 피인용수: 168 (OpenAlex)
- 요약: 언어·생태계 독립적 공격 트리 — 107개 공격 벡터, 94개 실사고 연결, 33개 방어책 매핑. 전문가 17명·개발자 134명 설문으로 검증.
- 독자 전달 제안: 공급망 챕터의 "지도". SolarWinds류(빌드 시스템 침해)도 이 분류 속 한 가지(빌드 단계)로 위치시키면 된다.

### 논문 21: SoK: Analysis of Software Supply Chain Security by Establishing Secure Design Properties
- 저자·연도: Chinenye Okafor, Taylor R. Schorlemmer, Santiago Torres-Arias, James C. Davis (2022)
- 발표처: SCORED '22
- DOI: 10.1145/3560835.3564556
- 피인용수: 52 (OpenAlex)
- 요약: 공급망 공격을 4단계로 나누고, 안전한 공급망의 3가지 속성 — 투명성(transparency)·유효성(validity)·분리(separation) — 을 제안해 기존 방어 프레임워크(SLSA 등 포함)를 매핑.
- 독자 전달 제안: SLSA·서명·OIDC 단기 자격증명을 "투명성/유효성/분리" 세 단어로 묶어 설명.

### 논문 22: Sigstore: Software Signing for Everybody
- 저자·연도: Zachary Newman, John Speed Meyers, Santiago Torres-Arias (2022)
- 발표처: ACM CCS 2022
- DOI: 10.1145/3548606.3560596
- 피인용수: 55 (OpenAlex)
- 요약: 서명은 SolarWinds 같은 공급망 침해의 유망한 완화책이지만 채택이 낮았다는 문제의식에서, OIDC 신원 기반 keyless 서명과 투명성 로그를 결합한 Sigstore 설계를 제시.
- 인용할 만한 문장:
  > "From the effects of XCodeGhost to SolarWinds, hackers have identified that targeting weak points in the supply chain allows them to compromise high-value targets" (초록)
- 독자 전달 제안: GitHub Actions의 artifact attestation·npm provenance가 어떤 원리 위에 있는지 설명할 때 원전.
- 참고: SLSA 자체는 학술 논문이 아닌 OpenSSF 명세 → web 리서치 소관.

### 논문 23: How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories
- 저자·연도: Michael Meli, Matthew R. McNiece, Bradley Reaves (2019)
- 발표처: NDSS 2019
- DOI: 10.14722/ndss.2019.23418
- 피인용수: 105 (OpenAlex)
- 요약: 약 6개월간의 실시간 커밋 스캔과 공개 스냅샷(오픈소스 저장소의 13%)으로 시크릿 유출을 측정. 10만 개 이상 저장소가 영향, 매일 수천 개의 새 시크릿이 유출.
- 인용할 만한 문장:
  > "We find that not only is secret leakage pervasive -affecting over 100,000 repositories -but that thousands of new, unique secrets are leaked every day." (초록)
- 독자 전달 제안: 장기 AWS 액세스 키 대신 OIDC로 가야 하는 근거. CI 로그를 통한 유출 자체를 다룬 동료 심사 논문은 이번에 찾지 못함(아래 한계 참고).

---

## E. 플레이키 테스트와 빌드 시간

### 논문 24: An empirical analysis of flaky tests
- 저자·연도: Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, Darko Marinov (2014)
- 발표처: FSE 2014 (22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering)
- DOI: 10.1145/2635868.2635920
- 피인용수: 443 (OpenAlex) — seminal
- 요약: 51개 오픈소스 프로젝트에서 플레이키 테스트를 고친 커밋 201개를 분석해 근본 원인·발현 방식·수정 전략을 분류한 첫 대규모 연구.
- 핵심 수치: 원인별 비율(비동기 대기·동시성·테스트 순서 의존 등)은 본문에 있으나 이번엔 초록만 확인 → 비율 인용 시 미확인.
- 인용할 만한 문장:
  > "an unmodified test is expected to either always pass or always fail for the same code under test. Unfortunately, in practice, some tests often called flaky tests—have non-deterministic outcomes." (초록)

### 논문 25: A Survey of Flaky Tests
- 저자·연도: Owain Parry, Gregory M. Kapfhammer, Michael Hilton, Phil McMinn (2021)
- 발표처: ACM TOSEM (Transactions on Software Engineering and Methodology)
- DOI: 10.1145/3476105
- 피인용수: 138 (OpenAlex) — 서베이
- 요약: 76편 문헌을 원인·비용·탐지·완화로 나눠 정리한 서베이. 개발자 59%가 월/주/일 단위로 플레이키 테스트를 겪는다는 선행 설문을 인용.
- 인용할 만한 문장:
  > "A recent survey of software developers found that 59% claimed to deal with flaky tests on a monthly, weekly, or daily basis." (초록)
- 독자 전달 제안: 플레이키 챕터의 입문 지도. 재시도(retry)로 덮기 전에 격리(quarantine)부터.

### 논문 26: An Empirical Study of Flaky Tests in Python
- 저자·연도: Martin Gruber, Stephan Lukasczyk, Florian Kroiß, Gordon Fraser (2021)
- 발표처: ICST 2021
- DOI: 10.1109/ICST49551.2021.00026 / arXiv: 2101.09077
- 요약: PyPI 22,352개 프로젝트, 테스트 876,186개 분석. 플레이키 7,571개 중 59%가 순서 의존, 28%가 테스트 인프라 문제, 나머지 13% 대부분 네트워크·난수 API.
- 인용할 만한 문장:
  > "A 95% confidence that a passing test case is not flaky on average would require 170 reruns." (초록)
- 독자 전달 제안: "한두 번 재실행해서 통과하면 괜찮다"는 직관을 깨는 수치.

### 논문 27: Taming Google-scale continuous testing
- 저자·연도: Atif Memon, Zebao Gao, Bao Nguyen, Sanjeev Dhanda, Eric Nickell, Rob Siemborski, John Micco (2017) — Crossref 저자 목록은 6번째까지 확인, 7번째(Micco)는 미확인
- 발표처: ICSE-SEIP 2017
- DOI: 10.1109/icse-seip.2017.16
- 피인용수: 234 (OpenAlex)
- 요약: Google 규모에서는 변경마다 전체 회귀 테스트가 불가능. 테스트 부하 제어와 결과 요약으로 피드백 지연을 줄였다. 실패하는 테스트는 매우 드물고, 실패하는 것은 대상 코드에 "가까운" 테스트이며, 최근 3명 넘는 개발자가 수정한 코드가 더 자주 깨진다.
- 인용할 만한 문장:
  > "very few of our tests ever fail, but those that do are generally \"closer\" to the code they test" (초록)
- 독자 전달 제안: 경로 필터·영향받는 테스트만 실행(affected tests) 전략의 근거.

### 논문 28: An empirical study of the long duration of continuous integration builds
- 저자·연도: Taher Ahmed Ghaleb, Daniel Alencar da Costa, Ying Zou (2019)
- 발표처: Empirical Software Engineering (Springer)
- DOI: 10.1007/s10664-019-09695-9
- 피인용수: 85 (OpenAlex)
- 요약: 초록 조회 실패 — 제목 수준 정보만 확인. 긴 CI 빌드의 요인 분석 연구로 알려져 있으나 수치 인용은 전문 확인 후.

### 논문 29: Studying the Interplay Between the Durations and Breakages of Continuous Integration Builds
- 저자·연도: Taher A. Ghaleb, Safwat Hassan, Ying Zou (2023; 온라인 2022)
- 발표처: IEEE TSE
- DOI: 10.1109/tse.2022.3222160
- 요약: 588개 프로젝트의 CI 빌드 924,616건. 빌드 깨짐을 고치려는 재시도·대기 같은 조치는 빌드를 길게 만들면서 통과를 보장하지도 않는다. 약 1/3 프로젝트는 시간과 안정성 중 하나를 희생.
- 인용할 만한 문장:
  > "actions to fix build breakages (e.g., retrying or waiting for build commands) not only increase build durations but also do not guarantee passing builds." (초록)

### 논문 30: Accelerating Continuous Integration by Caching Environments and Inferring Dependencies
- 저자·연도: Keheliya Gallaba, John Ewart, Yves Junqueira, Shane McIntosh (2022; 온라인 2020)
- 발표처: IEEE TSE
- DOI: 10.1109/tse.2020.3048335
- 요약: 빌드 명세 없이 의존성을 추론하고 빌드 환경을 캐시해 영향 없는 단계를 건너뛰는 Kotinos. 14,364건 빌드 기록에서 87.9% 이상이 가속 대상, 가속된 빌드의 74%가 2배 속도.
- 독자 전달 제안: 캐싱이 "얼마나" 효과가 있는지의 상한선 감각.

---

## F. 배포 전략·점진적 배포

### 논문 31: Continuous deployment at Facebook and OANDA
- 저자·연도: Tony Savor, Mitchell Douglas, Michael Gentili, Laurie Williams, Kent Beck, Michael Stumm (2016)
- 발표처: ICSE 2016 Companion (SEIP)
- DOI: 10.1145/2889160.2889223
- 피인용수: 131 (OpenAlex)
- 요약: 하루 수십~수천 회 배포하는 지속적 배포 관행을 두 회사 데이터로 분석한 초기 학술 보고. (초록 일부만 확인, 결과 수치는 미확인)

### 논문 32: Holistic configuration management at Facebook
- 저자·연도: Chunqiang Tang, Thawan Kooburat, Pradeep Venkatachalam, Akshay Chander, Zhe Wen, Aravind Narayanan 외 (2015)
- 발표처: SOSP 2015
- DOI: 10.1145/2815400.2815401
- 피인용수: 112 (OpenAlex)
- 요약: 매일 수천 건의 온라인 설정 변경으로 기능 롤아웃·A/B 실험·지역 부하 재분배를 관리하는 도구 체계. 코드 배포와 기능 공개를 분리하는 feature flag·점진적 공개의 원형 사례.
- 독자 전달 제안: Cloudflare Workers의 gradual deployments·feature flag 절의 배경.

### 논문 33: Gandalf: An Intelligent, End-To-End Analytics Service for Safe Deployment in Large-Scale Cloud Infrastructure
- 저자·연도: Ze Li, Qian Cheng, Ken Hsieh, Yingnong Dang, Peng Huang, Pankaj Singh, Xinsheng Yang, Qingwei Lin, Youjiang Wu, Sebastien Levy, Murali Chintalapati (2020)
- 발표처: NSDI 2020
- DOI: 미확인 (https://www.usenix.org/conference/nsdi20/presentation/li)
- 요약: Azure의 배포 안전 분석 서비스. 장애 신호와 진행 중인 롤아웃을 시공간 상관으로 연결해 나쁜 롤아웃을 광역 장애 전에 멈춘다. 18개월 이상 운영.
- 핵심 수치 (USENIX 초록): 데이터 플레인 정밀도 92.4%·재현율 100%, 컨트롤 플레인 정밀도 94.9%·재현율 99.8%.
- 독자 전달 제안: 카나리 + 자동 롤백의 "끝판왕" 사례. 소규모 팀 버전은 CloudWatch 알람 + CodeDeploy 자동 롤백, Workers gradual rollout.

### 논문 34: We're doing it live: A multi-method empirical study on continuous experimentation
- 저자·연도: Gerald Schermann, Jürgen Cito, Philipp Leitner, Uwe Zdun, Harald C. Gall (2018)
- 발표처: Information and Software Technology
- DOI: 10.1016/j.infsof.2018.02.010
- 피인용수: 74 (OpenAlex)
- 요약: 초록 조회 실패 — 카나리 릴리스·다크 런치·A/B 테스트 등 지속적 실험 관행을 인터뷰·설문으로 조사한 연구로 알려져 있으나 표본 규모·수치는 미확인.

---

## G. 인프라스트럭처 코드(IaC) 결함

### 논문 35: A systematic mapping study of infrastructure as code research
- 저자·연도: Akond Rahman, Rezvan Mahdavi-Hezaveh, Laurie Williams (2019)
- 발표처: Information and Software Technology
- DOI: 10.1016/j.infsof.2018.12.004
- 피인용수: Crossref 142
- 요약: IaC 연구 서베이(매핑 스터디). 세부 초록 미확인.

### 논문 36: The Seven Sins: Security Smells in Infrastructure as Code Scripts
- 저자·연도: Akond Rahman, Chris Parnin, Laurie Williams (2019)
- 발표처: ICSE 2019
- DOI: 10.1109/icse.2019.00033
- 피인용수: 222 (OpenAlex)
- 요약: IaC 스크립트 1,726개 질적 분석으로 7가지 보안 스멜 도출, SLIC 린터로 293개 저장소 15,232개 스크립트에서 21,201건 발견(하드코딩 비밀번호 1,326건). 버그 리포트 1,000건 중 응답 212, 수정 수용 148.
- 인용할 만한 문장:
  > "a hard-coded secret can persist for as long as 98 months, with a median lifetime of 20 months." (초록)
- 한계: 대상은 Puppet 등 당시 도구 중심(전문 미확인) — Terraform/CDK/CloudFormation 일반화는 조심.

### 논문 37: Gang of Eight: A Defect Taxonomy for Infrastructure as Code Scripts
- 저자·연도: Akond Rahman, Effat Farhana, Chris Parnin, Laurie Williams (2020)
- 발표처: ICSE 2020
- DOI: 10.1145/3377811.3380409
- 피인용수: 64 (OpenAlex)
- 요약: OpenStack 결함 커밋 1,448개로 8개 범주 IaC 결함 분류 체계를 만들고 실무자 66명 설문으로 검증, 291개 저장소 80,425 커밋에서 빈도 측정.
- 독자 전달 제안: "IaC 결함은 대규모 장애가 된다" → plan 검토·drift 감지를 CI에 넣는 이유.

---

## H. DORA / Accelerate (산업 연구)

### 자료 38: Accelerate: The Science of Lean Software and DevOps [단행본]
- 저자·연도: Nicole Forsgren, Jez Humble, Gene Kim (2018)
- 발행: IT Revolution
- ISBN: 9781942788331 (서지 사이트 검색으로 확인)
- 요약: State of DevOps 조사(4년치)를 통계적으로 분석해 소프트웨어 배포 성과를 측정하는 4대 지표(배포 빈도·변경 리드타임·변경 실패율·복구 시간)와 이를 끌어올리는 역량을 제시. 속도와 안정성이 상충하지 않는다는 주장의 원전.
- 주의: 4대 지표의 정확한 정의 문구는 원서 확인 필요. 최신 DORA는 지표 명칭·구성을 조정해 왔다(web 리서치의 dora.dev 현행 정의와 대조할 것).

### 자료 39: 2024 Accelerate State of DevOps Report (DORA) [그레이]
- 발행: Google Cloud / DORA, 2024-10-23 (Google Cloud 블로그 게시일 기준)
- 표본: 39,000명 이상(검색 요약 기준, 공식 페이지 원문에서는 미확인)
- 핵심 수치 (Google Cloud 블로그 원문):
  > "As AI adoption increased, it was accompanied by an estimated decrease in delivery throughput by 1.5% and an estimated reduction in delivery stability by 7.2%"
  - 맥락: AI 도입 25% 증가 시의 추정치(여러 2차 요약 기준, 블로그 인용문에서는 "25%" 조건 문구 미확인).
  - AI는 개인 생산성·몰입·직무 만족을 높이지만 배포 안정성·처리량에는 부정적. 소규모 배치·테스트 같은 기본기가 여전히 핵심.
  - 플랫폼 엔지니어링: 개발자 생산성↑, 단 초기에는 일시적 성과 하락 가능.
- 독자 전달 제안: "AI로 코드를 더 빨리 쓸수록 CI/CD 기본기가 더 중요해진다" — AI 팁 챕터의 핵심 근거.

### 자료 40: 2025 State of AI-assisted Software Development Report (DORA) [그레이]
- 발행: Google Cloud / DORA, 2025-09-24 (Google Cloud 블로그 게시일)
- 표본: 약 5,000명 ("nearly 5,000 technology professionals")
- 핵심 수치·주장 (Google Cloud 블로그 원문):
  - AI 사용률 90%, 80% 이상이 생산성 향상을 체감, 30%는 AI 생성 코드를 거의/전혀 신뢰하지 않음.
  - 2024와 달리 AI 도입이 배포 처리량·제품 성과와 양(+)의 관계. 그러나 "AI adoption does continue to have a negative relationship with software delivery stability".
  - 7개 팀 아키타입, 7개 역량으로 구성된 DORA AI Capabilities Model, 조직의 90%가 최소 하나의 플랫폼 도입.
  > "AI doesn't fix a team; it amplifies what's already there."
- 독자 전달 제안: 2024→2025 변화(처리량은 회복, 안정성은 여전히 음)를 나란히 보여 주면 "AI 시대 CI/CD = 안정성 방어선" 메시지가 선명해진다.

---

## I. AI 생성 코드: 생산성·품질·보안

### 논문 41: The Impact of AI on Developer Productivity: Evidence from GitHub Copilot [프리프린트]
- 저자·연도: Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer (2023)
- 발표처: arXiv 프리프린트
- arXiv: 2302.06590
- 요약: JavaScript HTTP 서버 구현 통제 실험. Copilot 그룹이 55.8% 빨리 완료.
- 한계: 단일 그린필드 과제, GitHub 소속 저자 포함.

### 논문 42: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity [프리프린트]
- 저자·연도: Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (2025, METR)
- 발표처: arXiv 프리프린트
- arXiv: 2507.09089
- 요약: 숙련 OSS 개발자 16명, 자기 프로젝트의 실제 과제 246개 RCT. AI 허용 시 오히려 완료 시간 19% 증가. 개발자는 사전 24% 단축을 예상하고 사후에도 20% 단축됐다고 믿음.
- 인용할 만한 문장:
  > "Surprisingly, we find that allowing AI actually increases completion time by 19%--AI tooling slowed developers down." (초록)
- 독자 전달 제안: 논문 41과 대비 — 과제 성격·숙련도·코드베이스 성숙도에 따라 효과가 뒤집힌다. "체감 ≠ 측정" → 팀은 DORA 지표로 재야 한다.

### 논문 43: Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects
- 저자·연도: Hao He, Courtney Miller, Shyam Agarwal, Christian Kästner, Bogdan Vasilescu (2025 프리프린트 / 2026 발표)
- 발표처: MSR 2026
- DOI: 10.1145/3793302.3793349 / arXiv: 2511.04427
- 요약: Cursor 도입 GitHub 프로젝트와 매칭 대조군의 이중차분(DiD). 개발 속도는 크게 오르지만 일시적이고, 정적 분석 경고와 코드 복잡도는 지속적으로 증가하며, 누적 복잡도가 이후 속도를 떨어뜨린다.
- 핵심 수치: 초록 v3 전문 미확인. web 검색 요약상 "첫 달 추가 라인 3~5배, 복잡도 약 41%·경고 약 30% 증가, 도입 806 vs 대조 1,380 저장소" → 본문 인용 전 논문 원문 대조 필요(현재 미확인).
- 독자 전달 제안: CI에 정적 분석·복잡도 게이트를 넣어야 하는 AI 시대의 근거.

### 논문 44: AI Writes Faster Than Humans Can Review: A Longitudinal Study of an Enterprise 2x Mandate [프리프린트]
- 저자·연도: Hao He, Shyam Agarwal, Yegor Denisov-Blanch, Pavel Azaletskiy, Sanmi Koyejo, Bogdan Vasilescu (2026)
- 발표처: arXiv 프리프린트
- arXiv: 2607.01904
- 요약: "병합 PR 2배" 목표를 내건 중견 기업의 개발자 802명·PR 196,212건(2024-01~2026-04) 패널. 1인당 처리량이 2026-04에 기준선 대비 2.09배. 리뷰어 1인당 부하가 약 2배가 되고 자동 리뷰가 사람 리뷰를 추월했지만, 병합률·되돌림(revert)률은 유지.
- 인용할 만한 문장:
  > "Adoption also restructured code review around automation: per-reviewer load roughly doubled and automated review overtook human review, while merge and revert rates held steady." (초록)
- 독자 전달 제안: AI 팀의 병목이 "리뷰"로 옮겨간다는 현장 데이터 — 자동 리뷰·CI 게이트의 역할 재정의.

### 논문 45: Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions
- 저자·연도: Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, Ramesh Karri (2022)
- 발표처: IEEE S&P 2022 (CACM 2025 재게재: 10.1145/3610721)
- DOI: 10.1109/sp46214.2022.9833571
- 피인용수: 439 (OpenAlex) — seminal
- 요약: MITRE CWE Top 25 관련 89개 시나리오로 1,689개 프로그램 생성 → 약 40%가 취약.
- 한계: 2021년 초기 Copilot 기준. 최신 모델에 그대로 일반화 금지(신선도 🕒).

### 논문 46: Do Users Write More Insecure Code with AI Assistants?
- 저자·연도: Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh (2023)
- 발표처: ACM CCS 2023
- DOI: 10.1145/3576915.3623157
- 피인용수: 219 (OpenAlex)
- 요약: 사용자 실험에서 AI 어시스턴트를 쓴 참가자가 유의하게 덜 안전한 코드를 썼고, 동시에 자기 코드가 안전하다고 더 믿었다(과신).
- 인용할 만한 문장:
  > "Participants with access to an AI assistant were also more likely to believe they wrote secure code" (초록)
- 독자 전달 제안: 보안 검사를 사람의 판단이 아니라 CI(SAST·시크릿 스캔)로 강제해야 하는 이유.

### 논문 47: Automated Code Review In Practice
- 저자·연도: Umut Cihan, Vahid Haratian, Arda İçöz, Mert Kaan Gül, Ömercan Devran, Emircan Furkan Bayendur, Baykal Mehmet Uçar, Eray Tüzün (2025)
- 발표처: ICSE 2025 SEIP (arXiv 코멘트 기준)
- arXiv: 2412.18531
- 요약: Beko의 10개 프로젝트·22개 저장소에 Qodo PR-Agent(GPT-4 Turbo) 기반 자동 리뷰 도입 사례 연구. 자동 코멘트의 73.8%가 해결 처리, 개발자는 소폭 품질 향상을 체감했지만 PR 종료 시간은 평균 5시간 52분 → 8시간 20분으로 증가, 잘못된·불필요한 코멘트 문제.
- 주의: 수치는 web 검색 요약 기준(초록 전문 재확인 권장).
- 독자 전달 제안: "AI 리뷰 봇은 공짜가 아니다" — 노이즈 관리(규칙 파일·대상 범위 제한) 팁.

---

## J. 에이전트가 만든 PR과 에이전트 워크플로 보안

### 논문 48: The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering [프리프린트]
- 저자·연도: Hao Li, Haoxiang Zhang, Ahmed E. Hassan (2025)
- arXiv: 2507.15003 (데이터셋 AIDev: github.com/SAILResearch/AI_Teammates_in_SE3)
- 요약: Codex·Devin·Copilot·Cursor·Claude Code 5개 에이전트가 만든 PR 45.6만여 건(6.1만 저장소, 4.7만 개발자) 데이터셋. 에이전트 PR은 빠르지만 사람 PR보다 수락률이 낮고 구조적으로 단순.
- 독자 전달 제안: 이후 논문 49~51의 공통 데이터 원천. 재현 가능(공개 데이터).

### 논문 49: On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub [프리프린트]
- 저자·연도: Miku Watanabe, Hao Li, Yutaro Kashiwa, Brittany Reid, Hajimu Iida, Ahmed E. Hassan (2025)
- arXiv: 2509.14745
- 요약: Claude Code로 생성된 PR 567개(157개 프로젝트). 83.8% 병합, 그중 54.9%는 수정 없이 병합. 리팩터링·문서·테스트 작업에 주로 쓰임.

### 논문 50: Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub
- 저자·연도: Ramtin Ehsani, Sakshi Pathak, Shriya Rawal, Abdullah Al Mujahid, Mia Mohammad Imran, Preetha Chatterjee (2026)
- 발표처: MSR 2026 (arXiv 코멘트 기준)
- arXiv: 2601.15195
- 요약: 에이전트 PR 33k 분석. 문서·CI·빌드 업데이트 과제가 병합 성공률 최고, 성능·버그 수정이 최저. 병합되지 않은 PR은 변경이 크고 파일이 많으며 CI/CD 검증을 통과하지 못하는 경우가 많다. 600개 질적 분석으로 거절 분류 체계(리뷰어 무관심, 중복 PR, 원치 않는 기능, 에이전트 정렬 실패 등).
- 인용할 만한 문장:
  > "Not-merged PRs tend to involve larger code changes, touch more files, and often do not pass the project's CI/CD pipeline validation." (초록)
- 독자 전달 제안: 에이전트에게도 "작은 배치 + 초록 CI"가 병합의 조건 — DORA 기본기와 연결.
- 참고: 검색 요약에 에이전트별 병합률(Codex 82.59% 등)이 있으나 초록에 없음 → 미확인.

### 논문 51: Comparing AI Coding Agents: A Task-Stratified Analysis of Pull Request Acceptance
- 저자·연도: Giovanni Pinna, Jingzhi Gong, David Williams, Federica Sarro (2026)
- 발표처: MSR 2026 Mining Challenge (arXiv 코멘트 기준)
- arXiv: 2602.08915
- 요약: AIDev의 PR 7,156건. 과제 유형이 수락률의 지배 요인 — 문서 82.1% vs 신기능 66.1%, 16%p 격차가 대부분 에이전트 간 차이보다 큼. 모든 과제에서 최고인 에이전트는 없음.
- 독자 전달 제안: "어느 에이전트가 최고냐"보다 "어떤 일을 맡기느냐". 에이전트 간 순위는 시점 의존(🕒).

### 논문 52: Security in the Age of AI Teammates: An Empirical Study of Agentic Pull Requests on GitHub [프리프린트]
- 저자·연도: Mohammed Latif Siddiq, Xinye Zhao, Vinicius Carvalho Lopes, Beatrice Casey, Joanna C. S. Santos (2026)
- 발표처: IST 투고·minor revision (arXiv 코멘트 기준, 게재 미확정)
- arXiv: 2601.00477
- 요약: AIDev 33k PR 중 보안 관련 1,293개(약 4%). 에이전트는 좁은 취약점 수정보다 테스트·문서·설정·에러 처리 같은 보강 작업을 주로 함. 보안 PR은 병합률이 낮고 리뷰가 길다. 거절은 보안 주제보다 PR 복잡도·장황함과 더 연관.

### 논문 53: Early Adoption of Agentic Coding Tools by GitHub Projects
- 저자·연도: Maliha Noushin Raida, Daqing Hou (2026)
- 발표처: KDD 2026 Workshop on Agentic Software Engineering (arXiv 코멘트 기준)
- arXiv: 2607.14037
- 요약: 2,361개 인기 저장소의 에이전트 PR 25,264건. 중앙값 저장소는 3개월에 1~2건뿐, 채택은 소수에 집중. 협업 형태는 "한 명의 사람이 감독"하는 모델이 지배적.

### 논문 54: Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection
- 저자·연도: Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz (2023)
- 발표처: AISec '23 (16th ACM Workshop on Artificial Intelligence and Security)
- DOI: 10.1145/3605764.3623985
- 피인용수: 542 (OpenAlex) — seminal
- 요약: LLM 통합 앱은 데이터와 지시의 경계를 흐린다. 모델이 읽어 들일 데이터에 프롬프트를 심는 "간접 프롬프트 인젝션"으로 데이터 탈취·API 조작이 가능함을 실증.
- 인용할 만한 문장:
  > "LLM-Integrated Applications blur the line between data and instructions" (초록)

### 논문 55: Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution [프리프린트]
- 저자·연도: Neil Fendley, Zhengyu Liu, Aonan Guan, Jiacheng Zhong, Yinzhi Cao (2026)
- arXiv: 2605.11229
- 요약: GitHub Actions·n8n의 LLM 에이전트 워크플로를 이슈 코멘트 같은 공격자 입력으로 탈취하는 JAW 프레임워크. GitHub 워크플로 4,714개와 n8n 템플릿 8개 탈취 성공. Claude Code·Gemini CLI·Qwen CLI·Cursor CLI의 공식 액션 포함 15개 액션에 걸침, GitHub·Google·Anthropic 등에 책임 공개.
- 인용할 만한 문장:
  > "An adversary may control and craft certain inputs, such as GitHub issue comments, to manipulate the LLM agent for unwanted actions, such as credential exfiltration and arbitrary command execution." (초록)
- 독자 전달 제안: AI 팁 챕터의 핵심 경고 — CI 안의 AI 에이전트는 ARGUS(논문 15)가 본 "신뢰할 수 없는 입력 → 실행" 문제의 새 판. 최소 권한·시크릿 비노출·트리거 제한.

### 논문 56: Specifying and Maintaining Agentic Workflows: An Empirical Study of GitHub Agentic Workflows [프리프린트]
- 저자·연도: Jasem Khelifi, Issam Oukhay, Ali Ouni, Mohammed Sayagh, Mohamed Aymen Saied (2026-09-23 게시)
- arXiv: 2609.27263
- 요약: GitHub Agentic Workflows(gh-aw) Markdown 파일 1,248개(276 저장소) 분석. 지시문 중앙값 556.5단어, 62.1%가 코드 블록 포함, 4개월째에도 78.2%가 갱신됨. 그러나 프롬프트 인젝션 방어를 명시한 비율은 9.4%.
- 인용할 만한 문장:
  > "only 9.4% explicitly address prompt-injection defense." (초록)
- 신선도: 검색일 3일 전 게시된 매우 최신 프리프린트. gh-aw 기능 현황은 web 리서치로 교차 확인.

---

## 교차 관찰 (research-lead 참고용)

1. **같은 결론이 세 층에서 반복된다:** CI는 품질 손실 없이 처리량을 올리고(1), DORA는 기본기(작은 배치·테스트)가 성과를 가른다고 하며(38–40), 에이전트 PR도 작고 CI를 통과해야 병합된다(50). 책의 척추 메시지로 쓸 만하다.
2. **AI 효과는 측정 방식에 따라 부호가 바뀐다:** 55.8% 빨라짐(41) vs 19% 느려짐(42) vs 속도↑·복잡도 지속↑(43) vs 처리량 2배·되돌림률 유지(44). 충돌이라기보다 과제·숙련도·기간 차이. 본문에서 한 수치만 인용하면 오해를 낳는다.
3. **GHA 보안 문제는 기본값과 참조 방식에 몰려 있다:** 과권한(14, 12), 신뢰 불가 입력 인젝션(15, 55), 태그 참조(18, 11). 세 가지 규칙(permissions 최소화, 입력을 env로, SHA 고정)으로 정리 가능.
4. **DORA 2024 vs 2025 차이:** 처리량 관계가 음→양으로 바뀌었고 안정성은 계속 음. 2025는 방법론·지표 구성이 바뀌었을 수 있어 직접 비교 시 주의.

## 수집 한계

- Semantic Scholar API가 429로 막혀 Crossref·OpenAlex·arXiv로 대체. 피인용수는 OpenAlex 기준이라 Google Scholar보다 낮게 나온다.
- ACM DL 전문 접근 불가(403) → 대부분 초록 기반. 원인별 비율(Luo 2014), Hilton 2016의 "릴리스 2배", Cursor 논문의 구체 수치, 에이전트별 병합률은 전문 미확인이라 본문 인용 전 확인 필요.
- USENIX 논문(14, 15, 33)은 DOI 없음 — URL로 대체.
- **공백:** (a) AWS·Cloudflare 특정 배포(CodeDeploy, Workers gradual deployments, OIDC 연동)를 다룬 동료 심사 실증 연구는 찾지 못함 — web 리서치 소관. (b) CI 로그/러너를 통한 시크릿 유출(ArtiPACKED 등)은 산업 보고서만 있고 심사 논문 미확인. (c) SLSA는 명세 문서만 있고 채택 효과를 정량화한 논문 미확인. (d) 카나리/프로그레시브 딜리버리의 효과를 정량 비교한 학술 연구는 대기업 사례(31–33)뿐, 소규모 팀 대상은 없음. (e) Terraform/CDK 등 현행 IaC 도구 대상 결함 연구는 이번 수집에 포함하지 못함(Rahman 연구는 당시 Puppet 등 중심으로 알려짐, 미확인).
