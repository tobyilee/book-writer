# 논문 리서치: 개발 워크플로 전략 (브랜치·PR·코드 리뷰·CI·GitHub Actions·Merge Queue)

- 검색 시점: 2026-09-26
- 메타 확인 방법: 저자·연도·발표처·DOI는 Crossref API와 OpenAlex API로 조회해 대조했다. 수치·인용문은 원문 PDF(저자 공개본·arXiv·USENIX 오픈 액세스)를 받아 텍스트로 뽑은 뒤 해당 페이지에서 직접 확인했다. 원문을 못 본 항목은 "초록 기준" 또는 "2차 출처"로 따로 표시했다.
- 피인용수: 조회 시점 2026-09-26. `OA`=OpenAlex, `CR`=Crossref. 두 DB 모두 Google Scholar보다 적게 센다. 상대 비교용으로만 쓴다.
- 페이지 표기: 원문 PDF의 쪽 순서(1부터)이며, 학회 논문집 쪽 번호가 아니다. 서지 쪽 범위는 Crossref 값이다.
- 대상 독자가 실무 개발자라서 통계 모형 설명은 줄이고, 결과와 독자에게 전할 방식 위주로 정리했다.

---

## A. 코드 리뷰

### 논문 1: Expectations, Outcomes, and Challenges of Modern Code Review (seminal)
- 저자·연도: Alberto Bacchelli, Christian Bird (2013)
- 발표처: 2013 35th International Conference on Software Engineering (ICSE), pp. 712-721
- DOI: 10.1109/ICSE.2013.6606617
- 피인용수: CR 540
- 원문 확인: 저자 공개 PDF(sback.it) 전문
- 요약: Microsoft의 도구 기반 코드 리뷰(CodeFlow)를 관찰·인터뷰·설문·코멘트 분류로 조사했다. 리뷰하는 첫째 동기는 결함 발견이지만, 실제 결과물은 결함 지적보다 코드 개선, 지식 전달, 팀 인지, 대안 제시 쪽이 많았다. 리뷰에서 가장 어려운 일은 "변경을 이해하는 것"이었다.
- 방법론: 16개 제품 팀의 개발자 17명을 관찰하고 인터뷰했다. 리뷰 코멘트 570개(200개 스레드)를 카드 소팅으로 분류했고, 관리자 165명과 개발자 873명에게 설문했다.
- 핵심 수치·결과:
  - 코멘트 분류: 코드 개선 165개(29%)가 가장 많았고, 결함은 78개(14%)로 9개 범주 중 4위였다. 결함 78개 가운데 65개는 로직 문제였다 (p.7, §V.A).
  - 결함 발견을 1순위 동기로 꼽은 비율: 개발자 383명(44%) (p.5)
  - 설문 응답률: 관리자 28%, 개발자 44% (p.4)
- 인용할 만한 문장:
  > "Review comments about defects are few, comprising one-eighth of the total in our sample, and mostly address 'micro' level and superficial concerns" (p.7, §V.B)
  > "the most difficult thing when doing a code review is understanding the reason of the change" (인터뷰 인용, p.7, §VI.A)
- 독자 전달 방식: "리뷰는 버그 잡는 그물보다는 팀이 코드를 함께 이해하는 자리다." PR 설명에 변경 이유를 써야 하는 근거로 쓸 수 있다.

### 논문 2: Modern Code Review: A Case Study at Google
- 저자·연도: Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, Alberto Bacchelli (2018)
- 발표처: ICSE-SEIP 2018 (40th ICSE: Software Engineering in Practice), pp. 181-190
- DOI: 10.1145/3183519.3183525
- 피인용수: CR 251
- 원문 확인: 저자 공개 PDF 전문
- 요약: Google의 리뷰 도구 Critique의 로그 약 900만 건과 인터뷰·설문을 분석했다. Google이 리뷰를 도입한 첫째 이유는 결함 발견이 아니라 가독성·유지보수성과 교육이었다. 다른 조직보다 변경이 작고 리뷰가 빠르며, 리뷰어는 대개 1명이었다.
- 방법론: 인터뷰 12건, 설문 응답 44건(응답률 45%), 2년간 리뷰 로그(변경 약 900만 건, 작성자·리뷰어 25,000명 이상, 코멘트 약 1,300만 건)
- 핵심 수치·결과 (p.6~7, §5):
  - 첫 피드백까지 걸리는 시간의 중앙값: 작은 변경은 1시간 미만, 아주 큰 변경은 약 5시간. 전체 리뷰 과정의 중앙값은 4시간 미만
  - 비교 대상(Rigby & Bird 2013 수치를 재인용): 승인까지 중앙값이 AMD 17.5시간, Chrome OS 15.7시간, Microsoft 세 프로젝트 14.7/19.8/18.9시간
  - 변경 크기: 35% 이상이 파일 1개만 수정하고, 약 90%가 파일 10개 미만을 수정한다. 10% 이상이 코드 한 줄만 바꾼다. 수정 줄 수의 중앙값은 24줄
  - 리뷰어: 리뷰어가 2명 이상인 변경은 25% 미만이고, 리뷰어 수의 중앙값은 1명
  - 80% 이상의 변경이 코멘트 해소를 최대 1회만 반복한다 (p.6)
  - 개발자 1명이 주당 작성하는 변경의 중앙값은 약 3건, 주당 리뷰하는 변경의 중앙값은 4건
  - Critique 사용자 97%가 만족 (p.7, 내부 만족도 설문)
- 인용할 만한 문장:
  > "Code review at Google has converged to a process with markedly quicker reviews and smaller changes, compared to the other projects previously investigated. Moreover, one reviewer is often deemed as sufficient, compared to two in the other projects." (p.7, Finding 4)
  > "Reviewing was introduced at Google to ensure code readability and maintainability." (p.5, Finding 1)
- 독자 전달 방식: "작고 빠른 PR"이 실제로 어떤 수준인지 보여 주는 기준점으로 쓴다(중앙값 24줄, 4시간 미만). 다만 Google의 monorepo, 도구, 가독성 인증 문화가 함께 있어서 나온 숫자라는 점을 같이 밝힌다.

### 논문 3: Convergent Contemporary Software Peer Review Practices
- 저자·연도: Peter C. Rigby, Christian Bird (2013)
- 발표처: Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering (ESEC/FSE 2013), pp. 202-212
- DOI: 10.1145/2491411.2491444
- 피인용수: OA 315 / CR 256
- 원문 확인: 초록(OpenAlex). 세부 수치는 Sadowski et al. 2018의 재인용으로 확인했다. 원문 PDF는 받지 못했다.
- 요약: Google(Android, Chromium OS), Microsoft(Bing, Office, SQL), AMD, Lucent, OSS 6개 프로젝트의 리뷰를 비교했다. 환경은 서로 달랐지만 리뷰 주기, 참여 인원 같은 특성이 비슷한 값으로 수렴했다. 활성 리뷰어는 2명이 최적이라는 결론이다.
- 핵심 수치: 리뷰에 참여하면 개발자가 아는 서로 다른 파일 수가 프로젝트에 따라 66~150% 늘었다 (초록). 리뷰어 2명 수렴과 승인 시간 중앙값은 논문 2 항목에 적었다.
- 인용할 만한 문장 (초록):
  > "Our knowledge sharing measure shows that conducting peer review increases the number of distinct files a developer knows about by 66% to 150% depending on the project."
- 독자 전달 방식: 리뷰가 지식을 퍼뜨린다는 주장을 수치로 뒷받침한다. 리뷰어 2명과 1명(Google)의 대비는 조직 맥락에 따른 선택지로 소개한다.

### 논문 4: What Types of Defects Are Really Discovered in Code Reviews? (seminal, 고전)
- 저자·연도: Mika V. Mäntylä, Casper Lassenius (2009년 5월호. OpenAlex는 온라인 공개 연도 2008로 기록)
- 발표처: IEEE Transactions on Software Engineering, pp. 430-448 (권·호 미확인)
- DOI: 10.1109/TSE.2008.71
- 피인용수: OA 206
- 원문 확인: 초록 기준
- 핵심 수치: 산업 리뷰 9건에서 결함 388개, 학생 리뷰 23건에서 371개를 분류했다. 리뷰에서 찾은 결함의 75%는 기능에 보이는 영향이 없는 진화성(evolvability) 결함이었다.
- 인용할 만한 문장 (초록):
  > "75 percent of defects found during the review do not affect the visible functionality of the software."
- 독자 전달 방식: Bacchelli & Bird의 결과("결함은 1/8")와 짝을 지어 "리뷰의 주된 산출물은 유지보수성"이라는 흐름을 만든다.

### 논문 5: Modern Code Reviews in Open-Source Projects: Which Problems Do They Fix?
- 저자·연도: Moritz Beller, Alberto Bacchelli, Andy Zaidman, Elmar Juergens (2014)
- 발표처: MSR 2014 (11th Working Conference on Mining Software Repositories), pp. 202-211
- DOI: 10.1145/2597073.2597082
- 피인용수: OA 266
- 원문 확인: 초록 기준
- 핵심 수치: OSS 두 프로젝트에서 리뷰 후 변경 1,400건 이상을 분류했다. 유지보수성 문제와 기능 문제의 비율은 75:25였다. 리뷰 코멘트의 7~35%는 반영되지 않았고, 변경의 10~22%는 명시적인 코멘트 없이 일어났다.
- 독자 전달 방식: 75:25 비율이 산업·학계·OSS에서 되풀이된다는 점을 강조한다.

### 논문 6: The Impact of Code Review Coverage and Code Review Participation on Software Quality
- 저자·연도: Shane McIntosh, Yasutaka Kamei, Bram Adams, Ahmed E. Hassan (2014)
- 발표처: MSR 2014, pp. 192-201
- DOI: 10.1145/2597073.2597076
- 피인용수: OA 356
- 원문 확인: 초록 기준
- 핵심 결과: Qt, VTK, ITK 프로젝트에서 리뷰 커버리지(리뷰를 거친 변경의 비율)와 참여도가 품질과 유의하게 연관됐다. 커버리지가 낮으면 릴리스 후 결함이 컴포넌트당 최대 2개, 참여도가 낮으면 최대 5개 더 생기는 것으로 추정됐다.
- 인용할 만한 문장 (초록):
  > "Low code review coverage and participation are estimated to produce components with up to two and five additional post-release defects respectively."
- 독자 전달 방식: 보호 브랜치에서 "리뷰 없는 머지 금지"를 설정할 근거. 형식적인 승인(러버 스탬프)은 참여도 부족에 해당한다는 연결점도 만들 수 있다.

### 논문 7: Characteristics of Useful Code Reviews: An Empirical Study at Microsoft
- 저자·연도: Amiangshu Bosu, Michaela Greiler, Christian Bird (2015)
- 발표처: 2015 IEEE/ACM 12th Working Conference on Mining Software Repositories (MSR), pp. 146-156
- DOI: 10.1109/MSR.2015.21
- 피인용수: OA 147
- 원문 확인: 초록 기준
- 핵심 결과: Microsoft 5개 프로젝트의 리뷰 코멘트 150만 개를 분류기로 분석했다. 리뷰어가 입사한 첫해에는 유용한 코멘트 비율이 크게 오르고 그 뒤 정체된다. 변경에 포함된 파일이 많을수록 유용한 코멘트의 비율이 낮아진다.
- 인용할 만한 문장 (초록):
  > "the more files that are in a change, the lower the proportion of comments in the code review that will be of value to the author of the change."
- 독자 전달 방식: 리뷰 크기와 리뷰 품질의 관계를 보여 주는 가장 직접적인 학술 근거. "큰 PR은 느리다"보다 "큰 PR은 리뷰가 얕아진다"는 쪽으로 설명한다.

### 논문 8: The Effects of Change Decomposition on Code Review — A Controlled Experiment
- 저자·연도: Marco di Biase, Magiel Bruntink, Arie van Deursen, Alberto Bacchelli (arXiv 공개 2018)
- 발표처: arXiv:1805.10978. 초록 아래 "Subjects: Human-Computer Interaction, Software Engineering" 표기로 보아 PeerJ Computer Science 게재로 추정되지만, 게재지와 DOI는 미확인
- 원문 확인: arXiv PDF 전문(초록)
- 핵심 결과: 전문가와 대학원생 28명이 참여한 통제 실험이다. 변경을 쪼개면 잘못 보고되는 이슈가 줄고 맥락을 찾는 행동이 늘었지만, 변경 이유에 대한 이해도와 찾아낸 결함 수에는 영향이 없었다.
- 독자 전달 방식: "PR을 쪼개면 버그를 더 잡는다"는 과장을 경계하게 한다. 쪼개면 리뷰의 잡음이 줄어든다는 정도로 정직하게 말한다.

### 논문 9: Do Small Code Changes Merge Faster? A Multi-Language Empirical Investigation (최근, 반례)
- 저자·연도: Gunnar Kudrjavets, Nachiappan Nagappan, Ayushi Rastogi (2022)
- 발표처: MSR 2022 (19th International Conference on Mining Software Repositories), pp. 537-548
- DOI: 10.1145/3524842.3528448 (arXiv:2203.05045)
- 피인용수: CR 9
- 원문 확인: arXiv PDF 전문
- 핵심 결과: 10개 언어의 인기 프로젝트 100개에서 PR 845,316건을 분석하고 Gerrit·Phabricator 리뷰 401,790건으로 교차 확인했다. PR의 크기와 구성은 머지까지 걸리는 시간과 관계가 없었다. 삽입·삭제·수정 비율과 머지 시간의 상관은 무시할 수준이었다(rs = 0.18 / 0.06 / -0.14, p.8).
- 인용할 만한 문장 (초록, p.1):
  > "Our study shows that pull request size and composition do not relate to time-to-merge."
- 독자 전달 방식: 작은 PR을 권하는 이유를 "빨리 머지된다"에 두지 말고 리뷰 품질(Bosu 2015)과 되돌리기 쉬움에 두라는 균형 자료. Google의 결과와 부딪히는 지점이라 책에서 긴장을 드러내기 좋다.

### 논문 10: Mining Code Review Data to Understand Waiting Times Between Acceptance and Merging
- 저자·연도: Gunnar Kudrjavets, Aditya Kumar, Nachiappan Nagappan, Ayushi Rastogi (2022)
- 발표처: MSR 2022, pp. 579-590
- DOI: 10.1145/3524842.3528432 (arXiv:2203.05048)
- 피인용수: CR 20
- 원문 확인: arXiv PDF(초록)
- 핵심 결과: Gerrit·Phabricator 코드 리뷰 약 50만 건에서 두 종류의 대기를 찾았다. 제안부터 첫 응답까지의 대기와, 승인부터 머지까지의 대기다. 승인 후 머지까지의 시간을 줄이면 Phabricator 리뷰가 29~63% 빨라질 수 있었다. 수동 머지를 자동 머지로 바꾸는 것을 권한다.
- 인용할 만한 문장 (초록):
  > "Our analysis suggests that switching from manual to automatic merges can help increase code velocity."
- 독자 전달 방식: auto-merge와 Merge Queue를 도입할 근거. "승인은 끝났는데 아무도 머지 버튼을 누르지 않는 시간"을 예로 든다.

### 논문 11: Nudge: Accelerating Overdue Pull Requests toward Completion (Microsoft)
- 저자·연도: Chandra Maddila, Sai Surya Upadrasta, Chetan Bansal, Nachiappan Nagappan, Georgios Gousios, Arie van Deursen (2023. OpenAlex는 2022로 기록)
- 발표처: ACM Transactions on Software Engineering and Methodology (TOSEM), pp. 1-30
- DOI: 10.1145/3544791
- 피인용수: OA 22
- 원문 확인: 초록 기준
- 핵심 수치: Microsoft 147개 저장소에서 무작위 시험을 했다. 기한을 넘긴 PR 8,500건의 해결 시간이 60% 줄었고, 알림의 73%가 긍정 처리됐다. 이후 8,000개 저장소로 넓혀 1년간 알림 210,000건을 보냈다.
- 독자 전달 방식: 리뷰 지연은 기술보다 사람의 주의가 문제라는 점. 리뷰 SLA와 리마인더 봇의 근거로 쓴다.

### 논문 12: Using Nudges to Accelerate Code Reviews at Scale (Meta)
- 저자·연도: Qianhua Shan, David Sukhdeo, Qianying Huang, Seth Rogers, Lawrence Chen, Elise Paradis, Peter C. Rigby, Nachiappan Nagappan (2022)
- 발표처: ESEC/FSE 2022 (30th), pp. 472-482
- DOI: 10.1145/3540250.3549104
- 피인용수: OA 17
- 원문 확인: 초록 기준 (OpenAlex 초록이 중간에서 잘려 있어 실험 결과 수치는 미확인)
- 핵심 수치 (초록): 개발자의 84.7%가 diff가 리뷰에 머무는 시간에 만족했다. 불만은 각 응답자 diff의 리뷰 시간 75백분위, 즉 24시간을 넘기는 diff와 밀접하게 연관됐다.
- 독자 전달 방식: "평균이 아니라 꼬리(p75)가 체감을 결정한다." 리뷰 지표를 설계할 때 쓸 수 있는 교훈.

### 논문 13 (서베이): Modern Code Reviews—Survey of Literature and Practice
- 저자·연도: Deepika Badampudi, Michael Unterkalmsteiner, Ricardo Britto (2023)
- 발표처: ACM TOSEM, pp. 1-61
- DOI: 10.1145/3585004
- 피인용수: OA 37
- 원문 확인: 초록 기준
- 요약: 2021년까지 나온 코드 리뷰 1차 연구 244편을 체계적으로 매핑했다. 실무자 Q-방법론 설문에서 1,300개 데이터 포인트를 얻었다. 실무자는 품질 영향과 프로세스 속성 연구를 중요하게 봤고, 인간 요인·지원 도구 연구에는 부정적이었다. 연구와 실무의 방향이 어긋나 있다는 결론이다.
- 보조 서베이: Nicole Davila, Ingrid Nunes, "A systematic literature review and taxonomy of modern code review", Journal of Systems and Software, 2021, DOI 10.1016/j.jss.2021.110951 (OA 72, 초록 미수집)
- 독자 전달 방식: 코드 리뷰 장의 "더 읽을거리"와 연구 지형 조감에 쓴다.

---

## B. Pull Request 기반 개발과 수락 요인

### 논문 14: An Exploratory Study of the Pull-based Software Development Model (seminal)
- 저자·연도: Georgios Gousios, Martin Pinzger, Arie van Deursen (2014)
- 발표처: ICSE 2014 (36th), pp. 345-355
- DOI: 10.1145/2568225.2568260
- 피인용수: CR 495
- 원문 확인: 저자 공개 PDF 전문
- 요약: GHTorrent 전체 데이터와 표본 291개 프로젝트로 PR 모델을 분석했다. PR은 빨리 처리되고, 머지 여부는 소수의 요인으로 결정되며, 거절 사유 가운데 기술적인 것은 소수였다.
- 핵심 수치:
  - 활성 저장소의 14%가 PR을 사용 (p.6, 2012~2013 기준)
  - 표본 PR의 84.73%가 결국 머지됨 (p.6)
  - 머지 시간: 80%가 3.7일, 90%가 10일, 95%가 26일 안에 머지됐다. 30%는 1시간 안에 머지 (p.6)
  - 대부분의 PR은 20줄 미만이고 하루 안에 처리된다. 토론은 평균 3개 코멘트 (p.7, RQ2)
  - 머지 결정에 가장 큰 영향을 준 요인은 PR이 최근에 수정된 코드를 건드리는지 여부 (p.8, RQ3)
  - 머지되지 않은 PR 중 27%는 동시 수정(obsolete·conflict·superseded) 때문에, 13%만 구현 오류 때문에 닫혔다. 53%는 분산 개발의 특성이나 소통 문제 때문이었다 (p.9, RQ4)
- 인용할 만한 문장:
  > "only 13% of the contributions are rejected due to technical issues, which is the primary reason for code reviewing, while a total 53% are rejected for reasons having to do with the distributed nature of the pull request process (concurrent modifications) or the way projects handle communication of project goals and practices." (p.9, §8)
- 독자 전달 방식: "PR이 거절되는 진짜 이유는 코드보다 타이밍과 소통"이라는 도입부. 브랜치가 오래 살아 있을수록 충돌·obsolete로 닫힐 위험이 커진다는 점과 연결한다.
- 주의: 2014년 GitHub 데이터이며, 그 뒤 PR 사용률은 크게 올랐다. 14%를 현재 수치로 쓰면 안 된다.

### 논문 15: Work Practices and Challenges in Pull-Based Development: The Integrator's Perspective
- 저자·연도: Georgios Gousios, Andy Zaidman, Margaret-Anne Storey, Arie van Deursen (2015)
- 발표처: ICSE 2015 (37th), pp. 358-368
- DOI: 10.1109/ICSE.2015.55
- 피인용수: OA 316
- 원문 확인: 초록 기준
- 핵심 결과: 통합자(integrator) 749명을 설문했다. 통합자는 프로젝트 품질을 유지하는 일과 기여의 우선순위를 정하는 일을 가장 어려워했다.
- 동반 논문: Gousios, Storey, Bacchelli, "Work practices and challenges in pull-based development: the contributor's perspective", ICSE 2016, pp. 285-296, DOI 10.1145/2884781.2884826 (CR 213, 내용 미수집)

### 논문 16: Influence of Social and Technical Factors for Evaluating Contribution in GitHub
- 저자·연도: Jason Tsay, Laura Dabbish, James Herbsleb (2014)
- 발표처: ICSE 2014, pp. 356-366
- DOI: 10.1145/2568225.2568315
- 피인용수: OA 456
- 원문 확인: 초록 기준
- 핵심 결과: PR 수락에는 기술적 신호(좋은 기여 관행)와 사회적 신호(제출자와 관리자의 관계)가 함께 쓰였다. 코멘트가 많은 PR은 수락 가능성이 훨씬 낮았다. 자리 잡은 프로젝트일수록 수락에 보수적이었다.
- 인용할 만한 문장 (초록):
  > "Pull requests with many comments were much less likely to be accepted, moderated by the submitter's prior interaction in the project."
- 독자 전달 방식: 오픈소스에 기여할 때 먼저 이슈로 논의해 관계를 만들라는 조언의 근거.

---

## C. 지속적 통합(CI)의 효과

### 논문 17: Quality and Productivity Outcomes Relating to Continuous Integration in GitHub (seminal)
- 저자·연도: Bogdan Vasilescu, Yue Yu, Huaimin Wang, Premkumar Devanbu, Vladimir Filkov (2015)
- 발표처: ESEC/FSE 2015 (10th Joint Meeting), pp. 805-816
- DOI: 10.1145/2786805.2786850
- 피인용수: CR 329
- 원문 확인: 저자 공개 PDF 전문. 데이터 공개(github.com/yuyue/pullreq_ci)
- 요약: Travis CI를 도입한 GitHub 프로젝트 246개의 도입 전후를 비교했다. CI를 쓰면 팀이 외부 기여를 더 많이 통합하면서도 품질이 떨어지지 않았다.
- 핵심 수치 (p.9, §4.1~4.2, 다른 변수를 고정했을 때):
  - CI를 쓰면 코어 개발자의 머지된 PR 수가 20.5% 늘고, 거절된 PR 수가 42.3% 줄었다
  - 외부 기여자의 거절 PR은 26% 줄었다
  - 코어 개발자가 보고한 버그는 48% 늘었다. 저자들은 이를 CI 덕분에 내부에서 버그를 더 찾게 된 것으로 해석했다. 외부 기여자의 버그 보고 수에는 영향이 없었다.
- 인용할 만한 문장 (초록):
  > "Our main finding is that continuous integration improves the productivity of project teams, who can integrate more outside contributions, without an observable diminishment in code quality."
- 독자 전달 방식: "CI는 속도와 품질 중 하나를 고르는 문제가 아니다"라는 명제의 대표 근거.

### 논문 18: Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects (seminal)
- 저자·연도: Michael Hilton, Timothy Tunnell, Kai Huang, Darko Marinov, Danny Dig (2016)
- 발표처: ASE 2016 (31st IEEE/ACM), pp. 426-437
- DOI: 10.1145/2970276.2970358
- 피인용수: CR 259
- 원문 확인: 저자 공개 PDF 전문
- 방법론: GitHub 프로젝트 34,544개, Travis CI 빌드 1,529,291건, 개발자 설문 442명(응답률 9.8%)
- 핵심 수치:
  - 조사 대상 프로젝트의 40%가 CI를 사용. 별 수 기준 최상위 그룹은 70%, 인기가 낮을수록 23%까지 떨어진다 (p.3~4)
  - CI 프로젝트는 월 0.54회, 비CI 프로젝트는 월 0.24회 릴리스한다. 같은 프로젝트도 CI 도입 전에는 월 0.34회였다 (p.7)
  - PR 수락 시간의 중앙값: CI 정보가 있으면 5.2시간, 없으면 6.8시간으로 1.6시간 빠르다 (p.8)
  - 평균 빌드 시간은 500초가 조금 안 된다 (p.7)
  - CI를 쓰지 않는 이유 1위는 "팀원이 CI에 익숙하지 않음"(47.00%), 2위는 "자동화 테스트가 없음"(44.12%) (p.6, Table 4)
  - CI를 쓰는 이유 1위는 "빌드가 깨질 걱정이 줄어서"(87.71%), 2위는 "버그를 더 일찍 잡아서"(79.61%) (p.8, Table 6)
- 인용할 만한 문장:
  > "Projects that use CI release more than twice as often as those that do not use CI." (p.7, Observation)
  > "CI is not widely perceived as helpful with debugging." (p.7, Observation)
- 독자 전달 방식: "CI는 안심을 산다"(87.71%). 도입 장벽은 기술보다 익숙함이라는 점을 1장·CI 장 도입부에 쓸 수 있다.
- 주의: Travis CI 시대의 데이터다. 현재 GitHub Actions 환경과 수치가 다를 수 있다.

### 논문 19: Trade-offs in Continuous Integration: Assurance, Security, and Flexibility
- 저자·연도: Michael Hilton, Nicholas Nelson, Timothy Tunnell, Darko Marinov, Danny Dig (2017)
- 발표처: ESEC/FSE 2017, pp. 197-207
- DOI: 10.1145/3106237.3106270
- 피인용수: OA 207
- 원문 확인: 초록 기준
- 핵심 결과: 인터뷰와 설문 두 건을 분석해 CI의 세 가지 트레이드오프를 정리했다. 속도와 확실성 사이의 보증(Assurance), 접근성과 정보 보안 사이의 보안(Security), 설정 옵션과 사용 편의 사이의 유연성(Flexibility)이다.
- 독자 전달 방식: CI 설계 장의 뼈대. 빠른 피드백과 철저한 검증 사이에서 무엇을 PR 단계에 두고 무엇을 머지 후나 야간 작업으로 미룰지 정하는 틀.

### 논문 20: Studying the Impact of Adopting CI on the Delivery Time of Pull Requests (반례·보정)
- 저자·연도: João Helis Bernardo, Daniel Alencar da Costa, Uirá Kulesza (2018)
- 발표처: MSR 2018 (15th), pp. 131-141
- DOI: 10.1145/3196398.3196421
- 피인용수: OA 46
- 원문 확인: 초록 기준
- 핵심 결과: 87개 프로젝트의 PR 162,653건을 분석했다. CI 도입 후 머지된 PR을 더 빨리 전달한 프로젝트는 51.3%뿐이었다. 도입 후 PR 제출이 크게 늘어난 것이 전달이 느려진 주요 원인이었다.
- 확장판: Bernardo, da Costa, Kulesza, Treude, "The impact of a continuous integration service on the delivery time of merged pull requests", Empirical Software Engineering, 2023, DOI 10.1007/s10664-023-10327-6 (arXiv:2305.16365). 설문 응답 450건을 더해, CI의 핵심 이점은 전달 속도보다 PR 결정을 더 잘 내리게 하는 데 있다고 결론지었다.
- 인용할 만한 문장 (2023 확장판 초록):
  > "adopting a CI service may not necessarily quicken the delivery of merge PRs. Instead, the pivotal benefit of a CI service is to improve the decision making on PR submissions"
- 독자 전달 방식: Hilton의 "1.6시간 빠름"과 나란히 놓고 "CI는 빨라지게 하는 도구라기보다 판단을 돕는 도구"로 정리한다.

### 논문 21: The Impact of Continuous Integration on Other Software Development Practices
- 저자·연도: Yangyang Zhao, Alexander Serebrenik, Yuming Zhou, Vladimir Filkov, Bogdan Vasilescu (2017)
- 발표처: ASE 2017 (32nd), pp. 60-71
- DOI: 10.1109/ASE.2017.8115619
- 피인용수: OA 178
- 원문 확인: 초록 기준 (세부 수치 미수집)
- 핵심 결과: Travis CI를 도입한 수백 개 프로젝트에서 커밋 방식, 이슈·PR 닫기, 테스트 관행이 어떻게 적응하는지 분석했다. 이전 연구가 말한 것보다 더 미묘한 그림이 나왔다.

### 논문 22 (서베이): The Effects of Continuous Integration on Software Development: A Systematic Literature Review
- 저자·연도: Eliezio Soares, Gustavo Sizilio, Jadson Santos, Daniel Alencar da Costa, Uirá Kulesza (2022)
- 발표처: Empirical Software Engineering (2022)
- DOI: 10.1007/s10664-021-10114-1 (arXiv:2103.05451)
- 피인용수: CR 45
- 원문 확인: arXiv PDF(초록)
- 요약: 연구 479편에서 실증 연구 101편을 골랐다. 여섯 가지 주제로 정리했다: 개발 활동, 프로세스, QA, 통합 패턴, 이슈·결함, 빌드 패턴. 전반적으로 긍정적이지만 기술·프로세스 과제도 따른다.
- 보조 서베이: Mojtaba Shahin, Muhammad Ali Babar, Liming Zhu, "Continuous Integration, Delivery and Deployment: A Systematic Review on Approaches, Tools, Challenges and Practices", IEEE Access, 2017, pp. 3909-3943, DOI 10.1109/ACCESS.2017.2685629 (OA 675). 2004~2016년 논문 69편을 검토해 접근법·도구 30개를 분류했다.

---

## D. Flaky Test

### 논문 23: An Empirical Analysis of Flaky Tests (seminal)
- 저자·연도: Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, Darko Marinov (2014)
- 발표처: FSE 2014 (22nd ACM SIGSOFT), pp. 643-653
- DOI: 10.1145/2635868.2635920
- 피인용수: CR 392
- 원문 확인: 저자 공개 PDF 전문
- 핵심 수치:
  - Apache 51개 프로젝트에서 flaky test를 고친 것으로 보이는 커밋 201건을 분석 (p.1)
  - 근본 원인 상위 3개: Async Wait 45%(161건 중 74건), Concurrency 20%(32건), Test Order Dependency 12%(19건) (p.4~5)
  - 78%는 처음 작성될 때부터 flaky했다. 96%는 플랫폼과 무관했다 (p.2, 발견 요약)
  - Async Wait flaky 가운데 54%는 waitFor로 고쳤다 (p.2)
  - Google TAP 수치를 재인용: 하루 평균 테스트 실패 160만 건 중 7.3만 건(4.56%)이 flaky 때문. 실패한 테스트를 같은 코드에 10번 다시 돌려 한 번이라도 통과하면 flaky로 분류 (p.1)
- 인용할 만한 문장:
  > "if a flaky test fails frequently, developers tend to ignore its failures and, thus, could miss real bugs." (p.1, §1)
- 독자 전달 방식: "flaky의 절반은 기다림을 잘못 쓴 탓"(sleep 대신 조건 대기). 재시도(retry)는 증상을 가릴 뿐이라는 경고.

### 논문 24: Taming Google-Scale Continuous Testing
- 저자·연도: Atif Memon, Zebao Gao, Bao Nguyen, Sanjeev Dhanda, Eric Nickell, Rob Siemborski, John Micco (2017)
- 발표처: ICSE-SEIP 2017 (39th ICSE), pp. 233-242
- DOI: 10.1109/ICSE-SEIP.2017.16
- 피인용수: CR 202
- 원문 확인: Google Research 공개 PDF 전문
- 핵심 수치:
  - TAP은 하루 평균 13,000개 이상의 코드 프로젝트를 통합·테스트한다. 빌드 80만 건, 테스트 실행 1억 5천만 건 (p.1)
  - 커밋은 평균 초당 1건. 변경마다 따로 테스트하는 것은 비용 대비 효과가 없어 약 45분(피크 시간)마다 "마일스톤"으로 묶어 실행한다 (p.1)
  - 영향받는 테스트 대상 550만 개 중 91.3%는 한 번도 실패하지 않았다. 통과와 실패를 모두 겪은 것은 2.07%, flaky를 걸러 내면 실제로 결함을 찾은 것은 1.23% (p.4)
  - 여러 사람이 여러 번 수정한 단일 파일은 거의 100% 실패를 일으켰다 (p.3)
- 인용할 만한 문장:
  > "it is impossible to weed out all flaky tests" (p.2, §I)
- 독자 전달 방식: 규모가 커지면 "모든 커밋을 모두 테스트"가 불가능해진다. 배치·선택 실행으로 가야 하는 이유를 설명하며 Merge Queue 장으로 넘어가는 다리로 쓴다.

### 논문 25 (서베이): A Survey of Flaky Tests
- 저자·연도: Owain Parry, Gregory M. Kapfhammer, Michael Hilton, Phil McMinn (2021)
- 발표처: ACM TOSEM, pp. 1-74
- DOI: 10.1145/3476105
- 피인용수: OA 138
- 원문 확인: 초록 기준
- 요약: flaky test 관련 논문 76편을 원인, 비용과 결과, 탐지, 완화와 수리의 네 축으로 정리했다. 초록은 개발자의 59%가 월·주·일 단위로 flaky test를 다룬다는 선행 설문을 인용한다(원 설문의 출처는 미확인).
- 후속: Parry et al., "Surveying the developer experience of flaky tests", ICSE-SEIP 2022, pp. 253-262, DOI 10.1145/3510457.3513037. 응답 170건과 StackOverflow 스레드 38개를 분석했다. 개발자는 flaky test가 CI를 방해한다는 데 강하게 동의했다. flaky를 자주 겪는 개발자일수록 진짜 실패를 무시할 가능성이 컸다. 원인 1위는 setup/teardown 문제로 인식됐다.
- 보조: Eck, Palomba, Castelluccio, Bacchelli, "Understanding flaky tests: the developer's perspective", ESEC/FSE 2019, pp. 830-840, DOI 10.1145/3338906.3338945 (OA 170, Mozilla 개발자 대상, 세부 수치 미수집)

### 논문 26: Predictive Test Selection (Facebook/Meta)
- 저자·연도: Mateusz Machalica, Alex Samylkin, Meredith Porth, Satish Chandra (2019)
- 발표처: ICSE-SEIP 2019 (41st), pp. 91-100
- DOI: 10.1109/ICSE-SEIP.2019.00018
- 피인용수: OA 106
- 원문 확인: 초록 기준
- 핵심 수치: 운영 환경에 배포한 결과, 변경 테스트의 인프라 비용을 절반으로 줄였다. 그러면서도 개별 테스트 실패의 95% 이상과 결함 있는 변경의 99.9% 이상을 개발자에게 보고했다. flaky도 모형에 반영했다.
- 독자 전달 방식: 큰 조직의 CI는 "전부 돌리기"에서 "확률적으로 고르기"로 간다. 일반 팀에는 경로 필터(paths)와 영향 분석이 그 축소판이라는 연결점.

### 논문 27: Flake Aware Culprit Finding (Google)
- 저자·연도: Tim A. D. Henderson, Bobby Dorward, Eric Nickell, Collin Johnston, Avi Kondareddy (2023)
- 발표처: 2023 IEEE Conference on Software Testing, Verification and Validation (ICST), pp. 362-373
- DOI: 10.1109/ICST57152.2023.00041
- 피인용수: OA 10
- 원문 확인: 초록 기준
- 핵심 결과: flaky 잡음이 있는 상황에서 문제 커밋을 찾기 위해 베이즈 추론과 잡음 있는 이진 탐색을 쓰는 알고리즘을 제안했다. Google의 테스트 파손 13,000건 이상으로 평가했다. 배치로 머지·테스트하면 범인을 찾는 비용이 생긴다는 Merge Queue 논의와 이어진다.

---

## E. 브랜칭·머지 충돌

### 논문 28: The Effect of Branching Strategies on Software Quality (Microsoft)
- 저자·연도: Emad Shihab, Christian Bird, Thomas Zimmermann (2012)
- 발표처: ESEM 2012 (ACM-IEEE International Symposium on Empirical Software Engineering and Measurement), pp. 301-310
- DOI: 10.1145/2372251.2372305
- 피인용수: OA 73
- 원문 확인: 초록 기준
- 핵심 결과: Windows Vista와 Windows 7에서 브랜치 구조와 품질의 관계를 처음으로 정량화했다. 브랜치 구조가 조직 구조와 어긋나면 릴리스 후 실패율이 높았다.
- 인용할 만한 문장 (초록):
  > "misalignment of branching structure and organizational structure is associated with higher post-release failure rates."
- 독자 전달 방식: 브랜치 전략 비교 장의 콘웨이 법칙식 관점. 브랜치를 팀 경계에 맞추라는 조언.

### 논문 29: Assessing the Value of Branches with What-if Analysis (Microsoft)
- 저자·연도: Christian Bird, Thomas Zimmermann (2012)
- 발표처: FSE 2012 (ACM SIGSOFT 20th), pp. 1-11
- DOI: 10.1145/2393596.2393648
- 피인용수: OA 115
- 원문 확인: 초록 기준
- 핵심 수치: 설문에서 가장 큰 문제로 꼽힌 것은 브랜치가 너무 많아 변경이 팀 사이를 오가는 데 오래 걸리는 것("branchmania")이었다. Windows에서 비용이 높고 이득이 낮은 브랜치를 없애면 변경당 지연이 8.9일 줄고 충돌은 평균 0.04건만 늘어난다고 추정했다.
- 인용할 만한 문장 (초록):
  > "By removing high-cost-low-benefit branches in Windows based on our what-if analysis, changes would each have saved 8.9 days of delay and only introduced 0.04 additional conflicts on average."
- 독자 전달 방식: 트렁크 기반 개발과 GitFlow 비교에서 "브랜치는 격리를 주는 대신 지연이라는 세금을 매긴다"는 틀의 근거.

### 논문 30: On the Nature of Merge Conflicts: A Study of 2,731 Open Source Java Projects Hosted by GitHub
- 저자·연도: Gleiph Ghiotto, Leonardo Murta, Márcio Barros, André van der Hoek (TSE 온라인 2018, 권호 2020)
- 발표처: IEEE Transactions on Software Engineering, pp. 892-915 (2020년 8월호)
- DOI: 10.1109/TSE.2018.2871083
- 피인용수: OA 68
- 원문 확인: 초록 기준
- 핵심 내용: 초록은 선행 연구를 인용해 "머지 시도의 10~20%가 충돌로 끝난다"고 쓴다. Java 프로젝트 2,731개의 충돌을 청크 수, 크기, 언어 구성요소, 해결 전략으로 특성화했다.
- 인용할 만한 문장 (초록):
  > "it has been reported that as much as 10 to 20 percent of all merge attempts result in a merge conflict"
- 주의: 10~20%는 이 논문이 선행 연구에서 가져온 수치다. 책에서는 "선행 연구에 따르면(Ghiotto et al. 재인용)"으로 쓴다.

### 논문 31: Software Practitioner Perspectives on Merge Conflicts and Resolutions
- 저자·연도: Shane McKee, Nicholas Nelson, Anita Sarma, Danny Dig (2017)
- 발표처: ICSME 2017, pp. 467-478
- DOI: 10.1109/ICSME.2017.53
- 피인용수: OA 53
- 원문 확인: 초록 기준
- 핵심 결과: 7개 조직의 실무자 10명을 인터뷰하고 162명 설문으로 검증했다. 실무자는 충돌 코드가 얼마나 복잡해 보이는지에 따라 해결 시점과 방법을 바꿨다.
- 보조 (seminal): Brun, Holmes, Ernst, Notkin, "Proactive detection of collaboration conflicts", ESEC/FSE 2011, pp. 168-178, DOI 10.1145/2025113.2025139 (OA 200). 충돌을 일찍 감지하자는 주장으로, 자주 통합해야 하는 근거다.

### 논문 32: Feature Toggles: Practitioner Practices and a Case Study
- 저자·연도: Md Tajmilur Rahman, Louis-Philippe Querel, Peter C. Rigby, Bram Adams (2016)
- 발표처: MSR 2016 (13th), pp. 201-211
- DOI: 10.1145/2901739.2901745
- 피인용수: OA 71
- 원문 확인: 초록 기준
- 핵심 결과: Google Chrome 릴리스 39개(5년)의 토글 사용을 분석했다. 토글은 빠른 릴리스와 장기 기능 개발을 함께 할 수 있게 하지만 기술 부채와 유지보수 부담을 만든다.
- 독자 전달 방식: 트렁크 기반 개발의 짝인 feature flag를 다룰 때 "flag도 부채"라는 균형 잡기.

### 논문 33: Why Google Stores Billions of Lines of Code in a Single Repository
- 저자·연도: Rachel Potvin, Josh Levenberg (2016)
- 발표처: Communications of the ACM, pp. 78-87
- DOI: 10.1145/2854146
- 피인용수: OA 157
- 원문 확인: 메타데이터만 확인 (본문 수치 미수집. 인용하려면 원문 대조 필요)
- 용도: 트렁크 기반 개발과 monorepo 사례의 1차 출처

### 논문 34 (최근, 프리프린트): AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates
- 저자·연도: George Xu, Arjun Subramanian, Nithilan Karthik (2026, arXiv)
- 발표처: arXiv:2607.04697 (동료 심사 미확인)
- 원문 확인: arXiv PDF(초록)
- 핵심 수치: AIDev-pop 데이터셋(PR 33,596건, 저장소 2,807개)을 썼다. 시간이 정확히 겹치는 기준으로 저장소의 40.2%에 동시에 열린 에이전트 PR 쌍이 있었다. 실제 3-way 머지를 재현했을 때 텍스트 충돌률은 다른 에이전트끼리 41.7%, 같은 에이전트끼리 19.8%였다.
- 독자 전달 방식: "AI 에이전트가 PR을 병렬로 쏟아 내는 시대에 Merge Queue와 짧은 브랜치가 더 중요해진다"는 최신 맥락. 심사 전 프리프린트라고 명시한다.

---

## F. Merge Queue / 항상 초록인 main

### 논문 35: Keeping Master Green at Scale (Uber SubmitQueue)
- 저자·연도: Sundaram Ananthanarayanan, Masoud Saeida Ardekani, Denis Haenikel, Balaji Varadarajan, Simon Soriano, Dhaval Patel, Ali-Reza Adl-Tabatabai (2019)
- 발표처: Proceedings of the Fourteenth EuroSys Conference 2019, Article pp. 1-15
- DOI: 10.1145/3302424.3303970
- 피인용수: CR 11 (Crossref가 적게 센다)
- 원문 확인: **논문 PDF 전문은 받지 못했다(ACM 403).** 저자 발표 슬라이드(sundaram.io/slides/eurosys19.pdf)와 The Morning Paper 요약(blog.acolyer.org, 2019-04-18)으로 확인했다. 아래에서 "슬라이드"는 저자 1차 자료, "TMP"는 2차 인용이다.
- 요약: monorepo에서 하루 수천 건의 변경이 들어와도 main이 항상 초록(모든 빌드 단계 통과)이도록 보장하는 시스템이다. 핵심은 세 가지다. 변경의 성공·충돌 확률을 예측해 가치 있는 빌드만 투기적으로(speculatively) 실행하는 speculation tree. 빌드 그래프로 서로 독립인 변경을 가려 병렬로 커밋하는 conflict analyzer. 빌드를 골라 실행하는 planner.
- 핵심 수치:
  - 동시에 들어온, 충돌 가능성 있는 변경 수가 늘면 충돌 확률이 5%에서 40%로 오른다 (슬라이드 p.10). TMP는 "16개 동시 변경에서 40%"로 인용
  - 단순 직렬 큐는 하루 수천 건 규모에서 확장되지 않는다 (슬라이드 p.17). TMP 인용: 하루 1,000건, 변경당 30분이면 마지막 변경의 대기 시간이 20일을 넘는다
  - 모든 경우를 투기 실행하면 변경 n개를 커밋하는 데 2^n개 빌드가 필요하다 (슬라이드 p.26)
  - 성공 예측은 로지스틱 회귀로 했고, 수작업으로 고른 특성 100개 이상을 썼다. 예측 정확도 97% (슬라이드 p.36)
  - 변경의 7.9%만 빌드 그래프를 바꾼다 (슬라이드 p.48)
  - 모두 투기 실행하는 방식은 Oracle보다 최대 15배 느리다. SubmitQueue의 P99 대기 시간은 극단적 경합에서도 4배 수준. conflict analyzer는 Oracle의 대기 시간을 최대 50% 줄인다 (슬라이드 p.52, 56, 57)
  - 도입 전 iOS main은 일주일 표본에서 52%의 시간만 초록이었다. 도입 후 1년 넘게 항상 초록 (TMP 인용. 원문 페이지 미확인)
- 인용할 만한 문장: 원문 PDF를 보지 못해 원문 인용은 없다. fact-checker는 위 TMP 수치를 원문과 대조하거나 "Uber 보고에 따르면"으로 완화해야 한다.
- 독자 전달 방식: GitHub Merge Queue가 푸는 문제("각 PR은 초록인데 합치면 빨간 main")의 학술 원형. 직렬 큐 → 배치 → 투기 실행으로 이어지는 진화를 그림으로 설명한다.
- 주의: GitHub Merge Queue의 구현 방식(임시 브랜치에 앞 PR을 누적해 테스트)은 SubmitQueue와 같지 않다. 개념의 계보로만 연결한다.

---

## G. GitHub Actions 실증 연구

### 논문 36: How Do Software Developers Use GitHub Actions to Automate Their Workflows?
- 저자·연도: Timothy Kinsman, Mairieli Wessel, Marco A. Gerosa, Christoph Treude (2021)
- 발표처: 2021 IEEE/ACM 18th International Conference on Mining Software Repositories (MSR), pp. 420-431
- DOI: 10.1109/MSR52588.2021.00054 (arXiv:2103.12224)
- 피인용수: CR 75
- 원문 확인: arXiv PDF 전문
- 핵심 수치: 저장소 416,266개 중 3,190개(0.7%)가 GitHub Actions를 도입했다(당시 기준). 사용된 Action 708개 가운데 42개(5.93%)만 verified였다. 도입 후 월간 거절 PR은 늘고, 머지된 PR의 커밋 수는 줄었다 (p.4, p.8).
- 인용할 만한 문장:
  > "After adopting GitHub Actions, on average, there are more rejected pull requests and fewer commits on merged pull requests." (p.8, Answer to RQ3)
- 주의: 0.7%는 Actions 출시 초기(2020년 무렵)의 수치다. 현재 채택률로 쓰면 안 된다.

### 논문 37: GitHub Actions: The Impact on the Pull Request Process (확장판)
- 저자·연도: Mairieli Wessel, Joseph Vargovich, Marco A. Gerosa, Christoph Treude (2023)
- 발표처: Empirical Software Engineering (2023)
- DOI: 10.1007/s10664-023-10369-w (arXiv:2206.14118)
- 피인용수: CR 34
- 원문 확인: arXiv PDF(초록)
- 핵심 수치: 가장 인기 있는 저장소 5,000개 중 1,489개(약 30%)가 Actions를 도입했다. 도입 후 PR 거절이 늘고, 승인된 PR은 대화가 늘고 커밋이 줄었다. 거절된 PR은 대화가 줄고 커밋이 늘었다. PR 승인까지의 시간은 늘었다.
- 독자 전달 방식: 자동화가 공짜가 아니라는 점. 검사가 엄격해지면 거절과 대기가 늘 수 있으니 필수 검사를 가려 설계하라는 교훈.

### 논문 38: On the Use of GitHub Actions in Software Development Repositories
- 저자·연도: Alexandre Decan, Tom Mens, Pooya Rostami Mazrae, Mehdi Golzadeh (2022)
- 발표처: 2022 IEEE International Conference on Software Maintenance and Evolution (ICSME), pp. 235-245
- DOI: 10.1109/ICSME55016.2022.00029
- 피인용수: OA 70 / CR 65
- 원문 확인: 초록 기준 (재현 패키지 Zenodo record 6634682)
- 핵심 수치: 저장소 약 68K개 중 43.9%가 Actions 워크플로를 사용했다. Action 재사용은 흔하지만 소수의 Action에 집중돼 있다. 보안과 버전 참조 방식 문제도 논의한다.
- 관련: Golzadeh, Decan, Mens, "On the rise and fall of CI services in GitHub", SANER 2022, pp. 662-672, DOI 10.1109/SANER53432.2022.00084. npm 패키지 저장소 91,810개를 9년간 추적했다. GitHub Actions는 18개월이 안 돼 지배적인 CI가 됐고 Travis는 줄었다.
- 관련: Decan, Mens, Onsori Delicheh, "On the outdatedness of workflows in the GitHub Actions ecosystem", Journal of Systems and Software, 2023, DOI 10.1016/j.jss.2023.111827 (초록 미수집, 수치 미확인)

### 논문 39: Resource Usage and Optimization Opportunities in Workflows of GitHub Actions (최근)
- 저자·연도: Islem Bouzenia, Michael Pradel (2024)
- 발표처: ICSE 2024 (IEEE/ACM 46th)
- DOI: 10.1145/3597503.3623303
- 피인용수: OA 24
- 원문 확인: 저자 공개 PDF(초록)
- 핵심 수치: 유료 저장소는 평균 연 $504의 비용이 든다. 자원의 91.2%가 테스트와 빌드에 쓰였다. 트리거별로는 PR 50.7%, push 30.9%, 스케줄 15.5%였다. 캐시를 쓴 유료 저장소는 32.9%에 그쳤다. 비활성 저장소의 스케줄 워크플로를 끄는 것만으로 실행 시간이 1.1~31.6% 줄 수 있다.
- 독자 전달 방식: 캐시, concurrency 취소, 경로 필터 같은 최적화 장의 동기.

### 논문 40: The Hidden Costs of Automation: An Empirical Study on GitHub Actions Workflow Maintenance
- 저자·연도: Pablo Valenzuela-Toledo, Alexandre Bergel, Timo Kehrer, Oscar Nierstrasz (2024)
- 발표처: SCAM 2024 (OpenAlex 기준, DOI 10.1109/SCAM63643.2024.00029. 학회명 전체 표기와 쪽 범위 미확인) / arXiv:2409.02366
- 원문 확인: arXiv PDF(초록)
- 핵심 결과: 10개 언어의 성숙한 프로젝트 약 200개에서 워크플로 파일의 진화를 분석했다. 버그 수정과 CI/CD 개선이 유지보수의 주요 동인이다. 워크플로도 유지보수해야 하는 코드라는 점("hidden costs of automation")을 보였다.

### 논문 41 (최근, 프리프린트): An Empirical Study of the Evolution of GitHub Actions Workflows
- 저자·연도: Pooya Rostami Mazrae, Alexandre Decan, Tom Mens, Mairieli Wessel (arXiv 2026)
- 발표처: arXiv:2602.14572 (SSRN 사전 공개 2025, DOI 10.2139/ssrn.5369484. 저널 게재 미확인)
- 원문 확인: arXiv PDF(초록)
- 핵심 수치: 저장소 49K개 이상, 워크플로 변경 이력 267K개 이상, 파일 버전 3.4M개 이상(2019-11~2025-08)을 분석했다. 저장소당 워크플로 파일의 중앙값은 3개다. 전체 워크플로 파일의 7.3%가 매주 바뀐다. 변경의 약 3/4은 단일 변경이다. LLM 코딩 도구가 워크플로 생성·유지보수 빈도에 영향을 줬다는 결정적 증거는 없었다.

### 논문 42: Developers' Perception of GitHub Actions: A Survey Analysis
- 저자·연도: Sk Golam Saroar, Maleknaz Nayebi (2023)
- 발표처: EASE 2023 (27th International Conference on Evaluation and Assessment in Software Engineering), pp. 121-130
- DOI: 10.1145/3593434.3593475 (arXiv:2303.04084)
- 피인용수: CR 27
- 원문 확인: arXiv PDF(초록)
- 핵심 수치: Action 개발자·사용자 90명을 설문했다. 60.87%가 YAML 작성이 어렵고 오류가 나기 쉽다고 답했다. 비슷한 Action 중에서는 verified 제작자와 별이 많은 쪽을 고른다. 논문 작성 시점 Marketplace의 Action은 16,730개.

---

## H. GitHub Actions 보안

### 논문 43: Characterizing the Security of GitHub CI Workflows
- 저자·연도: Igibek Koishybayev, Aleksandr Nahapetyan, Raima Zachariah, Siddharth Muralee, Bradley Reaves, Alexandros Kapravelos, Aravind Machiry (2022)
  - 저자 목록 출처: USENIX 공개 PDF 표지에서 확인 (Crossref 미등록, USENIX는 DOI를 발급하지 않음)
- 발표처: 31st USENIX Security Symposium (USENIX Security 2022), Boston. 쪽 범위 미확인
- DOI: 없음 (USENIX 오픈 액세스: usenix.org/system/files/sec22-koishybayev.pdf)
- 원문 확인: USENIX PDF 전문
- 핵심 수치 (p.1, 초록):
  - 저장소 213,854개의 워크플로 447,238개를 분석
  - 워크플로의 99.8%가 과도한 권한(저장소 read-write)을 가짐
  - 23.7%는 pull_request로 트리거되며 저장소 코드를 사용
  - 저장소의 99.7%가 외부 Action을 실행하고, 97%는 verified가 아닌 제작자의 Action을 하나 이상 실행. 18%는 보안 업데이트가 빠진 Action을 실행
  - pull_request_target 트리거: 저장소 7,485개(3.5%), 워크플로 8,874개(1.9%). 이 트리거는 설정된 모든 시크릿에 접근할 수 있다 (p.9, Table 4)
- 인용할 만한 문장:
  > "Our analysis shows that 99.8% of workflows are overprivileged and have read-write access (instead of read-only) to the repository." (p.1, Abstract)
- 독자 전달 방식: `permissions:` 최소화, Action을 SHA로 고정, pull_request_target 주의라는 보안 체크리스트의 정량 근거.

### 논문 44: ARGUS: A Framework for Staged Static Taint Analysis of GitHub Workflows and Actions
- 저자·연도: Siddharth Muralee, Igibek Koishybayev, Aleksandr Nahapetyan, Greg Tystahl, Brad Reaves, Antonio Bianchi, William Enck, Alexandros Kapravelos, Aravind Machiry (2023) — USENIX PDF 표지에서 확인
- 발표처: 32nd USENIX Security Symposium (USENIX Security 2023), Anaheim
- DOI: 없음 (usenix.org/system/files/usenixsecurity23-muralee.pdf)
- 원문 확인: USENIX PDF(초록)
- 핵심 수치: 워크플로 2,778,483개와 Action 31,725개를 분석해 워크플로 4,307개와 Action 80개에서 치명적인 코드 주입 취약점을 찾았다. 기존 패턴 기반 스캐너보다 발견율이 7배 이상 높았다.
- 인용할 만한 문장 (p.1, 초록):
  > "command injection vulnerabilities in the GitHub Actions ecosystem are not only pervasive but also require taint analysis to be detected."
- 독자 전달 방식: `${{ github.event.pull_request.title }}`를 run 스크립트에 바로 넣는 패턴이 왜 위험한지 설명한다(환경 변수로 넘기기).

### 논문 45: Automatic Security Assessment of GitHub Actions Workflows
- 저자·연도: Giacomo Benedetti, Luca Verderame, Alessio Merlo (2022)
- 발표처: SCORED '22 (2022 ACM Workshop on Software Supply Chain Offensive Research and Ecosystem Defenses), pp. 37-45
- DOI: 10.1145/3560835.3564554 (arXiv:2208.03837)
- 피인용수: CR 26
- 원문 확인: arXiv PDF(초록)
- 핵심 수치: 도구 GHAST로 오픈소스 프로젝트 50개를 분석해 보안 이슈 24,905건을 찾았다. 모두 해당 프로젝트에 보고했다.

---

## I. DORA / Accelerate

### 자료 46: Accelerate: The Science of Lean Software and DevOps (단행본)
- 저자·연도: Nicole Forsgren, Jez Humble, Gene Kim (2018)
- 발행처: IT Revolution Press. ISBN 9781942788331 (Open Library 조회)
- 원문 확인: 서지만 확인. 본문 수치(네 가지 핵심 지표, 엘리트 그룹 비교 배수 등)는 이 파일에서 확인하지 않았다. 네 지표의 정의와 최신 DORA 보고서 수치는 web 리서치(DORA 공식 보고서)에서 1차 출처로 가져와야 한다.
- 학술 선행: Nicole Forsgren, Jez Humble, "The Role of Continuous Delivery in IT and Organizational Performance", SSRN 2015, DOI 10.2139/ssrn.2681909 (OA 24, 초록 미수집)

---

## 책 장별 활용 매핑 (요약)

| 책 주제 | 핵심 근거 | 수치 한 줄 |
|---|---|---|
| 코드 리뷰의 목적 | Bacchelli & Bird 2013, Sadowski 2018, Mäntylä 2009, Beller 2014 | 결함 코멘트는 1/8(14%). 발견 결함의 75%는 진화성 결함 |
| 리뷰 속도·규모 기준점 | Sadowski 2018, Rigby & Bird 2013 | Google 중앙값 24줄, 4시간 미만, 리뷰어 1명 |
| PR 크기 논쟁 | Bosu 2015 대 Kudrjavets 2022, di Biase 2018 | 파일이 많을수록 유용한 코멘트 비율 하락 / 크기와 머지 시간은 무관 |
| 리뷰 지연 해소 | Kudrjavets 2022b, Maddila 2023, Shan 2022 | 자동 머지로 29~63% 단축 가능. Nudge로 해결 시간 -60% |
| PR 수락·거절 | Gousios 2014, Tsay 2014 | 거절의 13%만 기술적 이유, 27%는 동시 수정 |
| CI의 효과 | Vasilescu 2015, Hilton 2016, Bernardo 2018/2023 | 릴리스 2배 이상, PR 수락 1.6시간 빠름, 속도 이득은 절반의 프로젝트에만 |
| CI 설계 트레이드오프 | Hilton 2017 | Assurance / Security / Flexibility |
| Flaky test | Luo 2014, Memon 2017, Parry 2021/2022 | Async Wait 45%. Google 실패의 4.56%가 flaky |
| 브랜치 전략 | Bird & Zimmermann 2012, Shihab 2012, Rahman 2016 | 브랜치를 줄이면 변경당 8.9일 단축, 충돌은 +0.04 |
| 머지 충돌 | Ghiotto 2018(재인용 10~20%), McKee 2017, Xu 2026 | 에이전트 간 PR 충돌률 41.7% |
| Merge Queue | Ananthanarayanan 2019 | 동시 변경이 늘면 충돌 확률 5%에서 40%로 (슬라이드) |
| GitHub Actions 채택·영향 | Kinsman 2021, Wessel 2023, Decan 2022, Golzadeh 2022 | 68K 저장소의 43.9% 사용. 도입 후 거절 증가 |
| Actions 비용·유지보수 | Bouzenia 2024, Valenzuela-Toledo 2024, Rostami Mazrae 2026 | 유료 저장소 연 $504. 매주 워크플로 7.3%가 변경 |
| Actions 보안 | Koishybayev 2022, ARGUS 2023, Benedetti 2022 | 워크플로 99.8%가 과도한 권한 |

## 수집 한계

- **SubmitQueue(Uber) 논문 원문을 받지 못했다(ACM 403).** 수치는 저자 슬라이드와 The Morning Paper 2차 인용에 기댄다. 특히 "도입 전 main이 초록이던 시간 52%"는 원문과 대조해야 한다.
- **Merge Queue를 직접 다룬 동료 심사 논문은 SubmitQueue 말고 찾지 못했다.** GitHub/GitLab Merge Queue 동작과 Google TAP·Chromium CQ 같은 사례는 web 리서치(공식 문서·엔지니어링 블로그)가 채워야 한다.
- **DORA/Accelerate의 지표 수치는 확인하지 않았다.** 서지(ISBN)만 확인했다. 최신 DORA 보고서가 1차 출처다.
- 초록만 본 논문(Rigby & Bird 수치 원문, Zhao 2017, Shan 2022의 실험 결과, Eck 2019, Decan 2023 outdatedness, Potvin 2016)은 세부 수치를 인용하기 전에 원문 대조가 필요하다.
- Koishybayev 2022와 ARGUS 2023(USENIX)은 DOI가 없다. 대신 USENIX 오픈 액세스 URL을 적었다.
- 트렁크 기반 개발과 GitFlow를 직접 비교한 실증 논문은 찾지 못했다. 브랜칭 연구는 Microsoft(Windows) 사례가 중심이다.
- "리뷰 크기와 결함 발견률"의 고전 수치(예: 한 번에 200~400 LOC)는 SmartBear/Cisco 업계 보고라 학술 출처가 아니므로 여기에 넣지 않았다. 학술 근거는 Bosu 2015와 di Biase 2018 수준이다.
- 피인용수는 OpenAlex/Crossref 기준이며, Google Scholar 값보다 낮다.
