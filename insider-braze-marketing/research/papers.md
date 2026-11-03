# 논문 리서치: 고객 참여 플랫폼(Insider One·Braze)으로 하는 CRM 마케팅의 학술적 근거

- 검색 시점: 2026-11-03
- 장르: tech-book / 대상 독자: 주니어 마케터 (비학문 독자 → 증명·수식 생략, 결과·직관·수치 중심)
- 메타 확인 방법: 저자·연도·발표처·권호·쪽·DOI는 **Crossref API**로 조회해 일치 확인. 피인용수는 Crossref `is-referenced-by-count`(2026-11-03 조회, 이하 "Crossref 인용")이며 Google Scholar 수치보다 작게 나오는 것이 정상이다. 일부는 Semantic Scholar(S2) 수치도 병기.
- 수치 확인 방법: abstract 원문(S2 API로 받은 것)에서 직접 확인한 수치는 **[abstract 확인]**, 저자 소속 기관·학회 보도자료·2차 요약으로만 확인한 수치는 **[2차 출처 확인]**으로 표시. 둘 다 아니면 싣지 않거나 **미확인**으로 적었다.
- 인용문: abstract 원문을 직접 본 경우에만 영어 원문을 인용했다(쪽 번호는 abstract라 "Abstract"로 표기).
- 플랫폼 기능과의 연결: 각 항목 끝 "책에서의 쓰임"에 Insider One·Braze 기능(세그먼트, 캔버스/저니, 컨트롤 그룹, 지능형 발송 시간, 추천, 실험 등)과 연결 아이디어를 적었다. 기능명 자체는 이 문서의 검증 범위가 아니다(웹 리서치 쪽 소관).

---

## 주제 지도 (어느 챕터에 무엇을)

| 책의 개념 | 핵심 논문 | 한 줄 메시지 |
|---|---|---|
| 고객 여정·라이프사이클 | Lemon & Verhoef 2016 | 고객 경험은 구매 전·중·후 여러 접점의 총합이다 |
| RFM 세그먼트 | Fader, Hardie & Lee 2005 (JMR) | RFM 세 숫자만으로 미래 가치를 계산할 수 있다 |
| CLV | Gupta et al. 2006; Fader, Hardie & Lee 2005 (MkSc); Schmittlein et al. 1987 | "고객 한 명의 값"을 모델로 추정한다 |
| 리텐션의 경제성 | Rust, Lemon & Zeithaml 2004; (Reichheld & Sasser 1990, 주의 필요) | 리텐션 투자는 고객 자산 관점에서 평가한다 |
| 이탈 예측 | Neslin et al. 2006; Lemmens & Gupta 2020 | 모델의 정확도 차이가 곧 캠페인 수익 차이 |
| 업리프트·홀드아웃 | Ascarza 2018; Gutierrez & Gérardy 2017; Devriendt et al. 2018; Lewis & Rao 2015; Johnson et al. 2017; Gordon et al. 2023 | "이탈 위험 높은 사람"이 아니라 "메시지에 반응할 사람"을 겨냥하라. 효과는 컨트롤 그룹으로만 잰다 |
| A/B 테스트 함정 | Kohavi et al. 2009; Kohavi, Tang & Xu 2020; Fabijan et al. 2019; Johari et al. 2022; Kohavi, Deng & Vermeer 2022 | 엿보기(peeking), 표본비 불일치(SRM), 직관의 착각 |
| 발송 시간 최적화 | Singh et al. 2020 (arXiv); Bidargaddi et al. 2018 | 개인별 시간대 선택으로 오픈율이 오른다 — 단 효과 크기는 작다 |
| 푸시 알림 | Pielot et al. 2014; Sahami Shirazi et al. 2014; Mehrotra et al. 2016; Bidargaddi et al. 2018; Kim, Kim & Choi 2025 | 사용자는 하루 수십 개 알림을 받는다. 보내면 참여는 오르지만 피로·방해 비용이 있다 |
| 이메일 개인화·빈도 | Sahni et al. 2018; Wang, Lu & Shi 2022; Kumar, Zhang & Luo 2014 | 이름 하나로 오픈율이 오르기도, 재현이 안 되기도 한다. 메일 두 통도 수익을 깎을 수 있다 |
| 추천 시스템 | Linden et al. 2003; Gomez-Uribe & Hunt 2015; Jannach & Jugovac 2019 | 추천의 비즈니스 가치는 크지만, 측정은 생각보다 어렵다 |
| 밴딧 최적화 | Li et al. 2010; Scott 2015; Schwartz et al. 2017 | 실험하면서 동시에 이긴다 — 클릭이 아니라 전환을 최적화하라 |
| 옴니채널 | Verhoef, Kannan & Inman 2015; Neslin et al. 2006 (JSR); Kumar & Venkatesan 2005; Montaguti et al. 2016 | 멀티채널 고객이 더 가치 있다 — 캠페인으로 만들 수도 있다 |
| 프라이버시·동의 | Goldfarb & Tucker 2011; Aridor, Che & Salz 2023; Johnson, Shriver & Goldberg 2023; Utz et al. 2019 | 규제는 타기팅 효과를 줄이지만, 남는 고객은 더 "보이는" 고객이 된다. 동의 UI 설계가 동의율을 좌우한다 |

---

## A. 고객 라이프사이클·CRM의 이론적 바탕

### 논문 A1: Understanding Customer Experience Throughout the Customer Journey (서베이 성격)
- 저자·연도: Katherine N. Lemon, Peter C. Verhoef (2016)
- 발표처: Journal of Marketing, 80(6), 69–96
- DOI: 10.1509/jm.15.0420
- 피인용수: Crossref 4,961 (2026-11-03)
- 요약: 고객 경험(CX)을 구매 전(prepurchase)·구매(purchase)·구매 후(postpurchase) 단계에 걸친 여러 접점(touchpoint)의 총합으로 개념화한 리뷰 논문. 접점을 브랜드 소유·파트너 소유·고객 소유·사회적/외부 접점으로 나눈다. 마케팅 분야에서 "고객 여정" 용어를 학술적으로 정착시킨 대표 문헌.
- 방법론 요약: 문헌 리뷰 + 개념 프레임워크 제시 (실험·수치 없음).
- 핵심 수치·결과: 정량 결과 없음(개념 논문). 접점 4분류와 여정 3단계가 핵심.
- 독자 전달 방식 제안: Braze 캔버스/Insider One 저니 빌더를 "여정 3단계 위에 접점을 배치하는 도구"로 소개하는 도입부에 사용. "회사가 통제할 수 있는 접점(브랜드 소유)은 전체 경험의 일부일 뿐"이라는 겸손한 메시지.
- 비고: 본문 원문은 확인하지 못했고 위 분류는 널리 알려진 논문 구조에 기반한 요약이다. 본문에 분류명을 그대로 쓸 경우 fact-check 대상으로 둘 것.

### 논문 A2: Return on Marketing: Using Customer Equity to Focus Marketing Strategy
- 저자·연도: Roland T. Rust, Katherine N. Lemon, Valarie A. Zeithaml (2004)
- 발표처: Journal of Marketing, 68(1), 109–127
- DOI: 10.1509/jmkg.68.1.109.24030
- 피인용수: Crossref 1,515
- 요약: 고객 자산(customer equity = 모든 고객의 CLV 합)을 기준으로 마케팅 투자의 수익(ROI)을 비교하자는 프레임워크. 리텐션·획득·브랜드 투자를 같은 저울(고객 자산 변화)에 올린다.
- 핵심 수치·결과: 본 조사에서 abstract 수치는 확인하지 못함 → 수치 인용 금지, 개념만 사용.
- 독자 전달: "캠페인 성과를 오픈율이 아니라 고객 가치 변화로 보라"는 챕터의 이론적 근거.

### (주의 문헌) Zero Defections: Quality Comes to Services
- 저자·연도: Frederick F. Reichheld, W. Earl Sasser Jr. (1990)
- 발표처: Harvard Business Review, 1990년 9–10월호, pp.105–111 (권호 68(5)는 미확인)
- DOI: 없음(HBR 기사, Crossref에서 원문 레코드 미확인)
- 성격: 동료 심사 논문이 아닌 HBR 기사.
- 자주 인용되는 수치: "이탈을 5% 줄이면 이익이 25~85% 증가" [2차 출처 확인]. 기사 내 예시로 은행 지점 85%, 보험 중개 50%, 자동차 정비 체인 30% [2차 출처 확인].
- 주의: 실증 연구가 아니라 사례 기반 추정이며, Byron Sharp 등이 "사고 실험에 가깝고 리텐션 비용을 0으로 가정"했다고 비판 [2차 출처 확인]. **책에서 쓰려면 "업계에 널리 퍼진 주장이지만 근거는 약하다"는 반례 소재로 쓰는 편이 안전하다.** 업계 블로그의 "신규 획득 비용은 유지 비용의 5배" 같은 수치도 학술 출처를 찾지 못했다.

---

## B. RFM·CLV — 세그먼트를 숫자로 만드는 법

### 논문 B1: RFM and CLV: Using Iso-Value Curves for Customer Base Analysis (seminal)
- 저자·연도: Peter S. Fader, Bruce G. S. Hardie, Ka Lok Lee (2005)
- 발표처: Journal of Marketing Research, 42(4), 415–430
- DOI: 10.1509/jmkr.2005.42.4.415
- 피인용수: Crossref 480 / S2 642
- 요약: 실무에서 쓰던 RFM(최근성 Recency·빈도 Frequency·금액 Monetary)을 확률 모델과 연결해 고객별 CLV를 계산한다. "등가치 곡선(iso-value curve)"으로, 구매 이력은 달라도 미래 가치가 비슷한 고객들을 하나로 묶는다. 온라인 음악 판매 사이트 CDNOW 고객 데이터에 적용 [2차 출처 확인: 저자 abstract 요약].
- 방법론 요약: Pareto/NBD(구매 빈도·이탈) + 감마-감마(구매 금액) 모델을 결합, 입력은 RFM 세 값뿐.
- 독자 전달: "RFM 표의 칸마다 미래 가치가 다르다. 최근성이 낮은 VIP는 이미 떠났을 수 있다." 등고선 지도 비유(같은 높이 = 같은 가치). Insider One/Braze에서 RFM 세그먼트를 만들 때의 이론적 배경.

### 논문 B2: "Counting Your Customers" the Easy Way: An Alternative to the Pareto/NBD Model
- 저자·연도: Peter S. Fader, Bruce G. S. Hardie, Ka Lok Lee (2005)
- 발표처: Marketing Science, 24(2), 275–284
- DOI: 10.1287/mksc.1040.0098
- 피인용수: Crossref 368
- 요약: BG/NBD 모델. Pareto/NBD와 비슷한 예측력을 훨씬 쉬운 계산으로 얻는다. 오픈소스 CLV 라이브러리(예: Python `lifetimes`/PyMC-Marketing)가 이 모델을 구현한다 — 재현 가능성 높음(라이브러리 존재 여부는 웹 리서치에서 재확인 권장).
- 독자 전달: "구매가 멈춘 고객이 '쉬는 중'인지 '떠난 것'인지 확률로 말해 주는 모델."

### 논문 B3: Counting Your Customers: Who Are They and What Will They Do Next? (고전)
- 저자·연도: David C. Schmittlein, Donald G. Morrison, Richard Colombo (1987)
- 발표처: Management Science, 33(1), 1–24
- DOI: 10.1287/mnsc.33.1.1
- 피인용수: Crossref 512
- 요약: 비계약형(언제 떠났는지 알 수 없는) 고객 기반에서 "아직 살아 있는 고객"의 확률을 추정하는 Pareto/NBD 원논문. B1·B2의 뿌리.
- 독자 전달: 각주 수준으로 계보만 언급.

### 논문 B4: Modeling Customer Lifetime Value (서베이)
- 저자·연도: Sunil Gupta, Dominique Hanssens, Bruce Hardie, William Kahn, V. Kumar, Nathaniel Lin, Nalini Ravishanker, S. Sriram (2006)
- 발표처: Journal of Service Research, 9(2), 139–155
- DOI: 10.1177/1094670506293810
- 피인용수: Crossref 503 / S2 757
- 요약: CLV 모델링 접근(RFM 모델, 확률 모델, 경제계량 모델, 지속성 모델, 컴퓨터 과학/머신러닝 모델, 확산 모델)을 정리한 서베이. 이들 모델로 얻은 실증적 통찰을 리뷰하고 향후 연구 과제를 제시 [2차 출처 확인: SAGE PDF 소개문].
- 독자 전달: CLV 챕터의 "모델 지도". 주니어 마케터에게는 "CLV = (고객이 남아 있을 확률 × 한 번에 쓰는 돈 × 얼마나 자주)의 미래 합을 지금 가치로 할인한 것" 정도로 단순화.

---

## C. 이탈 예측과 리텐션 타기팅 — "누구에게 보낼 것인가"

### 논문 C1: Defection Detection: Measuring and Understanding the Predictive Accuracy of Customer Churn Models (seminal)
- 저자·연도: Scott A. Neslin, Sunil Gupta, Wagner Kamakura, Junxiang Lu, Charlotte H. Mason (2006)
- 발표처: Journal of Marketing Research, 43(2), 204–211
- DOI: 10.1509/jmkr.43.2.204
- 피인용수: Crossref 452 / S2 609
- 요약: 학계·실무자가 같은 학습 데이터로 이탈 모델을 만들고 테스트 데이터로 겨룬 "토너먼트" 연구. 방법론 선택이 예측 정확도에 미치는 영향을 분석.
- 핵심 수치·결과: 제출 모델 간 정확도 차이만으로 이탈 방지 캠페인 수익이 **수십만 달러** 달라질 수 있다 [2차 출처 확인]. 로짓 기반 모델이 판별분석·트리 기반보다 좋았다는 요약도 있음 [2차 출처 확인 — 원문 확인 전 단정 금지].
- 독자 전달: "Braze/Insider One의 예측 이탈 점수도 결국 모델이다. 모델 품질이 곧 돈이다."

### 논문 C2: Retention Futility: Targeting High-Risk Customers Might Be Ineffective (핵심 추천)
- 저자·연도: Eva Ascarza (2018)
- 발표처: Journal of Marketing Research, 55(1), 80–98
- DOI: 10.1509/jmr.16.0163
- 피인용수: Crossref 276 / S2 278. 2023년 AMA Weitz-Winer-O'Dell 상(5년 전 JMR 논문 중 장기 기여) 수상 [2차 출처 확인: AMA 보도자료]
- 요약: 이탈 위험이 가장 높은 고객이 리텐션 캠페인의 최선 타깃이 아닐 수 있다. 위험도(risk)가 아니라 **캠페인에 대한 민감도(반응 차이, 즉 업리프트)**로 타기팅해야 한다. 두 개의 필드 실험으로 입증.
- 핵심 수치·결과: 민감도 기준 타기팅이 이탈률을 **4.1~8.7%p** 줄였다(위험도 기준 대비) [2차 출처 확인: AMA·MSI 소개문].
- 독자 전달: 책의 "결정적 장면" 후보. "이탈 예측 점수 상위 10%에게 쿠폰을 보냈는데 효과가 없었다 — 왜?" 의사가 '가장 아픈 환자'가 아니라 '치료가 듣는 환자'를 고르는 것에 비유.

### 논문 C3: Managing Churn to Maximize Profits (최근)
- 저자·연도: Aurélie Lemmens, Sunil Gupta (2020)
- 발표처: Marketing Science, 39(5), 956–973
- DOI: 10.1287/mksc.2020.1229
- 피인용수: Crossref 120
- 요약: 이탈 확률 순, 반응도 순 타기팅 모두 "고객별로 캠페인 이익에 기여하는 정도가 다르다"는 점을 무시한다. 개입의 **기대 이익 증분(profit lift)** 순으로 고객을 정렬하고 캠페인 규모까지 정하는 방법을 제안, 두 개의 필드 실험에서 경쟁 모델보다 우수 [2차 출처 확인: 에라스뮈스대 연구 포털].
- 핵심 수치·결과: 보도 매체마다 수치가 다르다(최소 4% 이익 증가 / 단일 캠페인 2,800만 달러 / 이익 2배 이상 등) [2차 출처, 상호 불일치] → **책에서는 구체 수치 인용을 피하고 "이익 기준 타기팅이 더 낫다"는 방향만 쓸 것.** 저자는 "이 방법이 누가 이탈할지 예측하는 데는 오히려 오차가 더 크다"고 인정 [2차 출처 확인: HBS Working Knowledge].
- 독자 전달: C2 → C3로 이어지는 "위험도 → 반응도 → 이익" 3단 진화 서사.

---

## D. 업리프트 모델링과 홀드아웃(컨트롤) 그룹 — "보낸 덕분인가"

### 논문 D1: Causal Inference and Uplift Modelling: A Review of the Literature (서베이)
- 저자·연도: Pierre Gutierrez, Jean-Yves Gérardy (2017)
- 발표처: Proceedings of The 3rd International Conference on Predictive Applications and APIs, PMLR 67, 1–13
- URL: https://proceedings.mlr.press/v67/gutierrez17a.html (DOI 없음)
- 피인용수: 미확인(Crossref 미등록)
- 요약: 업리프트 모델링을 "행동(처치)이 고객 결과에 주는 증분 효과를 모델링하는 기법"으로 정의하고, 인과추론과 머신러닝 양쪽 관점에서 정리. 접근을 세 갈래로 분류 — ① 두 모델 방식(Two-Model: 처치군·대조군 각각 모델 후 차이), ② 클래스 변환(Class Transformation), ③ 업리프트 직접 모델링 [PMLR 페이지 abstract 확인].
- 독자 전달: 고객 4분류(설득 가능 Persuadables / 어차피 살 사람 Sure things / 어차피 안 살 사람 Lost causes / 건드리면 역효과 Sleeping dogs)로 설명 — 이 4분류는 업리프트 실무 문헌의 표준 설명이나 **이 논문에 그대로 나오는지는 미확인**이므로 "업계에서 흔히 쓰는 분류" 정도로 표기.

### 논문 D2: A Literature Survey and Experimental Evaluation of the State-of-the-Art in Uplift Modeling
- 저자·연도: Floris Devriendt, Darie Moldovan, Wouter Verbeke (2018)
- 발표처: Big Data, 6(1), 13–41
- DOI: 10.1089/big.2017.0104
- 피인용수: Crossref 98 / S2 135
- 요약: 업리프트 모델 서베이 + 여러 공개 데이터셋에서의 실험 비교. 제목 그대로 "처방적 분석(prescriptive analytics)으로 가는 디딤돌". 세부 수치는 원문 미확인.

### 논문 D3: Uplift Modeling: From Causal Inference to Personalization (최근, 튜토리얼)
- 저자·연도: 저자 미확인 (2023)
- 발표처: CIKM 2023 튜토리얼 (Proceedings of the 32nd ACM International Conference on Information and Knowledge Management)
- DOI: 10.1145/3583780.3615298 / arXiv: 2308.09066
- 피인용수: S2 19
- 요약: 업리프트 모델링은 개인·하위집단 수준의 처치 인과효과를 추정하는 머신러닝 기법 모음이며, 이커머스 개인화의 핵심 트렌드가 되었다. 특히 프로모션 캠페인에서 혜택과 비용을 저울질하는 데 유용 [abstract 확인].
- 인용할 만한 문장:
  > "Uplift modeling can be particularly useful for personalized promotional campaigns, where the potential benefit caused by a promotion needs to be weighed against the potential costs." (Abstract)
- 비고: 저자명 미확인 — 본문 인용 시 "CIKM 2023 튜토리얼(arXiv 2308.09066)"로만 표기하거나 fact-checker가 arXiv 페이지에서 확인.

### 논문 D4: The Unfavorable Economics of Measuring the Returns to Advertising (seminal)
- 저자·연도: Randall A. Lewis, Justin M. Rao (2015)
- 발표처: The Quarterly Journal of Economics, 130(4), 1941–1973
- DOI: 10.1093/qje/qjv023
- 피인용수: Crossref 263 / S2 308
- 요약: 미국 대형 소매업체·증권사와 진행한 **25개 대규모 필드 실험**(대부분 수백만 고객, 디지털 광고비 합계 280만 달러)을 분석. 무작위 실험을 해도 광고 수익률을 정밀하게 재기는 매우 어렵다 — 개별 고객 구매의 변동성이 광고 효과보다 훨씬 크기 때문 [2차 출처 확인: QJE abstract 인용 요약].
- 핵심 수치·결과: 유의미한 신뢰구간을 얻으려면 실험이 **1,000만 인-주(person-weeks)를 넘기기** 쉽다 [2차 출처 확인].
- 독자 전달: "컨트롤 그룹 5%로 캠페인 효과를 보려 했는데 결과가 '유의하지 않음'만 나온다"는 상황의 이론적 설명. 홀드아웃 그룹 크기 설계 챕터의 근거. 노이즈 낀 라디오에서 작은 목소리 듣기 비유.

### 논문 D5: Ghost Ads: Improving the Economics of Measuring Online Ad Effectiveness
- 저자·연도: Garrett A. Johnson, Randall A. Lewis, Elmar I. Nubbemeyer (2017)
- 발표처: Journal of Marketing Research, 54(6), 867–884
- DOI: 10.1509/jmr.15.0297
- 피인용수: Crossref 157. 2017 Paul E. Green 상, 2022 Weitz-Winer-O'Dell 상 수상 [2차 출처 확인: AMA]
- 요약: 대조군에 공익광고(PSA)를 보여주는 대신, "광고가 노출되었을 사람"을 기록만 하는 고스트 광고 방식으로 실험 비용·노이즈를 줄인다. 세부 수치 미확인.
- 독자 전달: CEP의 "컨트롤 그룹은 아무것도 받지 않는다, 하지만 '받을 뻔했던 순간'을 기록해 비교한다"는 설계 원리와 연결(Braze/Insider의 글로벌·캠페인 컨트롤 그룹 기능 설명 시).

### 논문 D6: Close Enough? A Large-Scale Exploration of Non-Experimental Approaches to Advertising Measurement (최근)
- 저자·연도: Brett R. Gordon, Robert Moakler, Florian Zettelmeyer (2023)
- 발표처: Marketing Science, 42(4), 768–793
- DOI: 10.1287/mksc.2022.1413 / arXiv: 2201.07055
- 피인용수: Crossref 80
- 요약: Facebook의 **663개 대규모 실험**(사용자·실험 수준 특징 5,000개 이상)을 기준으로, 비실험적 방법(이중/탈편향 머신러닝 DML, 층화 성향점수매칭 SPSM)이 실험 결과를 재현하는지 검증. DML이 SPSM보다 낫지만 **둘 다 잘 맞추지 못했다** [2차 출처 확인: arXiv abstract·Kellogg].
- 핵심 수치·결과: 리프트 추정의 절대 퍼센트포인트 차이 중앙값이 퍼널 상단 **115%**, 중단 **107%**, 하단 **62%** [2차 출처 확인: arXiv abstract 인용].
- 독자 전달: "컨트롤 그룹 없이 '보낸 사람 vs 안 보낸 사람'을 비교하면 왜 안 되는가"의 가장 강력한 최신 증거. 딥러닝을 써도 무작위 실험을 대체하지 못한다.

---

## E. A/B 테스트의 함정

### 논문 E1: Controlled Experiments on the Web: Survey and Practical Guide (서베이·seminal)
- 저자·연도: Ron Kohavi, Roger Longbotham, Dan Sommerfield, Randal M. Henne (2009)
- 발표처: Data Mining and Knowledge Discovery, 18(1), 140–181
- DOI: 10.1007/s10618-008-0114-1
- 피인용수: S2 826
- 요약: 온라인 통제 실험의 실무 가이드. 통계적 검정력·표본 크기·분산 감소, 실험 시스템 아키텍처, 무작위화·해싱(생각보다 단순하지 않음)을 다룬다. "가장 높은 연봉 받는 사람의 의견(HiPPO)이 아니라 고객의 목소리를 들으라"는 메시지로 유명 [abstract 확인].
- 인용할 만한 문장:
  > "Controlled experiments embody the best scientific design for establishing a causal relationship between changes and their influence on user-observable behavior." (Abstract)
  > "Our experience indicates that significant learning and return-on-investment (ROI) are seen when development teams listen to their customers, not to the Highest Paid Person's Opinion (HiPPO)." (Abstract)

### 논문 E2: Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing (단행본)
- 저자·연도: Ron Kohavi, Diane Tang, Ya Xu (2020)
- 발표처: Cambridge University Press
- DOI: 10.1017/9781108653985
- 피인용수: Crossref 276
- 요약: Microsoft·Google·LinkedIn 실험 플랫폼 책임자들의 표준 교과서. SRM, 가드레일 지표, 신선도 효과/초두 효과 등. 책 전체를 "A/B 테스트 더 읽을거리"로 추천하기 좋음.

### 논문 E3: Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners
- 저자·연도: Aleksander Fabijan, Jayant Gupchup, Somit Gupta, Jeff Omhover, Wen Qin, Lukas Vermeer, Pavel Dmitriev (2019)
- 발표처: KDD '19 (Proceedings of the 25th ACM SIGKDD), 2156–2164
- DOI: 10.1145/3292500.3330722
- 피인용수: Crossref 24 / S2 37
- 요약: 표본비 불일치(SRM) = 실험군·대조군에 배정된 비율이 기대와 다른 상황. 열이 여러 질병의 증상이듯 SRM은 다양한 데이터 품질 문제의 증상이다. 4개 회사·25개 이상 제품 경험으로 SRM 유형 분류와 예방 지침을 제시 [abstract 확인].
- 핵심 수치·결과: Microsoft 실험의 약 **6%**에서 SRM 발생 [2차 출처 확인: Microsoft Research ExP 블로그].
- 인용할 만한 문장:
  > "Just like fever is a symptom for multiple types of illness, an SRM is a symptom for a variety of data quality issues." (Abstract)
- 독자 전달: "50:50으로 나눴는데 이메일 수신자가 52:48이다 — 결과를 믿어도 되나?" 예: 발송 실패·하드 바운스·푸시 토큰 없는 사용자 제외가 한쪽에만 걸리면 SRM이 생긴다(이 예시는 저자 추론이 아닌 집필용 응용).

### 논문 E4: Always Valid Inference: Continuous Monitoring of A/B Tests (엿보기 문제)
- 저자·연도: Ramesh Johari, Pete Koomen, Leonid Pekelis, David Walsh (2022)
- 발표처: Operations Research, 70(3), 1806–1821
- DOI: 10.1287/opre.2021.2135
- 피인용수: Crossref 58 / S2 120
- 요약: A/B 테스트는 보통 고정 표본 p-값으로 분석하지만, 사용자가 결과를 계속 들여다보다(continuous monitoring) 좋아 보일 때 멈추면 그 추론은 "전혀 믿을 수 없게" 된다. 언제 멈춰도 유효한 p-값·신뢰구간(always valid)을 정의. 대형 상용 A/B 테스트 플랫폼에 구현되어 수십만 건 실험 분석에 쓰였다 [abstract 확인; abstract는 플랫폼명을 밝히지 않음].
- 인용할 만한 문장:
  > "these inferences are wholly unreliable if users endogenously choose samples sizes by continuously monitoring their tests." (Abstract)
- 독자 전달: "캠페인 대시보드를 매일 열어 보고 '이겼다' 싶을 때 끄면 안 되는 이유."

### 논문 E5: A/B Testing Intuition Busters: Common Misunderstandings in Online Controlled Experiments (최근)
- 저자·연도: Ron Kohavi, Alex Deng, Lukas Vermeer (2022)
- 발표처: KDD '22 (Proceedings of the 28th ACM SIGKDD), 3168–3177
- DOI: 10.1145/3534678.3539160
- 피인용수: Crossref 23 / S2 30
- 요약: A/B 도구 벤더·에이전시까지 퍼뜨리는 "직관적이지만 틀린" 개념들을 통계적으로 반박하고, 플랫폼 설계자가 실수를 어렵게 만드는 방법을 권고 [abstract 확인]. (본문에 p-값 오해, 위양성 위험, 너무 좋은 결과의 의심(Twyman's law) 등이 다뤄진다고 알려져 있으나 세부 항목은 **원문 미확인**.)

---

## F. 발송 시간 최적화(STO)와 푸시 알림

### 논문 F1: An RNN-Survival Model to Decide Email Send Times
- 저자·연도: Harvineet Singh, Moumita Sinha, Atanu R. Sinha, Sahil Garg, Neha Banerjee (2020)
- 발표처: arXiv 프리프린트 (arXiv: 2004.09900) — 동료 심사 학회 게재 여부 미확인
- 피인용수: 미확인
- 요약: 수신자별로 시간대(bin)마다 "열어볼 위험률(hazard)"을 RNN-생존분석 모델로 예측해 발송 시간을 순위화. 약 100만 고객·5개월 이메일 데이터.
- 핵심 수치·결과: 개인별 상위 10개 시간대에 보낸 메일의 오픈율 **19.24%** vs 무작위 10개 시간대 **16.48%**(상대 약 17% 향상) [2차 출처 확인: 검색 요약에 인용된 본문 문장]. 관찰 데이터 기반 평가이며 무작위 필드 실험은 아님.
- 독자 전달: Braze Intelligent Timing·Insider의 STO 기능의 원리 설명("각자 메일함 여는 습관 시간에 맞춰 보낸다"). 단, 학술적으로 **무작위 실험으로 검증된 STO 논문은 찾지 못했다** — 벤더 주장 수치는 웹 리서치에서 별도 확인하고 "벤더 발표 수치"로 표기할 것.

### 논문 F2: To Prompt or Not to Prompt? A Microrandomized Trial of Time-Varying Push Notifications to Increase Proximal Engagement With a Mobile Health App (핵심 추천)
- 저자·연도: Niranjan Bidargaddi, Daniel Almirall, Susan Murphy, Inbal Nahum-Shani, Michael Kovalcik, Timothy Pituch, Haitham Maaieh, Victor Strecher (2018)
- 발표처: JMIR mHealth and uHealth, 6(11), e10123
- DOI: 10.2196/10123
- 피인용수: Crossref 208 / S2 187
- 요약: 상용 직장 웰빙 앱 사용자 **1,255명**을 89일간 미세무작위시험(MRT) — 하루 6개 시각 중 하나에서 "보낸다/안 보낸다"를 매번 50:50으로 무작위화해 푸시의 인과 효과를 측정 [abstract 확인].
- 핵심 수치·결과 [모두 abstract 확인]:
  - 맞춤 메시지 푸시를 보내면 24시간 내 앱 참여 확률 **3.9% 증가**(위험비 1.039, 95% CI 1.01–1.08)
  - 주말 **8.7%** 증가 vs 주중 **2.5%** 증가(차이는 통계적으로 유의하지 않음, P=.18)
  - 효과가 가장 큰 시점은 주말 낮 12:30, **11.8%** 증가(90% CI)
  - 시간이 지나며 효과가 약해지는 경향이 있었으나 유의하지 않음(P=.84)
- 인용할 만한 문장:
  > "Users were estimated to be 3.9% more likely to engage with the app in the next 24 hours when a tailored health message was sent versus when it was not sent" (Abstract, Results)
- 독자 전달: 푸시의 "진짜 효과"는 생각보다 작다(수 % 수준) — 그래서 컨트롤 그룹 없이는 보이지 않는다. 동시에 "언제 보내느냐"에 따라 효과가 달라진다는 STO의 근거. 같은 사람에게 매번 동전을 던져 보낼지 정하는 실험 설계 자체가 좋은 교육 소재.

### 논문 F3: An In-Situ Study of Mobile Phone Notifications
- 저자·연도: Martin Pielot, Karen Church, Rodrigo de Oliveira (2014)
- 발표처: MobileHCI '14 (Proceedings of the 16th International Conference on Human-Computer Interaction with Mobile Devices & Services), 233–242
- DOI: 10.1145/2628363.2628364
- 피인용수: Crossref 298 / S2 388
- 요약: 15명의 1주일간 실제 알림 로그 + 일기 조사.
- 핵심 수치·결과: 참가자는 하루 평균 **63.5개** 알림을 처리, 대부분 메신저와 이메일 [2차 출처 확인: 논문 PDF 발췌 검색 결과]. 표본이 15명으로 작다는 점 명시 필요.
- 독자 전달: "당신의 마케팅 푸시는 하루 60여 개 알림 중 하나다."

### 논문 F4: Large-Scale Assessment of Mobile Notifications
- 저자·연도: Alireza Sahami Shirazi, Niels Henze, Tilman Dingler, Martin Pielot, Dominik Weber, Albrecht Schmidt (2014)
- 발표처: CHI '14 (Proceedings of the SIGCHI Conference on Human Factors in Computing Systems), 3055–3064
- DOI: 10.1145/2556288.2557189
- 피인용수: Crossref 276 / S2 374
- 요약: **4만 명 이상**에게서 **약 2억 건**의 알림을 수집한 최초의 대규모 분석, 사용자가 어떤 알림을 좋아하고 싫어하는지 분석 [2차 출처 확인: abstract 인용]. 세부 결과(앱 범주별 선호 등)는 원문 미확인.

### 논문 F5: My Phone and Me: Understanding People's Receptivity to Mobile Notifications
- 저자·연도: Abhinav Mehrotra, Veljko Pejovic, Jo Vermeulen, Robert Hendley, Mirco Musolesi (2016)
- 발표처: CHI '16, 1021–1032
- DOI: 10.1145/2858036.2858566
- 피인용수: Crossref 233 / S2 291
- 요약: 알림에 대한 반응 시간과 체감 방해도는 알림의 표현 방식, 알림 유형, 발신자-수신자 관계, 사용자가 하던 작업의 유형·진행도·복잡도에 따라 달라진다. **중요하거나 유용한 내용의 알림도 방해가 될 수 있다** [2차 출처 확인: UCL Discovery abstract].
- 규모: 사용자 20명, 알림 약 1만 건, 설문 응답 474건 [2차 출처, 추출 품질 낮음 → 미확인 취급 권장].
- 독자 전달: 푸시 피로·옵트아웃 챕터 — "좋은 내용이면 괜찮다"는 착각 반박.

### 논문 F6: Push the Paw: A Field Experiment on Personalised Push Notifications and User Engagement (최근)
- 저자·연도: Kim, Kim, Choi (2025) — 이름(given name) 미확인
- 발표처: Australasian Marketing Journal, 34(1), 76–85 (온라인 2025-07)
- DOI: 10.1177/14413582251356702 (SSRN 프리프린트 10.2139/ssrn.4993370)
- 피인용수: Crossref 4
- 요약: 반려동물 활동 모니터링 앱 회사가 직접 설계·실행한 필드 실험(보호자 **595명**). 개인화 푸시가 일반 푸시보다 참여가 유의하게 높았고, **보호자 이름 + 반려동물 이름**을 모두 넣은 알림이 반려동물 이름만 넣은 알림보다 참여가 높았다. 사용자의 참여 이력 데이터를 넣는 것도 효과가 있었으나 이름 개인화만 한 것보다 유의하게 더 크지는 않았다 [abstract 확인].
- 독자 전달: Liquid(Braze)·개인화 태그(Insider) 실습 예제의 근거로 좋음 — "이름 변수 두 개가 행동 이력보다 나을 수 있다." 단 표본이 작고 단일 앱이라는 한계 명시.

---

## G. 이메일 개인화·빈도·동의

### 논문 G1: Personalization in Email Marketing: The Role of Noninformative Advertising Content (seminal)
- 저자·연도: Navdeep S. Sahni, S. Christian Wheeler, Pradeep Chintagunta (2018)
- 발표처: Marketing Science, 37(2), 236–258
- DOI: 10.1287/mksc.2017.1066
- 피인용수: Crossref 216
- 요약: 정보 가치가 없는 개인화(제목줄에 수신자 이름 넣기)의 효과를 대규모 필드 실험으로 검증.
- 핵심 수치·결과 [2차 출처 확인: Chicago Booth Review, Stanford GSB 워킹페이퍼 abstract, 영국 FCA 리뷰]:
  - 제목줄에 이름 → 오픈 확률 약 **20%** 상대 증가(약 9.05% → 10.80%)
  - 주 실험의 세일즈 리드 **31%** 증가(워킹페이퍼 abstract)
  - 수신 거부 감소(구체 수치는 출처별로 표현이 달라 미확인)
- **반대 증거:** 2023년 Marketing Letters 34(4) 게재 연구(DOI 10.1007/s11002-023-09701-7, 제목·저자 미확인)가 이름 개인화 효과를 재현하지 못함 — 오픈율·클릭률 개선 없음 [2차 출처 확인: RePEc 요약].
- 독자 전달: "개인화는 효과가 있다/없다"가 아니라 "우리 고객에서 테스트해 보라"의 최고 사례. G1 + 반례 + F6를 묶어 "개인화 효과는 맥락 의존"으로.

### 논문 G2: Does Customer Email Engagement Improve Profitability? Evidence from a Field Experiment in Subscription Service Retailing (최근, 핵심 추천)
- 저자·연도: Wang, Lu, Shi (2022) — 이름(given name) 미확인
- 발표처: Manufacturing & Service Operations Management, 24(5), 2703–2721
- DOI: 10.1287/msom.2022.1122
- 피인용수: Crossref 19
- 요약: 미국 대형 세차 체인(구독형)의 필드 실험. 이메일 참여 캠페인이 리텐션과 서비스 이용량을 모두 늘렸지만, 늘어난 이용량은 곧 운영비 — 일부 고객군에서는 이익을 깎았다 [abstract 확인].
- 핵심 수치·결과 [abstract 확인]:
  - 보름 간격 이메일 2통(1개월) → 5개월 후 리텐션 가능성 **7.4% 증가**, 5개월간 이탈 오즈 **26.3% 감소**
  - 구독자 기간당 서비스 이용량 **7.0% 증가**
  - 효과는 시간이 지나며 감쇠, 두 번째 메일 이후 **피로** 신호
  - 중간 등급 저빈도 이용자·최상위 등급에는 이익 증가, 중간 등급 고빈도·기본 등급에는 이익 **감소** → 선택적 발송 권고
- 인용할 만한 문장:
  > "Our study highlights that email engagement is a double-edged sword" (Abstract, Managerial implications)
- 독자 전달: "참여가 늘면 무조건 좋다"를 깨는 사례. 세그먼트별 발송 전략·CLV 연결 챕터의 결론부.

### 논문 G3: Modeling Customer Opt-In and Opt-Out in a Permission-Based Marketing Context
- 저자·연도: V. Kumar, Xi Zhang, Anita Luo (2014)
- 발표처: Journal of Marketing Research, 51(4), 403–419
- DOI: 10.1509/jmr.13.0169
- 피인용수: Crossref 119
- 요약: 허락 기반(permission-based) 이메일 마케팅에서 옵트인·옵트아웃 시점을 모델링. 관련 학위논문 abstract에 따르면 ① 마케팅 강도(발송 빈도 등)가 옵트인·옵트아웃 시점에 영향을 주고 ② 고객 특성에 따라 옵트인·아웃 가능성이 다르며 ③ 기업은 옵트아웃 시점을 늦춰 이익을 높일 수 있다 [2차 출처 확인: 동일 저자군 GSU 학위논문 abstract — 논문 자체 abstract 미확인].
- 독자 전달: 빈도 캡(frequency capping) 기능의 학술 근거. 수치 인용은 피할 것.

---

## H. 추천 시스템과 개인화

### 논문 H1: Amazon.com Recommendations: Item-to-Item Collaborative Filtering (고전)
- 저자·연도: Greg Linden, Brent Smith, Jeremy York (2003)
- 발표처: IEEE Internet Computing, 7(1), 76–80
- DOI: 10.1109/MIC.2003.1167344
- 피인용수: Crossref 4,200
- 요약: "이 상품을 산 고객이 함께 산 상품" — 사용자 간 유사도 대신 상품 간 유사도를 오프라인에서 미리 계산해 대규모 실시간 추천을 가능하게 한 아이템 기반 협업 필터링. 수치 결과는 이번 조사에서 미확인.
- 독자 전달: Insider One·Braze 추천 블록(함께 본/함께 산 상품)의 원리를 한 문단으로 설명할 때.

### 논문 H2: The Netflix Recommender System: Algorithms, Business Value, and Innovation
- 저자·연도: Carlos A. Gomez-Uribe, Neil Hunt (2015)
- 발표처: ACM Transactions on Management Information Systems, 6(4), 1–19
- DOI: 10.1145/2843948
- 피인용수: Crossref 1,163
- 핵심 수치·결과 [2차 출처 확인 — 여러 매체가 본문 문장을 인용]:
  - 추천 시스템이 시청 시간의 **약 80%**에서 선택에 영향(나머지는 검색)
  - 홈페이지에서 시청 시간 **3시간 중 2시간**이 발견됨
  - 개인화·추천의 결합 효과로 연간 **10억 달러 이상** 절감(이탈 감소 기반 추정)
- 주의: 10억 달러는 회사 내부 추정이며 외부 검증 불가 — "넷플릭스가 스스로 추정한 값"으로 표기.

### 논문 H3: Measuring the Business Value of Recommender Systems (서베이·최근 쪽)
- 저자·연도: Dietmar Jannach, Michael Jugovac (2019)
- 발표처: ACM Transactions on Management Information Systems, 10(4), 1–23
- DOI: 10.1145/3370082 / arXiv: 1908.08328
- 피인용수: Crossref 225 / S2 256
- 요약: 실제 배포된 추천 시스템의 필드 테스트 문헌을 리뷰하고, 어떤 비즈니스 지표(클릭률, 전환, 매출, 참여 등)가 쓰였는지 정리. 학계의 오프라인 실험 정확도 개선이 실제 비즈니스 가치로 이어지는지는 불분명하다고 비판 [abstract 확인].
- 독자 전달: "추천 블록 넣었더니 CTR 올랐다 — 그게 매출 증분인가?"로 D 섹션(증분 측정)과 연결. 개별 사례 수치(예: 추천 기여 매출 비중)는 본문에 많으나 이번 조사에서 미추출 → 필요 시 arXiv 1908.08328 원문에서 뽑을 것.

---

## I. 멀티암드 밴딧 — 실험하면서 최적화하기

### 논문 I1: A Contextual-Bandit Approach to Personalized News Article Recommendation (seminal)
- 저자·연도: Lihong Li, Wei Chu, John Langford, Robert E. Schapire (2010)
- 발표처: WWW '10 (Proceedings of the 19th International Conference on World Wide Web), 661–670
- DOI: 10.1145/1772690.1772758 / arXiv: 1003.0146
- 피인용수: Crossref 1,621 / S2 3,649
- 요약: 개인화 뉴스 추천을 맥락 밴딧 문제로 모델링한 LinUCB 논문. 사용자·기사 맥락으로 기사를 고르면서 클릭 피드백으로 전략을 계속 조정한다. 무작위 트래픽 로그로 밴딧을 오프라인 평가하는 방법도 제안 [abstract 확인].
- 핵심 수치·결과: Yahoo! 프런트 페이지 데이터 **3,300만 건 이상** 이벤트에서, 맥락 없는 밴딧 대비 **클릭 12.5% 향상**. 데이터가 적을수록 이점이 더 커짐 [abstract 확인].
- 인용할 만한 문장:
  > "Results showed a 12.5% click lift compared to a standard context-free bandit algorithm, and the advantage becomes even greater when data gets more scarce." (Abstract)

### 논문 I2: Multi-Armed Bandit Experiments in the Online Service Economy
- 저자·연도: Steven L. Scott (2015)
- 발표처: Applied Stochastic Models in Business and Industry, 31(1), 37–45
- DOI: 10.1002/asmb.2104
- 피인용수: Crossref 63 / S2 108
- 요약: Google 애널리틱스 콘텐츠 실험에 쓰인 톰슨 샘플링 기반 밴딧 실험의 실무 해설(저자 소속 Google). 고전 A/B 테스트보다 빠르게 결론을 내고 실험 중 손실을 줄일 수 있다는 논지. 세부 수치는 원문 미확인.

### 논문 I3: Customer Acquisition via Display Advertising Using Multi-Armed Bandit Experiments (핵심 추천)
- 저자·연도: Eric M. Schwartz, Eric T. Bradlow, Peter S. Fader (2017)
- 발표처: Marketing Science, 36(4), 500–522
- DOI: 10.1287/mksc.2016.1023
- 피인용수: Crossref 232 / S2 326
- 요약: 대형 소매은행의 온라인 디스플레이 캠페인(광고 노출 **7억 5천만 회 이상**)에서 계층 모델 기반 밴딧 정책을 실제로 운영 [2차 출처 확인: INFORMS abstract 인용].
- 핵심 수치·결과 [2차 출처 확인]:
  - 2개월간 대조 정책 대비 고객 획득률 **8% 향상**, 추가 비용 없음
  - 전환 대신 **클릭률을 최적화했다면 고객 획득이 약 10% 감소**했을 것
- 독자 전달: Braze/Insider의 자동 승자 선택·다변량 최적화 기능 설명 + "최적화 목표 지표를 잘못 고르면(클릭) 진짜 목표(전환)가 나빠진다"는 교훈. 카지노 슬롯머신 비유는 고전적이지만 여전히 직관적.

---

## J. 옴니채널

### 논문 J1: From Multi-Channel Retailing to Omni-Channel Retailing: Introduction to the Special Issue (서베이 성격)
- 저자·연도: Peter C. Verhoef, P. K. Kannan, J. Jeffrey Inman (2015)
- 발표처: Journal of Retailing, 91(2), 174–181
- DOI: 10.1016/j.jretai.2015.02.005
- 피인용수: Crossref 2,371 / S2 2,631
- 요약: 멀티채널(채널을 따로 관리)에서 옴니채널(채널·접점을 통합 관리해 고객 경험과 성과를 최적화)로의 전환을 정의한 특집호 서문. 정의 문장은 본문 미확인 → 직접 인용 금지, 의역만.
- 독자 전달: "이메일팀, 앱푸시팀, 카카오톡 담당이 따로 노는 것 = 멀티채널, 한 고객 프로필 위에서 조율 = 옴니채널" — CEP 도입의 존재 이유.

### 논문 J2: Challenges and Opportunities in Multichannel Customer Management
- 저자·연도: Scott A. Neslin, Dhruv Grewal, Robert Leghorn, Venkatesh Shankar, Marije L. Teerling, Jacquelyn S. Thomas, Peter C. Verhoef (2006)
- 발표처: Journal of Service Research, 9(2), 95–112
- DOI: 10.1177/1094670506293559 (검색 결과의 SAGE URL로 확인, Crossref 조회는 미실시)
- 요약: 멀티채널 고객 관리를 "기업과 고객이 상호작용하는 채널의 설계·배치·조율·평가를 통해 고객 획득·유지·성장으로 고객 가치를 높이는 것"으로 정의하고 5대 과제를 제시 [2차 출처 확인].

### 논문 J3: Who Are the Multichannel Shoppers and How Do They Perform? Correlates of Multichannel Shopping Behavior
- 저자·연도: V. Kumar, Rajkumar Venkatesan (2005)
- 발표처: Journal of Interactive Marketing, 19(2), 44–62
- DOI: 10.1002/dir.20034
- 피인용수: Crossref 385 / S2 549
- 요약: 어떤 고객이 멀티채널 쇼퍼가 되는지, 그리고 그들이 매출·구매 빈도 등에서 더 나은지 분석한 대표 문헌. **구체 수치(예: 멀티채널 고객의 매출 배수)는 이번 조사에서 확인하지 못함** → 수치 인용 금지.

### 논문 J4: Can Marketing Campaigns Induce Multichannel Buying and More Profitable Customers? A Field Experiment (핵심 추천)
- 저자·연도: Elisa Montaguti, Scott A. Neslin, Sara Valentini (2016)
- 발표처: Marketing Science, 35(2), 201–217
- DOI: 10.1287/mksc.2015.0923
- 피인용수: Crossref 80
- 요약: 유럽(이탈리아) 멀티채널 도서 소매업체 고객 **3만 명 이상**을 대상으로 메시지·금전 인센티브를 달리한 4개 캠페인 필드 실험. 잘 설계된 캠페인은 멀티채널 고객 비율과 평균 고객 수익성을 모두 높였다. 성향점수매칭으로 자기선택을 통제해도 멀티채널 고객이 더 수익성이 높았다. 효과는 **비금전 인센티브** 캠페인에서 나왔고, 메커니즘은 고객 반발(reactance) 감소와 지각된 행동 통제감 증가로 해석 [2차 출처 확인: 볼로냐대 저장소 abstract, INFORMS 보도자료].
- 독자 전달: "쿠폰 없이도 채널 확장을 유도할 수 있다" — 앱 설치 유도 캠페인, 매장→앱 전환 캠페인 사례 챕터.

---

## K. 프라이버시·동의

### 논문 K1: Privacy Regulation and Online Advertising (seminal)
- 저자·연도: Avi Goldfarb, Catherine E. Tucker (2011)
- 발표처: Management Science, 57(1), 57–71
- DOI: 10.1287/mnsc.1100.1246
- 피인용수: Crossref 603
- 요약: EU e-Privacy Directive(2002/58/EC) 시행 전후, **9,596개** 디스플레이 광고 캠페인에 무작위 노출된 **330만 명** 설문 응답자를 3중 차분으로 분석. 시행 후 유럽의 광고는 구매 의향을 바꾸는 효과가 크게 떨어졌다. 일반 콘텐츠 사이트(뉴스 등)와 작고 비대화형인 광고에서 하락이 컸다 [2차 출처 확인].
- 핵심 수치·결과: 유럽의 광고 효과가 다른 지역 대비 평균 **약 65% 감소**(측정 지표는 클릭이 아니라 "설문으로 측정한 구매 의향") [2차 출처 확인: 텔레포니카·CEI 등 인용, 논문 본문 직접 확인은 못 함].
- 독자 전달: "개인 데이터 기반 타기팅이 막히면 광고는 덜 먹힌다" — 그래서 1st-party 데이터와 동의 기반 CRM이 중요해졌다는 서사의 출발점.

### 논문 K2: The Effect of Privacy Regulation on the Data Industry: Empirical Evidence from GDPR (최근)
- 저자·연도: Guy Aridor, Yeon-Koo Che, Tobias Salz (2023)
- 발표처: The RAND Journal of Economics, 54(4), 695–730 (NBER WP 26900, 2020)
- DOI: 10.1111/1756-2171.12455
- 피인용수: Crossref 71
- 요약: 온라인 여행 분야 데이터 중개업체 데이터로 GDPR의 옵트인 요구 효과를 분석. 프라이버시를 중시하는 소비자는 쿠키 삭제 같은 비효율적 방법 대신 명시적 옵트아웃으로 이동했다 [2차 출처 확인: Kellogg·TSE abstract].
- 핵심 수치·결과 [2차 출처 확인]:
  - 중개업체가 관찰하는 소비자 수 **12.5% 감소**
  - 남은 소비자는 더 오래 추적 가능(추적 가능성 약 **8%** 상승 — 한 2차 요약에만 나옴, 보수적으로 다룰 것)
  - 남은 소비자의 광고주에 대한 평균 가치가 올라, 옵트아웃으로 인한 손실 대부분을 상쇄
  - 머신러닝 예측 정확도는 유의하게 나빠지지 않음
- 독자 전달: "동의한 고객은 줄지만 더 선명해진다" — 동의 관리 챕터의 균형 잡힌 근거.

### 논문 K3: Privacy and Market Concentration: Intended and Unintended Consequences of the GDPR (최근)
- 저자·연도: Garrett A. Johnson, Scott K. Shriver, Samuel G. Goldberg (2023)
- 발표처: Management Science, 69(10), 5695–5721
- DOI: 10.1287/mnsc.2023.4709
- 피인용수: Crossref 172 / S2 136
- 요약·수치 [abstract 확인]: 2.7만 개 이상 상위 웹사이트의 웹 기술 벤더 사용 패널. GDPR 시행 다음 주, EU 거주자 대상 웹사이트의 벤더 사용 **15% 감소**, 웹사이트들이 상위 벤더를 남기면서 벤더 시장 집중도 **17% 증가**. 집중도 증가는 쿠키 등 개인정보를 쓰는 벤더와 Facebook·Google 소유 벤더에서 주로 발생. 총량 변화는 2018년 말 대부분 회복되었지만 광고 벤더 범주에서는 영향이 지속.
- 독자 전달: 규제가 오히려 대형 플랫폼 쏠림을 낳는 아이러니 — 부록/칼럼용.

### 논문 K4: (Un)informed Consent: Studying GDPR Consent Notices in the Field
- 저자·연도: Christine Utz, Martin Degeling, Sascha Fahl, Florian Schaub, Thorsten Holz (2019)
- 발표처: CCS '19 (ACM SIGSAC Conference on Computer and Communications Security), 973–990
- DOI: 10.1145/3319535.3354212 / arXiv: 1909.02638
- 피인용수: Crossref 348 / S2 483
- 요약·수치 [abstract 확인]: GDPR 이후 유럽 인기 웹사이트의 **60% 이상**이 쿠키 동의 배너를 띄운다. 독일 웹사이트 방문자 **8만 명 이상** 대상 3개 실험 — ① 화면 하단(왼쪽) 배너에 상호작용이 더 많고 ② 이진 선택(수락/거부)일 때가 범주·회사별 개별 허용 방식보다 추적 수락이 많으며 ③ 넛지(nudging)가 선택에 큰 영향을 준다. 사소해 보이는 구현 결정이 동의 상호작용을 크게 바꾼다.
- 인용할 만한 문장:
  > "Our experiments show that seemingly small implementation decisions can substantially impact whether and how people interact with consent notices." (Abstract)
- 독자 전달: 푸시 권한 요청(사전 프롬프트/소프트 옵트인)·마케팅 수신 동의 UI 설계 챕터의 근거. 단 이 연구는 쿠키 배너 대상이므로 "푸시 권한에도 같은 원리가 적용될 가능성"으로 조심스럽게 연결. 넛지는 다크 패턴·법적 리스크와 함께 다룰 것.

---

## 챕터별 활용 팁 (집필자용)

1. **가장 강한 "반전" 소재 3개:** Ascarza 2018(위험 높은 고객을 겨냥하면 헛수고), Gordon et al. 2023(딥러닝 관찰 분석도 실험을 못 따라감, 오차 중앙값 62~115%), Wang·Lu·Shi 2022(메일 2통이 리텐션은 올리고 이익은 깎음).
2. **"효과는 작다"는 현실 감각:** Bidargaddi 2018의 푸시 효과 +3.9%, Singh 2020의 STO 19.24% vs 16.48%, Lewis & Rao 2015의 "1,000만 인-주". 주니어 마케터의 기대치 조정에 유용.
3. **재현 실패도 가르치기:** Sahni 2018(이름 개인화 +20% 오픈) vs 2023 Marketing Letters 재현 실패.
4. **수치를 쓰면 안 되는 곳:** Reichheld & Sasser "5% → 25~85%", Lemmens & Gupta의 이익 증가 폭(출처별 불일치), Kumar & Venkatesan 멀티채널 배수, 넷플릭스 10억 달러(자체 추정).

---

## 수집 한계

- 다수 논문(JMR·Marketing Science·HBR 등)은 유료라 전문을 읽지 못했다. 수치는 Semantic Scholar abstract 원문 또는 저자 기관·학회 보도자료 등 2차 출처로 확인했고, 각 항목에 확인 등급을 표시했다. 2차 출처 등급 수치는 본문 사용 전 fact-checker가 원문(가능하면 SSRN/arXiv 프리프린트)과 대조하는 것을 권장.
- **발송 시간 최적화(STO)는 학술 근거가 얇다** — 무작위 필드 실험으로 개인별 STO를 검증한 동료 심사 논문을 찾지 못했다. arXiv 프리프린트 1편(관찰 평가)과 mHealth MRT 1편이 전부. 벤더(Braze·Insider) 수치는 웹 리서치에서 확인 필요.
- **이커머스 앱 마케팅 푸시(비헬스케어)의 대규모 무작위 실험 논문**도 찾지 못했다. F2는 헬스 앱, F6은 반려동물 앱(595명)이다.
- 한국 시장(카카오 알림톡·국내 개인정보보호법) 관련 학술 논문은 조사 범위에서 다루지 못했다.
- 일부 저자 이름(given name)·공저자 목록은 미확인으로 남겼다(D3, F6, G2, G1 반례 논문).
- 피인용수는 Crossref 기준으로 Google Scholar보다 크게 낮다. "피인용 수천 회" 같은 표현을 본문에 쓰려면 Google Scholar 수치를 따로 확인할 것.
