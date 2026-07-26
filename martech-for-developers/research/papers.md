# Martech 학술 근거 리서치

검색 수행일: **2026-07-25**
담당: paper-researcher / slug `martech-for-developers` / genre `tech-book`

## 이 문서를 읽는 법 (저술가·fact-checker용)

- 모든 인용의 **저자·연도·학회/저널·DOI·arXiv ID는 2026-07-25 세션에서 실제 조회한 API 응답 또는 페이지에서 복사**했다. 조회 경로는 Crossref API(`api.crossref.org`), arXiv API(`export.arxiv.org`), Semantic Scholar Graph API, 그리고 개별 랜딩 페이지(arxiv.org/abs, papers.nips.cc, research.google, rfc-editor.org)다.
- **확인 수준** 표기 규칙:
  - `초록 확인` — 논문 초록 전문을 실제로 읽었다. 직접 인용 가능.
  - `문서 확인` — 논문이 아닌 1차 문서(RFC 원문, 기업 기술 보고서 페이지, 공식 제품 문서, 저자 노트)를 직접 조회했다. 직접 인용 가능하되 **peer-reviewed 논문이 아니라는 점을 반드시 함께 표기**하라.
  - `메타데이터 확인` — Crossref/Semantic Scholar/arXiv의 권위 있는 서지 레코드(제목·저자·연도·발표처·DOI)를 확인했으나 **초록 본문은 못 봤다**. 주장 요약은 제목·분야 통념 수준으로만 쓰고, **구체 수치를 이 논문에 귀속시키지 마라**.
  - `확인 불가` — 서지조차 확정하지 못했다. 인용 금지.
- **직접 인용(> 블록)은 `초록 확인` 항목에서만** 넣었고, 원문 영어를 그대로 옮겼다.
- 페이지·권/호는 Crossref가 반환한 값만 적었다. 반환되지 않은 필드는 `-`로 남겼다.
- 마케팅 효과 연구는 재현성·해석 논쟁이 심하다. 결론이 갈리는 곳은 **「상충하는 연구 결과」 섹션에 병기**했고, 개별 항목에서 임의로 한쪽으로 결론내지 않았다.

---

# D. 마케팅 원리의 학술적 뿌리

## D-1. RFM 세그먼테이션

### D-1-1. Bult & Wansbeek (1995) — 다이렉트 메일 타깃 선택의 최적화

- **정확한 인용**: Jan Roelf Bult, Tom Wansbeek, "Optimal Selection for Direct Mail," *Marketing Science*, Vol. 14, No. 4, pp. 378–394, 1995. DOI: `10.1287/mksc.14.4.378`
- **출처**: [https://doi.org/10.1287/mksc.14.4.378 | 1995 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 다이렉트 메일에서 "누구에게 보낼 것인가"를 수익 기준으로 최적화하는 문제를 정식화한 초기 정전. RFM류 휴리스틱 선택 대신 응답 확률 모형에 기반한 선택 규칙을 제시한다.
- **개발자에게 중요한 이유**: RFM은 "이론"이 아니라 **다이렉트 마케팅 시대의 실무 휴리스틱**이고, 학계는 애초부터 그것을 최적화 문제로 대체하려 했다. RFM 세그먼트를 구현할 때 "최적이라서 쓰는 게 아니라 싸고 설명 가능해서 쓴다"는 걸 알고 써야 한다.
- **확인 수준**: `메타데이터 확인`

### D-1-2. Fader, Hardie & Lee (2005) — RFM과 CLV를 잇는 다리

- **정확한 인용**: Peter S. Fader, Bruce G.S. Hardie, Ka Lok Lee, "RFM and CLV: Using Iso-Value Curves for Customer Base Analysis," *Journal of Marketing Research*, Vol. 42, No. 4, pp. 415–430, 2005. DOI: `10.1509/jmkr.2005.42.4.415`
- **출처**: [https://doi.org/10.1509/jmkr.2005.42.4.415 | 2005 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: RFM의 세 축을 확률 모형(Pareto/NBD 계열 + 지출 모형)으로 재해석하면, 서로 다른 RFM 조합이 같은 CLV를 갖는 **등가치 곡선(iso-value curve)** 을 그릴 수 있다. 즉 RFM은 CLV의 거친 근사이며 확률 모형은 그 근사를 정밀화한다.
- **개발자에게 중요한 이유**: "RFM 스코어와 LTV 예측 중 뭘 써야 하나"는 실무에서 늘 나오는 질문이다. 두 지표의 관계를 명시적으로 연결한 정전이므로 "RFM은 CLV의 저차원 프록시"라는 서술의 근거가 된다.
- **확인 수준**: `메타데이터 확인`

> **RFM 기원에 대한 경고**: RFM 용어 자체가 1960~70년대 미국 다이렉트 마케팅 업계(카탈로그 소매)에서 나왔다는 서술이 널리 퍼져 있으나, **이번 세션에서 기원을 확정하는 1차 학술 문헌을 확인하지 못했다.** 책에서 "RFM은 19XX년 누가 만들었다"고 단정하지 마라.

---

## D-2. CLV / LTV 모델링

### D-2-1. Schmittlein, Morrison & Colombo (1987) — Pareto/NBD 원 논문 ⭐

- **정확한 인용**: David C. Schmittlein, Donald G. Morrison, Richard Colombo, "Counting Your Customers: Who-Are They and What Will They Do Next?," *Management Science*, Vol. 33, No. 1, pp. 1–24, 1987. DOI: `10.1287/mnsc.33.1.1`
- **출처**: [https://doi.org/10.1287/mnsc.33.1.1 | 1987 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: 687 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장**: 비계약형(non-contractual) 관계에서 고객은 "탈퇴 버튼"을 누르지 않는다 — 그냥 조용히 안 온다. 이 논문은 구매 빈도(NBD)와 잠재 생존 시간(Pareto)을 각각 확률분포로 모델링해, 거래 이력만으로 "이 고객이 아직 살아 있을 확률 P(alive)"과 미래 거래 기대값을 추정하는 틀을 세웠다.
- **개발자에게 중요한 이유**: 이커머스·앱에는 "해지"라는 이벤트가 없다. 그래서 이탈을 **관측 라벨이 아니라 잠재 변수**로 다뤄야 한다는 게 이 계열의 출발점이다. CDP에서 "휴면 고객" 플래그를 만들 때 무엇을 가정하는지 정확히 설명해준다.
- **확인 수준**: `메타데이터 확인`

### D-2-2. Fader, Hardie & Lee (2005) — BG/NBD

- **정확한 인용**: Peter S. Fader, Bruce G. S. Hardie, Ka Lok Lee, "'Counting Your Customers' the Easy Way: An Alternative to the Pareto/NBD Model," *Marketing Science*, Vol. 24, No. 2, pp. 275–284, 2005. DOI: `10.1287/mksc.1040.0098`
- **출처**: [https://doi.org/10.1287/mksc.1040.0098 | 2005 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: 501 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장**: Pareto/NBD는 추정이 수치적으로 까다롭다. BG/NBD는 "이탈은 **구매 직후에만** 일어날 수 있다"는 가정으로 바꿔 Beta-Geometric 프로세스를 쓴다. 스프레드시트로도 추정 가능할 만큼 단순해지면서 예측력은 비슷하다.
- **개발자에게 중요한 이유**: `lifetimes`·`PyMC-Marketing`의 `BetaGeoFitter`가 바로 이 모델이다. 라이브러리를 쓰기 전에 **"이탈은 구매 직후에만 발생한다"는 가정**을 알아야 한다 — 이 가정이 깨지는 도메인에서 결과가 이상해진다.
- **확인 수준**: `메타데이터 확인`

### D-2-3. Fader, Hardie & Shang (2010) — BG/BB (이산 시간)

- **정확한 인용**: Peter S. Fader, Bruce G. S. Hardie, Jen Shang, "Customer-Base Analysis in a Discrete-Time Noncontractual Setting," *Marketing Science*, Vol. 29, No. 6, pp. 1086–1108, 2010. DOI: `10.1287/mksc.1100.0580` (워킹페이퍼 SSRN `10.2139/ssrn.1373469`, 2009)
- **출처**: [https://doi.org/10.1287/mksc.1100.0580 | 2010 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 거래가 연속 시간이 아니라 **이산적 기회**(연 1회 기부, 시즌 구매 등)에서만 일어나는 상황을 위한 Beta-Geometric/Beta-Bernoulli 모델.
- **개발자에게 중요한 이유**: 데이터 그레인에 따라 **다른 모델을 골라야 한다**는 반례. 하나의 LTV 모델을 전 제품에 붙이려는 유혹을 깬다.
- **확인 수준**: `메타데이터 확인`

### D-2-4. Gupta et al. (2006) — CLV 모델링 서베이

- **정확한 인용**: Sunil Gupta, Dominique Hanssens, Bruce Hardie, William Kahn, V. Kumar, Nathaniel Lin, Nalini Ravishanker, S. Sriram, "Modeling Customer Lifetime Value," *Journal of Service Research*, Vol. 9, No. 2, pp. 139–155, 2006. DOI: `10.1177/1094670506293810`
- **출처**: [https://doi.org/10.1177/1094670506293810 | 2006 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: CLV 모델링 접근법(RFM, 확률 모형, 계량경제 모형, 지속시간 모형, ML, 확산 모형)을 한자리에서 비교하는 서베이. **CLV는 하나의 공식이 아니라 문제 설정에 따라 갈리는 모델 패밀리**임을 정리했다.
- **개발자에게 중요한 이유**: "LTV 계산식 알려줘"에 단일 답이 없는 이유를 권위 있게 설명한다.
- **확인 수준**: `메타데이터 확인`

### D-2-5. Braun & Schweidel (2011) — 이탈 원인이 여러 개일 때

- **정확한 인용**: Michael Braun, David A. Schweidel, "Modeling Customer Lifetimes with Multiple Causes of Churn," *Marketing Science*, Vol. 30, No. 5, pp. 881–902, 2011. DOI: `10.1287/mksc.1110.0665` (워킹페이퍼 SSRN `10.2139/ssrn.1671661`, 2010)
- **출처**: [https://doi.org/10.1287/mksc.1110.0665 | 2011 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 고객 이탈을 단일 사건이 아니라 **경쟁 위험(competing risks)** 으로 본다 — 자발적 해지, 비자발적 실패(결제 실패), 이사 등 원인이 다르면 대응도 달라야 한다.
- **개발자에게 중요한 이유**: `churn = 1` 이진 라벨로 뭉개는 관행의 한계. 결제 실패 이탈에 리텐션 캠페인을 쏘는 건 무의미하다 — 카드 갱신 플로우가 답이다.
- **확인 수준**: `메타데이터 확인`

### D-2-6. Gamma-Gamma 지출 모델 — **peer-review 논문이 아니다** ⭐

- **정확한 인용**: Bruce Hardie (Fader & Hardie), "The Gamma-Gamma Model of Monetary Value," **미간행 기술 노트(unpublished note)**, brucehardie.com Note #25, 최종 갱신 2013-02-25. Fader et al. (2005)을 원출처로 참조한다.
- **출처**: [https://www.brucehardie.com/notes/025/ | note 갱신 2013 | 검색 시점 2026-07-25] (페이지 직접 조회)
- **핵심 주장**: 거래당 지출액을 감마 분포로, 고객 간 지출 이질성을 다시 감마 분포로 모델링해 "이 고객의 평균 지출액"을 베이지안 축약(shrinkage) 추정한다. 거래 횟수 모델(BG/NBD)과 곱해 CLV를 만든다.
- **개발자에게 중요한 이유 (정직성 포인트)**: `lifetimes.GammaGammaFitter`가 구현하는 대상이 저널 논문이 아니라 **저자 개인 웹사이트의 PDF 노트**다. 마테크 스택의 "학술적 권위"가 어디쯤에서 끊기는지 보여주는 최고의 사례.
- **확인 수준**: `문서 확인` (노트 랜딩 페이지 직접 조회 — 저널 게재 논문이 아님을 확인)

### D-2-7. LTV/CAC 3:1 — **학술 근거 확인 불가, 업계 관행** ⭐

- 이번 세션에서 **3:1 비율을 지지하는 peer-reviewed 연구를 찾지 못했다.** 웹 검색 결과 이 규칙은 SaaS 투자자·운영자 커뮤니티(특히 David Skok 계열 SaaS 메트릭 글)에서 확산된 rule of thumb으로 반복 서술된다.
- **출처**: [https://www.wallstreetprep.com/knowledge/ltv-cac-ratio/ 등 업계 자료 | 검색 시점 2026-07-25]
- **책에서의 처리 권고**: "LTV:CAC 3:1은 **학술적으로 검증된 임계값이 아니라 VC/SaaS 업계의 경험칙**이다. 정당화 논리(생애가치의 1/3까지 획득에 써도 마진과 성장 여력이 남는다)는 있지만, 이 숫자가 최적이라는 실증 연구는 확인되지 않는다"고 명시하라. **이 구분 자체가 이 책의 차별점이다.**
- **확인 수준**: `학술 근거 확인 불가 (업계 관행)`

---

## D-3. 코호트·리텐션·생존 분석

- 이 축의 학술적 뿌리는 **D-2의 확률 모형 계열과 사실상 같다.** 비계약형에서는 Pareto/NBD·BG/NBD가 곧 생존 모형 역할을 하고(잠재 생존 시간), 계약형에서는 위험률(hazard) 모형이 직접 쓰인다.
- **경쟁 위험 확장**: Braun & Schweidel (2011) → D-2-5
- **이산-시간 코호트**: Fader, Hardie & Shang (2010) → D-2-3
- **확인 불가 항목**: "코호트 리텐션 커브가 멱법칙/로그 형태로 안정화된다"는 실무 서술이 흔한데, 이번 세션에서 이를 확립한 **정전 논문을 특정하지 못했다.** 책에서 이 주장을 쓰려면 fact-checker의 별도 검증이 필요하다.
- **확인 수준**: (개별 논문은 D-2 항목을 따름) / 리텐션 커브 형태 주장은 `확인 불가`

---

## D-4. 퍼널 / 저니 오케스트레이션

### D-4-1. Lemon & Verhoef (2016) — 고객 여정의 학술적 정의 ⭐

- **정확한 인용**: Katherine N. Lemon, Peter C. Verhoef, "Understanding Customer Experience Throughout the Customer Journey," *Journal of Marketing*, Vol. 80, No. 6, pp. 69–96, 2016. DOI: `10.1509/jm.15.0420`
- **출처**: [https://doi.org/10.1509/jm.15.0420 | 2016 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: **4,866** (Semantic Scholar, 2026-07-25 조회) — 이 축에서 압도적으로 인용된 프레임워크 논문
- **핵심 주장**: 고객 경험을 **구매 전 → 구매 → 구매 후**의 순환 여정으로 정의하고, 각 단계의 터치포인트를 브랜드 소유·파트너 소유·고객 소유·사회적/외부 소유의 네 유형으로 분류한다.
- **개발자에게 중요한 이유**: CEP의 "저니 빌더" UI가 왜 그런 모양인지의 학술적 대응물. 특히 **우리가 제어할 수 없는 터치포인트가 프레임워크에 이미 들어 있다**는 점이 어트리뷰션 한계와 직결된다.
- **확인 수준**: `메타데이터 확인`

### D-4-2. Anderl et al. (2016) — 그래프/마르코프 기반 저니 어트리뷰션

- **정확한 인용**: Eva Anderl, Ingo Becker, Florian von Wangenheim, Jan Hendrik Schumann, "Mapping the customer journey: Lessons learned from graph-based online attribution modeling," *International Journal of Research in Marketing*, Vol. 33, No. 3, pp. 457–474, 2016. DOI: `10.1016/j.ijresmar.2016.03.001` (워킹페이퍼 SSRN `10.2139/ssrn.2685167`)
- **출처**: [https://doi.org/10.1016/j.ijresmar.2016.03.001 | 2016 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 고객 여정을 **마르코프 그래프**(노드=채널 접점, 엣지=전이)로 표현하고, 채널을 "제거했을 때 전환 확률이 얼마나 떨어지는가"(removal effect)로 기여도를 배분하는 어트리뷰션을 제안·평가한다.
- **개발자에게 중요한 이유**: GA4·CDP의 "데이터 기반 어트리뷰션"이 말하는 마르코프 제거 효과의 학술 대응물. 개발자에게는 **어트리뷰션이 그래프 알고리즘 문제로 환원된다**는 게 직관적이다.
- **확인 수준**: `메타데이터 확인`

---

## D-5. 세그멘테이션 · 개인화 (효과와 역효과)

### D-5-1. Ansari & Mela (2003) — 이메일 콘텐츠 개인화의 초기 실증

- **정확한 인용**: Asim Ansari, Carl F. Mela, "E-Customization," *Journal of Marketing Research*, Vol. 40, No. 2, pp. 131–145, 2003. DOI: `10.1509/jmkr.40.2.131.19224`
- **출처**: [https://doi.org/10.1509/jmkr.40.2.131.19224 | 2003 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 이메일의 콘텐츠 구성·링크 배치를 개인별로 최적화하는 통계 프레임워크를 제시하고 커스터마이즈가 클릭 반응을 높인다는 실증을 낸다.
- **개발자에게 중요한 이유**: "개인화 콘텐츠 블록"이라는 마테크 기능의 학술적 조상. 단 **2003년 데이터**라는 시대적 한계를 함께 말해야 한다.
- **확인 수준**: `메타데이터 확인`

### D-5-2. Goldfarb & Tucker (2011) — 개인화 역효과의 대표 실증 ⭐

- **정확한 인용**: Avi Goldfarb, Catherine Tucker, "Online Display Advertising: Targeting and Obtrusiveness," *Marketing Science*, Vol. 30, No. 3, pp. 389–404, 2011. DOI: `10.1287/mksc.1100.0583`
- **출처**: [https://doi.org/10.1287/mksc.1100.0583 | 2011 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar 초록 전문)
- **피인용수**: 814 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장 (초록 기반)**: 대규모 필드 실험에서 (1) 광고를 웹사이트 콘텐츠에 **맞추는 것**과 (2) 광고를 **눈에 띄게 만드는 것**은 **각각 따로** 구매 의향을 높인다. 그러나 **둘을 결합하면 역효과**가 나서 하나만 한 광고보다 성과가 나빠진다. 저자들은 이 실패가 프라이버시 우려와 관련된다고 본다 — 소득 공개를 거부한 사람, 프라이버시가 민감한 카테고리에서 결합의 부정 효과가 가장 강했다.
- **인용할 만한 문장** (초록 원문):
  > "Ads that match both website content and are obtrusive do worse at increasing purchase intent than ads that do only one or the other. This failure appears to be related to privacy concerns: the negative effect of combining targeting with obtrusiveness is strongest for people who refuse to give their income and for categories where privacy matters most."
- **범위 한정 (반드시 함께 쓸 것)**: 종속변수는 **구매 의향(purchase intent)** 이지 실제 매출이 아니다. 매체는 **온라인 디스플레이 광고**다. "개인화는 역효과다"로 일반화하지 마라.
- **개발자에게 중요한 이유**: "개인화를 세게 할수록 성과가 좋아진다"는 선형 가정이 **실증적으로 깨진다**는, 가장 인용하기 좋은 근거.
- **확인 수준**: `초록 확인`

### D-5-3. White et al. (2007/2008) — 개인화 리액턴스

- **정확한 인용**: Tiffany Barnett White, Debra L. Zahay, Helge Thorbjørnsen, Sharon Shavitt, "Getting too personal: Reactance to highly personalized email solicitations," *Marketing Letters*, Vol. 19, pp. 39–50. DOI: `10.1007/s11002-007-9027-9`
  - **연도 주의**: Crossref는 issued 연도를 **2007**로 반환했고 권/페이지는 **Vol. 19, pp. 39–50**이다(해당 권은 통상 2008년으로 인용된다). 책에서는 `White et al. (2008), Marketing Letters 19: 39–50` 또는 `(2007/2008)`로 쓰고 단정 표기를 피하라.
- **출처**: [https://doi.org/10.1007/s11002-007-9027-9 | Crossref issued 2007 / Vol.19 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 과도하게 개인화된 이메일 권유는 **심리적 리액턴스(reactance)** 를 유발해 반응을 낮출 수 있다.
- **개발자에게 중요한 이유**: 왜 "어제 보신 그 상품, 아직 고민 중이시죠?" 같은 카피가 역효과를 내는지를 설명하는 학술 언어를 제공한다.
- **확인 수준**: `메타데이터 확인`

### D-5-4. Tucker (2013/2014) — 프라이버시 통제권과 개인화 광고 ⚠️ 서지 상충

- **정확한 인용**: Catherine E. Tucker, "Social Networks, Personalized Advertising, and Privacy Controls," *Journal of Marketing Research*. **Crossref에 상충하는 두 레코드가 존재한다**:
  - DOI `10.1509/jmr.10.0355` — issued 2013, **Vol. 51**, pp. 546–562
  - DOI `10.1177/002224371305000501` — issued 2013, **Vol. 50**, pp. 546–562
  - 널리 통용되는 인용은 *JMR* **51(5), 546–562 (2014)** 다. **인용 시 DOI `10.1509/jmr.10.0355`를 쓰고, 권/연도는 fact-checker가 출판사 페이지로 재확인할 것.**
- **출처**: [https://doi.org/10.1509/jmr.10.0355 | Crossref issued 2013 | 검색 시점 2026-07-25] (Crossref API). 워킹페이퍼 SSRN `10.2139/ssrn.1694319`.
- **핵심 주장**: 소셜 네트워크가 이용자에게 **프라이버시 통제권을 더 준 이후** 개인화 광고의 성과가 오히려 올라갔다는 자연 실험 계열 결과.
- **개발자에게 중요한 이유**: "동의·통제 UI는 마케팅 성과의 비용"이라는 가정에 대한 반례. 프라이버시 설계가 성과와 트레이드오프만은 아니라는 근거.
- **확인 수준**: `메타데이터 확인` + **서지 상충 플래그**

### D-5-5. Awad & Krishnan (2006) — 개인화-프라이버시 역설

- **정확한 인용**: Naveen Farag Awad, M. S. Krishnan, "The Personalization Privacy Paradox: An Empirical Evaluation of Information Transparency and the Willingness to be Profiled Online for Personalization," *MIS Quarterly*, Vol. 30, No. 1, pp. 13–28, 2006. DOI: `10.2307/25148715`
- **출처**: [https://doi.org/10.2307/25148715 | 2006 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 이용자는 개인화를 원한다고 말하면서도 프로파일링에는 동의하지 않는다 — 정보 투명성이 이 역설에 어떻게 작용하는지 실증한 IS 분야 정전.
- **개발자에게 중요한 이유**: CDP를 만들며 "동의를 받으면 되지 않나"라고 생각하는 개발자에게 **선언된 선호와 실제 행동이 어긋난다**는 걸 보여준다.
- **확인 수준**: `메타데이터 확인`

---

## D-6. 추천 시스템

### D-6-1. Linden, Smith & York (2003) — 아이템 기반 협업 필터링

- **정확한 인용**: G. Linden, B. Smith, J. York, "Amazon.com recommendations: item-to-item collaborative filtering," *IEEE Internet Computing*, Vol. 7, No. 1, pp. 76–80, 2003. DOI: `10.1109/mic.2003.1167344`
- **출처**: [https://doi.org/10.1109/mic.2003.1167344 | 2003 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 사용자 기반 CF는 사용자 수에 비례해 비싸진다. 아이템-아이템 유사도를 **오프라인에 미리 계산**해두면 온라인 추천은 조회 몇 번으로 끝난다.
- **개발자에게 중요한 이유**: **추천의 실전 제약은 정확도가 아니라 지연시간과 카탈로그 크기**임을 처음으로 명확히 보여준 산업 논문. 오프라인 사전계산 + 온라인 조회 패턴은 지금도 그대로다.
- **확인 수준**: `메타데이터 확인`

### D-6-2. Koren, Bell & Volinsky (2009) — 행렬 분해

- **정확한 인용**: Yehuda Koren, Robert Bell, Chris Volinsky, "Matrix Factorization Techniques for Recommender Systems," *Computer* (IEEE), Vol. 42, No. 8, pp. 30–37, 2009. DOI: `10.1109/mc.2009.263`
- **출처**: [https://doi.org/10.1109/mc.2009.263 | 2009 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: Netflix Prize에서 검증된 잠재 요인 모델을 실무자용으로 설명한다. 사용자·아이템을 같은 잠재 공간의 벡터로 놓고 내적으로 선호를 예측하며, 편향 항과 시간 변화를 다룬다.
- **개발자에게 중요한 이유**: **임베딩이 딥러닝 이전에 이미 추천의 표준이었다**는 걸 보여준다. 오늘날 벡터 DB에 유저·아이템 임베딩을 넣는 설계의 직계 조상.
- **확인 수준**: `메타데이터 확인`

### D-6-3. He et al. (2017) — Neural Collaborative Filtering

- **정확한 인용**: Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, Tat-Seng Chua, "Neural Collaborative Filtering," arXiv:**1708.05031** (v2), 최초 제출 2017-08-16.
- **출처**: [https://arxiv.org/abs/1708.05031 | 2017 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 행렬 분해의 내적을 신경망으로 대체해 사용자-아이템 상호작용의 비선형성을 학습한다.
- **개발자에게 중요한 이유**: "추천에 딥러닝"의 대표 레퍼런스. 단 **D-6-7·D-6-8의 반박과 반드시 함께** 소개해야 한다.
- **확인 수준**: `메타데이터 확인`

### D-6-4. Hidasi et al. (2015) — 세션 기반 추천 (GRU4Rec)

- **정확한 인용**: Balázs Hidasi, Alexandros Karatzoglou, Linas Baltrunas, Domonkos Tikk, "Session-based Recommendations with Recurrent Neural Networks," arXiv:**1511.06939** (v4), 최초 제출 2015-11-21. (arXiv 코멘트: "Camera ready version (17th February, 2016)")
- **출처**: [https://arxiv.org/abs/1511.06939 | 2015 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 로그인하지 않은 익명 세션처럼 **장기 사용자 프로필이 없는 상황**에서 세션 내 클릭 시퀀스를 RNN(GRU)으로 모델링해 다음 아이템을 예측한다.
- **개발자에게 중요한 이유**: 마테크에서 가장 흔한 현실 — **식별되지 않은 방문자** — 에 직접 대응한다. ID 그래프가 해결 못 하는 구간을 세션 모델이 메운다.
- **확인 수준**: `메타데이터 확인`

### D-6-5. Kang & McAuley (2018) — SASRec

- **정확한 인용**: Wang-Cheng Kang, Julian McAuley, "Self-Attentive Sequential Recommendation," arXiv:**1808.09781** (v1), 제출 2018-08-20. (arXiv 코멘트: "Accepted by ICDM'18 as a long paper")
- **출처**: [https://arxiv.org/abs/1808.09781 | 2018 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 시퀀스 추천에 단방향 셀프 어텐션을 적용해 RNN보다 긴 의존성을 병렬로 학습한다.
- **개발자에게 중요한 이유**: 트랜스포머가 NLP를 넘어 추천으로 넘어온 전환점. 오늘날 "행동 시퀀스 트랜스포머"의 기준선.
- **확인 수준**: `메타데이터 확인`

### D-6-6. Sun et al. (2019) — BERT4Rec

- **정확한 인용**: Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, Peng Jiang, "BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer," arXiv:**1904.06690** (v2), 제출 2019-04-14. (arXiv 코멘트: "To appear in CIKM 2019")
- **출처**: [https://arxiv.org/abs/1904.06690 | 2019 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 단방향 시퀀스 모델의 한계를 지적하고 BERT식 **마스크드 아이템 예측**으로 양방향 컨텍스트를 학습한다.
- **개발자에게 중요한 이유**: 개발자에게 가장 친숙한 모델(BERT)의 추천 버전이라 개념 전이가 쉽다.
- **확인 수준**: `메타데이터 확인`

### D-6-7. Ferrari Dacrema, Cremonesi & Jannach (2019) — "정말 진전이 있었나?" ⭐⭐

- **정확한 인용**: Maurizio Ferrari Dacrema, Paolo Cremonesi, Dietmar Jannach, "Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches," *Proceedings of the 13th ACM Conference on Recommender Systems (RecSys 2019)*. arXiv:**1907.06902** (v3), 제출 2019-07-16. DOI: `10.1145/3298689.3347058`
- **출처**: [https://arxiv.org/abs/1907.06902 | 2019 | 검색 시점 2026-07-25] (arXiv API + Semantic Scholar 초록 전문)
- **피인용수**: 686 (Semantic Scholar, 2026-07-25 조회)
- **핵심 수치 (초록 그대로)**: 최상위 학회에 발표된 **18개** 신경망 추천 알고리즘을 체계적으로 재현 시도했다. **합리적 노력으로 재현 가능한 것은 7개**뿐이었다. 그 7개 중 **6개는 최근접 이웃·그래프 기반 같은 단순 휴리스틱으로 자주 능가**당했다. 나머지 1개는 베이스라인을 확실히 이겼지만, 잘 튜닝된 비신경망 선형 랭킹 방법을 일관되게 이기지는 못했다.
- **인용할 만한 문장** (초록 원문):
  > "Specifically, we considered 18 algorithms that were presented at top-level research conferences in the last years. Only 7 of them could be reproduced with reasonable effort. For these methods, it however turned out that 6 of them can often be outperformed with comparably simple heuristic methods, e.g., based on nearest-neighbor or graph-based techniques."
- **재현성**: 코드 공개 — `https://github.com/MaurizioFD/RecSys2019_DeepLearning_Evaluation` (arXiv 코멘트에 명시)
- **개발자에게 중요한 이유**: 이 책에서 **가장 중요한 논문 중 하나**. "우리도 딥러닝 추천을 도입해야 하나?"에 대해 **잘 튜닝된 단순 베이스라인부터 세우라**는 답을 학술적 권위로 뒷받침한다.
- **확인 수준**: `초록 확인`

### D-6-8. Rendle et al. (2020) — NCF vs 행렬 분해 재검토

- **정확한 인용**: Steffen Rendle, Walid Krichene, Li Zhang, John Anderson, "Neural Collaborative Filtering vs. Matrix Factorization Revisited," arXiv:**2005.09683** (v2), 제출 2020-05-19.
- **출처**: [https://arxiv.org/abs/2005.09683 | 2020 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: NCF(D-6-3)의 "학습된 유사도가 내적을 이긴다"는 결론을, 제대로 튜닝한 내적 기반 행렬 분해와 다시 비교해 재검토한다.
- **개발자에게 중요한 이유**: D-6-7과 함께 **베이스라인 튜닝의 중요성**을 보여주는 구체 사례. 제1저자 Steffen Rendle은 Factorization Machines 창시자라 반박의 무게가 다르다.
- **확인 수준**: `메타데이터 확인` / 상충 처리는 「상충하는 연구 결과」 참조

### D-6-9. Covington, Adams & Sargin (2016) — YouTube 2단계 아키텍처

- **정확한 인용**: Paul Covington, Jay Adams, Emre Sargin, "Deep Neural Networks for YouTube Recommendations," *Proceedings of the 10th ACM Conference on Recommender Systems (RecSys 2016)*, pp. 191–198. DOI: `10.1145/2959100.2959190`
- **출처**: [https://doi.org/10.1145/2959100.2959190 | 2016 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 대규모 추천을 **후보 생성(candidate generation) → 랭킹(ranking)** 2단계로 나누는 산업 표준 아키텍처를 공개했다.
- **개발자에게 중요한 이유**: 마테크의 "실시간 추천 API"에서 왜 항상 리콜과 랭킹이 나뉘는지 — 지연시간 예산을 어떻게 배분하는지 — 의 원형.
- **확인 수준**: `메타데이터 확인`

### D-6-10. Wang et al. (2019) — 세션 기반 추천 서베이

- **정확한 인용**: Shoujin Wang, Longbing Cao, Yan Wang, Quan Z. Sheng, Mehmet Orgun, Defu Lian, "A Survey on Session-based Recommender Systems," arXiv:**1902.04864** (v3), 제출 2019-02-13. (arXiv 코멘트: "Accepted by ACM Computing Surveys. 39 pages, 163 references")
- **출처**: [https://arxiv.org/abs/1902.04864 | 2019 | 검색 시점 2026-07-25] (arXiv API)
- **개발자에게 중요한 이유**: 세션 기반 추천 전체를 조감하는 서베이 — 개별 논문 대신 이 서베이를 인용하면 안전하다.
- **확인 수준**: `메타데이터 확인`

---

## D-7. CTR / 전환 예측

### D-7-1. McMahan et al. (2013) — FTRL, "현장에서 본 광고 클릭 예측" ⭐

- **정확한 인용**: H. Brendan McMahan, Gary Holt, D. Sculley, Michael Young, Dietmar Ebner, Julian Grady, Lan Nie, Todd Phillips, Eugene Davydov, Daniel Golovin, Sharat Chikkerur, Dan Liu 외, "Ad click prediction: a view from the trenches," *Proceedings of the 19th ACM SIGKDD (KDD 2013)*, pp. 1222–1230. DOI: `10.1145/2487575.2488200`
- **출처**: [https://doi.org/10.1145/2487575.2488200 | 2013 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: Google 검색 광고 CTR 예측 시스템의 실전 교훈 — **FTRL-Proximal** 온라인 학습(희소 모델 유지 + 정확도), 메모리 절약, 확률 캘리브레이션, 실전 진단·시각화 방법론.
- **개발자에게 중요한 이유**: 딥러닝 이전에 **로지스틱 회귀 + FTRL이 수십억 피처 규모의 산업 표준**이었고, 지연시간·비용 제약이 심한 곳에서는 지금도 강력한 베이스라인이다.
- **확인 수준**: `메타데이터 확인`

### D-7-2. He et al. (2014) — GBDT 피처 + 로지스틱 회귀 (Facebook)

- **정확한 인용**: Xinran He, Junfeng Pan, Ou Jin, Tianbing Xu, Bo Liu, Tao Xu, Yanxin Shi, Antoine Atallah, Ralf Herbrich, Stuart Bowers, Joaquin Quiñonero Candela, "Practical Lessons from Predicting Clicks on Ads at Facebook," *Proceedings of the Eighth International Workshop on Data Mining for Online Advertising (ADKDD 2014)*, pp. 1–9. DOI: `10.1145/2648584.2648589`
- **출처**: [https://doi.org/10.1145/2648584.2648589 | 2014 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 부스티드 결정 트리로 피처를 변환한 뒤 선형 분류기에 넣는 하이브리드, 그리고 데이터 신선도(freshness)가 성능에 미치는 영향 등 실전 교훈.
- **개발자에게 중요한 이유**: **모델 아키텍처보다 피처와 데이터 신선도가 더 중요할 수 있다**는 산업계 메시지. 실시간 피처 파이프라인 투자에 대한 근거.
- **확인 수준**: `메타데이터 확인`

### D-7-3. Juan et al. (2016) — Field-aware Factorization Machines

- **정확한 인용**: Yuchin Juan, Yong Zhuang, Wei-Sheng Chin, Chih-Jen Lin, "Field-aware Factorization Machines for CTR Prediction," *Proceedings of the 10th ACM Conference on Recommender Systems (RecSys 2016)*, pp. 43–50. DOI: `10.1145/2959100.2959134`
- **출처**: [https://doi.org/10.1145/2959100.2959134 | 2016 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 피처를 "필드"(광고주, 디바이스, 시간대 등)로 묶고 필드 조합마다 별도 잠재 벡터를 두어 상호작용을 학습한다. Kaggle CTR 대회 우승 계열.
- **개발자에게 중요한 이유**: 마테크 데이터는 대부분 **고차원 범주형 희소 피처**다. "왜 원핫 + 선형 모델로는 부족한가"를 설명하는 다리.
- **확인 수준**: `메타데이터 확인`

### D-7-4. Cheng et al. (2016) — Wide & Deep ⭐

- **정확한 인용**: Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishi Aradhye, Glen Anderson, Greg Corrado, Wei Chai, Mustafa Ispir, Rohan Anil, Zakaria Haque, Lichan Hong, Vihan Jain, Xiaobing Liu, Hemal Shah, "Wide & Deep Learning for Recommender Systems," arXiv:**1606.07792** (v1), 제출 2016-06-24.
- **출처**: [https://arxiv.org/abs/1606.07792 | 2016 | 검색 시점 2026-07-25] (arXiv API + arXiv abs 페이지 초록 전문)
- **핵심 주장**: **암기(memorization)** 는 교차 피처를 쓰는 wide 선형 모델이 잘하고, **일반화(generalization)** 는 임베딩을 쓰는 deep 신경망이 잘한다. 둘을 **공동 학습**하면 장점을 합칠 수 있다. Google Play(10억+ 활성 사용자, 100만+ 앱)에 실제 배포해 온라인 실험에서 wide-only·deep-only 대비 앱 획득이 유의하게 증가했다.
- **인용할 만한 문장** (초록 원문):
  > "We productionized and evaluated the system on Google Play, a commercial mobile app store with over one billion active users and over one million apps. Online experiment results show that Wide & Deep significantly increased app acquisitions compared with wide-only and deep-only models."
- **수치 주의**: 초록은 "significantly increased"라고만 하고 **구체적 증가율(%)은 초록에 없다.** 본문 표 수치를 인용하려면 fact-checker가 PDF로 직접 확인해야 한다. 초록만 근거로 "X% 상승"이라고 쓰지 마라.
- **개발자에게 중요한 이유**: 마테크 문맥에서 "규칙 기반 세그먼트(암기)"와 "ML 모델(일반화)"이 **대립이 아니라 결합 대상**이라는 설계 은유를 준다.
- **확인 수준**: `초록 확인`

### D-7-5. Guo et al. (2017) — DeepFM

- **정확한 인용**: Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, Xiuqiang He, "DeepFM: A Factorization-Machine based Neural Network for CTR Prediction," arXiv:**1703.04247** (v1), 제출 2017-03-13.
- **출처**: [https://arxiv.org/abs/1703.04247 | 2017 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: Wide & Deep의 wide 부분에 필요한 **수작업 피처 엔지니어링을 FM으로 대체**해 저차·고차 상호작용을 end-to-end로 학습한다.
- **개발자에게 중요한 이유**: "피처 크로스를 사람이 손으로 정의해야 하는가"라는 실무 부담에 대한 직접적 답 — 마테크팀 인력 구조와 직결된다.
- **확인 수준**: `메타데이터 확인`

### D-7-6. Zhou et al. (2017) — Deep Interest Network (DIN)

- **정확한 인용**: Guorui Zhou, Chengru Song, Xiaoqiang Zhu, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li, Kun Gai, "Deep Interest Network for Click-Through Rate Prediction," arXiv:**1706.06978** (v4), 최초 제출 2017-06-21.
- **출처**: [https://arxiv.org/abs/1706.06978 | 2017 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 사용자의 과거 행동 전체를 고정 벡터로 뭉개지 말고, **지금 보여줄 후보 광고에 따라 관련 행동에만 어텐션**을 준다(로컬 활성화).
- **개발자에게 중요한 이유**: "사용자 프로필을 하나의 임베딩으로 만든다"는 CDP식 발상의 한계를 정확히 짚는다. 같은 사용자라도 **맥락에 따라 다른 프로필이 필요하다.**
- **확인 수준**: `메타데이터 확인`

### D-7-7. Zhou et al. (2018) — DIEN

- **정확한 인용**: Guorui Zhou, Na Mou, Ying Fan, Qi Pi, Weijie Bian, Chang Zhou, Xiaoqiang Zhu, Kun Gai, "Deep Interest Evolution Network for Click-Through Rate Prediction," arXiv:**1809.03672** (v5), 최초 제출 2018-09-11. (arXiv 코멘트: "9 pages. Accepted by AAAI 2019")
- **출처**: [https://arxiv.org/abs/1809.03672 | 2018 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: DIN을 확장해 **관심사가 시간에 따라 변화(evolve)** 하는 과정을 명시적으로 모델링한다.
- **개발자에게 중요한 이유**: "최근 30일 행동" 같은 고정 윈도우 피처의 한계를 보여준다.
- **확인 수준**: `메타데이터 확인`

---

## D-8. A/B 테스트와 온라인 실험

### D-8-1. Kohavi et al. (2009) — 웹 통제 실험 서베이 겸 실무 가이드 ⭐

- **정확한 인용**: Ron Kohavi, Roger Longbotham, Dan Sommerfield, Randal M. Henne, "Controlled experiments on the web: survey and practical guide," *Data Mining and Knowledge Discovery*, Vol. 18, pp. 140–181. DOI: `10.1007/s10618-008-0114-1` (Crossref issued 2008; 통상 `(2009), DMKD 18: 140–181`로 인용)
- **선행 학회 버전**: Ron Kohavi, Randal M. Henne, Dan Sommerfield, "Practical guide to controlled experiments on the web," *KDD 2007*, pp. 959–967. DOI: `10.1145/1281192.1281295`
- **출처**: [https://doi.org/10.1007/s10618-008-0114-1 | Crossref issued 2008 / Vol.18 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 웹 A/B 테스트의 통계적 기초(가설 검정, 검정력, 표본 크기), 흔한 함정(SRM, 계측 오류, Simpson's paradox), 조직적 운영 원칙을 한 문서에 정리한 실무 정전.
- **개발자에게 중요한 이유**: 마테크 툴의 "실험" 탭이 무엇을 계산하는지, 왜 결과를 믿으면 안 되는 경우가 많은지의 표준 레퍼런스. **이 축의 첫 인용은 이 논문으로 하라.**
- **확인 수준**: `메타데이터 확인`

### D-8-2. Kohavi et al. (2013) — 대규모 온라인 통제 실험

- **정확한 인용**: Ron Kohavi, Alex Deng, Brian Frasca, Toby Walker, Ya Xu, Nils Pohlmann, "Online controlled experiments at large scale," *Proceedings of the 19th ACM SIGKDD (KDD 2013)*, pp. 1168–1176. DOI: `10.1145/2487575.2488217`
- **출처**: [https://doi.org/10.1145/2487575.2488217 | 2013 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: 실험을 **플랫폼으로** 운영할 때의 아키텍처·거버넌스 이슈(동시 실험, 실험 간 간섭, 자동 알림). 사내 실험 플랫폼 설계의 근거.
- **확인 수준**: `메타데이터 확인`

### D-8-3. Kohavi et al. (2012) — 신뢰할 수 있는 온라인 통제 실험

- **정확한 인용**: Ron Kohavi, Alex Deng, Brian Frasca, Roger Longbotham, Toby Walker, Ya Xu, "Trustworthy online controlled experiments," *Proceedings of the 18th ACM SIGKDD (KDD 2012)*, pp. 786–794. DOI: `10.1145/2339530.2339653`
- **출처**: [https://doi.org/10.1145/2339530.2339653 | 2012 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: 실험 결과가 **틀리는 방식**을 카탈로그화한 논문. "숫자가 나왔으니 맞겠지"를 깨는 데 쓴다.
- **확인 수준**: `메타데이터 확인`

### D-8-4. Deng et al. (2013) — CUPED (분산 축소)

- **정확한 인용**: Alex Deng, Ya Xu, Ron Kohavi, Toby Walker, "Improving the sensitivity of online controlled experiments by utilizing pre-experiment data," *Proceedings of the 6th ACM WSDM (WSDM 2013)*, pp. 123–132. DOI: `10.1145/2433396.2433413`
- **출처**: [https://doi.org/10.1145/2433396.2433413 | 2013 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 실험 **이전** 기간의 지표를 공변량으로 써서 분산을 줄이면 같은 트래픽으로 더 작은 효과를 검출할 수 있다.
- **개발자에게 중요한 이유**: "표본이 부족해서 실험을 못 한다"는 제약에 대한 구체적 해법. 캠페인 대상 수가 원래 적은 마테크 실험에서 특히 중요하다.
- **확인 수준**: `메타데이터 확인`

### D-8-5. Johari et al. (2017/2022) — 피킹(peeking) 문제와 항상 유효한 추론 ⭐

- **정확한 인용 (학회)**: Ramesh Johari, Pete Koomen, Leonid Pekelis, David Walsh, "Peeking at A/B Tests," *Proceedings of the 23rd ACM SIGKDD (KDD 2017)*, pp. 1517–1525. DOI: `10.1145/3097983.3097992`
- **정확한 인용 (저널 확장판)**: 동일 저자, "Always Valid Inference: Continuous Monitoring of A/B Tests," *Operations Research*, Vol. 70, No. 3, pp. 1806–1821, 2022. DOI: `10.1287/opre.2021.2135`
- **출처**: [https://doi.org/10.1145/3097983.3097992 | 2017], [https://doi.org/10.1287/opre.2021.2135 | 2022] | 검색 시점 2026-07-25 (Crossref API)
- **핵심 주장**: 고정 표본 크기를 전제한 p-값을 **실험 진행 중 반복해서 들여다보고 유의해지면 멈추는** 관행은 1종 오류율을 크게 부풀린다. 저자들은 **언제 멈춰도 유효한(always valid)** 순차적 p-값·신뢰구간을 제시한다.
- **개발자에게 중요한 이유**: 마테크 대시보드는 **실시간으로 유의성을 보여준다.** 그 UI가 조장하는 행동이 바로 피킹이다. 실험 플랫폼을 만든다면 순차 검정을 기본값으로 삼으라는 근거.
- **확인 수준**: `메타데이터 확인`

### D-8-6. Benjamini & Hochberg (1995) — 다중 검정 보정 (FDR)

- **정확한 인용**: Yoav Benjamini, Yosef Hochberg, "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing," *Journal of the Royal Statistical Society, Series B (Statistical Methodology)*, Vol. 57, No. 1, pp. 289–300, 1995. DOI: `10.1111/j.2517-6161.1995.tb02031.x`
- **출처**: [https://doi.org/10.1111/j.2517-6161.1995.tb02031.x | 1995 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 여러 가설을 동시에 검정할 때 Bonferroni처럼 family-wise error를 통제하면 검정력이 지나치게 떨어진다. 대신 **기각된 가설 중 거짓 발견의 기대 비율(FDR)** 을 통제하자는 절차.
- **개발자에게 중요한 이유**: 캠페인 하나에 지표 20개를 붙이고 "뭐라도 유의하면 성공"이라 보고하는 관행이 왜 위험한지, 어떻게 보정하는지의 표준 레퍼런스.
- **확인 수준**: `메타데이터 확인`

### D-8-7. Eckles, Karrer & Ugander (2016/2017) — 네트워크 간섭 (SUTVA 위반)

- **정확한 인용**: Dean Eckles, Brian Karrer, Johan Ugander, "Design and Analysis of Experiments in Networks: Reducing Bias from Interference," *Journal of Causal Inference*, Vol. 5. DOI: `10.1515/jci-2015-0021` (Crossref issued 2016)
- **출처**: [https://doi.org/10.1515/jci-2015-0021 | Crossref issued 2016 / Vol.5 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 사용자가 서로 영향을 주는 상황(SUTVA 위반)에서 개인 단위 무작위 배정은 처치 효과를 편향되게 추정한다. 클러스터 무작위화 등 설계로 편향을 줄이는 방법을 분석한다.
- **개발자에게 중요한 이유**: 추천·소셜 기능·마켓플레이스 가격 실험에서 **A그룹의 변화가 B그룹으로 새어나간다.** 마테크에서는 "친구 초대", "공유 쿠폰", 재고 공유 마켓플레이스에서 실제 문제가 된다.
- **확인 수준**: `메타데이터 확인`

### D-8-8. Saveski et al. (2017) — 네트워크 효과 탐지

- **정확한 인용**: Martin Saveski, Jean Pouget-Abadie, Guillaume Saint-Jacques, Weitao Duan, Souvik Ghosh, Ya Xu, Edoardo M. Airoldi, "Detecting Network Effects," *Proceedings of the 23rd ACM SIGKDD (KDD 2017)*, pp. 1027–1035. DOI: `10.1145/3097983.3098192`
- **출처**: [https://doi.org/10.1145/3097983.3098192 | 2017 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: "무작위화 자체를 무작위화"해서(개인 단위 vs 클러스터 단위) 네트워크 간섭이 실제로 존재하는지 **검정**하는 설계.
- **개발자에게 중요한 이유**: 간섭이 있는지 없는지를 **가정하지 말고 측정하라**는 실용적 처방.
- **확인 수준**: `메타데이터 확인`

### D-8-9. 홀드아웃 그룹 설계 — 별도 정전 논문 미확인

- 상시 홀드아웃(global holdout / universal control)은 실무에서 널리 쓰이지만, **이번 세션에서 그것을 정식화한 독립 학술 논문을 특정하지 못했다.** 개념적 근거는 D-10의 증분성/고스트 광고 계열(Johnson et al. 2017)과 통제 실험 일반론(Kohavi 계열)에서 가져와야 한다.
- **확인 수준**: `학술 근거 확인 불가 (업계 관행 — 통제 실험 일반론으로 정당화)`

---

## D-9. 어트리뷰션 (라스트터치 편향 · Shapley · 마르코프 · MMM)

### D-9-1. Berman (2018) — 라스트터치는 광고주 이익을 **깎는다** ⭐⭐

- **정확한 인용**: Ron Berman, "Beyond the Last Touch: Attribution in Online Advertising," *Marketing Science*, Vol. 37, No. 5, pp. 771–792, 2018. DOI: `10.1287/mksc.2018.1104` (워킹페이퍼 SSRN `10.2139/ssrn.2384211`, 2013)
- **출처**: [https://doi.org/10.1287/mksc.2018.1104 | 2018 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar 초록 전문)
- **피인용수**: 135 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장 (초록 기반)**: 광고주가 여러 퍼블리셔에서 동시에 입찰하면 퍼블리셔 간 **외부효과(externalities)** 가 생긴다. 어트리뷰션이란 이 불확실성을 측정하고 외부효과를 보정하려는 시도다. 분석 모델로 보면 퍼블리셔 외부효과 때문에 광고주는 균형에서 **진실한 입찰(truthful bidding)에서 이탈**하고 이익이 낮아진다. **라스트터치 어트리뷰션을 쓰면 어트리뷰션을 아예 안 쓰는 것보다 광고주 이익이 줄어든다.** 강한 광고주는 어트리뷰션 때문에 과다 입찰하게 되어 노출 배분이 왜곡되는 손해를 본다. 반면 **Shapley value 기반 어트리뷰션은 시장 전환율이 너무 높지 않을 때 광고주 이익을 개선**한다.
- **인용할 만한 문장** (초록 원문):
  > "Our analysis of a common attribution method known as last-touch shows that it reduces advertiser profits compared to not using attribution at all, and that stronger advertisers suffer from a misallocation of consumer impressions due to overbidding for ads resulting from the attribution process. Our analysis of an attribution scheme based on the Shapley value shows that it will improve the profits of advertisers when conversion rates in the market are not too high."
- **개발자에게 중요한 이유**: "라스트터치는 부정확하다" 정도가 아니라 **"라스트터치를 쓰면 아예 안 쓰느니만 못하다"** 는 훨씬 강한 주장을 학술적으로 뒷받침한다. Shapley value가 왜 마테크 어트리뷰션 문서에 계속 등장하는지의 근거이기도 하다.
- **범위 한정**: 이론 모델 + 분석적 결과다(대규모 관측 데이터 실증이 아니라). Shapley의 개선 효과에는 **"시장 전환율이 너무 높지 않을 때"** 라는 조건이 붙는다 — 이 조건을 빼고 인용하지 마라.
- **확인 수준**: `초록 확인`

### D-9-2. Anderl et al. (2016) — 마르코프 제거 효과

→ D-4-2 참조. DOI `10.1016/j.ijresmar.2016.03.001`. `메타데이터 확인`

### D-9-3. Jin, Wang, Sun, Chan & Koehler (2017) — 베이지안 MMM (Google 기술 보고서) ⭐

- **정확한 인용**: Yuxue Jin, Yueqing Wang, Yunting Sun, David Chan, Jim Koehler, "Bayesian Methods for Media Mix Modeling with Carryover and Shape Effects," **Google Inc. 기술 보고서(technical report)**, 2017. ※ **peer-reviewed 논문이 아니다.**
- **출처**: [https://research.google/pubs/bayesian-methods-for-media-mix-modeling-with-carryover-and-shape-effects/ | 2017 | 검색 시점 2026-07-25] (research.google 페이지 직접 조회, 초록 전문)
- **핵심 주장**: 광고에는 **지연 효과(carryover)** 와 **체감 수익(shape/saturation)** 이 있어 선형 회귀로는 잡기 어렵다. 유연한 함수 형태로 이 둘을 모델링하고 **베이지안**으로 추정해 과거 모델의 사전 지식을 활용한다. 사후 표본에서 ROAS·mROAS 같은 기여도 지표를 계산하는 방법을 보인다.
- **핵심 수치·한계 (초록 그대로 — 이게 이 논문의 진짜 가치다)**: 시뮬레이션 결과 **데이터가 클 때는 잘 추정되지만, 표본이 작으면 사전분포가 사후에 큰 영향을 주고 편향된 추정으로 이어질 수 있다.** 또한 실제 샴푸 광고주 데이터에 적용한 결과, **모델에 기반한 최적 미디어 믹스는 파라미터 추정의 분산 때문에 그 자체의 분산이 크다.**
- **인용할 만한 문장** (초록 원문):
  > "Simulation studies show that the model can be estimated very well for large size data sets, but prior distributions have a big impact on the posteriors when the sample size is small and may lead to biased estimates."
  > "We further illustrate that the optimal media mix based on the model has a large variance due to the variance of the parameter estimates."
- **개발자에게 중요한 이유**: MMM을 만든 당사자(Google)가 **"최적 믹스의 분산이 크다"** 고 초록에 명시했다는 사실이 결정적이다. MMM 대시보드가 뱉는 "채널별 최적 예산"을 점 추정치로 받아들이면 안 된다는 걸 벤더 자신의 문서로 말할 수 있다.
- **확인 수준**: `문서 확인` (**peer-reviewed 아님 — 기업 기술 보고서 페이지 초록 조회**)

### D-9-4. Chen et al. (2018) — 유료 검색의 MMM 편향 보정

- **정확한 인용**: Aiyou Chen, David Chan, Mike Perry, Yuxue Jin, Yunting Sun, Yueqing Wang, Jim Koehler, "Bias Correction For Paid Search In Media Mix Modeling," arXiv:**1807.03292** (v1), 제출 2018-07-09.
- **출처**: [https://arxiv.org/abs/1807.03292 | 2018 | 검색 시점 2026-07-25] (arXiv API)
- **개발자에게 중요한 이유**: MMM에서 **유료 검색은 특히 편향되기 쉽다**(수요가 높을 때 검색량도 높고 광고비도 높다 — 역인과). 이 문제를 Google 팀이 직접 다룬 문서.
- **확인 수준**: `메타데이터 확인`

### D-9-5. Google Meridian — 오픈소스 MMM의 방법론 계보

- **정체**: Google이 공개한 **오픈소스 베이지안 MMM 프레임워크**. 코드는 Apache 2.0, 문서는 CC BY 4.0. (문서 페이지 최종 갱신 표기: 2026-07-09 UTC)
- **출처**: [https://developers.google.com/meridian/docs/basics/about-the-project | 문서 갱신 2026-07-09 | 검색 시점 2026-07-25], [https://developers.google.com/meridian/docs/basics/reference-list | 검색 시점 2026-07-25]
- **방법론 (문서에서 확인)**: 베이지안 추론 + 인과추론 토대. 사후분포를 산출하고, **사용자가 사전분포(priors)로 기존 비즈니스 지식을 주입**할 수 있으며, **과거 실험으로 커스텀 ROI 사전분포를 설정(experiment calibration)** 할 수 있다. Reach/Frequency 데이터를 반영하는 계층적 모델을 지원한다. TensorFlow Probability 기반.
- **인용할 만한 문장** (문서 원문):
  > "Meridian is designed to estimate the true causal impact of your marketing."
- **Meridian이 인용하는 Google 연구 문서 목록 (reference-list 페이지에서 그대로)**:
  - Jin, Y., Wang, Y., Sun, Y., Chan, D., Koehler, J. (2017). "Bayesian Methods for Media Mix Modeling with Carryover and Shape Effects" → D-9-3
  - Sun, Y., Wang, Y., Jin, Y., Chan, D., Koehler, J. (2017). "Geo-level Bayesian Hierarchical Media Mix Modeling"
  - Wang, Y., Jin, Y., Sun, Y., Chan, D., Koehler, J. (2017). "A Hierarchical Bayesian Approach to Improve Media Mix Models Using Category Data"
  - Chen, A., Chan, D., Koehler, J., Wang, Y., Sun, Y., Jin, Y., Perry, M. (2018). "Bias Correction For Paid Search In Media Mix Modeling" → D-9-4
  - Zhang, Y., Wurm, M., Li, E., Wakim, A., Kelly, J., Price, B., Liu, Y. (2023). "Media Mix Model Calibration With Bayesian Priors"
  - Zhang, Y., Wurm, M., Wakim, A., Li, E., Liu, Y. (2023). "Bayesian Hierarchical Media Mix Model Incorporating Reach and Frequency Data"
  - 그 외 학술 서적/논문: Gelman et al. *Bayesian Data Analysis* (2018), Pearl *Causality* (2009), Hernán & Robins *Causal Inference: What If* (2020), Gelman & Rubin (1992), Brooks & Gelman (1998), Ng, Wang & Dai (2021) "Bayesian Time Varying Coefficient Model with Applications to Marketing Mix Modeling"
- **개발자에게 중요한 이유**: **Meridian의 학술 계보는 peer-reviewed 저널이 아니라 Google 사내 기술 보고서 + 베이지안 통계 교과서**다. 오픈소스 MMM의 "학술적 권위"가 어디서 오는지를 정확히 보여준다. 그리고 **실험으로 사전분포를 캘리브레이션한다**는 설계는 D-10(증분성 실험)과 MMM을 잇는 다리다.
- **확인 수준**: `문서 확인` (공식 제품 문서 페이지 직접 조회 — 논문 아님) / 개별 Google 보고서는 **제목·저자·연도만 Meridian 문서에서 확인**, 원문 미조회

### D-9-6. Runge, Skokan, Zhou & Pauwels (2024) — Meta Robyn의 학술적 소개

- **정확한 인용**: Julian Runge, Igor Skokan, Gufeng Zhou, Koen Pauwels, "Packaging Up Media Mix Modeling: An Introduction to Robyn's Open-Source Approach," arXiv:**2403.14674** (v3), 최초 제출 2024-03-08.
- **출처**: [https://arxiv.org/abs/2403.14674 | 2024 | 검색 시점 2026-07-25] (arXiv API)
- **Robyn 방법론 (공식 저장소·문서 기반)**: Meta Marketing Science의 실험적 오픈소스 MMM 패키지. **Ridge 회귀**, 하이퍼파라미터 튜닝에 **다목적 진화 알고리즘(Nevergrad)**, 추세·계절 분해, 예산 배분에 그래디언트 기반 최적화를 조합한다.
  - **출처**: [https://github.com/facebookexperimental/Robyn | 검색 시점 2026-07-25] (웹 검색 결과 기반 — 저장소 페이지 직접 파싱은 하지 않음)
- **개발자에게 중요한 이유**: Google Meridian(베이지안)과 Meta Robyn(정규화 회귀 + 진화 알고리즘)의 **방법론이 근본적으로 다르다**는 걸 대조할 수 있다. "MMM"이 단일 기법이 아니라는 뜻이다.
- **확인 수준**: `메타데이터 확인` (arXiv 서지) / Robyn 방법론 세부는 `웹 검색 기반 — 1차 문서 직접 확인 필요`

### D-9-7. Vaver & Koehler (2011) — 지오 실험 (Google 기술 보고서)

- **정확한 인용**: Jon Vaver, Jim Koehler, "Measuring Ad Effectiveness Using Geo Experiments," **Google Inc. 기술 보고서**, 2011. ※ peer-reviewed 아님.
- **출처**: [https://research.google/pubs/measuring-ad-effectiveness-using-geo-experiments/ | 2011 | 검색 시점 2026-07-25] (페이지 직접 조회, 초록 전문)
- **핵심 주장**: 겹치지 않는 지리적 지역을 **무작위로** 통제군/처치군에 배정하고, 지역 타깃 광고로 각 조건을 실현한다. 개념적으로 단순하고, 체계적인 설계 절차가 있으며, 결과 해석이 쉽다.
- **인용할 만한 문장** (초록 원문):
  > "In these experiments, non-overlapping geographic regions are randomly assigned to a control or treatment condition, and each region realizes its assigned condition through the use of geo-targeted advertising."
- **개발자에게 중요한 이유**: **쿠키/디바이스 ID 없이도 인과 측정이 가능하다**는 게 지오 실험의 핵심이다. 프라이버시 규제로 개인 단위 추적이 어려워질수록 이 설계의 가치가 커진다 — 챕터에서 "포스트-쿠키 측정"의 답 중 하나로 쓸 수 있다.
- **확인 수준**: `문서 확인` (**peer-reviewed 아님 — 기업 기술 보고서 페이지 초록 조회**)

---

## D-10. 증분성(incrementality) · 인과추론

### D-10-1. Blake, Nosko & Tadelis (2015) — eBay 검색광고 실험 ⭐⭐

- **정확한 인용 (저널)**: Thomas Blake, Chris Nosko, Steven Tadelis, "Consumer Heterogeneity and Paid Search Effectiveness: A Large-Scale Field Experiment," *Econometrica*, Vol. 83, No. 1, pp. 155–174, 2015. DOI: `10.3982/ecta12423`
- **정확한 인용 (워킹페이퍼)**: 동일 저자, NBER Working Paper **No. 20171**, May 2014. DOI: `10.3386/w20171`
- **출처**: [https://doi.org/10.3982/ecta12423 | 2015 | 검색 시점 2026-07-25] (Crossref API), [https://www.nber.org/papers/w20171 | 2014 | 검색 시점 2026-07-25] (NBER 페이지 직접 조회)
- **핵심 주장 (NBER 페이지에서 확인 — 범위 한정 포함)**:
  - **브랜드 키워드 광고는 측정 가능한 단기 효익이 없었다** ("brand-keyword ads have no measurable short-term benefits"). 이미 eBay를 찾아온 사람이 광고를 클릭했을 뿐이다.
  - **비브랜드 키워드**에서는 **신규 고객·저빈도 고객은 광고에 긍정적으로 반응**했다.
  - 그러나 광고비의 대부분은 **광고가 없어도 구매했을 기존·상시 이용자**에게 지출되고 있었고, 그 결과 **전체 평균 수익률은 마이너스**였다.
- **인용할 만한 문장** (NBER 초록 원문 일부):
  > "We present results from a series of large scale field experiments done at eBay that were designed to measure the causal effectiveness of paid search ads."
- **개발자에게 중요한 이유**: 이 책의 어트리뷰션 챕터에서 **가장 강력한 사례**다. "광고 플랫폼이 보고하는 전환은 대부분 광고가 없어도 일어났을 전환"이라는 명제를, 최고 수준 경제학 저널(Econometrica)에 실린 대규모 무작위 실험으로 뒷받침한다.
- **⚠️ 오인용 경고 (반드시 지킬 것)**: 이 연구는 **"온라인 광고는 효과 없다"** 가 아니다. 정확히는 (1) **브랜드 키워드** 검색광고에 단기 효과가 없었고, (2) **비브랜드**에서는 **신규·저빈도 고객에게 효과가 있었으나** (3) 지출이 효과 없는 기존 고객 쪽에 몰려 **평균 수익률이 음수**였다는 것이다. **eBay라는 이미 강한 브랜드의 검색광고**라는 맥락도 함께 말해야 한다.
- **확인 수준**: `초록 확인` (NBER 워킹페이퍼 페이지) / Econometrica 게재본 본문 미조회

### D-10-2. Gordon, Zettelmeyer, Bhargava & Chapsky (2019) — Facebook 대규모 실험과 관측 방법 비교 ⭐⭐

- **정확한 인용**: Brett R. Gordon, Florian Zettelmeyer, Neha Bhargava, Dan Chapsky, "A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook," *Marketing Science*, Vol. 38, No. 2, pp. 193–225, 2019. DOI: `10.1287/mksc.2018.1135` (워킹페이퍼 SSRN `10.2139/ssrn.3033144`, 2017)
- **출처**: [https://doi.org/10.1287/mksc.2018.1135 | 2019 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar). ※ INFORMS 출판사 페이지는 HTTP 403으로 접근 실패.
- **피인용수**: 291 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장 (Semantic Scholar가 제공한 요약 초록 — 전문 아님)**:
  > "Observational methods often fail to accurately recover the treatment effects generated from randomized advertising experiments on Facebook."
- **개발자에게 중요한 이유**: 광고 플랫폼이 보고하는 관측 기반 전환 지표와 **무작위 실험이 말하는 진짜 증분 효과가 자주 어긋난다**는 명제의 대표 근거.
- **⚠️ 인용 주의**: 위 문장은 저널이 제공하는 **한 줄 요약**이며 논문 초록 전문이 아니다. **이 논문에 구체적 수치(몇 %, 몇 배)를 귀속시키지 마라.** 수치가 필요하면 아래 D-10-3(후속 연구, 초록 전문 확보)을 쓰라.
- **확인 수준**: `초록 확인 (요약본만)` — 초록 전문·본문 미조회

### D-10-3. Gordon, Moakler & Zettelmeyer (2023) — "Close Enough?" 관측 방법의 실제 오차 크기 ⭐⭐

- **정확한 인용**: Brett R. Gordon, Robert Moakler, Florian Zettelmeyer, "Close Enough? A Large-Scale Exploration of Non-Experimental Approaches to Advertising Measurement," *Marketing Science*, Vol. 42, No. 4, pp. 768–793, 2023. DOI: `10.1287/mksc.2022.1413`. arXiv:**2201.07055** (v2, 최종 개정 2022-10-04).
- **출처**: [https://arxiv.org/abs/2201.07055 | 2022 | 검색 시점 2026-07-25] (arXiv abs 페이지 초록 전문), [https://doi.org/10.1287/mksc.2022.1413 | 2023 | 검색 시점 2026-07-25] (Crossref API)
- **피인용수**: 65 (Semantic Scholar, 2026-07-25 조회)
- **핵심 수치 (초록 전문에서 그대로 — 이 문서에서 가장 인용 가치 높은 수치다)**:
  - Facebook의 **대규모 실험 663건**을 분석했다.
  - **5,000개 이상의 사용자 수준 피처**에 접근했다 — 대부분의 광고주나 측정 파트너가 접근할 수 있는 것보다 훨씬 풍부한 데이터다.
  - 두 가지 비실험 방법을 평가했다: **double/debiased machine learning (DML)** 과 **stratified propensity score matching (SPSM)**.
  - **RCT 기준 리프트 중앙값**: 퍼널 상단 **29%**, 중단 **18%**, 하단 **5%**.
  - **DML 추정 리프트 중앙값**: 상단 **83%**, 중단 **58%**, 하단 **24%**.
  - **SPSM 추정 리프트 중앙값**: 상단 **173%**, 중단 **176%**, 하단 **64%**.
  - **DML이 SPSM보다는 낫지만, 어느 쪽도 잘 작동하지 않았다** — 딥러닝으로 성향점수·결과 모델을 유연하게 구성해도 마찬가지였다.
- **인용할 만한 문장** (초록 원문):
  > "The median RCT lifts are 29%, 18%, and 5% for the upper, middle, and lower funnel outcomes, respectively. Using DML (SPSM), the median lift by funnel is 83% (173%), 58% (176%), and 24% (64%), respectively, indicating significant relative measurement errors."
  > "Overall, despite having access to large-scale experiments and rich user-level data, we are unable to reliably estimate an ad campaign's causal effect."
- **개발자에게 중요한 이유**: **이 책에서 가장 강력한 정량 근거다.** 하단 퍼널 실제 리프트가 5%인데 관측 기반 방법은 24~64%로 보고했다 — 즉 **5배에서 13배 과대추정**이다. "그냥 데이터가 더 많으면 되지 않나?"라는 개발자의 직관을, 5,000개 피처와 663개 실험을 쓰고도 안 됐다는 사실로 반박한다.
- **확인 수준**: `초록 확인` (arXiv 초록 전문)

### D-10-4. Johnson, Lewis & Nubbemeyer (2017) — 고스트 광고(Ghost Ads)

- **정확한 인용**: Garrett A. Johnson, Randall A. Lewis, Elmar I. Nubbemeyer, "Ghost Ads: Improving the Economics of Measuring Online Ad Effectiveness," *Journal of Marketing Research*, Vol. 54, No. 6, pp. 867–884, 2017. DOI: `10.1509/jmr.15.0297` (워킹페이퍼 SSRN `10.2139/ssrn.2620078`, 2015)
- **출처**: [https://doi.org/10.1509/jmr.15.0297 | 2017 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: 150 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장**: 전통적인 광고 리프트 실험은 통제군에게 **공익광고(PSA) 같은 대체 광고를 실제로 노출**해야 해서 비용이 든다. 고스트 광고는 **"이 사용자가 통제군이 아니었다면 이 광고에 노출됐을 것"이라는 사실만 기록**하고 실제로는 아무것도 띄우지 않는다. 그 결과 통제군 노출 비용 없이 정확한 비교군을 얻는다.
- **관련**: 같은 저자들의 메타 스터디 "The Online Display Ad Effectiveness Funnel & Carry-Over: A Meta-Study of Ghost Ad Experiments" (SSRN `10.2139/ssrn.2701578`, 2015)
- **개발자에게 중요한 이유**: 마테크 개발자가 **직접 구현할 수 있는 설계 패턴**이다. 자사 캠페인에서도 "발송 대상으로 선정되었으나 발송하지 않은 그룹"을 로깅해두면 같은 원리로 증분 효과를 측정할 수 있다 — 홀드아웃 설계의 정밀한 버전.
- **확인 수준**: `메타데이터 확인` (Semantic Scholar가 초록 미제공)

---

## D-11. 업리프트 모델링 / 개인 처치 효과 (CATE)

### D-11-1. Rzepakowski & Jaroszewicz (2010/2012) — 업리프트 결정 트리

- **정확한 인용 (저널)**: Piotr Rzepakowski, Szymon Jaroszewicz, "Decision trees for uplift modeling with single and multiple treatments," *Knowledge and Information Systems*, Vol. 32, pp. 303–327. DOI: `10.1007/s10115-011-0434-0` (Crossref issued 2011; 통상 2012년 권으로 인용)
- **정확한 인용 (학회)**: 동일 저자, "Decision Trees for Uplift Modeling," *2010 IEEE International Conference on Data Mining (ICDM 2010)*, pp. 441–450. DOI: `10.1109/icdm.2010.62`
- **출처**: [https://doi.org/10.1007/s10115-011-0434-0 | Crossref issued 2011 | 검색 시점 2026-07-25], [https://doi.org/10.1109/icdm.2010.62 | 2010 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 결정 트리의 분할 기준을 "결과 예측 정확도"가 아니라 **"처치군과 통제군의 결과 분포 차이를 최대화"** 하도록 바꾼다. 즉 **누가 반응할까가 아니라 누가 캠페인 때문에 반응이 달라질까**를 직접 학습한다.
- **개발자에게 중요한 이유**: 업리프트 모델링이 일반 분류 모델과 무엇이 다른지를 **알고리즘 수준에서** 가장 명확히 보여주는 논문. 손실 함수/분할 기준이 다르다는 게 핵심이다.
- **확인 수준**: `메타데이터 확인`

### D-11-2. Devriendt, Moldovan & Verbeke (2018) — 업리프트 모델링 서베이 + 실험적 비교 ⭐

- **정확한 인용**: Floris Devriendt, Darie Moldovan, Wouter Verbeke, "A Literature Survey and Experimental Evaluation of the State-of-the-Art in Uplift Modeling: A Stepping Stone Toward the Development of Prescriptive Analytics," *Big Data*, Vol. 6, No. 1, pp. 13–41, 2018. DOI: `10.1089/big.2017.0104` (PubMed ID 29570415)
- **출처**: [https://doi.org/10.1089/big.2017.0104 | 2018 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: 127 (Semantic Scholar, 2026-07-25 조회)
- **개발자에게 중요한 이유**: 업리프트 모델링 전체를 조감하면서 **실제로 여러 방법을 벤치마킹**한 서베이. 챕터에서 "업리프트 방법론들"을 개관할 때 개별 논문 대신 이걸 인용하면 안전하다. Semantic Scholar가 초록을 제공하지 않으므로 **구체 수치는 귀속시키지 말 것.**
- **확인 수준**: `메타데이터 확인`

### D-11-3. Künzel, Sekhon, Bickel & Yu (2019) — 메타러너 (S/T/X-learner) ⭐

- **정확한 인용**: Sören R. Künzel, Jasjeet S. Sekhon, Peter J. Bickel, Bin Yu, "Metalearners for estimating heterogeneous treatment effects using machine learning," *Proceedings of the National Academy of Sciences (PNAS)*, Vol. 116, No. 10, pp. 4156–4165, 2019. DOI: `10.1073/pnas.1804597116`
- **출처**: [https://doi.org/10.1073/pnas.1804597116 | 2019 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 이질적 처치 효과(CATE)를 추정하기 위해 **기존 ML 알고리즘을 감싸는 메타 알고리즘**(S-learner, T-learner, X-learner)을 정식화한다. 특히 X-learner는 처치군·통제군 크기가 크게 불균형할 때 유리하다.
- **개발자에게 중요한 이유**: **가장 실무 친화적인 진입점**이다. "새 알고리즘을 배워야 한다"가 아니라 "쓰던 XGBoost를 이렇게 조립하면 CATE가 나온다"는 이야기라서 개발자에게 전달하기 쉽다. 처치/통제 불균형은 마테크 캠페인에서 항상 발생한다(홀드아웃이 보통 5~10%).
- **확인 수준**: `메타데이터 확인`

### D-11-4. Wager & Athey (2018) — 인과 포레스트

- **정확한 인용**: Stefan Wager, Susan Athey, "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests," *Journal of the American Statistical Association*, Vol. 113, No. 523, pp. 1228–1242, 2018. DOI: `10.1080/01621459.2017.1319839`
- **관련**: Susan Athey, Julie Tibshirani, Stefan Wager, "Generalized random forests," *The Annals of Statistics*, Vol. 47, 2019. DOI: `10.1214/18-aos1709`. R 패키지 `grf` — DOI `10.32614/cran.package.grf`
- **출처**: [https://doi.org/10.1080/01621459.2017.1319839 | 2018 | 검색 시점 2026-07-25], [https://doi.org/10.1214/18-aos1709 | 2019 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 랜덤 포레스트를 이질적 처치 효과 추정에 맞게 변형(honest splitting)하면 **점 추정뿐 아니라 신뢰구간까지** 얻을 수 있다.
- **개발자에게 중요한 이유**: 업리프트 예측에 **불확실성 구간**을 붙일 수 있다는 게 실무적으로 중요하다 — "이 세그먼트는 업리프트 +2%p인데 신뢰구간이 -5%p~+9%p"라면 캠페인을 보내지 말아야 한다.
- **재현성**: `grf` R 패키지로 공개.
- **확인 수준**: `메타데이터 확인`

### D-11-5. Zhao & Harinen (2019) — 다중 처치 업리프트 + 비용 최적화 (CausalML 계열)

- **정확한 인용**: Zhenyu Zhao, Totte Harinen, "Uplift Modeling for Multiple Treatments with Cost Optimization," arXiv:**1908.05372** (v3), 최초 제출 2019-08-14.
- **출처**: [https://arxiv.org/abs/1908.05372 | 2019 | 검색 시점 2026-07-25] (arXiv API)
- **개발자에게 중요한 이유**: 실무에서는 "보낼까 말까"가 아니라 **"5% 쿠폰 vs 10% 쿠폰 vs 무료배송 중 뭘 보낼까"** 다. 다중 처치 + 비용을 함께 다루는 이 계열이 실제 캠페인 설계에 더 가깝다. Uber의 오픈소스 `causalml` 배경 논문 중 하나.
- **확인 수준**: `메타데이터 확인`

---

## D-12. 멀티암드 밴딧 / 컨텍스추얼 밴딧

### D-12-1. Li, Chu, Langford & Schapire (2010) — LinUCB ⭐

- **정확한 인용**: Lihong Li, Wei Chu, John Langford, Robert E. Schapire, "A Contextual-Bandit Approach to Personalized News Article Recommendation," arXiv:**1003.0146** (v2), 제출 2010-02-28. *Proceedings of the 19th International Conference on World Wide Web (WWW 2010)*, Raleigh, NC. DOI: `10.1145/1772690.1772758`
- **출처**: [https://arxiv.org/abs/1003.0146 | 2010 | 검색 시점 2026-07-25] (arXiv API — journal_ref 및 DOI 필드에서 확인)
- **핵심 주장**: 뉴스 기사 추천을 **컨텍스추얼 밴딧** 문제로 정식화하고, 선형 페이오프 가정 하에 신뢰상한(UCB)을 계산하는 LinUCB 알고리즘을 제시한다. 또한 **로그 데이터만으로 밴딧 정책을 오프라인 평가**하는 편향 없는 방법도 함께 제시한다.
- **개발자에게 중요한 이유**: 두 가지가 결정적이다. (1) 콘텐츠 선택을 **A/B 테스트가 아니라 지속적 학습 루프**로 보는 관점. (2) **오프라인 정책 평가** — 프로덕션에 올리기 전에 로그로 정책을 평가할 수 있다는 건 엔지니어링 관점에서 매우 실용적이다.
- **확인 수준**: `메타데이터 확인`

### D-12-2. Chapelle & Li (2011) — Thompson Sampling의 실증적 재평가 ⭐

- **정확한 인용**: Olivier Chapelle, Lihong Li, "An Empirical Evaluation of Thompson Sampling," *Advances in Neural Information Processing Systems 24 (NIPS 2011)*.
- **출처**: [https://papers.nips.cc/paper_files/paper/2011/hash/e53a0a2978c28872a4505bdb51db06dc-Abstract.html | 2011 | 검색 시점 2026-07-25] (NIPS 페이지 직접 조회, 초록 전문)
- **핵심 주장 (초록 기반)**: Thompson sampling은 탐색-활용 트레이드오프를 다루는 가장 오래된 휴리스틱 중 하나인데 문헌에서 놀랄 만큼 인기가 없었다. 저자들은 시뮬레이션·실데이터에서 **매우 경쟁력 있음**을 보이고, **구현이 아주 쉬우므로 표준 베이스라인에 포함되어야 한다**고 주장한다.
- **인용할 만한 문장** (초록 원문):
  > "Thompson sampling is one of oldest heuristic to address the exploration / exploitation trade-off, but it is surprisingly not very popular in the literature. We present here some empirical results using Thompson sampling on simulated and real data, and show that it is highly competitive. And since this heuristic is very easy to implement, we argue that it should be part of the standard baselines to compare against."
- **개발자에게 중요한 이유**: 마테크 도구가 "AI 최적화"라고 부르는 기능 상당수가 실제로는 Thompson sampling이다. **구현이 쉽다**는 점(베타 분포에서 샘플링해서 argmax)이 개발자에게 특히 매력적이며, 직접 만들 수 있다는 걸 보여준다.
- **확인 수준**: `초록 확인`

---

## D-13. Send-time optimization / 발송 빈도 · 피로도

> **이 축의 결론부터**: **발송 빈도(frequency)와 피로도**에는 최상위 저널의 실증 근거가 **있다**. 반면 마테크 벤더가 파는 형태의 **"개인별 최적 발송 시각(send-time optimization)"** 에는 최상위 저널 근거를 **이번 세션에서 찾지 못했다** — 있는 것은 응용 저널의 ML 예측 논문 수준이다. 이 비대칭을 책에 그대로 써라.

### D-13-1. Godfrey, Seiders & Voss (2011) — "이만하면 충분하다" (빈도의 역U자) ⭐

- **정확한 인용**: Andrea Godfrey, Kathleen Seiders, Glenn B. Voss, "Enough Is Enough! The Fine Line in Executing Multichannel Relational Communication," *Journal of Marketing*, Vol. 75, No. 4, pp. 94–109, 2011. DOI: `10.1509/jmkg.75.4.94`
- **일반 독자용 요약판**: 동일 저자, "When Is Enough Enough? Balancing on the Fine Line in Multichannel Marketing Communications," *GfK Marketing Intelligence Review*, Vol. 4, pp. 8–15, 2012. DOI: `10.2478/gfkmir-2014-0029`
- **출처**: [https://doi.org/10.1509/jmkg.75.4.94 | 2011 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: 166 (Semantic Scholar, 2026-07-25 조회)
- **핵심 주장**: 멀티채널 관계형 커뮤니케이션의 **빈도가 성과에 미치는 영향에 최적점이 존재**한다 — 너무 적어도, 너무 많아도 안 된다. 제목 자체가 결론이다.
- **개발자에게 중요한 이유**: **빈도 제한(frequency cap)** 이라는 마테크 기능의 학술적 근거가 바로 이것이다. "몇 회가 최적인가"는 도메인마다 다르지만, **최적점이 존재한다는 구조 자체**는 근거가 있다.
- **⚠️ 주의**: Semantic Scholar가 초록을 제공하지 않아 **구체적 최적 빈도 수치를 이 논문에 귀속시키지 마라.** "주당 N회가 최적"이라고 쓰려면 fact-checker의 본문 확인이 필요하다.
- **확인 수준**: `메타데이터 확인`

### D-13-2. Zhang, Kumar & Cosguner (2017) — 이메일 프로그램의 동태적 관리 ⭐

- **정확한 인용**: Xi (Alan) Zhang, V. Kumar, Koray Cosguner, "Dynamically Managing a Profitable Email Marketing Program," *Journal of Marketing Research*, Vol. 54, No. 6, pp. 851–866, 2017. DOI: `10.1509/jmr.16.0210`
- **출처**: [https://doi.org/10.1509/jmr.16.0210 | 2017 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 이메일 발송을 **정적인 규칙이 아니라 동태적 최적화 문제**로 본다 — 지금 한 통 더 보내는 것의 단기 이익과, 그로 인한 구독 해지·피로도의 장기 손실을 함께 고려한다.
- **개발자에게 중요한 이유**: 캠페인 시스템을 설계할 때 **"보낼까 말까"를 상태 기반 의사결정 문제**로 모델링해야 하는 이유. 오늘의 전환율만 최적화하는 시스템은 리스트를 태워 먹는다.
- **확인 수준**: `메타데이터 확인`

### D-13-3. Bonfrer & Drèze (2009) — 이메일 캠페인 성과의 실시간 평가

- **정확한 인용**: André Bonfrer, Xavier Drèze, "Real-Time Evaluation of E-mail Campaign Performance," *Marketing Science*, Vol. 28, No. 2, pp. 251–263, 2009. DOI: `10.1287/mksc.1080.0393` (워킹페이퍼 SSRN `10.2139/ssrn.941878`, 2006)
- **출처**: [https://doi.org/10.1287/mksc.1080.0393 | 2009 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 이메일 캠페인의 오픈·클릭이 발송 후 시간에 따라 어떻게 감쇠하는지를 모델링해, **캠페인 종료 전에 최종 성과를 예측**한다.
- **개발자에게 중요한 이유**: "발송 후 몇 시간이면 결과를 판단해도 되나"라는 실무 질문의 학술적 답. 발송 시각 최적화의 **간접적** 근거이기도 하다(시간대별 반응 곡선이 존재한다는 뜻이므로).
- **확인 수준**: `메타데이터 확인`

### D-13-4. Araújo et al. (2022) — 발송 시각 예측 (응용 저널)

- **정확한 인용**: Carolina Araújo, Christophe Soares, Ivo Pereira, Duarte Coelho, Miguel Ângelo Rebelo, Ana Madureira, "A Novel Approach for Send Time Prediction on Email Marketing," *Applied Sciences* (MDPI), Vol. 12, No. 16, Article 8310, 2022. DOI: `10.3390/app12168310`
- **출처**: [https://doi.org/10.3390/app12168310 | 2022 | 검색 시점 2026-07-25] (Crossref API)
- **⚠️ 위상 경고**: *Applied Sciences*(MDPI)는 마케팅 최상위 저널이 아니다. **"send-time optimization에 학술 근거가 있다"의 근거로 쓰기에는 약하다.** 이 논문은 "그런 시도가 학술 문헌에 존재한다" 수준으로만 인용하라.
- **관련**: Abhishek Pal 외, "Dynamic Best Send Time Prediction for Marketing Email Campaigns," *2022 JCICE*, pp. 92–99. DOI: `10.1109/jcice56791.2022.00029`
- **확인 수준**: `메타데이터 확인`

### D-13-5. Send-time optimization (벤더가 파는 형태) — **학술 근거 확인 불가**

- 마테크 벤더가 광고하는 "개인별 최적 발송 시각 AI"에 대해 **최상위 마케팅/CS 저널의 검증 연구를 이번 세션에서 찾지 못했다.** 웹 검색에서 나온 것은 (a) 업계 블로그의 "최적 발송 시간" 통계, (b) 특허 문서(USPTO), (c) 위 D-13-4 같은 응용 저널 논문이다.
- **출처**: [웹 검색 결과 — omnisend.com, USPTO 11341516 / 11431663 등 | 검색 시점 2026-07-25]
- **책에서의 처리 권고**: "빈도 제한에는 근거가 있고(D-13-1, D-13-2), **발송 시각 최적화는 대체로 벤더 주도 기능**이다. 자사 데이터로 A/B 검증하기 전에는 효과를 믿지 마라"고 쓰라.
- **확인 수준**: `학술 근거 확인 불가 (업계 관행)`

---

## D-14. 딜리버러빌리티 (이메일 인증 · 푸시)

> 이 축은 **논문이 아니라 IETF RFC가 1차 소스**다. 세 RFC 모두 rfc-editor.org 원문 페이지를 직접 조회해 번호·제목·저자·발행일·카테고리·초록을 확인했다.

### D-14-1. RFC 7208 — SPF (Sender Policy Framework)

- **정확한 인용**: S. Kitterman, "Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1," **RFC 7208**, IETF, **April 2014**, 카테고리: **Standards Track**. (RFC 4408을 obsolete)
- **출처**: [https://www.rfc-editor.org/rfc/rfc7208.html | 2014-04 | 검색 시점 2026-07-25] (원문 직접 조회)
- **인용할 만한 문장** (초록 원문):
  > "This document describes version 1 of the Sender Policy Framework (SPF) protocol, whereby ADministrative Management Domains (ADMDs) can explicitly authorize the hosts that are allowed to use their domain names, and a receiving host can check such authorization."
- **개발자에게 중요한 이유**: SPF는 **DNS TXT 레코드로 "이 도메인을 대신해 메일을 보낼 수 있는 IP"를 선언**하는 것이다. 마테크 도구(SendGrid, Braze 등)를 붙일 때 반드시 건드리는 지점이며, 여기서 틀리면 전달률이 무너진다.
- **확인 수준**: `문서 확인` (RFC 원문 페이지 — 번호·날짜·카테고리·초록 확인)

### D-14-2. RFC 6376 — DKIM (DomainKeys Identified Mail)

- **정확한 인용**: D. Crocker (Ed.), T. Hansen (Ed.), M. Kucherawy (Ed.), "DomainKeys Identified Mail (DKIM) Signatures," **RFC 6376**, IETF, **September 2011**, 카테고리: **Standards Track**.
- **출처**: [https://www.rfc-editor.org/rfc/rfc6376.html | 2011-09 | 검색 시점 2026-07-25] (원문 직접 조회)
- **인용할 만한 문장** (초록 원문):
  > "DKIM separates the question of the identity of the Signer of the message from the purported author of the message. Assertion of responsibility is validated through a cryptographic signature and by querying the Signer's domain directly to retrieve the appropriate public key."
- **개발자에게 중요한 이유**: DKIM은 **서명하는 주체와 From 헤더의 저자가 다를 수 있다**는 걸 명시적으로 분리한다. 마케팅 이메일이 "우리 도메인"으로 보이지만 실제로는 벤더 인프라에서 나가는 구조가 바로 이것이다.
- **확인 수준**: `문서 확인` (RFC 원문 페이지)

### D-14-3. RFC 7489 — DMARC

- **정확한 인용**: M. Kucherawy (Ed.), E. Zwicky (Ed.), "Domain-based Message Authentication, Reporting, and Conformance (DMARC)," **RFC 7489**, IETF, **March 2015**, 카테고리: **Informational**.
- **출처**: [https://www.rfc-editor.org/rfc/rfc7489.html | 2015-03 | 검색 시점 2026-07-25] (원문 직접 조회)
- **인용할 만한 문장** (초록 첫 문단 원문):
  > "Domain-based Message Authentication, Reporting, and Conformance (DMARC) is a scalable mechanism by which a mail-originating organization can express domain-level policies and preferences for message validation, disposition, and reporting, that a mail-receiving organization can use to improve mail handling."
- **⚠️ 정확성 포인트**: DMARC는 **Standards Track이 아니라 Informational**이다. 업계에서 "표준"이라 부르지만 IETF 분류상으로는 정보성 문서다 — 이 구분을 책에 정확히 쓰면 신뢰가 올라간다.
- **개발자에게 중요한 이유**: DMARC는 SPF/DKIM 결과를 **From 도메인과 정렬(alignment)** 시키고, 실패 시 정책(none/quarantine/reject)과 리포팅을 정의한다. 마케팅 발송 도메인 설계(서브도메인 분리 등)가 전부 여기서 나온다.
- **확인 수준**: `문서 확인` (RFC 원문 페이지)

### D-14-4. 푸시 알림 개인화 필드 실험

- **정확한 인용**: Jeeyeon Kim, Wookyoung Kim, Jeonghye Choi, "Push the Paw: A Field Experiment on Personalised Push Notifications and User Engagement," *Australasian Marketing Journal*, Vol. 34, No. 1, pp. 76–85, 2025. DOI: `10.1177/14413582251356702` (워킹페이퍼 SSRN `10.2139/ssrn.4993370`, "Personalizing Push Notifications: A Field Experiment on Engagement", 2024)
- **출처**: [https://doi.org/10.1177/14413582251356702 | 2025 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: 푸시 개인화의 **필드 실험** 근거. 최신(2025) 연구라 신선도 측면에서도 쓸 만하다.
- **⚠️ 주의**: 초록 미조회. **결과 방향(효과가 있었는지, 얼마나)을 이 논문에 귀속시키지 마라.** 인용하려면 fact-checker 검증 필요.
- **확인 수준**: `메타데이터 확인`

### D-14-5. 스팸 필터링 연구 · 푸시 opt-out 연구 — **미조회**

- 스팸 필터링의 학술 문헌(베이지안 필터링 계열, 최신 ML 스팸 탐지)과 푸시 알림 **opt-out** 에 특화된 연구는 **이번 세션에서 조회하지 못했다.**
- **확인 수준**: `확인 불가 (미조회)`

---

## D-15. 가격 · 프로모션 · 쿠폰 타겟팅의 인과 효과 — **미확보**

- 이번 세션에서 **최상위 저널의 쿠폰 타겟팅 인과 효과 연구를 확보하지 못했다.** Crossref 검색에서 나온 것은 주제가 어긋나거나(경쟁-가격 필드 실험) 위상이 낮은 저널이었다.
- **대체 경로 (검증된 것으로)**: 쿠폰/오퍼 타겟팅의 "누구에게 보낼 것인가"는 **D-11의 업리프트 모델링**이 정면으로 다룬다 — 특히 D-11-5(다중 처치 + 비용 최적화)가 "5% 쿠폰 vs 10% 쿠폰" 문제에 직접 대응한다. 이 축은 D-11로 흡수해 서술하는 게 안전하다.
- **확인 수준**: `확인 불가 (미조회)`

---

# C. 기반 기술의 학술적 뿌리

## C-16. 근사 자료구조 (스케치) 원 논문

### C-16-1. Bloom (1970) — 블룸 필터 ⭐

- **정확한 인용**: Burton H. Bloom, "Space/time trade-offs in hash coding with allowable errors," *Communications of the ACM*, Vol. 13, No. 7, pp. 422–426, 1970. DOI: `10.1145/362686.362692`
- **출처**: [https://doi.org/10.1145/362686.362692 | 1970 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 집합 멤버십 질의에서 **오탐(false positive)을 허용**하면 공간을 극적으로 줄일 수 있다. 제목이 곧 논지다 — 공간/시간을 오차와 교환한다.
- **개발자에게 중요한 이유**: 마테크에서 "이 사용자에게 이미 이 캠페인을 보냈나?"를 수억 건 규모로 빠르게 판단할 때의 표준 도구. **오탐은 허용되지만 누락은 안 된다**는 성질이 중복 발송 방지 로직과 정확히 맞는다(잘못 걸러낼 수는 있어도 중복 발송은 안 한다).
- **확인 수준**: `메타데이터 확인`

### C-16-2. Flajolet, Fusy, Gandouet & Meunier (2007) — HyperLogLog ⭐

- **정확한 인용**: Philippe Flajolet, Éric Fusy, Olivier Gandouet, Frédéric Meunier, "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm," *Discrete Mathematics & Theoretical Computer Science*, **DMTCS Proceedings vol. AH** (AofA 2007 conference proceedings), 2007. DOI: `10.46298/dmtcs.3545`
- **출처**: [https://doi.org/10.46298/dmtcs.3545 | 2007 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 스트림의 **고유 원소 개수(cardinality)** 를 매우 작은 메모리로 추정한다. 해시값의 선행 0 개수(leading zeros)라는 통계량을 여러 버킷으로 나눠 조화평균으로 결합한다.
- **개발자에게 중요한 이유**: **"이 세그먼트에 몇 명이 들어 있나"** 를 실시간으로 답하는 마테크 기능의 정체가 바로 이것이다. 세그먼트 크기 숫자가 새로고침할 때마다 조금씩 달라지는 이유이기도 하다 — 근사값이기 때문이다. 이 사실을 마케터에게 설명할 수 있어야 한다.
- **확인 수준**: `메타데이터 확인`

### C-16-3. Heule, Nunkesser & Hall (2013) — 실무의 HyperLogLog (HLL++)

- **정확한 인용**: Stefan Heule, Marc Nunkesser, Alexander Hall, "HyperLogLog in practice," *Proceedings of the 16th International Conference on Extending Database Technology (EDBT 2013)*, pp. 683–692. DOI: `10.1145/2452376.2452456`
- **출처**: [https://doi.org/10.1145/2452376.2452456 | 2013 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: Google이 실제 운영하면서 발견한 원 알고리즘의 문제(작은 카디널리티 영역의 편향, 64비트 해시 필요성, 희소 표현)를 고친 개선판.
- **개발자에게 중요한 이유**: BigQuery의 `APPROX_COUNT_DISTINCT`, Redis의 `PFCOUNT` 등이 실제로 구현하는 건 원 논문이 아니라 **이 개선판 계열**이다. 논문과 프로덕션 구현이 다르다는 좋은 예.
- **확인 수준**: `메타데이터 확인`

### C-16-4. Cormode & Muthukrishnan (2005) — Count-Min Sketch

- **정확한 인용**: Graham Cormode, S. Muthukrishnan, "An improved data stream summary: the count-min sketch and its applications," *Journal of Algorithms*, Vol. 55, No. 1, pp. 58–75, 2005. DOI: `10.1016/j.jalgor.2003.12.001`
  - 학회 버전: 동일 저자, *LATIN 2004*, LNCS, pp. 29–38. DOI: `10.1007/978-3-540-24698-5_7`
  - 대중적 해설: 동일 저자, "Approximating Data with the Count-Min Sketch," *IEEE Software*, Vol. 29, No. 1, pp. 64–69, 2012. DOI: `10.1109/ms.2011.127`
- **출처**: [https://doi.org/10.1016/j.jalgor.2003.12.001 | 2005 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 스트림에서 각 원소의 **빈도(frequency)** 를 작은 2차원 카운터 배열로 추정한다. 여러 해시 함수로 카운트하고 **최솟값을 취해** 충돌로 인한 과대추정을 줄인다.
- **개발자에게 중요한 이유**: "가장 많이 본 상품 Top-N", "가장 자주 발생한 이벤트"를 전체 카운트 없이 구하는 방법. **과소추정은 절대 없고 과대추정만 있다**는 단방향 오차 성질이 실무 의사결정에서 중요하다.
- **확인 수준**: `메타데이터 확인`

### C-16-5. Dunning & Ertl (2019) — t-digest

- **정확한 인용**: Ted Dunning, Otmar Ertl, "Computing Extremely Accurate Quantiles Using t-Digests," arXiv:**1902.04023** (v1), 제출 2019-02-11. (arXiv 코멘트: "22 pages, 10 figures")
- **출처**: [https://arxiv.org/abs/1902.04023 | 2019 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 분위수(quantile)를 근사하는 자료구조로, **극단 분위수(p99, p999)에서 특히 정확도가 높고** 병합(merge)이 가능하다.
- **개발자에게 중요한 이유**: "세그먼트 상위 1% 고소비 고객", "p95 응답 시간" 같은 분위수 지표를 분산 환경에서 계산할 때 쓴다. **병합 가능하다**는 성질이 결정적이다 — 파티션별로 계산한 뒤 합칠 수 있다.
- **확인 수준**: `메타데이터 확인`

### C-16-6. Dasgupta, Lang, Rhodes & Thaler (2016) — Theta Sketch 프레임워크 ⚠️ 저자 정정

- **정확한 인용**: Anirban Dasgupta, Kevin Lang, **Lee Rhodes**, **Justin Thaler**, "A Framework for Estimating Stream Expression Cardinalities," arXiv:**1510.01455** (v2), 최초 제출 2015-10-06. 학회 게재: *19th International Conference on Database Theory (ICDT 2016)*, Bordeaux, France, LIPIcs Vol. 48.
- **출처**: [https://arxiv.org/abs/1510.01455 | 2015 | 검색 시점 2026-07-25] (arXiv API — 저자 목록 직접 확인), [https://drops.dagstuhl.de/storage/00lipics/lipics-vol048-icdt2016/LIPIcs.ICDT.2016.6/LIPIcs.ICDT.2016.6.pdf | ICDT 2016 | 검색 시점 2026-07-25] (웹 검색으로 확인)
- **⚠️ 저자 정정 기록**: 이 논문의 저자를 "Dasgupta, Lang, Stokes, Tirthapura"로 적는 자료가 돌아다니는데 **틀렸다.** arXiv API가 반환한 실제 저자는 **Anirban Dasgupta, Kevin Lang, Lee Rhodes, Justin Thaler**다. (Gibbons & Tirthapura는 관련된 다른 논문의 저자다.) 이 항목은 **"인용을 기억으로 만들면 안 되는 이유"의 실물 사례**로 책에 쓸 수 있다.
- **핵심 주장**: 각 스트림에서 돌릴 수 있는 매우 넓은 부류의 샘플링 알고리즘을 규정하고, 각 스트림의 샘플을 **보편적(universal)으로 결합**해 합집합·교집합·차집합 같은 **집합 연산의 카디널리티**를 추정하는 프레임워크를 제시한다.
- **개발자에게 중요한 이유**: HyperLogLog는 합집합은 되지만 **교집합·차집합이 약하다.** 마테크 세그먼테이션은 정확히 그 연산 — "A 세그먼트 AND B 세그먼트 NOT C 세그먼트가 몇 명인가" — 을 요구한다. Apache DataSketches의 Theta Sketch가 이 논문의 구현이고, 이게 CDP 세그먼트 빌더의 실시간 카운트를 떠받친다.
- **확인 수준**: `메타데이터 확인` (arXiv 저자·ID 직접 확인) / ICDT 게재 사실은 웹 검색 기반

---

## C-17. 스트림 처리 이론

### C-17-1. Akidau et al. (2015) — Dataflow Model ⭐⭐

- **정확한 인용**: Tyler Akidau, Robert Bradshaw, Craig Chambers, Slava Chernyak, Rafael J. Fernández-Moctezuma, Reuven Lax, Sam McVeety, Daniel Mills, Frances Perry, Eric Schmidt, Sam Whittle, "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing," *Proceedings of the VLDB Endowment (PVLDB)*, Vol. 8, No. 12, pp. 1792–1803, 2015. DOI: `10.14778/2824032.2824076`
  - ※ Crossref는 제목을 축약형 "The dataflow model"로 반환했다. 통용되는 전체 제목은 위와 같다.
- **출처**: [https://doi.org/10.14778/2824032.2824076 | 2015 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 무한(unbounded)·순서 뒤섞인(out-of-order) 스트림 처리를 **네 가지 질문**으로 분해한다 — *무엇을* 계산하는가(변환), *이벤트 시간의 어디서* 계산하는가(윈도잉), *처리 시간의 언제* 결과를 내는가(워터마크·트리거), *어떻게* 개선분을 반영하는가(누적/철회). 정확성·지연시간·비용은 **동시에 최적화할 수 없고 명시적으로 교환**해야 한다.
- **개발자에게 중요한 이유**: 마테크 이벤트 파이프라인의 근본 문제가 여기 다 있다. **모바일 앱이 오프라인이었다가 3일 뒤에 이벤트를 올리면** 어제 마감한 세그먼트는 어떻게 되는가? 이 논문은 그 질문에 이름(이벤트 시간 vs 처리 시간, 워터마크, 지연 데이터)을 붙여준다. Apache Beam·Flink의 이론적 토대.
- **확인 수준**: `메타데이터 확인`

### C-17-2. Kreps, Narkhede & Rao (2011) — Kafka 원 논문 ⚠️ 위상 주의

- **정확한 인용**: Jay Kreps, Neha Narkhede, Jun Rao, "Kafka: a Distributed Messaging System for Log Processing," **NetDB'11** (6th International Workshop on Networking Meets Databases), Athens, Greece, June 12, 2011.
- **출처**: [https://notes.stephenholiday.com/Kafka.pdf | 2011 | 검색 시점 2026-07-25] — **PDF 다운로드는 됐으나 텍스트 파싱에 실패해 초록을 직접 읽지 못했다.** 서지 정보는 웹 검색으로 교차 확인.
- **⚠️ 위상 주의**: 이 논문은 **워크숍 논문이고 DOI가 없다.** Crossref 검색에서 정규 레코드를 찾지 못했다. "Kafka 논문"을 인용할 때 저널/주요 학회 논문인 것처럼 쓰지 마라. (관련 정규 게재본으로는 Wang et al., "Building a replicated logging system with Apache Kafka," *PVLDB* 8(12):1654–1655, 2015, DOI `10.14778/2824032.2824063` 가 있다 — Crossref 확인됨.)
- **개발자에게 중요한 이유**: 마테크의 이벤트 백본이 거의 예외 없이 Kafka(또는 그 개념)라는 점, 그리고 **로그를 1급 추상으로 삼는다**는 발상이 Kappa 아키텍처와 CDP 재처리(replay)의 근거라는 점.
- **확인 수준**: `메타데이터 확인 (웹 검색 교차 확인)` / **원문 초록 미확인**

### C-17-3. Carbone et al. (2017) — Flink의 상태 관리 (exactly-once의 실체)

- **정확한 인용**: Paris Carbone, Stephan Ewen, Gyula Fóra, Seif Haridi, Stefan Richter, Kostas Tzoumas, "State management in Apache Flink®," *Proceedings of the VLDB Endowment (PVLDB)*, Vol. 10, No. 12, pp. 1718–1729, 2017. DOI: `10.14778/3137765.3137777`
- **출처**: [https://doi.org/10.14778/3137765.3137777 | 2017 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 분산 스트림 처리에서 **일관된 상태 스냅샷**을 어떻게 저비용으로 찍고 장애 시 복구하는가 — exactly-once 처리 의미론의 구현 기반.
- **개발자에게 중요한 이유**: **"exactly-once"는 마법이 아니라 체크포인트 + 재생 + 멱등성의 조합**이라는 걸 보여준다. 마테크에서 이건 곧 "중복 발송을 하지 않는다"의 인프라 기반이며, 캠페인 발송 같은 **외부 부수효과**에는 exactly-once가 그대로 적용되지 않는다는 한계도 여기서 나온다.
- **확인 수준**: `메타데이터 확인`

### C-17-4. Lambda / Kappa 아키텍처 — **peer-reviewed 논문 아님** ⭐

- **Lambda 아키텍처**: Nathan Marz의 블로그 글("How to beat the CAP theorem")에서 시작해, Nathan Marz & James Warren, *Big Data: Principles and Best Practices of Scalable Realtime Data Systems* (Manning, **2015**) 로 정식화되었다. **책이지 논문이 아니다.**
- **Kappa 아키텍처**: Kafka 공동 창시자 **Jay Kreps**가 **2014년** O'Reilly Radar에 쓴 블로그 글 "Questioning the Lambda Architecture"에서 제안했다. **블로그 글이지 논문이 아니다.**
- **출처**: [https://www.oreilly.com/radar/questioning-the-lambda-architecture/ | 2014 | 검색 시점 2026-07-25] (웹 검색 결과 기반 — 원문 페이지 직접 파싱은 하지 않음)
- **책에서의 처리 권고**: 이 책의 정직성 포인트 중 하나다. **데이터 엔지니어링에서 가장 많이 인용되는 두 "아키텍처"가 둘 다 peer-reviewed 문헌이 아니다.** 이건 이 분야의 지식이 어떻게 형성되는지를 보여준다 — 실무자의 블로그와 책이 학술 논문보다 영향력이 크다.
- **확인 수준**: `학술 근거 없음 (업계 문헌 — 책 1권 + 블로그 1편)`

---

## C-18. 컬럼 지향 저장 · OLAP

### C-18-1. Stonebraker et al. (2005) — C-Store ⚠️ DOI 주의

- **정확한 인용 (원본)**: Mike Stonebraker, Daniel J. Abadi, Adam Batkin, Xuedong Chen, Mitch Cherniack, Miguel Ferreira, Edmond Lau, Amerson Lin, Sam Madden, Elizabeth O'Neil, Pat O'Neil, Alex Rasin 외, "C-Store: A Column-oriented DBMS," *VLDB 2005*.
- **⚠️ DOI 주의**: Crossref에서 **VLDB 2005 원본에 대응하는 DOI를 찾지 못했다.** 검색으로 나온 DOI `10.1145/3226595.3226638`은 2018년 기념 논문집 *Making Databases Work: the Pragmatic Wisdom of Michael Stonebraker*, pp. 491–518에 실린 **재수록본(book-chapter)** 이다. 원본을 인용하려면 DOI 없이 `VLDB 2005`로 표기하라.
- **출처**: [https://doi.org/10.1145/3226595.3226638 | 재수록 2018 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 읽기 위주 분석 워크로드에서는 행이 아니라 **열 단위 저장**이 압축·I/O 양면에서 유리하다.
- **개발자에게 중요한 이유**: BigQuery·Snowflake·ClickHouse·Redshift가 왜 컬럼 저장인지, 그리고 CDP가 왜 트랜잭션 DB와 분석 DB를 분리하는지의 뿌리.
- **확인 수준**: `메타데이터 확인 (재수록본 DOI만)` / 원본 DOI `확인 불가`

### C-18-2. Abadi, Boncz, Harizopoulos, Idreos & Madden (2013) — 컬럼 스토어 서베이 ⭐

- **정확한 인용**: Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos, Samuel Madden, "The Design and Implementation of Modern Column-Oriented Database Systems," *Foundations and Trends in Databases*, Vol. 5, No. 3, pp. 197–280, 2013. DOI: `10.1561/1900000024`
- **출처**: [https://doi.org/10.1561/1900000024 | 2013 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: 컬럼 스토어의 설계 기법(벡터화 실행, 늦은 구체화(late materialization), 압축, 조인 처리)을 한 문서에서 다루는 **서베이**. C-Store·MonetDB 개별 논문 대신 이걸 인용하는 게 안전하고 포괄적이다.
- **확인 수준**: `메타데이터 확인`

### C-18-3. Melnik et al. (2010/2011/2020) — Dremel

- **정확한 인용 (원본)**: Sergey Melnik, Andrey Gubarev, Jing Jing Long, Geoffrey Romer, Shiva Shivakumar, Matt Tolton, Theo Vassilakis, "Dremel: Interactive Analysis of Web-Scale Datasets," *Proceedings of the VLDB Endowment (PVLDB)*, Vol. 3, No. 1, pp. 330–339, 2010. DOI: `10.14778/1920841.1920886`
  - CACM 재수록: 동일 저자, *Communications of the ACM*, Vol. 54, No. 6, pp. 114–123, 2011. DOI: `10.1145/1953122.1953148`
  - 10년 회고: Melnik 외 (Ahmadi, Delorey, Min, Pasumansky, Shute 추가), *PVLDB*, Vol. 13, No. 12, pp. 3461–3472, 2020. DOI: `10.14778/3415478.3415568`
  - ※ Crossref는 세 레코드 모두 제목을 "Dremel"로 축약 반환했다.
- **출처**: [https://doi.org/10.14778/1920841.1920886 | 2010 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: **중첩(nested) 데이터를 컬럼 방식으로 저장**하는 인코딩(repetition/definition level)과, 다단계 서빙 트리로 수조 행 규모 질의를 초 단위로 처리하는 구조.
- **개발자에게 중요한 이유**: **BigQuery의 조상**이고, **Parquet의 중첩 인코딩이 이 논문에서 나왔다.** 마테크 이벤트 데이터는 본질적으로 중첩 JSON인데(`event.properties.items[]`), 그걸 컬럼으로 저장하는 방법이 여기 있다. 2020년 회고 논문은 10년간 무엇이 맞았고 틀렸는지를 저자들이 직접 평가해서 특히 인용 가치가 높다.
- **확인 수준**: `메타데이터 확인`

### C-18-4. Yang et al. (2014) — Druid

- **정확한 인용**: Fangjin Yang, Eric Tschetter, Xavier Léauté, Nelson Ray, Gian Merlino, Deep Ganguli, "Druid: A Real-time Analytical Data Store," *Proceedings of the 2014 ACM SIGMOD International Conference on Management of Data (SIGMOD 2014)*, pp. 157–168. DOI: `10.1145/2588555.2595631` (Crossref는 제목을 "Druid"로 축약 반환)
- **출처**: [https://doi.org/10.1145/2588555.2595631 | 2014 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: **실시간 인제스트와 과거 데이터 질의를 하나의 시스템**에서 처리하는 분석 저장소. 시계열/이벤트 데이터에 특화된 컬럼 저장 + 비트맵 인덱스.
- **개발자에게 중요한 이유**: 마테크 실시간 대시보드("지금 이 캠페인의 클릭 수")의 전형적 백엔드. **Druid에 진짜 SIGMOD 논문이 있다**는 게 이 항목의 확인 결과다.
- **확인 수준**: `메타데이터 확인`

### C-18-5. Im et al. (2018) — Pinot

- **정확한 인용**: Jean-François Im, Kishore Gopalakrishna, Subbu Subramaniam, Mayank Shrivastava, Adwait Tumbde, Xiaotian Jiang, Jennifer Dai, Seunghyun Lee, Neha Pawar, Jialiang Li, Ravi Aringunram, "Pinot: Realtime OLAP for 530 Million Users," *Proceedings of the 2018 International Conference on Management of Data (SIGMOD 2018)*, pp. 583–594. DOI: `10.1145/3183713.3190661` (Crossref는 제목을 "Pinot"으로 축약 반환)
- **출처**: [https://doi.org/10.1145/3183713.3190661 | 2018 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: LinkedIn 규모(제목의 5억 3천만 사용자)에서 **사용자 대면 실시간 분석**을 어떻게 하는지. 마테크 대시보드가 "왜 이렇게 빠른가/느린가"를 설명하는 근거. **Pinot에도 진짜 SIGMOD 논문이 있다.**
- **확인 수준**: `메타데이터 확인`

---

## C-19. 엔티티 해석 (Entity Resolution) / 레코드 링키지 — ID 그래프의 학술적 대응물

### C-19-1. Fellegi & Sunter (1969) — 확률적 레코드 링키지의 이론 ⭐⭐

- **정확한 인용**: Ivan P. Fellegi, Alan B. Sunter, "A Theory for Record Linkage," *Journal of the American Statistical Association (JASA)*, Vol. 64, No. 328, pp. 1183–1210, 1969. DOI: `10.1080/01621459.1969.10501049`
- **출처**: [https://doi.org/10.1080/01621459.1969.10501049 | 1969 | 검색 시점 2026-07-25] (Crossref API)
- **관련 실무 해설**: Thomas N. Herzog, Fritz J. Scheuren, William E. Winkler, "Estimating the Parameters of the Fellegi–Sunter Record Linkage Model," in *Data Quality and Record Linkage Techniques*, Springer, pp. 93–106. DOI: `10.1007/0-387-69505-2_9`
- **핵심 주장**: 두 레코드가 같은 실체를 가리키는지를 **확률적 결정 문제**로 정식화한다. 필드별 일치/불일치 패턴에 대해 "일치 가정 하 확률 / 불일치 가정 하 확률"의 비(가능도비)를 계산하고, 두 개의 임계값으로 **매치 / 논매치 / 사람이 봐야 함(clerical review)** 세 영역으로 나눈다. 주어진 오류율 제약 하에서 이 규칙이 최적임을 보인다.
- **개발자에게 중요한 이유**: **ID 그래프의 학술적 조상이 바로 이것이다.** 마테크 벤더가 "identity resolution"이라 부르는 기능은 1969년 인구조사 통계학에서 나온 이 이론의 후예다. 특히 **세 번째 영역(사람이 봐야 함)** 의 존재가 중요하다 — 확률적 매칭은 애초에 "확신 못 하는 구간"을 설계에 포함하고 있었다. 마테크 도구가 그 구간을 자동으로 붙여버리는 게 문제의 근원이다.
- **확인 수준**: `메타데이터 확인`

### C-19-2. Mudgal et al. (2018) — 딥러닝 기반 엔티티 매칭의 설계 공간

- **정확한 인용**: Sidharth Mudgal, Han Li, Theodoros Rekatsinas, AnHai Doan, Youngchoon Park, Ganesh Krishnan, Rohit Deep, Esteban Arcaute, Vijay Raghavendra, "Deep Learning for Entity Matching: A Design Space Exploration," *Proceedings of the 2018 International Conference on Management of Data (SIGMOD 2018)*, pp. 19–34. DOI: `10.1145/3183713.3196926`
- **출처**: [https://doi.org/10.1145/3183713.3196926 | 2018 | 검색 시점 2026-07-25] (Crossref API + Semantic Scholar)
- **피인용수**: 678 (Semantic Scholar, 2026-07-25 조회)
- **개발자에게 중요한 이유**: 엔티티 매칭에 딥러닝을 쓸 때의 **설계 선택지를 체계화**한 논문. "언제 딥러닝이 도움이 되고 언제 안 되는가"를 다룬다는 점에서 실무 판단에 직접 쓰인다.
- **⚠️ 주의**: Semantic Scholar가 초록을 제공하지 않았다. **"구조화 데이터에서는 전통 기법이, 텍스트 데이터에서는 딥러닝이 낫다" 같은 구체적 결론을 이 논문에 귀속시키려면 fact-checker의 본문 확인이 필요하다.**
- **확인 수준**: `메타데이터 확인`

### C-19-3. Li et al. (2020) — Ditto (사전학습 언어모델 기반 매칭)

- **정확한 인용**: Yuliang Li, Jinfeng Li, Yoshihiko Suhara, AnHai Doan, Wang-Chiew Tan, "Deep Entity Matching with Pre-Trained Language Models," arXiv:**2004.00584** (v3), 최초 제출 2020-04-01. *PVLDB* 게재 — DOI: `10.14778/3421424.3421431` (arXiv 코멘트: "To appear in VLDB 2021")
- **출처**: [https://arxiv.org/abs/2004.00584 | 2020 | 검색 시점 2026-07-25] (arXiv API — DOI 필드 직접 확인)
- **개발자에게 중요한 이유**: 엔티티 매칭을 **BERT류 사전학습 모델의 시퀀스 쌍 분류 문제**로 재구성한다. 개발자에게 가장 친숙한 형태로 ER을 설명할 수 있고, LLM 시대의 ID 해석으로 가는 다리가 된다.
- **확인 수준**: `메타데이터 확인`

### C-19-4. Papadakis et al. (2020) — 블로킹·필터링 서베이 ⭐

- **정확한 인용**: George Papadakis, Dimitrios Skoutas, Emmanouil Thanos, Themis Palpanas, "Blocking and Filtering Techniques for Entity Resolution: A Survey," *ACM Computing Surveys*, Vol. 53, No. 2, pp. 1–42, 2020. DOI: `10.1145/3377455`
  - ※ Crossref가 반환한 제목은 "Blocking and Filtering Techniques for Entity Resolution"이다(부제 표기는 자료마다 다르다).
- **관련**: George Papadakis 외, "Comparative analysis of approximate blocking techniques for entity resolution," *PVLDB*, Vol. 9, No. 9, pp. 684–695, 2016. DOI: `10.14778/2947618.2947624`
- **출처**: [https://doi.org/10.1145/3377455 | 2020 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: ER의 진짜 병목은 매칭 정확도가 아니라 **O(n²) 비교를 어떻게 피할 것인가(블로킹)** 다. 수천만 프로필의 ID 그래프를 만들 때 개발자가 실제로 부딪히는 문제가 이것이고, 이 서베이가 그 지도다.
- **확인 수준**: `메타데이터 확인`

### C-19-5. Thirumuruganathan et al. (2021) — 블로킹에 딥러닝 적용

- **정확한 인용**: Saravanan Thirumuruganathan, Han Li, Nan Tang, Mourad Ouzzani, Yash Govind, Derek Paulsen, Glenn Fung, AnHai Doan, "Deep learning for blocking in entity matching: a design space exploration," *Proceedings of the VLDB Endowment (PVLDB)*, Vol. 14, No. 11, pp. 2459–2472, 2021. DOI: `10.14778/3476249.3476294`
- **출처**: [https://doi.org/10.14778/3476249.3476294 | 2021 | 검색 시점 2026-07-25] (Crossref API)
- **개발자에게 중요한 이유**: 임베딩 + ANN 검색으로 블로킹을 하는 최신 접근 — 벡터 DB를 쓰는 요즘 ID 해석 구현의 학술적 대응물.
- **확인 수준**: `메타데이터 확인`

---

## C-20. 프라이버시 기술

### C-20-1. Dwork, McSherry, Nissim & Smith (2006) — 차등 프라이버시 ⭐⭐

- **정확한 인용 (원본)**: Cynthia Dwork, Frank McSherry, Kobbi Nissim, Adam Smith, "Calibrating Noise to Sensitivity in Private Data Analysis," *Theory of Cryptography Conference (TCC 2006)*, Lecture Notes in Computer Science, pp. 265–284. DOI: `10.1007/11681878_14`
- **정확한 인용 (재수록)**: 동일 저자, *Journal of Privacy and Confidentiality*, Vol. 7, No. 3, pp. 17–51, 2017. DOI: `10.29012/jpc.v7i3.405`
- **출처**: [https://doi.org/10.1007/11681878_14 | 2006 | 검색 시점 2026-07-25], [https://doi.org/10.29012/jpc.v7i3.405 | 2017 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 질의의 **민감도(sensitivity)** — 한 사람의 데이터가 바뀔 때 결과가 최대 얼마나 변하는지 — 에 비례해 노이즈를 주입하면, 개인 정보 유출을 수학적으로 제한할 수 있다.
- **개발자에게 중요한 이유**: **"익명화했으니 괜찮다"는 말이 왜 무의미한지**의 근본 답. 차등 프라이버시는 데이터가 아니라 **질의 메커니즘**에 보장을 건다. 오늘날 Privacy Sandbox(C-20-6)·Apple/Google 텔레메트리가 전부 이 개념 위에 서 있다.
- **확인 수준**: `메타데이터 확인`

### C-20-2. Sweeney (2002) — k-익명성

- **정확한 인용**: Latanya Sweeney, "k-Anonymity: A Model for Protecting Privacy," *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, Vol. 10, No. 5, pp. 557–570, 2002. DOI: `10.1142/s0218488502001648`
- **출처**: [https://doi.org/10.1142/s0218488502001648 | 2002 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 공개된 데이터의 각 레코드가 **최소 k−1개의 다른 레코드와 준식별자(quasi-identifier)에서 구별되지 않도록** 일반화·억제한다.
- **개발자에게 중요한 이유**: 광고 플랫폼의 **"최소 대상 수 1,000명 미만이면 리포트를 안 준다"** 같은 임계값 규칙이 이 계열의 사고에서 나왔다. 동시에 k-익명성만으로는 부족하다(동질성 공격 등)는 것이 이후 차등 프라이버시로 넘어가는 동기다.
- **확인 수준**: `메타데이터 확인`

### C-20-3. McMahan et al. (2017) — 연합 학습 (FedAvg) ⭐

- **정확한 인용**: H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas, "Communication-Efficient Learning of Deep Networks from Decentralized Data," arXiv:**1602.05629** (v4), 최초 제출 2016-02-17. 게재: *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (AISTATS) 2017*, JMLR W&CP Vol. 54.
- **출처**: [https://arxiv.org/abs/1602.05629 | 2016 | 검색 시점 2026-07-25] (arXiv API — journal_ref 필드에서 AISTATS 2017 확인)
- **핵심 주장**: 데이터를 중앙으로 모으지 않고 **각 기기에서 로컬 학습 후 모델 업데이트만 평균**(FederatedAveraging)해서 학습한다.
- **개발자에게 중요한 이유**: "데이터를 모아야 개인화할 수 있다"는 CDP의 기본 전제에 대한 구조적 대안. 다만 마테크 실무에 실제로 도입된 사례는 드물다는 점도 함께 말해야 균형이 맞는다.
- **확인 수준**: `메타데이터 확인`

### C-20-4. Erlingsson, Pihur & Korolova (2014) — RAPPOR (로컬 차등 프라이버시)

- **정확한 인용**: Úlfar Erlingsson, Vasyl Pihur, Aleksandra Korolova, "RAPPOR: Randomized Aggregatable Privacy-Preserving Ordinal Response," arXiv:**1407.6981** (v2), 제출 2014-07-25. 게재: *ACM CCS 2014*. DOI: `10.1145/2660267.2660348` (arXiv 코멘트: "14 pages, accepted at ACM CCS 2014")
- **출처**: [https://arxiv.org/abs/1407.6981 | 2014 | 검색 시점 2026-07-25] (arXiv API — DOI 필드 직접 확인)
- **핵심 주장**: 클라이언트가 **서버로 보내기 전에** 자기 응답에 무작위화를 적용(로컬 DP)하고, 서버는 집계 수준에서만 통계를 복원한다. Chrome 텔레메트리에 실제 배포됐다.
- **개발자에게 중요한 이유**: **수집 시점에 프라이버시를 넣는다**는 발상. 중앙 DP(신뢰할 수 있는 큐레이터 가정)와 로컬 DP(서버도 못 믿음)의 차이를 설명하는 데 최적이며, SDK 설계 관점에서 개발자에게 직접 와닿는다.
- **확인 수준**: `메타데이터 확인`

### C-20-5. Pinkas, Schneider & Zohner (2018) — Private Set Intersection

- **정확한 인용**: Benny Pinkas, Thomas Schneider, Michael Zohner, "Scalable Private Set Intersection Based on OT Extension," *ACM Transactions on Privacy and Security (TOPS)*, Vol. 21, No. 2, pp. 1–35, 2018. DOI: `10.1145/3154794`
- **관련**: Ágnes Kiss, Jian Liu, Thomas Schneider, N. Asokan, Benny Pinkas, "Private Set Intersection for Unequal Set Sizes with Mobile Applications," *Proceedings on Privacy Enhancing Technologies*, Vol. 2017, No. 4, pp. 177–197. DOI: `10.1515/popets-2017-0044`
- **출처**: [https://doi.org/10.1145/3154794 | 2018 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 두 당사자가 각자의 집합을 공개하지 않고 **교집합만** 알아내는 프로토콜을, OT extension을 써서 실용적 규모로 확장한다.
- **개발자에게 중요한 이유**: **데이터 클린룸(clean room)** 과 "고객 리스트 매칭 광고"(Customer Match류)의 암호학적 토대. 광고주와 플랫폼이 서로의 전체 리스트를 안 보고 겹치는 사람만 찾는다는 게 이 기술이다. 특히 **비대칭 집합 크기**(광고주 10만 명 vs 플랫폼 10억 명)를 다룬 위 관련 논문이 실무에 가깝다.
- **확인 수준**: `메타데이터 확인`

### C-20-6. Ghazi et al. (2024/2025) — Privacy Sandbox 리포트의 차등 프라이버시 분석 ⭐

- **정확한 인용**: Badih Ghazi, Charlie Harrison, Arpana Hosabettu, Pritish Kamath, Alexander Knop, Ravi Kumar, Ethan Leeman, Pasin Manurangsi, Mariana Raykova, Vikas Sahu, Phillipp Schoppmann, "On the Differential Privacy and Interactivity of Privacy Sandbox Reports," arXiv:**2412.16916** (v3), 최초 제출 2024-12-22. (arXiv 코멘트: "To appear in Proceedings of Privacy Enhancing Technologies **2025**")
- **출처**: [https://arxiv.org/abs/2412.16916 | 2024 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: Privacy Sandbox의 **Attribution Reporting API (ARA)** 와 **Private Aggregation API (PAA)** 를 추상 모델로 형식화하고, 특정 가정 하에서 형식적 DP 보장을 만족함을 보인다. 질의와 데이터베이스가 이전 응답에 따라 **대화형으로 변할 수 있는** 경우까지 다룬다.
- **개발자에게 중요한 이유**: 포스트-쿠키 광고 측정 API가 **어떤 조건에서 어떤 프라이버시 보장을 주는지**를 형식적으로 따진 문서. "가정 하에서"라는 단서가 중요하다.
- **확인 수준**: `메타데이터 확인` (arXiv 서지·게재 예정 학회 확인)

### C-20-7. Tholoniat et al. (2024) — Cookie Monster (온디바이스 프라이버시 예산)

- **정확한 인용**: Pierre Tholoniat, Kelly Kostopoulou, Peter McNeely, Prabhpreet Singh Sodhi, Anirudh Varanasi, Benjamin Case, Asaf Cidon, Roxana Geambasu, Mathias Lécuyer, "Cookie Monster: Efficient On-device Budgeting for Differentially-Private Ad-Measurement Systems," *ACM SIGOPS 30th Symposium on Operating Systems Principles (SOSP '24)*, November 4–6, 2024, Austin, TX. arXiv:**2405.16719** (v5). DOI: `10.1145/3694715.3695965`
- **출처**: [https://arxiv.org/abs/2405.16719 | 2024 | 검색 시점 2026-07-25] (arXiv API — journal_ref 및 DOI 필드에서 SOSP'24 확인)
- **개발자에게 중요한 이유**: **최상위 시스템 학회(SOSP)에 실린** 광고 측정 프라이버시 논문. 프라이버시 예산(privacy budget)을 기기에서 어떻게 효율적으로 관리하는가 — 시스템 엔지니어링 관점에서 개발자에게 가장 잘 맞는 프라이버시 논문이다.
- **확인 수준**: `메타데이터 확인`

### C-20-8. Grib et al. (2026) — Privacy Sandbox의 흥망 ⭐ 최신

- **정확한 인용**: Rachid Youssef Grib, Alberto Verna, Nikhil Jha, Martino Trevisan, Marco Mellia, "The Rise and Fall of Google's Privacy Sandbox," arXiv:**2607.00693** (v1), 제출 **2026-07-01**. (arXiv 코멘트: "This work has been accepted for publication at **ACM CCS 2026**")
- **출처**: [https://arxiv.org/abs/2607.00693 | 2026-07 | 검색 시점 2026-07-25] (arXiv API)
- **개발자에게 중요한 이유**: **이 문서에서 가장 최신(제출 3주 전) 논문**이다. Privacy Sandbox의 실제 배포와 그 궤적을 측정 관점에서 회고한 연구가 최상위 보안 학회(CCS 2026)에 채택됐다는 사실 자체가, 포스트-쿠키 전환이 어떻게 흘러갔는지를 다룰 때 신선도 높은 근거가 된다.
- **⚠️ 주의**: 초록 미조회. **제목의 "Fall"에 기대어 결론을 추정하지 마라.** 실제 결론을 인용하려면 fact-checker가 초록/본문을 확인해야 한다.
- **확인 수준**: `메타데이터 확인` (arXiv 서지·게재 예정 학회만)

---

## C-21. LLM의 마케팅 적용

### C-21-1. Yu et al. (2018) — Spider (text-to-SQL 벤치마크) ⭐

- **정확한 인용**: Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, Zilin Zhang, Dragomir Radev, "Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task," arXiv:**1809.08887** (v5), 최초 제출 2018-09-24. (arXiv 코멘트: "EMNLP 2018, Long Paper")
- **출처**: [https://arxiv.org/abs/1809.08887 | 2018 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 여러 도메인·복잡한 스키마에 걸친 text-to-SQL 벤치마크. 핵심은 **훈련에서 본 적 없는 데이터베이스에 일반화**해야 한다는 설정이다.
- **개발자에게 중요한 이유**: "마케터가 자연어로 물으면 CDP가 SQL을 만들어 답한다"는 기능의 평가 기준이 여기서 나왔다. **cross-domain 설정**이 중요한 이유는, 우리 회사 스키마는 어떤 모델도 학습한 적이 없기 때문이다.
- **확인 수준**: `메타데이터 확인`

### C-21-2. Li et al. (2023) — BIRD (현실적 대규모 DB 벤치마크) ⭐

- **정확한 인용**: Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Rongyu Cao, Ruiying Geng, Nan Huo, Xuanhe Zhou, Chenhao Ma, Guoliang Li, Kevin C. C. Chang 외 3인, "Can LLM Already Serve as A Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs," arXiv:**2305.03111** (v3), 최초 제출 2023-05-04. (arXiv 코멘트: "**NeurIPS 2023**")
- **출처**: [https://arxiv.org/abs/2305.03111 | 2023 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장**: 제목이 곧 질문이다 — "LLM이 이미 데이터베이스 인터페이스로 쓸 만한가?" 대규모·지저분한 실제 DB(더러운 값, 외부 지식 필요, 효율성 고려)에 기반한 벤치마크를 만든다.
- **개발자에게 중요한 이유**: Spider보다 **실무에 훨씬 가깝다.** 실제 마테크 데이터웨어하우스는 값이 지저분하고, 컬럼 이름이 암호 같고, 도메인 지식 없이는 질의를 못 만든다. "text-to-SQL이 된다더라"와 "우리 데이터에서 된다"의 간격을 설명하는 데 이 벤치마크를 쓰라.
- **확인 수준**: `메타데이터 확인`

### C-21-3. Hong et al. (2024/2025) — LLM 기반 text-to-SQL 서베이 ⭐

- **정확한 인용**: Zijin Hong, Zheng Yuan, Qinggang Zhang, Hao Chen, Junnan Dong, Feiran Huang, Xiao Huang, "Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL," arXiv:**2406.08426** (v8), 최초 제출 2024-06-12. (arXiv 코멘트: "Accepted to **IEEE TKDE 2025**")
- **출처**: [https://arxiv.org/abs/2406.08426 | 2024 | 검색 시점 2026-07-25] (arXiv API)
- **개발자에게 중요한 이유**: **이 축의 최우선 인용 대상.** LLM text-to-SQL 전체를 조감하는 서베이이고, IEEE TKDE(최상위 데이터 저널)에 채택됐으며, v8까지 갱신돼 신선도도 높다. 개별 모델 논문 대신 이걸 인용하면 안전하다.
- **확인 수준**: `메타데이터 확인`

### C-21-4. Liu et al. (2025) — 개인화 LLM 서베이

- **정확한 인용**: Jiahong Liu, Zexuan Qiu, Zhongyang Li, Quanyu Dai, Wenhao Yu, Jieming Zhu, Minda Hu, Menglin Yang, Tat-Seng Chua, Irwin King, "A Survey of Personalized Large Language Models: Progress and Future Directions," arXiv:**2502.11528** (v2), 최초 제출 **2025-02-17**. (arXiv 코멘트: "34 pages, 8 figures, 7 tables, **Under Review**")
- **출처**: [https://arxiv.org/abs/2502.11528 | 2025 | 검색 시점 2026-07-25] (arXiv API)
- **핵심 주장 (웹 검색 요약 기준)**: 개인화 LLM을 세 층위로 정리한다 — 입력 수준(개인화 컨텍스트 프롬프팅), 모델 수준(개인화 어댑터 파인튜닝), 목적 수준(개인화 선호 정렬).
- **⚠️ 위상 주의**: **"Under Review" 프리프린트다.** peer-reviewed 논문으로 인용하지 마라.
- **개발자에게 중요한 이유**: "LLM으로 개인화한다"가 실제로는 세 가지 다른 기술 선택지라는 걸 정리해준다 — 프롬프트에 프로필을 넣을 것인가, 사용자별 어댑터를 둘 것인가, 선호 정렬을 할 것인가. 아키텍처 결정에 직결된다.
- **확인 수준**: `메타데이터 확인` (프리프린트, 미게재)

### C-21-5. Zhang et al. (2024) — LLM 개인화 서베이 (TMLR 게재)

- **정확한 인용**: Zhehao Zhang, Ryan A. Rossi, Branislav Kveton, Yijia Shao, Diyi Yang, Hamed Zamani, Franck Dernoncourt, Joe Barrow, Tong Yu, Sungchul Kim, Ruiyi Zhang, Jiuxiang Gu, Tyler Derr, Hongjie Chen, Junda Wu 외 6인, "Personalization of Large Language Models: A Survey," arXiv:**2411.00027** (v3), 최초 제출 2024-10-29. (arXiv 코멘트: "Accepted at the **Transactions on Machine Learning Research (TMLR)** journal")
- **출처**: [https://arxiv.org/abs/2411.00027 | 2024 | 검색 시점 2026-07-25] (arXiv API)
- **개발자에게 중요한 이유**: C-21-4와 주제가 겹치지만 **이쪽은 TMLR에 실제 게재됐다.** 인용 안정성을 원하면 이걸 쓰라.
- **확인 수준**: `메타데이터 확인` (게재 확인)

### C-21-6. Aghaei et al. (2025) — 마케팅 관리에서의 LLM ⚠️ 프리프린트

- **정확한 인용**: Raha Aghaei, Ali A. Kiaei, Mahnaz Boush, Javad Vahidi, Mohammad Zavvar, Zeynab Barzegar, Mahan Rofoosheh, "Harnessing the Potential of Large Language Models in Modern Marketing Management: Applications, Future Directions, and Strategic Recommendations," arXiv:**2501.10685** (v1), 제출 **2025-01-18**. (arXiv 코멘트: "40 pages, 9 figures")
- **출처**: [https://arxiv.org/abs/2501.10685 | 2025 | 검색 시점 2026-07-25] (arXiv API)
- **⚠️ 위상 경고**: **arXiv 프리프린트이며 학회/저널 게재 정보가 없다.** 마케팅 분야 심사를 거치지 않았다. "LLM이 마케팅에 쓰인다"는 개관 용도로만 쓰고, **여기서 나온 주장이나 수치를 근거로 삼지 마라.**
- **확인 수준**: `메타데이터 확인` (미게재 프리프린트)

### C-21-7. LLM 생성 카피의 효과 크기 연구 — **미확보**

- "LLM이 쓴 마케팅 카피가 사람이 쓴 것보다 성과가 좋다/나쁘다"에 대한 **peer-reviewed 필드 실험을 이번 세션에서 확보하지 못했다.**
- **책에서의 처리 권고**: LLM 카피 생성을 다룰 때 **효과 크기를 주장하지 말고**, "생성 속도와 변형 수를 늘려 A/B 테스트 가능한 후보를 많이 만든다"는 **프로세스 관점**으로 서술하라. 그 후 D-8(실험 방법론)으로 연결하면 근거가 탄탄하다.
- **확인 수준**: `확인 불가 (미조회)`

---

## C-22. Feature store / 학습-서빙 스큐 / ML 시스템의 기술 부채

### C-22-1. Sculley et al. (2015) — ML 시스템의 숨겨진 기술 부채 ⭐⭐

- **정확한 인용**: D. Sculley, Gary Holt, Daniel Golovin, Eugene Davydov, Todd Phillips, Dietmar Ebner, Vinay Chaudhary, Michael Young, Jean-François Crespo, Dan Dennison, "Hidden Technical Debt in Machine Learning Systems," *Advances in Neural Information Processing Systems 28 (NIPS 2015)*.
- **출처**: [https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html | 2015 | 검색 시점 2026-07-25] (NeurIPS 페이지 직접 조회, 초록 전문)
- **핵심 주장 (초록 기반)**: 머신러닝은 복잡한 예측 시스템을 빠르게 만드는 강력한 도구지만, **이 빠른 성과를 공짜라고 생각하는 것은 위험하다.** 소프트웨어 공학의 기술 부채 프레임으로 보면 실제 ML 시스템은 막대한 지속적 유지보수 비용을 떠안는 게 일반적이다. 저자들은 ML 특유의 위험 요인을 열거한다 — **경계 침식(boundary erosion), 얽힘(entanglement), 숨은 피드백 루프(hidden feedback loops), 선언되지 않은 소비자(undeclared consumers), 데이터 의존성, 설정 문제, 외부 세계의 변화**, 그리고 여러 시스템 수준 안티패턴.
- **인용할 만한 문장** (초록 원문):
  > "Machine learning offers a fantastically powerful toolkit for building useful complex prediction systems quickly. This paper argues it is dangerous to think of these quick wins as coming for free. Using the software engineering framework of technical debt, we find it is common to incur massive ongoing maintenance costs in real-world ML systems."
- **개발자에게 중요한 이유**: **이 책의 개발자 독자에게 가장 직접적으로 꽂히는 논문이다.** 마테크 스택은 이 논문이 경고한 모든 안티패턴의 전시장이다:
  - **숨은 피드백 루프** — 추천 모델이 노출을 바꾸고, 그 노출이 다음 학습 데이터가 된다.
  - **선언되지 않은 소비자** — CDP의 세그먼트 정의를 바꿨더니 아무도 모르던 다운스트림 캠페인 7개가 깨진다.
  - **얽힘(CACE: Change Anything Change Everything)** — 피처 하나를 바꾸면 모든 것이 바뀐다.
- **확인 수준**: `초록 확인`

### C-22-2. Baylor et al. (2017) — TFX (프로덕션 ML 플랫폼)

- **정확한 인용**: Denis Baylor, Eric Breck, Heng-Tze Cheng, Noah Fiedel, Chuan Yu Foo, Zakaria Haque, Salem Haykal, Mustafa Ispir, Vihan Jain, Levent Koc, Chiu Yuen Koo, Lukasz Lew 외, "TFX: A TensorFlow-Based Production-Scale Machine Learning Platform," *Proceedings of the 23rd ACM SIGKDD (KDD 2017)*, pp. 1387–1395. DOI: `10.1145/3097983.3098021` (Crossref는 제목을 "TFX"로 축약 반환)
- **출처**: [https://doi.org/10.1145/3097983.3098021 | 2017 | 검색 시점 2026-07-25] (Crossref API)
- **핵심 주장**: 프로덕션 ML 플랫폼이 갖춰야 할 구성요소 — 데이터 검증, 변환, 학습, 모델 검증, 서빙 — 를 통합한 시스템.
- **개발자에게 중요한 이유**: **학습-서빙 스큐(training-serving skew)** 를 시스템 차원에서 다룬 논문. 학습 때 쓴 피처 변환 로직과 서빙 때 쓰는 로직이 달라지는 문제 — 마테크에서 "배치로 계산한 세그먼트"와 "실시간으로 판단한 세그먼트"가 어긋나는 그 문제 — 의 정면 대응.
- **확인 수준**: `메타데이터 확인`

### C-22-3. Feature store — **정전 학술 논문 부재** ⭐

- "Feature store"라는 개념 자체를 정의·평가한 **peer-reviewed 정전 논문을 이번 세션에서 찾지 못했다.** Crossref 검색 결과는 위상이 불분명한 저널의 논문들이었고, 인용에 부적합하다고 판단해 제외했다.
- **개념의 실제 출처**: Feature store는 Uber의 Michelangelo 등 **산업계 엔지니어링 블로그와 벤더 문서**에서 형성된 개념이다. 학술적으로 가장 가까운 대응물은 **C-22-2 (TFX)** 와 **C-22-1 (기술 부채 — 특히 데이터 의존성)** 이다.
- **책에서의 처리 권고**: "feature store는 학술 개념이 아니라 **산업계가 학습-서빙 스큐라는 실제 문제에 붙인 이름**이다. 학술적 뿌리를 찾으면 TFX와 ML 기술 부채 논문으로 간다"고 쓰라. **Lambda/Kappa(C-17-4)와 같은 패턴** — 이 분야의 중요 개념 상당수가 논문이 아니라 현장에서 나왔다.
- **확인 수준**: `학술 근거 없음 (업계 개념)`

---

# 상충하는 연구 결과 (병기 — 한쪽으로 결론내지 마라)

## 상충-1. 신경망 추천이 실제로 더 나은가

- **연구 A (긍정)**: He et al. (2017) NCF — 신경망으로 상호작용을 학습하면 내적 기반 행렬 분해보다 낫다. [arXiv:1708.05031]
- **연구 B (부정)**: Ferrari Dacrema, Cremonesi & Jannach (2019) — 최상위 학회 신경망 추천 18개 중 **재현 가능한 것은 7개**, 그중 **6개는 단순 최근접 이웃/그래프 휴리스틱에 자주 밀렸다.** [arXiv:1907.06902, DOI 10.1145/3298689.3347058]
- **연구 C (부정, 표적 반박)**: Rendle, Krichene, Zhang & Anderson (2020) — 제대로 튜닝한 내적 기반 행렬 분해와 다시 비교하면 NCF의 우위가 성립하지 않는다. [arXiv:2005.09683]
- **책에서의 서술 권고**: "신경망 추천이 무조건 낫다"고 쓰지 마라. **"잘 튜닝된 단순 베이스라인을 먼저 세우고, 그것을 이기는지로 판단하라"** 가 이 논쟁의 실무적 결론이다. 이 대립 자체를 챕터의 서사로 쓰는 게 가장 정직하다.

## 상충-2. 온라인 광고는 효과가 있는가 (있다 / 측정이 틀렸다)

- **연구 A (효과 회의)**: Blake, Nosko & Tadelis (2015) — eBay 대규모 필드 실험. **브랜드 키워드 광고는 측정 가능한 단기 효익 없음**, 비브랜드에서도 지출이 효과 없는 기존 고객에 몰려 **평균 수익률 음수**. [Econometrica 83(1):155–174, DOI 10.3982/ecta12423]
- **연구 B (효과 부분 긍정, 같은 논문 안)**: 같은 연구에서 **신규·저빈도 고객은 비브랜드 광고에 긍정 반응**했다. 즉 광고 자체가 무효가 아니라 **타깃이 잘못됐다**는 것이다.
- **연구 C (측정 방법의 문제)**: Gordon, Moakler & Zettelmeyer (2022/2023) — RCT 리프트 중앙값이 퍼널 하단 **5%** 인데 관측 기반 DML은 **24%**, SPSM은 **64%** 로 추정했다. **광고가 무효인 게 아니라 관측 기반 측정이 크게 과대추정한다.** [arXiv:2201.07055, DOI 10.1287/mksc.2022.1413]
- **책에서의 서술 권고**: **"광고는 효과 없다"로 쓰면 오독이다.** 정확한 명제는 두 개다 — (1) 효과는 세그먼트별로 크게 다르고, 지출은 효과 없는 세그먼트에 몰리는 경향이 있다. (2) 관측 데이터 기반 기여도 수치는 실험 대비 수 배 과대추정될 수 있다.

## 상충-3. 개인화는 효과가 있는가

- **연구 A (긍정)**: Ansari & Mela (2003) — 이메일 콘텐츠 커스터마이즈가 반응을 높인다. [DOI 10.1509/jmkr.40.2.131.19224]
- **연구 B (조건부 역효과)**: Goldfarb & Tucker (2011) — 타깃팅과 노출 강도를 **결합하면** 구매 의향이 오히려 떨어진다. 프라이버시 우려가 매개. [DOI 10.1287/mksc.1100.0583]
- **연구 C (심리적 역효과)**: White et al. (2007/2008) — 과도한 개인화는 리액턴스를 유발한다. [DOI 10.1007/s11002-007-9027-9]
- **연구 D (프라이버시 통제가 오히려 도움)**: Tucker (2013/2014) — 프라이버시 통제권을 준 뒤 개인화 광고 성과가 올라갔다. [DOI 10.1509/jmr.10.0355]
- **책에서의 서술 권고**: 개인화 효과는 **선형이 아니라 역U자 또는 조건부**다. "얼마나"가 아니라 "어떤 조건에서"가 옳은 질문이다.

## 상충-4. MMM은 믿을 만한가

- **긍정 측**: Google Meridian·Meta Robyn 모두 프로덕션 도구로 배포됐고, 실험으로 사전분포를 캘리브레이션하는 설계를 제공한다.
- **한계 측 (같은 저자들이 직접 명시)**: Jin et al. (2017) 초록 — **"표본이 작으면 사전분포가 사후에 큰 영향을 주고 편향된 추정으로 이어질 수 있다"**, 그리고 **"모델 기반 최적 미디어 믹스는 파라미터 추정의 분산 때문에 분산이 크다."**
- **방법론 자체가 다름**: Meridian은 베이지안 계층 모델(TensorFlow Probability), Robyn은 Ridge 회귀 + Nevergrad 진화 알고리즘. **같은 데이터에 두 도구를 돌리면 다른 답이 나올 수 있다.**
- **책에서의 서술 권고**: MMM 결과를 **점 추정치가 아니라 분포로** 다루라고 쓰라. 근거는 벤더 자신의 문서다 — 이게 가장 반박하기 어려운 서술 방식이다.

## 상충-5. 어트리뷰션은 없는 것보다 나은가

- **Berman (2018)**: **라스트터치 어트리뷰션은 아예 안 쓰는 것보다 광고주 이익을 낮춘다.** Shapley 기반은 "시장 전환율이 너무 높지 않을 때" 이익을 개선한다. [DOI 10.1287/mksc.2018.1104]
- **반대 축**: 실무에서 라스트터치는 여전히 기본값이다. 계산이 싸고, 설명이 쉽고, 채널 팀 간 정치적 분쟁이 적기 때문이다.
- **책에서의 서술 권고**: 라스트터치를 "부정확하지만 실용적"이라고 쓰면 **연구 결과와 어긋난다.** Berman의 결과는 훨씬 강하다 — 이론 모델 결과라는 단서를 달되, 그 강도를 희석하지 마라.

---

# 「학술 근거 없음 / 업계 관행」 목록 ⭐

> **이 목록이 이 책의 차별점이다.** 마테크 실무에서 "당연한 것"으로 통용되지만 학술적 뒷받침이 없거나 약한 것들이다.

| # | 항목 | 실제 출처 | 판정 | 관련 절 |
|---|------|-----------|------|---------|
| 1 | **LTV:CAC 3:1 규칙** | SaaS 투자자·운영자 커뮤니티(David Skok 계열) rule of thumb | **학술 근거 확인 불가 (업계 관행)** — 이 값이 최적이라는 실증 연구 없음 | D-2-7 |
| 2 | **Gamma-Gamma 지출 모델** | Bruce Hardie의 **미간행 개인 웹사이트 노트** (brucehardie.com Note #25, 2013 갱신) | **peer-review 아님** — 널리 쓰이는 `lifetimes` 라이브러리가 구현하는 대상이 저널 논문이 아님 | D-2-6 |
| 3 | **Send-time optimization (개인별 최적 발송 시각 AI)** | 벤더 기능 + 특허(USPTO 11341516, 11431663) + 응용 저널(MDPI) | **학술 근거 확인 불가 (업계 관행)** — 최상위 저널 검증 연구 미확인. 단 **발송 빈도/피로도에는 근거 있음**(D-13-1, D-13-2) | D-13-5 |
| 4 | **Lambda 아키텍처** | Nathan Marz 블로그 + Marz & Warren, *Big Data* (Manning, 2015) — **책** | **peer-review 아님 (업계 문헌)** | C-17-4 |
| 5 | **Kappa 아키텍처** | Jay Kreps, "Questioning the Lambda Architecture," O'Reilly Radar, **2014 블로그 글** | **peer-review 아님 (업계 문헌)** | C-17-4 |
| 6 | **Feature store** | Uber Michelangelo 등 산업계 엔지니어링 블로그·벤더 문서 | **학술 정전 논문 부재 (업계 개념)** — 가장 가까운 학술 대응물은 TFX(C-22-2)와 ML 기술 부채(C-22-1) | C-22-3 |
| 7 | **Google Meridian / Meta Robyn의 학술 계보** | Google 사내 **기술 보고서** + 베이지안 통계 교과서 / Meta 오픈소스 저장소 | **peer-review 논문 아님** — 오픈소스 MMM의 권위는 기업 기술 보고서에서 온다 | D-9-5, D-9-6 |
| 8 | **Google 지오 실험 방법론** | Vaver & Koehler (2011), **Google Inc. 기술 보고서** | **peer-review 아님** (단 방법론 자체는 표준적 RCT 설계) | D-9-7 |
| 9 | **상시 홀드아웃 / universal control 설계** | 마테크 실무 관행 | **독립 정전 논문 미확인** — 통제 실험 일반론(Kohavi 계열)과 고스트 광고(D-10-4)로 정당화해야 함 | D-8-9 |
| 10 | **Kafka 원 논문의 위상** | NetDB'11 **워크숍 논문, DOI 없음** | **정규 학회/저널 논문 아님** — Crossref 레코드 미확인 | C-17-2 |
| 11 | **RFM의 기원** | 미국 다이렉트 마케팅 업계(카탈로그 소매) 통설 | **1차 학술 문헌 확인 불가** — "19XX년 누가 만들었다"고 단정 금지 | D-1 |
| 12 | **DMARC가 "표준"이라는 표현** | RFC 7489는 **Informational** 카테고리 (Standards Track 아님) | **분류 정정 필요** — SPF(7208)·DKIM(6376)은 Standards Track, DMARC(7489)만 Informational | D-14-3 |

---

# 확인 불가 목록 (미조회 · 서지 미확정)

| # | 항목 | 상태 | 조치 |
|---|------|------|------|
| 1 | 코호트 리텐션 커브의 함수 형태(멱법칙/로그 안정화) 주장 | **확인 불가 (정전 논문 미특정)** | 이 주장을 쓰려면 fact-checker 별도 검증 필요 | 
| 2 | 스팸 필터링 학술 연구 (베이지안 필터·ML 스팸 탐지) | **확인 불가 (미조회)** | D-14 딜리버러빌리티는 RFC 3종으로만 서술 |
| 3 | 푸시 알림 **opt-out** 특화 연구 | **확인 불가 (미조회)** | D-14-4(푸시 개인화 필드 실험)로 대체 |
| 4 | 가격·프로모션·쿠폰 타겟팅의 인과 효과 (최상위 저널) | **확인 불가 (미조회)** | D-11(업리프트, 특히 다중 처치+비용 최적화)로 흡수 서술 |
| 5 | LLM 생성 마케팅 카피의 효과 크기 (필드 실험) | **확인 불가 (미조회)** | 효과 크기 주장 금지. "후보 생성량 증가 → A/B 검증" 프로세스 관점으로 서술 |
| 6 | C-Store (VLDB 2005) **원본 DOI** | **확인 불가** — Crossref에 원본 레코드 없음 | `VLDB 2005`로 DOI 없이 표기. 2018 재수록본 DOI(`10.1145/3226595.3226638`)를 원본인 것처럼 쓰지 말 것 |
| 7 | Kafka 원 논문 **초록 원문** | **미확인** — PDF 다운로드는 됐으나 텍스트 파싱 실패 | 서지는 웹 교차 확인. 초록 직접 인용 금지 |
| 8 | Gordon et al. (2019) **초록 전문** | **미확인** — INFORMS 페이지 HTTP 403 | Semantic Scholar 한 줄 요약만 확보. **이 논문에 구체 수치 귀속 금지**, 수치는 D-10-3(2023) 사용 |
| 9 | Tucker (2013/2014) 권/연도 | **서지 상충** — Crossref에 Vol.50(2013)과 Vol.51(2013) 두 레코드 | DOI `10.1509/jmr.10.0355` 사용, 권/연도는 출판사 페이지 재확인 필요 |
| 10 | Devriendt et al. (2018), Mudgal et al. (2018), Godfrey et al. (2011), Johnson et al. (2017), Lemon & Verhoef (2016) 등의 **초록** | **미확인** (Semantic Scholar 초록 미제공) | 서지는 확정. **구체 수치·결론 방향 귀속 금지** |
| 11 | Grib et al. (2026) "The Rise and Fall of Google's Privacy Sandbox" **초록** | **미확인** | 제목의 "Fall"로 결론 추정 금지 |
| 12 | Robyn 방법론 세부 (Ridge + Nevergrad) | **웹 검색 기반** — 공식 저장소 직접 파싱 안 함 | 1차 문서(github.com/facebookexperimental/Robyn) 확인 후 서술 |

---

# 신선도 원장

**검색 시점: 전 항목 2026-07-25.** 조회 경로: `CR`=Crossref API, `AX`=arXiv API, `S2`=Semantic Scholar Graph API, `PG`=랜딩 페이지 직접 조회, `WS`=웹 검색.

| 절 | 논문·소스 | 저자·연도 | arXiv ID / DOI | 조회 | 확인 수준 |
|----|-----------|-----------|----------------|------|-----------|
| D-1-1 | Optimal Selection for Direct Mail | Bult & Wansbeek, 1995 | 10.1287/mksc.14.4.378 | CR | 메타데이터 |
| D-1-2 | RFM and CLV: Iso-Value Curves | Fader, Hardie & Lee, 2005 | 10.1509/jmkr.2005.42.4.415 | CR | 메타데이터 |
| D-2-1 | Counting Your Customers (Pareto/NBD) | Schmittlein, Morrison & Colombo, 1987 | 10.1287/mnsc.33.1.1 | CR+S2 | 메타데이터 |
| D-2-2 | Counting Your Customers the Easy Way (BG/NBD) | Fader, Hardie & Lee, 2005 | 10.1287/mksc.1040.0098 | CR+S2 | 메타데이터 |
| D-2-3 | Customer-Base Analysis in Discrete-Time (BG/BB) | Fader, Hardie & Shang, 2010 | 10.1287/mksc.1100.0580 | CR | 메타데이터 |
| D-2-4 | Modeling Customer Lifetime Value | Gupta et al., 2006 | 10.1177/1094670506293810 | CR | 메타데이터 |
| D-2-5 | Multiple Causes of Churn | Braun & Schweidel, 2011 | 10.1287/mksc.1110.0665 | CR | 메타데이터 |
| D-2-6 | The Gamma-Gamma Model of Monetary Value | Hardie (note), 2013 갱신 | (DOI 없음 — 미간행 노트) | PG | **문서 확인** |
| D-4-1 | Understanding Customer Experience | Lemon & Verhoef, 2016 | 10.1509/jm.15.0420 | CR+S2 | 메타데이터 |
| D-4-2 | Mapping the Customer Journey (그래프/마르코프) | Anderl et al., 2016 | 10.1016/j.ijresmar.2016.03.001 | CR | 메타데이터 |
| D-5-1 | E-Customization | Ansari & Mela, 2003 | 10.1509/jmkr.40.2.131.19224 | CR | 메타데이터 |
| D-5-2 | Online Display Advertising: Targeting and Obtrusiveness | Goldfarb & Tucker, 2011 | 10.1287/mksc.1100.0583 | CR+S2 | **초록 확인** |
| D-5-3 | Getting too personal (reactance) | White et al., 2007/2008 | 10.1007/s11002-007-9027-9 | CR | 메타데이터 |
| D-5-4 | Social Networks, Personalized Advertising, Privacy Controls | Tucker, 2013/2014 | 10.1509/jmr.10.0355 ⚠️상충 | CR | 메타데이터 |
| D-5-5 | Personalization Privacy Paradox | Awad & Krishnan, 2006 | 10.2307/25148715 | CR | 메타데이터 |
| D-6-1 | Amazon item-to-item CF | Linden, Smith & York, 2003 | 10.1109/mic.2003.1167344 | CR | 메타데이터 |
| D-6-2 | Matrix Factorization Techniques | Koren, Bell & Volinsky, 2009 | 10.1109/mc.2009.263 | CR | 메타데이터 |
| D-6-3 | Neural Collaborative Filtering | He et al., 2017 | arXiv:1708.05031 | AX | 메타데이터 |
| D-6-4 | Session-based Rec with RNN (GRU4Rec) | Hidasi et al., 2015 | arXiv:1511.06939 | AX | 메타데이터 |
| D-6-5 | Self-Attentive Sequential Rec (SASRec) | Kang & McAuley, 2018 | arXiv:1808.09781 | AX | 메타데이터 |
| D-6-6 | BERT4Rec | Sun et al., 2019 | arXiv:1904.06690 | AX | 메타데이터 |
| D-6-7 | Are We Really Making Much Progress? | Ferrari Dacrema et al., 2019 | arXiv:1907.06902 / 10.1145/3298689.3347058 | AX+S2 | **초록 확인** |
| D-6-8 | NCF vs Matrix Factorization Revisited | Rendle et al., 2020 | arXiv:2005.09683 | AX | 메타데이터 |
| D-6-9 | DNN for YouTube Recommendations | Covington, Adams & Sargin, 2016 | 10.1145/2959100.2959190 | CR | 메타데이터 |
| D-6-10 | Survey on Session-based Rec Systems | Wang et al., 2019 | arXiv:1902.04864 | AX | 메타데이터 |
| D-7-1 | Ad click prediction: view from the trenches (FTRL) | McMahan et al., 2013 | 10.1145/2487575.2488200 | CR | 메타데이터 |
| D-7-2 | Practical Lessons Predicting Clicks at Facebook | He et al., 2014 | 10.1145/2648584.2648589 | CR | 메타데이터 |
| D-7-3 | Field-aware Factorization Machines | Juan et al., 2016 | 10.1145/2959100.2959134 | CR | 메타데이터 |
| D-7-4 | Wide & Deep Learning | Cheng et al., 2016 | arXiv:1606.07792 | AX+PG | **초록 확인** |
| D-7-5 | DeepFM | Guo et al., 2017 | arXiv:1703.04247 | AX | 메타데이터 |
| D-7-6 | Deep Interest Network (DIN) | Zhou et al., 2017 | arXiv:1706.06978 | AX | 메타데이터 |
| D-7-7 | Deep Interest Evolution Network (DIEN) | Zhou et al., 2018 | arXiv:1809.03672 | AX | 메타데이터 |
| D-8-1 | Controlled experiments on the web | Kohavi et al., 2009 | 10.1007/s10618-008-0114-1 | CR | 메타데이터 |
| D-8-1b | Practical guide to controlled experiments | Kohavi, Henne & Sommerfield, 2007 | 10.1145/1281192.1281295 | CR | 메타데이터 |
| D-8-2 | Online controlled experiments at large scale | Kohavi et al., 2013 | 10.1145/2487575.2488217 | CR | 메타데이터 |
| D-8-3 | Trustworthy online controlled experiments | Kohavi et al., 2012 | 10.1145/2339530.2339653 | CR | 메타데이터 |
| D-8-4 | CUPED (pre-experiment data) | Deng et al., 2013 | 10.1145/2433396.2433413 | CR | 메타데이터 |
| D-8-5 | Peeking at A/B Tests | Johari et al., 2017 | 10.1145/3097983.3097992 | CR | 메타데이터 |
| D-8-5b | Always Valid Inference | Johari et al., 2022 | 10.1287/opre.2021.2135 | CR | 메타데이터 |
| D-8-6 | Controlling the False Discovery Rate | Benjamini & Hochberg, 1995 | 10.1111/j.2517-6161.1995.tb02031.x | CR | 메타데이터 |
| D-8-7 | Experiments in Networks: Reducing Bias from Interference | Eckles, Karrer & Ugander, 2016 | 10.1515/jci-2015-0021 | CR | 메타데이터 |
| D-8-8 | Detecting Network Effects | Saveski et al., 2017 | 10.1145/3097983.3098192 | CR | 메타데이터 |
| D-9-1 | Beyond the Last Touch | Berman, 2018 | 10.1287/mksc.2018.1104 | CR+S2 | **초록 확인** |
| D-9-3 | Bayesian Methods for MMM (Google TR) | Jin, Wang, Sun, Chan & Koehler, 2017 | (기술 보고서, DOI 없음) | PG | **문서 확인** |
| D-9-4 | Bias Correction For Paid Search in MMM | Chen et al., 2018 | arXiv:1807.03292 | AX | 메타데이터 |
| D-9-5 | Google Meridian 문서·참고문헌 목록 | Google, 문서 갱신 2026-07-09 | (제품 문서) | PG | **문서 확인** |
| D-9-6 | Packaging Up Media Mix Modeling (Robyn) | Runge, Skokan, Zhou & Pauwels, 2024 | arXiv:2403.14674 | AX | 메타데이터 |
| D-9-7 | Measuring Ad Effectiveness Using Geo Experiments (Google TR) | Vaver & Koehler, 2011 | (기술 보고서, DOI 없음) | PG | **문서 확인** |
| D-10-1 | Consumer Heterogeneity and Paid Search Effectiveness (eBay) | Blake, Nosko & Tadelis, 2015 | 10.3982/ecta12423 / NBER w20171 (10.3386/w20171) | CR+PG | **초록 확인**(NBER) |
| D-10-2 | Comparison of Approaches to Advertising Measurement (Facebook) | Gordon, Zettelmeyer, Bhargava & Chapsky, 2019 | 10.1287/mksc.2018.1135 | CR+S2 | 초록 **요약본만** ⚠️ |
| D-10-3 | Close Enough? Non-Experimental Approaches | Gordon, Moakler & Zettelmeyer, 2022/2023 | arXiv:2201.07055 / 10.1287/mksc.2022.1413 | AX-PG+CR | **초록 확인** |
| D-10-4 | Ghost Ads | Johnson, Lewis & Nubbemeyer, 2017 | 10.1509/jmr.15.0297 | CR+S2 | 메타데이터 |
| D-11-1 | Decision trees for uplift modeling | Rzepakowski & Jaroszewicz, 2011/2012 | 10.1007/s10115-011-0434-0 / 10.1109/icdm.2010.62 | CR | 메타데이터 |
| D-11-2 | Uplift Modeling 서베이 + 실험 평가 | Devriendt, Moldovan & Verbeke, 2018 | 10.1089/big.2017.0104 | CR+S2 | 메타데이터 |
| D-11-3 | Metalearners for HTE (S/T/X-learner) | Künzel, Sekhon, Bickel & Yu, 2019 | 10.1073/pnas.1804597116 | CR | 메타데이터 |
| D-11-4 | Causal Forest / Generalized Random Forests | Wager & Athey 2018 / Athey et al. 2019 | 10.1080/01621459.2017.1319839 / 10.1214/18-aos1709 | CR | 메타데이터 |
| D-11-5 | Uplift Modeling for Multiple Treatments with Cost Optimization | Zhao & Harinen, 2019 | arXiv:1908.05372 | AX | 메타데이터 |
| D-12-1 | Contextual-Bandit for News Rec (LinUCB) | Li, Chu, Langford & Schapire, 2010 | arXiv:1003.0146 / 10.1145/1772690.1772758 | AX | 메타데이터 |
| D-12-2 | An Empirical Evaluation of Thompson Sampling | Chapelle & Li, 2011 | (NIPS 24, DOI 없음) | PG | **초록 확인** |
| D-13-1 | Enough Is Enough! (빈도의 최적점) | Godfrey, Seiders & Voss, 2011 | 10.1509/jmkg.75.4.94 | CR+S2 | 메타데이터 |
| D-13-2 | Dynamically Managing a Profitable Email Program | Zhang, Kumar & Cosguner, 2017 | 10.1509/jmr.16.0210 | CR | 메타데이터 |
| D-13-3 | Real-Time Evaluation of E-mail Campaign Performance | Bonfrer & Drèze, 2009 | 10.1287/mksc.1080.0393 | CR | 메타데이터 |
| D-13-4 | A Novel Approach for Send Time Prediction | Araújo et al., 2022 | 10.3390/app12168310 ⚠️저널 위상 낮음 | CR | 메타데이터 |
| D-14-1 | RFC 7208 — SPF | Kitterman, 2014-04 (Standards Track) | RFC 7208 | PG | **문서 확인** |
| D-14-2 | RFC 6376 — DKIM | Crocker, Hansen & Kucherawy, 2011-09 (Standards Track) | RFC 6376 | PG | **문서 확인** |
| D-14-3 | RFC 7489 — DMARC | Kucherawy & Zwicky, 2015-03 (**Informational**) | RFC 7489 | PG | **문서 확인** |
| D-14-4 | Push the Paw (푸시 개인화 필드 실험) | Kim, Kim & Choi, 2025 | 10.1177/14413582251356702 | CR | 메타데이터 |
| C-16-1 | Space/time trade-offs in hash coding (Bloom filter) | Bloom, 1970 | 10.1145/362686.362692 | CR | 메타데이터 |
| C-16-2 | HyperLogLog | Flajolet, Fusy, Gandouet & Meunier, 2007 | 10.46298/dmtcs.3545 | CR | 메타데이터 |
| C-16-3 | HyperLogLog in practice | Heule, Nunkesser & Hall, 2013 | 10.1145/2452376.2452456 | CR | 메타데이터 |
| C-16-4 | Count-Min Sketch | Cormode & Muthukrishnan, 2005 | 10.1016/j.jalgor.2003.12.001 | CR | 메타데이터 |
| C-16-5 | Computing Extremely Accurate Quantiles Using t-Digests | Dunning & Ertl, 2019 | arXiv:1902.04023 | AX | 메타데이터 |
| C-16-6 | Framework for Estimating Stream Expression Cardinalities (Theta) | Dasgupta, Lang, **Rhodes & Thaler**, 2015/2016 | arXiv:1510.01455 (ICDT 2016) | AX+WS | 메타데이터 ⚠️저자 정정 |
| C-17-1 | The Dataflow Model | Akidau et al., 2015 | 10.14778/2824032.2824076 | CR | 메타데이터 |
| C-17-2 | Kafka: a Distributed Messaging System | Kreps, Narkhede & Rao, 2011 | (NetDB'11 워크숍, **DOI 없음**) | WS | 메타데이터(교차) ⚠️ |
| C-17-3 | State management in Apache Flink | Carbone et al., 2017 | 10.14778/3137765.3137777 | CR | 메타데이터 |
| C-18-1 | C-Store: A Column-oriented DBMS | Stonebraker et al., 2005 | 원본 DOI **없음** / 재수록 10.1145/3226595.3226638 | CR | 메타데이터(재수록) ⚠️ |
| C-18-2 | Design and Implementation of Modern Column-Oriented DBs | Abadi, Boncz, Harizopoulos, Idreos & Madden, 2013 | 10.1561/1900000024 | CR | 메타데이터 |
| C-18-3 | Dremel | Melnik et al., 2010 / 2011 / 2020 | 10.14778/1920841.1920886 / 10.1145/1953122.1953148 / 10.14778/3415478.3415568 | CR | 메타데이터 |
| C-18-4 | Druid: A Real-time Analytical Data Store | Yang et al., 2014 | 10.1145/2588555.2595631 | CR | 메타데이터 |
| C-18-5 | Pinot: Realtime OLAP for 530 Million Users | Im et al., 2018 | 10.1145/3183713.3190661 | CR | 메타데이터 |
| C-19-1 | A Theory for Record Linkage | Fellegi & Sunter, 1969 | 10.1080/01621459.1969.10501049 | CR | 메타데이터 |
| C-19-2 | Deep Learning for Entity Matching | Mudgal et al., 2018 | 10.1145/3183713.3196926 | CR+S2 | 메타데이터 |
| C-19-3 | Deep Entity Matching with Pre-Trained LMs (Ditto) | Li et al., 2020 | arXiv:2004.00584 / 10.14778/3421424.3421431 | AX | 메타데이터 |
| C-19-4 | Blocking and Filtering Techniques for Entity Resolution | Papadakis et al., 2020 | 10.1145/3377455 | CR | 메타데이터 |
| C-19-5 | Deep learning for blocking in entity matching | Thirumuruganathan et al., 2021 | 10.14778/3476249.3476294 | CR | 메타데이터 |
| C-20-1 | Calibrating Noise to Sensitivity (Differential Privacy) | Dwork, McSherry, Nissim & Smith, 2006 | 10.1007/11681878_14 / 10.29012/jpc.v7i3.405 | CR | 메타데이터 |
| C-20-2 | k-Anonymity | Sweeney, 2002 | 10.1142/s0218488502001648 | CR | 메타데이터 |
| C-20-3 | Communication-Efficient Learning from Decentralized Data (FedAvg) | McMahan et al., 2016/2017 | arXiv:1602.05629 (AISTATS 2017) | AX | 메타데이터 |
| C-20-4 | RAPPOR (Local DP) | Erlingsson, Pihur & Korolova, 2014 | arXiv:1407.6981 / 10.1145/2660267.2660348 | AX | 메타데이터 |
| C-20-5 | Scalable Private Set Intersection Based on OT Extension | Pinkas, Schneider & Zohner, 2018 | 10.1145/3154794 | CR | 메타데이터 |
| C-20-6 | DP and Interactivity of Privacy Sandbox Reports | Ghazi et al., 2024 (PETS 2025) | arXiv:2412.16916 | AX | 메타데이터 |
| C-20-7 | Cookie Monster (SOSP '24) | Tholoniat et al., 2024 | arXiv:2405.16719 / 10.1145/3694715.3695965 | AX | 메타데이터 |
| C-20-8 | The Rise and Fall of Google's Privacy Sandbox | Grib et al., **2026-07** (CCS 2026) | arXiv:2607.00693 | AX | 메타데이터 |
| C-21-1 | Spider (text-to-SQL 벤치마크) | Yu et al., 2018 | arXiv:1809.08887 | AX | 메타데이터 |
| C-21-2 | BIRD (Can LLM Serve as a DB Interface?) | Li et al., 2023 (NeurIPS 2023) | arXiv:2305.03111 | AX | 메타데이터 |
| C-21-3 | Survey of LLM-based Text-to-SQL | Hong et al., 2024 (IEEE TKDE 2025) | arXiv:2406.08426 | AX | 메타데이터 |
| C-21-4 | Survey of Personalized LLMs | Liu et al., **2025-02** | arXiv:2502.11528 ⚠️Under Review | AX | 메타데이터 |
| C-21-5 | Personalization of LLMs: A Survey | Zhang et al., 2024 (TMLR) | arXiv:2411.00027 | AX | 메타데이터 |
| C-21-6 | LLMs in Modern Marketing Management | Aghaei et al., **2025-01** | arXiv:2501.10685 ⚠️미게재 프리프린트 | AX | 메타데이터 |
| C-22-1 | Hidden Technical Debt in Machine Learning Systems | Sculley et al., 2015 (NIPS 28) | (DOI 없음) | PG | **초록 확인** |
| C-22-2 | TFX: Production-Scale ML Platform | Baylor et al., 2017 | 10.1145/3097983.3098021 | CR | 메타데이터 |

---

# 확인 수준별 집계

| 확인 수준 | 건수 | 해당 항목 |
|-----------|------|-----------|
| **초록 확인** — 논문 초록 전문을 읽음. 직접 인용 가능 | **8** | D-5-2 Goldfarb & Tucker, D-6-7 Ferrari Dacrema, D-7-4 Wide & Deep, D-9-1 Berman, D-10-1 Blake(NBER), D-10-3 Gordon "Close Enough?", D-12-2 Chapelle & Li, C-22-1 Sculley |
| **문서 확인** — 논문이 아닌 1차 문서 직접 조회. 인용 가능하되 **peer-review 아님을 병기** | **7** | D-2-6 Gamma-Gamma 노트, D-9-3 Google MMM TR, D-9-5 Meridian 제품 문서, D-9-7 Google 지오실험 TR, D-14-1 RFC 7208, D-14-2 RFC 6376, D-14-3 RFC 7489 |
| **초록 확인 (요약본만)** ⚠️ | **1** | D-10-2 Gordon et al. 2019 — 저널 한 줄 요약뿐. **수치 귀속 절대 금지, 수치는 D-10-3 사용** |
| **메타데이터 확인** — 권위 서지 확정, 초록 미조회. **수치·결론 방향 귀속 금지** | **84** | 아래 신선도 원장 표 참조 |
| **확인 불가 / 미조회** | **12** | 「확인 불가 목록」 참조 |
| **학술 근거 없음 / 업계 관행** | **12** | 「학술 근거 없음」 목록 참조 |
| **총 서지 확정 논문·문서** | **100** | 초록 8 + 문서 7 + 요약본 1 + 메타데이터 84 |

> **본문 전체(full text)를 읽은 항목은 0건이다.** 이 문서의 어떤 항목도 `본문 확인` 수준이 아니다. 본문 표·그림의 수치가 필요하면 **fact-checker가 PDF를 직접 열어야 한다.**

---

# 참고문헌 (전체, 절 순서)

**D-1 RFM**
1. Bult, J.R., Wansbeek, T. (1995). Optimal Selection for Direct Mail. *Marketing Science* 14(4), 378–394. doi:10.1287/mksc.14.4.378
2. Fader, P.S., Hardie, B.G.S., Lee, K.L. (2005). RFM and CLV: Using Iso-Value Curves for Customer Base Analysis. *JMR* 42(4), 415–430. doi:10.1509/jmkr.2005.42.4.415

**D-2 CLV**
3. Schmittlein, D.C., Morrison, D.G., Colombo, R. (1987). Counting Your Customers: Who-Are They and What Will They Do Next? *Management Science* 33(1), 1–24. doi:10.1287/mnsc.33.1.1
4. Fader, P.S., Hardie, B.G.S., Lee, K.L. (2005). "Counting Your Customers" the Easy Way: An Alternative to the Pareto/NBD Model. *Marketing Science* 24(2), 275–284. doi:10.1287/mksc.1040.0098
5. Fader, P.S., Hardie, B.G.S., Shang, J. (2010). Customer-Base Analysis in a Discrete-Time Noncontractual Setting. *Marketing Science* 29(6), 1086–1108. doi:10.1287/mksc.1100.0580
6. Gupta, S., Hanssens, D., Hardie, B., Kahn, W., Kumar, V., Lin, N., Ravishanker, N., Sriram, S. (2006). Modeling Customer Lifetime Value. *Journal of Service Research* 9(2), 139–155. doi:10.1177/1094670506293810
7. Braun, M., Schweidel, D.A. (2011). Modeling Customer Lifetimes with Multiple Causes of Churn. *Marketing Science* 30(5), 881–902. doi:10.1287/mksc.1110.0665
8. Hardie, B. (2013 갱신). The Gamma-Gamma Model of Monetary Value. 미간행 노트. brucehardie.com/notes/025/

**D-4 저니**
9. Lemon, K.N., Verhoef, P.C. (2016). Understanding Customer Experience Throughout the Customer Journey. *Journal of Marketing* 80(6), 69–96. doi:10.1509/jm.15.0420
10. Anderl, E., Becker, I., von Wangenheim, F., Schumann, J.H. (2016). Mapping the customer journey: Lessons learned from graph-based online attribution modeling. *IJRM* 33(3), 457–474. doi:10.1016/j.ijresmar.2016.03.001

**D-5 개인화**
11. Ansari, A., Mela, C.F. (2003). E-Customization. *JMR* 40(2), 131–145. doi:10.1509/jmkr.40.2.131.19224
12. Goldfarb, A., Tucker, C. (2011). Online Display Advertising: Targeting and Obtrusiveness. *Marketing Science* 30(3), 389–404. doi:10.1287/mksc.1100.0583
13. White, T.B., Zahay, D.L., Thorbjørnsen, H., Shavitt, S. (2007/2008). Getting too personal: Reactance to highly personalized email solicitations. *Marketing Letters* 19, 39–50. doi:10.1007/s11002-007-9027-9
14. Tucker, C.E. (2013/2014). Social Networks, Personalized Advertising, and Privacy Controls. *JMR*. doi:10.1509/jmr.10.0355 ⚠️권/연도 상충
15. Awad, N.F., Krishnan, M.S. (2006). The Personalization Privacy Paradox. *MIS Quarterly* 30(1), 13–28. doi:10.2307/25148715

**D-6 추천**
16. Linden, G., Smith, B., York, J. (2003). Amazon.com recommendations: item-to-item collaborative filtering. *IEEE Internet Computing* 7(1), 76–80. doi:10.1109/mic.2003.1167344
17. Koren, Y., Bell, R., Volinsky, C. (2009). Matrix Factorization Techniques for Recommender Systems. *Computer* 42(8), 30–37. doi:10.1109/mc.2009.263
18. He, X., Liao, L., Zhang, H., Nie, L., Hu, X., Chua, T.-S. (2017). Neural Collaborative Filtering. arXiv:1708.05031
19. Hidasi, B., Karatzoglou, A., Baltrunas, L., Tikk, D. (2015). Session-based Recommendations with Recurrent Neural Networks. arXiv:1511.06939
20. Kang, W.-C., McAuley, J. (2018). Self-Attentive Sequential Recommendation. arXiv:1808.09781 (ICDM'18)
21. Sun, F., Liu, J., Wu, J., Pei, C., Lin, X., Ou, W., Jiang, P. (2019). BERT4Rec. arXiv:1904.06690 (CIKM 2019)
22. Ferrari Dacrema, M., Cremonesi, P., Jannach, D. (2019). Are We Really Making Much Progress? *RecSys 2019*. arXiv:1907.06902; doi:10.1145/3298689.3347058
23. Rendle, S., Krichene, W., Zhang, L., Anderson, J. (2020). Neural Collaborative Filtering vs. Matrix Factorization Revisited. arXiv:2005.09683
24. Covington, P., Adams, J., Sargin, E. (2016). Deep Neural Networks for YouTube Recommendations. *RecSys 2016*, 191–198. doi:10.1145/2959100.2959190
25. Wang, S., Cao, L., Wang, Y., Sheng, Q.Z., Orgun, M., Lian, D. (2019). A Survey on Session-based Recommender Systems. arXiv:1902.04864 (ACM CSUR)

**D-7 CTR**
26. McMahan, H.B. et al. (2013). Ad click prediction: a view from the trenches. *KDD 2013*, 1222–1230. doi:10.1145/2487575.2488200
27. He, X. et al. (2014). Practical Lessons from Predicting Clicks on Ads at Facebook. *ADKDD 2014*, 1–9. doi:10.1145/2648584.2648589
28. Juan, Y., Zhuang, Y., Chin, W.-S., Lin, C.-J. (2016). Field-aware Factorization Machines for CTR Prediction. *RecSys 2016*, 43–50. doi:10.1145/2959100.2959134
29. Cheng, H.-T. et al. (2016). Wide & Deep Learning for Recommender Systems. arXiv:1606.07792
30. Guo, H., Tang, R., Ye, Y., Li, Z., He, X. (2017). DeepFM. arXiv:1703.04247
31. Zhou, G. et al. (2017). Deep Interest Network for CTR Prediction. arXiv:1706.06978
32. Zhou, G. et al. (2018). Deep Interest Evolution Network. arXiv:1809.03672 (AAAI 2019)

**D-8 실험**
33. Kohavi, R., Longbotham, R., Sommerfield, D., Henne, R.M. (2009). Controlled experiments on the web. *DMKD* 18, 140–181. doi:10.1007/s10618-008-0114-1
34. Kohavi, R., Henne, R.M., Sommerfield, D. (2007). Practical guide to controlled experiments on the web. *KDD 2007*, 959–967. doi:10.1145/1281192.1281295
35. Kohavi, R. et al. (2013). Online controlled experiments at large scale. *KDD 2013*, 1168–1176. doi:10.1145/2487575.2488217
36. Kohavi, R. et al. (2012). Trustworthy online controlled experiments. *KDD 2012*, 786–794. doi:10.1145/2339530.2339653
37. Deng, A., Xu, Y., Kohavi, R., Walker, T. (2013). Improving the sensitivity of online controlled experiments (CUPED). *WSDM 2013*, 123–132. doi:10.1145/2433396.2433413
38. Johari, R., Koomen, P., Pekelis, L., Walsh, D. (2017). Peeking at A/B Tests. *KDD 2017*, 1517–1525. doi:10.1145/3097983.3097992
39. Johari, R., Koomen, P., Pekelis, L., Walsh, D. (2022). Always Valid Inference. *Operations Research* 70(3), 1806–1821. doi:10.1287/opre.2021.2135
40. Benjamini, Y., Hochberg, Y. (1995). Controlling the False Discovery Rate. *JRSS-B* 57(1), 289–300. doi:10.1111/j.2517-6161.1995.tb02031.x
41. Eckles, D., Karrer, B., Ugander, J. (2016). Design and Analysis of Experiments in Networks. *Journal of Causal Inference* 5. doi:10.1515/jci-2015-0021
42. Saveski, M. et al. (2017). Detecting Network Effects. *KDD 2017*, 1027–1035. doi:10.1145/3097983.3098192

**D-9 어트리뷰션 / MMM**
43. Berman, R. (2018). Beyond the Last Touch: Attribution in Online Advertising. *Marketing Science* 37(5), 771–792. doi:10.1287/mksc.2018.1104
44. Jin, Y., Wang, Y., Sun, Y., Chan, D., Koehler, J. (2017). Bayesian Methods for Media Mix Modeling with Carryover and Shape Effects. Google Inc. 기술 보고서.
45. Chen, A. et al. (2018). Bias Correction For Paid Search In Media Mix Modeling. arXiv:1807.03292
46. Runge, J., Skokan, I., Zhou, G., Pauwels, K. (2024). Packaging Up Media Mix Modeling: An Introduction to Robyn's Open-Source Approach. arXiv:2403.14674
47. Vaver, J., Koehler, J. (2011). Measuring Ad Effectiveness Using Geo Experiments. Google Inc. 기술 보고서.

**D-10 증분성**
48. Blake, T., Nosko, C., Tadelis, S. (2015). Consumer Heterogeneity and Paid Search Effectiveness. *Econometrica* 83(1), 155–174. doi:10.3982/ecta12423 (NBER WP 20171, doi:10.3386/w20171)
49. Gordon, B.R., Zettelmeyer, F., Bhargava, N., Chapsky, D. (2019). A Comparison of Approaches to Advertising Measurement. *Marketing Science* 38(2), 193–225. doi:10.1287/mksc.2018.1135
50. Gordon, B.R., Moakler, R., Zettelmeyer, F. (2023). Close Enough? *Marketing Science* 42(4), 768–793. doi:10.1287/mksc.2022.1413; arXiv:2201.07055
51. Johnson, G.A., Lewis, R.A., Nubbemeyer, E.I. (2017). Ghost Ads. *JMR* 54(6), 867–884. doi:10.1509/jmr.15.0297

**D-11 업리프트 / CATE**
52. Rzepakowski, P., Jaroszewicz, S. (2011/2012). Decision trees for uplift modeling with single and multiple treatments. *KAIS* 32, 303–327. doi:10.1007/s10115-011-0434-0
53. Rzepakowski, P., Jaroszewicz, S. (2010). Decision Trees for Uplift Modeling. *ICDM 2010*, 441–450. doi:10.1109/icdm.2010.62
54. Devriendt, F., Moldovan, D., Verbeke, W. (2018). A Literature Survey and Experimental Evaluation of the State-of-the-Art in Uplift Modeling. *Big Data* 6(1), 13–41. doi:10.1089/big.2017.0104
55. Künzel, S.R., Sekhon, J.S., Bickel, P.J., Yu, B. (2019). Metalearners for estimating heterogeneous treatment effects. *PNAS* 116(10), 4156–4165. doi:10.1073/pnas.1804597116
56. Wager, S., Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. *JASA* 113(523), 1228–1242. doi:10.1080/01621459.2017.1319839
57. Athey, S., Tibshirani, J., Wager, S. (2019). Generalized random forests. *Annals of Statistics* 47. doi:10.1214/18-aos1709
58. Zhao, Z., Harinen, T. (2019). Uplift Modeling for Multiple Treatments with Cost Optimization. arXiv:1908.05372

**D-12 밴딧**
59. Li, L., Chu, W., Langford, J., Schapire, R.E. (2010). A Contextual-Bandit Approach to Personalized News Article Recommendation. *WWW 2010*. arXiv:1003.0146; doi:10.1145/1772690.1772758
60. Chapelle, O., Li, L. (2011). An Empirical Evaluation of Thompson Sampling. *NIPS 24*.

**D-13 빈도 / 발송 시각**
61. Godfrey, A., Seiders, K., Voss, G.B. (2011). Enough Is Enough! *Journal of Marketing* 75(4), 94–109. doi:10.1509/jmkg.75.4.94
62. Zhang, X.(A.), Kumar, V., Cosguner, K. (2017). Dynamically Managing a Profitable Email Marketing Program. *JMR* 54(6), 851–866. doi:10.1509/jmr.16.0210
63. Bonfrer, A., Drèze, X. (2009). Real-Time Evaluation of E-mail Campaign Performance. *Marketing Science* 28(2), 251–263. doi:10.1287/mksc.1080.0393
64. Araújo, C. et al. (2022). A Novel Approach for Send Time Prediction on Email Marketing. *Applied Sciences* 12(16), 8310. doi:10.3390/app12168310

**D-14 딜리버러빌리티**
65. Kitterman, S. (2014). RFC 7208 — Sender Policy Framework (SPF), Version 1. IETF, Standards Track.
66. Crocker, D., Hansen, T., Kucherawy, M. (Eds.) (2011). RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures. IETF, Standards Track.
67. Kucherawy, M., Zwicky, E. (Eds.) (2015). RFC 7489 — DMARC. IETF, **Informational**.
68. Kim, J., Kim, W., Choi, J. (2025). Push the Paw: A Field Experiment on Personalised Push Notifications and User Engagement. *Australasian Marketing Journal* 34(1), 76–85. doi:10.1177/14413582251356702

**C-16 스케치**
69. Bloom, B.H. (1970). Space/time trade-offs in hash coding with allowable errors. *CACM* 13(7), 422–426. doi:10.1145/362686.362692
70. Flajolet, P., Fusy, É., Gandouet, O., Meunier, F. (2007). HyperLogLog. *DMTCS Proceedings* vol. AH. doi:10.46298/dmtcs.3545
71. Heule, S., Nunkesser, M., Hall, A. (2013). HyperLogLog in practice. *EDBT 2013*, 683–692. doi:10.1145/2452376.2452456
72. Cormode, G., Muthukrishnan, S. (2005). An improved data stream summary: the count-min sketch and its applications. *Journal of Algorithms* 55(1), 58–75. doi:10.1016/j.jalgor.2003.12.001
73. Dunning, T., Ertl, O. (2019). Computing Extremely Accurate Quantiles Using t-Digests. arXiv:1902.04023
74. Dasgupta, A., Lang, K., Rhodes, L., Thaler, J. (2015/2016). A Framework for Estimating Stream Expression Cardinalities. arXiv:1510.01455; *ICDT 2016*, LIPIcs vol. 48.

**C-17 스트림**
75. Akidau, T. et al. (2015). The Dataflow Model. *PVLDB* 8(12), 1792–1803. doi:10.14778/2824032.2824076
76. Kreps, J., Narkhede, N., Rao, J. (2011). Kafka: a Distributed Messaging System for Log Processing. *NetDB'11*. (DOI 없음)
77. Wang, G. et al. (2015). Building a replicated logging system with Apache Kafka. *PVLDB* 8(12), 1654–1655. doi:10.14778/2824032.2824063
78. Carbone, P. et al. (2017). State management in Apache Flink. *PVLDB* 10(12), 1718–1729. doi:10.14778/3137765.3137777
79. Marz, N., Warren, J. (2015). *Big Data: Principles and Best Practices of Scalable Realtime Data Systems*. Manning. (**책 — peer-review 아님**)
80. Kreps, J. (2014). Questioning the Lambda Architecture. O'Reilly Radar. (**블로그 — peer-review 아님**)

**C-18 컬럼/OLAP**
81. Stonebraker, M. et al. (2005). C-Store: A Column-oriented DBMS. *VLDB 2005*. (원본 DOI 없음; 재수록 doi:10.1145/3226595.3226638)
82. Abadi, D., Boncz, P., Harizopoulos, S., Idreos, S., Madden, S. (2013). The Design and Implementation of Modern Column-Oriented Database Systems. *Foundations and Trends in Databases* 5(3), 197–280. doi:10.1561/1900000024
83. Melnik, S. et al. (2010). Dremel. *PVLDB* 3(1), 330–339. doi:10.14778/1920841.1920886
84. Melnik, S. et al. (2011). Dremel. *CACM* 54(6), 114–123. doi:10.1145/1953122.1953148
85. Melnik, S. et al. (2020). Dremel [10년 회고]. *PVLDB* 13(12), 3461–3472. doi:10.14778/3415478.3415568
86. Yang, F. et al. (2014). Druid. *SIGMOD 2014*, 157–168. doi:10.1145/2588555.2595631
87. Im, J.-F. et al. (2018). Pinot. *SIGMOD 2018*, 583–594. doi:10.1145/3183713.3190661

**C-19 엔티티 해석**
88. Fellegi, I.P., Sunter, A.B. (1969). A Theory for Record Linkage. *JASA* 64(328), 1183–1210. doi:10.1080/01621459.1969.10501049
89. Herzog, T.N., Scheuren, F.J., Winkler, W.E. Estimating the Parameters of the Fellegi–Sunter Record Linkage Model. In *Data Quality and Record Linkage Techniques*, Springer, 93–106. doi:10.1007/0-387-69505-2_9
90. Mudgal, S. et al. (2018). Deep Learning for Entity Matching. *SIGMOD 2018*, 19–34. doi:10.1145/3183713.3196926
91. Li, Y., Li, J., Suhara, Y., Doan, A., Tan, W.-C. (2020). Deep Entity Matching with Pre-Trained Language Models. arXiv:2004.00584; doi:10.14778/3421424.3421431
92. Papadakis, G., Skoutas, D., Thanos, E., Palpanas, T. (2020). Blocking and Filtering Techniques for Entity Resolution. *ACM Computing Surveys* 53(2), 1–42. doi:10.1145/3377455
93. Thirumuruganathan, S. et al. (2021). Deep learning for blocking in entity matching. *PVLDB* 14(11), 2459–2472. doi:10.14778/3476249.3476294

**C-20 프라이버시**
94. Dwork, C., McSherry, F., Nissim, K., Smith, A. (2006). Calibrating Noise to Sensitivity in Private Data Analysis. *TCC 2006*, LNCS, 265–284. doi:10.1007/11681878_14 (재수록: *JPC* 7(3), 17–51, 2017. doi:10.29012/jpc.v7i3.405)
95. Sweeney, L. (2002). k-Anonymity: A Model for Protecting Privacy. *IJUFKS* 10(5), 557–570. doi:10.1142/s0218488502001648
96. McMahan, H.B., Moore, E., Ramage, D., Hampson, S., Agüera y Arcas, B. (2016/2017). Communication-Efficient Learning of Deep Networks from Decentralized Data. arXiv:1602.05629; *AISTATS 2017*, JMLR W&CP 54.
97. Erlingsson, Ú., Pihur, V., Korolova, A. (2014). RAPPOR. arXiv:1407.6981; *ACM CCS 2014*. doi:10.1145/2660267.2660348
98. Pinkas, B., Schneider, T., Zohner, M. (2018). Scalable Private Set Intersection Based on OT Extension. *ACM TOPS* 21(2), 1–35. doi:10.1145/3154794
99. Kiss, Á., Liu, J., Schneider, T., Asokan, N., Pinkas, B. (2017). Private Set Intersection for Unequal Set Sizes with Mobile Applications. *PoPETs* 2017(4), 177–197. doi:10.1515/popets-2017-0044
100. Ghazi, B. et al. (2024). On the Differential Privacy and Interactivity of Privacy Sandbox Reports. arXiv:2412.16916; *PETS 2025*.
101. Tholoniat, P. et al. (2024). Cookie Monster. *SOSP '24*. arXiv:2405.16719; doi:10.1145/3694715.3695965
102. Grib, R.Y., Verna, A., Jha, N., Trevisan, M., Mellia, M. (2026). The Rise and Fall of Google's Privacy Sandbox. arXiv:2607.00693; *ACM CCS 2026*.

**C-21 LLM**
103. Yu, T. et al. (2018). Spider. arXiv:1809.08887; *EMNLP 2018*.
104. Li, J. et al. (2023). Can LLM Already Serve as A Database Interface? (BIRD). arXiv:2305.03111; *NeurIPS 2023*.
105. Hong, Z. et al. (2024). Next-Generation Database Interfaces: A Survey of LLM-based Text-to-SQL. arXiv:2406.08426; *IEEE TKDE 2025*.
106. Liu, J. et al. (2025). A Survey of Personalized Large Language Models. arXiv:2502.11528 (Under Review)
107. Zhang, Z. et al. (2024). Personalization of Large Language Models: A Survey. arXiv:2411.00027; *TMLR*.
108. Aghaei, R. et al. (2025). Harnessing the Potential of Large Language Models in Modern Marketing Management. arXiv:2501.10685 (미게재 프리프린트)

**C-22 ML 시스템**
109. Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. *NIPS 28*.
110. Baylor, D. et al. (2017). TFX: A TensorFlow-Based Production-Scale Machine Learning Platform. *KDD 2017*, 1387–1395. doi:10.1145/3097983.3098021

---

*문서 종료. 검색 수행일 2026-07-25. 모든 서지는 당일 Crossref / arXiv / Semantic Scholar API 및 랜딩 페이지 조회 결과에서 복사했다.*
