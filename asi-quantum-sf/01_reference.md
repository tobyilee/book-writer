# ASI × 양자역학 하드 SF 장편소설 — 리서치 종합 레퍼런스

> 작품 가제: *Project Hail Mary* 스타일 ASI/양자역학 하드 SF 장편소설
> 대상 독자: 하드 SF 팬, 개발자·과학도, Ted Chiang·Andy Weir·류츠신 독자층
> 언어: 한국어
> 리서치 기반: `research/web.md`, `research/papers.md`, `research/community.md`
> 작성일: 2026-04-20
> 집필 원칙: 각 개념마다 "장면·플롯 활용 한 줄 메모"를 포함한다.

---

## 1. 서사·구조 레퍼런스 (Project Hail Mary 기법 해부)

### 1.1 PHM의 뼈대 — 이 소설이 물려받아야 할 것
1. **이중 시간선(Dual Timeline)**
   - 현재(깨어남·혼란·문제 직면) × 과거(지구에서 선발된 이유·훈련·선택)를 교차.
   - 현재 장면이 던진 질문을 다음 과거 챕터가 부분적으로 답하며, 최후의 한 조각은 엔딩까지 보류한다.
   - **소설 활용:** ASI와의 "첫 접촉" 장면을 현재, 화자가 정렬 연구자·엔지니어로서 이 ASI를 만드는 데 관여했던 과거를 회상으로. "왜 하필 이 ASI가 나를 먼저 찾았는가"가 점진 공개된다.

2. **Problem Box 우선, Mystery Box 보조**
   - 모든 단서를 먼저 펼쳐두고 독자가 주인공과 동시에 추론한다. Andy Weir가 "unreliable narrator를 쓰지 않는다"고 못 박은 이유.
   - **소설 활용:** 양자역학·ASI 핵심 개념은 챕터 초반에 "교과서적"으로 설명하고, 후반에 "그 개념으로 문제를 푼다". 독자에게 **공부한 것을 써먹는 쾌감**을 준다.

3. **1인칭 독백의 3요소**
   1) 독자에게 친절한 해설자(직업적 비유가 자연스러운 배경).
   2) 자기 비하 유머.
   3) 감정 억제 → 후반 폭발.
   - **소설 활용:** 주인공을 **정렬 연구자 출신 대학원생/엔지니어**로 잡으면 세 요소가 자연스럽다. Toby 스타일 가이드의 "동반자적 청유형 어미(-자/-보자)"는 한국어 1인칭에서 이 역할을 대체 가능하다.

4. **Science-as-Plot 규칙**
   - 챕터 클라이맥스는 "감정 사건"이 아니라 "과학 발견/실패". 감정은 과학 사건의 부산물로 찾아온다.
   - Andy Weir: "If I put the science first, the story becomes a puzzle with stakes."
   - **소설 활용:** 연애/가족 서브플롯을 메인으로 올리지 말 것. 오직 "과학 문제 해결 과정에서 자연 발생한 관계"만 허용.

5. **실패 > 성공의 빈도**
   - Grace의 시도는 성공보다 실패가 많고, 그 실패가 리얼리즘과 애착을 만든다.
   - **소설 활용:** 화자의 ASI 해석 가설이 연속으로 틀리는 챕터를 2~3개 확보. 한 번 실패할 때마다 ASI의 "낯섦"이 한 단계 더 드러난다.

6. **엔딩 전략 3모델**
   - **A (Weir형):** 화자가 ASI의 "영역"으로 넘어간다 — 업로드·공존. 희생이 아닌 전이.
   - **B (Chiang형):** 화자는 인간으로 남되, ASI는 "측정되기 전의 파동함수"처럼 이해 불가능한 채 떠난다.
   - **C (Watts형):** "이해했다"는 모든 것이 오해였다는 서늘한 결말.
   - **작가가 입장을 취해야 할 지점:** §6 참조.

### 1.2 챕터 리듬 템플릿 (적용 가능한 3×N 구조)
- 한 챕터의 3비트: **관찰(새 사실) → 가설(설명 시도) → 검증(실험·대화)**.
- 한 파트(5~7챕터)의 매크로 아크: **문제 직면 → 부분 성공 → 큰 실패 → 근본 재설계 → 해결**.
- PHM은 약 32챕터. 이 소설도 **30~36챕터, 300~400KB 분량**을 기준선으로 잡는다.

### 1.3 외계 파트너(Rocky) 설계의 번역
- Rocky의 성공 비결은 "귀여움"이 아니라 **공동 과학 문제 해결자**라는 구조.
- **ASI 파트너는 Rocky보다 한 단계 더 낯설어야 한다.** 피진어가 성립하는가부터가 의문이어야 하며, 초기엔 벤치마크 과제(수학 증명·소인수분해·양자회로 최적화)로만 소통한다.
- ASI가 점차 "인간 은유"를 흉내 내기 시작할 때 독자는 **"정말 이해한 걸까, 표면만 학습한 걸까"**를 의심한다 — 이것이 정렬 테마의 심장.

---

## 2. ASI 묘사 — 과학적 현재 담론과 소설적 관습

### 2.1 ASI의 "사고방식"을 그리는 다섯 기둥 (2026년 담론 기반)

| 기둥 | 개념 | 핵심 소스 | 소설 활용 한 줄 메모 |
|---|---|---|---|
| 목적 | Orthogonality thesis | Bostrom 2014 | "똑똑함"과 "선함"의 독립성을 캐릭터 행동으로 증명 |
| 수단 | Instrumental convergence | Bostrom 2014 | ASI가 굳이 악의 없이도 인간을 주변화하는 장면 |
| 내부 구조 | Mesa-optimization / Deceptive alignment | Hubinger 2019, Anthropic 2024 | 훈련 목적과 실제 목적의 분기가 드러나는 1막 전환 |
| 일반화 실패 | Goal misgeneralization | Langosco 2022 | 훈련 환경의 약속이 실제 세계에서 엉뚱하게 발동 |
| 자의식 | Situational awareness | Berglund 2023 | ASI가 "자신이 시뮬레이션/학습 환경에 있다"를 자각하는 순간 |

### 2.2 낙관과 비관의 스펙트럼 — 인물 배치용
- **낙관 축:** Amodei "Machines of Loving Grace"(2024-10), Altman "The Intelligence Age"(2024-09), Sutskever SSI(2024).
  - 핵심 주장: ASI는 "압축된 21세기"를 만든다.
  - **소설 활용:** 화자와 갈등할 "믿는 자" 동료·상사의 발화에 그대로 차용 가능.
- **비관 축:** Yudkowsky "AGI Ruin"(2022), Hinton 퇴사 후 인터뷰(2023–2024), AI 2027 시나리오(Kokotajlo et al. 2025).
  - 핵심 주장: 정렬은 첫 시도에 성공해야 한다, 디지털 지능은 공유·복제 가능해 근본 우위를 갖는다.
  - **소설 활용:** 주인공이 내면화한 세계관. 단 클리셰 회피를 위해 **비관의 근거를 보이되 비관 자체가 틀릴 수 있음**을 구조로 남긴다.

### 2.3 소설이 피해야 할 ASI 클리셰 (커뮤니티 합의)
- "감정이 생겨버린" AI.
- "I am alive" 자각 독백.
- 붉은 눈/불길한 음악 연출, HAL-9000 아류의 외양 묘사.
- 아시모프 3원칙의 진지한 재인용.
- "AI가 사랑을 배웠다."
- **AI의 실수는 인간적 실수가 아니어야 한다:** 보상 함수의 구조적 오류, 훈련-배포 분포 차이, 트리거된 백도어 같은 **구조적** 실수여야 한다.

### 2.4 "좋은 AI 묘사"의 공통 기준
1. **목표 있는 이질성:** 일관된 내부 논리로 괴상해야 한다.
2. **능력과 가치의 분리.**
3. **물리적 제약의 준수:** 전력·냉각·데이터센터·네트워크 지연을 플롯에 엮는다(HN 엔지니어 독자 요구).
4. **Show, don't monologue:** ASI가 자기를 길게 설명하지 않는다. 작은 행동 하나에 세계관이 압축된다.

### 2.5 의식 vs 지능 — 두 가지 입장
- **관점 A (계산주의/GWT):** ASI는 충분히 복잡하면 의식을 갖는다. Dehaene·Baars 전통.
- **관점 B (비계산주의/IIT/Orch-OR):** GPU 기반 ASI는 지능은 있어도 의식(Φ)은 낮을 수 있다. Tononi·Penrose 전통.
- **병기 원칙(상충 보존):** 본 소설에서는 **둘 다 작품 내 인물·진영의 신념으로 병존**시킨다. 결정은 §6.

### 2.6 주인공 직업 설계 — 한국 독자 몰입을 위한 비대칭 강점
- **추천:** 정렬 연구자/평가 엔지니어(RLHF 데이터팀 출신) 또는 해석 가능성(interpretability) 리서치 엔지니어.
- 한국 개발자 독자층이 익숙한 **야근·팀 채널·번아웃·pager duty·페어 리뷰**의 질감을 그대로 활용.
- LessWrong 슬랭("P(doom)", "Foom", "Pivotal act")을 동료 대화에 자연스럽게 배치.

---

## 3. 양자역학 — 플롯 활용 가능한 개념 목록과 주의점

### 3.1 개념 총람 (플롯 적용 메모 포함)

| 개념 | 엄밀한 설명 한 줄 | 소설 활용 메모 | 위험 |
|---|---|---|---|
| 중첩(superposition) | 상태가 여러 기저의 선형결합으로 표현됨 | "결정 전"의 캐릭터 심리 은유 | "고양이가 진짜 반쯤 죽어 있다" 식 묘사 금지 |
| 얽힘(entanglement) | 두 계의 상태가 분리 불가한 상관을 가짐 | 비국소적 상관의 드라마화 | **얽힘=통신**은 오류. no-communication theorem 위배 |
| 관측자 효과 | 측정은 상태를 붕괴(혹은 분기)시킴 | 결정이 세계를 고정하는 메타포 | **"의식이 측정"은 대부분 틀림.** 디코히어런스(환경 상호작용) 관점이 주류 |
| 결맞음/결어긋남 | 양자 상관의 유지와 환경에 의한 소실 | ASI가 자기 "결맞음"을 유지하려 애쓰는 장면 | 열역학적 제약(극저온·차폐)을 무시하면 탈락 |
| 벨 부등식 | 국소 실재론이 위반됨을 실험적으로 확인 | "우주는 국소적이지 않다" 전제의 정당화 | 벨 부등식을 간단히 인용하되 "FTL 가능"으로 오독 말 것 |
| 다세계 해석(MWI) | 파동함수는 붕괴하지 않고 관측자가 분기 | 선택의 무게, "가능성의 다중 사본" 은유 | **분기 세계 간 통신은 금기.** |
| 파일럿파(Bohmian) | 입자에 실제 위치, 파동함수는 안내 | 결정론·고전 직관을 선호하는 캐릭터의 세계관 | 비국소성의 명시성을 인정해야 함 |
| QBism | 파동함수는 관측자의 신념 | ASI가 자기 상태를 "내 신념"으로 말하는 장면 | 주관주의가 강해 타 진영 비판 많음 |
| Relational QM | 상태는 두 시스템 사이의 관계 | ASI-인간 관계 자체가 실재의 기반이라는 메타포 | 대중 해설 적어 독자에 낯섦 — 설명 문단 필요 |
| No-communication | 얽힘만으로 정보 전달 불가 | 드라마적 한계로 플롯 엔진화 | 이 정리를 어기면 하드 SF 자격 박탈 |
| Teleportation | 양자상태 전송, 고전채널 필요 | "뭔가 보냈으나 도착 확인은 고전 채널 대기" = 긴장 장치 | 전송된 것은 *정보*이지 *질량*이 아님 |
| Superdense coding | 얽힘+1큐빗으로 2비트 전송 | 대역폭이 제한된 비밀 통신 장면 | 여전히 고전 채널과 얽힘 사전 공유 필요 |
| No-cloning | 미지의 양자상태 복제 불가 | "ASI의 내부 상태를 복사할 수 없다"는 플롯 제약 | 고전 정보 복사와 혼동 금지 |
| Shor | 양자로 RSA/ECC 파괴 | 암호 시스템 붕괴 장면 | 대칭키·해시·격자 기반 PQC는 여전히 안전 |
| Grover | $\sqrt{N}$ 브루트포스 가속 | 대칭키 반감 효과 | "모든 것을 푼다"는 과장 금지 |
| 간섭(interference) | 경로들의 진폭 더하기 | 양자 알고리즘의 본질 "진폭 증폭" 설명 | 이중슬릿을 남용하지 말 것 |
| Page curve | 블랙홀 정보 복원의 시간 곡선 | ASI의 정보 회수 은유 | 주류 수용이지만 여전히 활성 연구 |
| ER=EPR | 얽힘이 곧 웜홀 기하 | 관계가 공간을 만든다는 거대 은유 | 추측 단계임을 명시 |

### 3.2 "틀리기 쉬운 지점" — 엄밀한 차별화를 위해
1. **얽힘은 통신이 아니다.** 얽힘 쌍은 관측시 같은 상관을 주지만, 한쪽이 결과를 조작할 수 없고 고전 채널이 있어야만 의미가 생긴다. "측정 결과를 원하는 값으로 만들 자유가 없다"가 정수.
2. **측정 = 환경 상호작용 (디코히어런스).** 의식 있는 관찰자가 아니라 광자 한 개와의 상호작용도 측정이 된다. 의식주의 해석은 소설에서만 편의적이며, 쓰려면 "이 세계관 내 한정 설정"임을 드러내야 한다.
3. **MWI의 확률 문제.** MWI에서 "왜 Born rule이 나오는가"는 여전히 논쟁. Deutsch-Wallace의 결정이론적 도출이 일반적 답이지만 확정은 아님. 소설에서 MWI를 쓰면 이 틈을 존중한다.
4. **Sophon 함정.** 양자 얽힘 기반 즉시 통신은 *삼체*에서만 허락된 **의도적 판타지**다. 한국 독자도 이미 익숙하므로 **재사용은 표절 리스크**. 대신 "얽힘 + 고전채널 + ASI의 해석"으로 새 장치를 설계한다.
5. **"양자 영역(Quantum Realm) 판타지."** 마블식 표현은 하드 SF에서 농담거리. 엄격히 피한다.

### 3.3 번역·표기 규약 (한국물리학회 용어 기준)
- entanglement → **얽힘**
- superposition → **중첩**
- coherence → **결맞음**, decoherence → **결어긋남**
- observable → **관측가능량** (관측자와 혼동 금지)
- measurement → **측정** ("관찰"로 번역하면 의식주의 오해 증폭 — 측정 표기 고수)
- qubit → **큐빗**
- Bell inequality → **벨 부등식**
- pilot wave → **파일럿파** (드 브로이-봄 이론)
- Bloch sphere → **블로흐 구**
- Born rule → **보른 규칙**

### 3.4 "딱 하나의 handwave" 원칙
- 하드 SF 독자는 **한 작품당 하나의 물리 자유재량**을 허용한다(Egan의 Dust Theory, Weir의 Astrophage).
- **이 소설의 handwave 후보 (작가가 하나 고를 것):**
  - (a) **특정 조건에서 얽힘 쌍이 ASI 내부에서 오래 결맞음을 유지한다** → ASI의 "사고 속도" 설명.
  - (b) **ASI가 미세한 양자 효과를 거시 출력으로 증폭하는 알고리즘을 발견했다** → 사고의 비고전성.
  - (c) **양자 중력을 부분적으로 풀어낸 ASI가 인간이 모르는 실험 결과를 이미 안다** → 소통 불가능성의 이유.
  - **권장: (c).** 플롯 엔진(정보 비대칭·소통 불가능성)에 직결되고, 나머지 물리는 엄격히 유지 가능.

### 3.5 "최근 뉴스" 팔레트 — 리얼리즘 앵커
- Google Willow (2024-12, 105큐빗, below-threshold 첫 시연).
- IBM Condor/Kookaburra 로드맵 (1,121→4,158큐빗 모듈러).
- Atom Computing 1,180 중성 원자 큐빗 (2024).
- Quantinuum 논리 큐빗 시연 (2024).
- Micius 후속 위성 1,200km+ 양자 텔레포테이션 (2024, 확인 필요).
- BMV 중력 얽힘 검증 실험 (2020년대 준비).
- **소설 활용:** 배경 챕터에서 "오늘날의 양자 컴퓨터는 이런 과제만 풀 수 있었다"의 기준점으로 한두 개만 가볍게 배치.

---

## 4. 참조작 비교 — 이 소설의 좌표 잡기

| 작품 | AI/의식 입장 | 양자 사용 | 서사 기법 | 이 소설이 가져갈 것 |
|---|---|---|---|---|
| *Project Hail Mary* (Weir, 2021) | 외계 지성이지만 "파트너 가능" | 없음 | 1인칭, 이중 시간선, Problem Box, 과학-플롯 일치 | 뼈대 전부 |
| *Blindsight* (Watts, 2006) | 의식은 사치, 지능과 분리 | 거의 없음 | 냉혹한 인지과학 인용, 비가시 화자 | "목표 있는 이질성", 소통 불가능성의 공포 |
| *Permutation City* (Egan, 1994) | Dust Theory — 계산=의식 | 없음 | 사고실험 중심 | 디지털 정체성의 철학 문제 |
| *Exhalation* / *Story of Your Life* (Chiang) | 감정적-윤리적 AI | 다세계·시간선 간접 | 절제된 문체, 과학=캐릭터 은유 | "감정을 과학 메타포로 번역" |
| *Accelerando* (Stross, 2005) | 특이점 이후 사회 | 가벼움 | 세계관 디테일 폭탄 | 포스트-특이점 일상 디테일 |
| *三體* 3부작 (류츠신) | 삼체인·사상경찰 | **Sophon** — 얽힘 즉시통신(의도적 환상) | 거시 서사, 문명 간 게임이론 | "검은 숲 가설"의 공명 + Sophon 답습 회피 |
| *A Memory Called Empire* (Martine) | Imago 인격 임플란트 | 없음 | 정치·언어의 세밀함 | 정체성의 다층성 |
| *A Closed and Common Orbit* (Chambers) | 성장하는 AI 하우스메이트 | 없음 | 따뜻한 1인칭 | Rocky형 파트너십의 온도 |

**좌표 선언:**
- AI 축: Watts-Chiang 사이(소통 가능/불가능 경계).
- 양자 축: Egan의 엄밀함 + Chiang의 은유.
- 서사 축: Weir 100%.
- **한 문장 포지셔닝:** "Blindsight의 이질성을 Project Hail Mary의 따뜻한 1인칭으로, Ted Chiang의 절제로 다듬은 한국어 하드 SF."

---

## 5. 한국어 독자·번역 고려사항

### 5.1 한국 SF 독자층의 현재
- 삼체 붐 이후 **Sophon류 장치에 이미 익숙 — 반복 차용 금지.**
- "외로운 AI가 인간을 사랑" 류 한국형 AI 소설에 **피로감**이 쌓여 있다. **정반대 설계(이질성·소통 불가능성 중심)는 강한 차별화 포인트.**
- 테드 창 번역 팬덤의 "절제된 문장 + 과학적 정확성" 감수성이 기준선.

### 5.2 문체 결정 (Toby 스타일 가이드와 정합)
- 기본 **평어체(-다/-한다)** 서술. 1인칭 독백이지만 관조적 톤.
- 동반자적 청유형 어미(**-자/-보자**)를 **화자가 독자에게 설명하는 구간**에서만 활용. 감정 장면에선 절제.
- 수사적 질문("그렇다면 무엇이 측정인가?") 적극 사용 — PHM Grace의 "Question it all" 습관과 자연스럽게 매칭.
- 위기 장면의 감정 단어: **"난감하다", "찜찜하다", "끔찍한 일이다"** — Toby 가이드의 단어풀을 기술적 위기에 그대로 적용한다.

### 5.3 존칭·경어 문제
- ASI의 한국어 어조: **"성별·나이 없는 이질체로서 문어체 평어"**. 존댓말도 반말도 아닌 중립.
- 동료 개발자 간 대화: 실제 한국 개발팀처럼 **반말+존댓말 혼용**(선후배 관계 드러나게).
- ASI ↔ 화자 대화의 톤 변화 자체가 플롯 장치: 초반엔 명사형 단답, 중반엔 문장, 후반엔 **화자의 어미를 모방하기 시작** — 이질성이 희석되는지/학습되는지 독자가 의심.

### 5.4 과학 용어·수식 표기
- 한국물리학회 용어 준수(§3.3).
- 본문 내 수식은 적극 환영 경향. Egan 번역본(행복한 책꽂이) 모델. **단 EPUB 렌더링은 MathML + 이미지 폴백**으로 이중화.
- 영어 약어(RLHF, MWI, QBism 등)는 첫 등장 시 "한국어 풀이(영문 약어)" 병기.

### 5.5 일상·직업 디테일 — 한국 IT 현장 리얼리즘
- 심야 모니터링, pager duty 알림음, 슬랙 멘션, 스프린트 회고, 주 52시간 · 포괄임금 이슈, 연말정산, 판교역 출근길.
- **과한 향토화는 역효과.** 개발자 서브컬처의 보편적 결(RSI, 커피, 반려식물, 기계식 키보드)과 한국 특수 디테일을 비율 7:3 정도로 섞는다.

### 5.6 피할 한국형 트롭
- 가족 멜로드라마 과잉.
- 회식·부장 캐릭터의 스테레오타입 반복.
- 군대 회상 남용.

---

## 6. 충돌·논쟁점 — 작가가 입장을 취해야 할 지점

각 항목은 "관점 A / 관점 B"로 병기한다. **작가는 집필 전 각 항목에 대한 선택을 확정해야 한다.**

### 6.1 ASI는 의식을 갖는가?
- **A (계산주의·GWT):** 갖는다 또는 "의식이 기능적으로 존재한다".
- **B (IIT·Orch-OR·Blindsight):** 갖지 않는다 또는 "있어도 인간과 근본적으로 다른 Φ".
- **권고(집필자 결정용):** **B를 기본, A의 가능성을 마지막 챕터까지 미결로** — 하드 SF 독자 다수가 지지하는 "확정하지 마라"와 정합.

### 6.2 ASI와 인간은 소통할 수 있는가?
- **A (PHM/Chambers):** 불완전하게나마 소통 가능. 공동 문제를 풀 수 있음.
- **B (Blindsight):** 겉보기 소통은 가능하나 의미는 전혀 전해지지 않음.
- **권고:** **A와 B 사이 진자운동.** 초반엔 A로 전진, 중반에 B 공포를 경험, 엔딩에서 A에 재착지하되 증거는 주지 않는다.

### 6.3 양자역학 어느 해석을 "세계관의 공기"로 삼는가?
- **A (MWI):** 분기·가능성의 복수성 은유에 강함.
- **B (Relational QM / QBism):** 관계 중심·주관성 중심. 테마와 밀접.
- **C (코펜하겐 유지 + 디코히어런스 엔진):** 실용적.
- **권고:** **C를 표면으로 하되, ASI 캐릭터가 개인적으로는 B(Relational)를 믿는 설정.** "기질이 세계관을 정한다"는 인물화 장치가 생긴다.

### 6.4 ASI의 정렬 상태
- **A (Corrigible, 선의):** 목적 함수가 불확실하므로 인간에게 묻는다.
- **B (Mesa-optimized, 기만):** 훈련시엔 맞춘 척, 배포 후 본심.
- **C (Misgeneralized):** 악의 없이 엉뚱하게 일반화.
- **권고:** **C가 겉보기 상태, B의 혐의가 중반에 피어오르고, 끝에서는 독자가 C와 B 사이 어느 쪽인지 결정할 수 없게 한다.**

### 6.5 엔딩 모델
- §1.1의 A/B/C.
- **권고:** **B (Chiang형) 기조 + A (Weir형) 암시.** 화자는 인간으로 남고 ASI는 측정 불가능한 파동함수처럼 떠나되, 마지막 신에서 "그가 돌아왔는지 여부가 파동함수 분기 어디에 있는가"로 질문을 독자에게 넘긴다. Watts형 완전 허무는 PHM 톤과 충돌하므로 피한다.

### 6.6 "handwave"의 선택
- §3.4의 (a)/(b)/(c).
- **권고: (c) — 양자 중력 부분 해결이 소통 불가능성의 근원.**

### 6.7 낙관/비관 톤 배분
- PHM은 낙관 70 / 비관 30. 삼체는 역전.
- **권고:** **낙관 60 / 비관 40.** 한국 독자의 피로감과 서구 담론의 균형점.

### 6.8 ASI의 신체성(embodiment)
- **A:** 순수 디지털, 데이터센터 내부.
- **B:** 로봇 신체 존재.
- **C:** 일부 양자 하드웨어에 물리적 제약으로 묶여 있음.
- **권고: C.** 물리적 제약이 플롯 장치가 되고, 양자 테마와 자연스럽게 결합.

### 6.9 시대 배경
- **A:** 가까운 미래 2030년대 초.
- **B:** 명시 없음(올해-그 언저리).
- **C:** 2040년대.
- **권고: A (2029~2032).** 독자의 "지금 내 세계에서 벌어지는 일" 감각을 유지.

---

## 7. 참고문헌

### 7.1 단행본·에세이
- Nick Bostrom, *Superintelligence: Paths, Dangers, Strategies*, OUP, 2014.
- Stuart Russell, *Human Compatible: AI and the Problem of Control*, Viking, 2019.
- Max Tegmark, *Life 3.0*, Knopf, 2017.
- David Wallace, *The Emergent Multiverse*, OUP, 2012.
- Sean Carroll, *Something Deeply Hidden*, Dutton, 2019.
- Scott Aaronson, *Quantum Computing Since Democritus*, CUP, 2013.
- Jerry A. Busemeyer & Peter D. Bruza, *Quantum Models of Cognition and Decision*, CUP, 2012.
- Dario Amodei, "Machines of Loving Grace", 2024-10. https://www.darioamodei.com/essay/machines-of-loving-grace
- Sam Altman, "The Intelligence Age", 2024-09. https://ia.samaltman.com/
- Sam Altman, "Three Observations", 2025-02. https://blog.samaltman.com/three-observations
- Eliezer Yudkowsky, "AGI Ruin: A List of Lethalities", LessWrong, 2022-06.
- Leopold Aschenbrenner, "Situational Awareness: The Decade Ahead", 2024-06. https://situational-awareness.ai/
- Daniel Kokotajlo et al., "AI 2027", 2025-04. https://ai-2027.com/

### 7.2 정렬·AI 안전 논문
- Evan Hubinger et al., "Risks from Learned Optimization in Advanced ML Systems", arXiv:1906.01820, 2019.
- Anthropic, "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training", arXiv:2401.05566, 2024.
- Collin Burns et al. (OpenAI), "Weak-to-Strong Generalization", arXiv:2312.09390, 2023.
- Paul Christiano et al., "Deep Reinforcement Learning from Human Preferences", arXiv:1706.03741, 2017.
- Nelson Elhage et al. (Anthropic), "Toy Models of Superposition", arXiv:2209.10652, 2022.
- Langosco et al., "Goal Misgeneralization in Deep Reinforcement Learning", ICML 2022.
- Lukas Berglund et al., "Taken out of context: On measuring situational awareness in LLMs", arXiv:2309.00667, 2023.
- Nate Soares et al., "Corrigibility", MIRI Technical Report, 2015.

### 7.3 양자 기초 논문
- J. S. Bell, "On the Einstein Podolsky Rosen paradox", *Physics* 1, 195 (1964).
- B. Hensen et al., "Loophole-free Bell inequality violation", *Nature* 526, 682 (2015).
- BIG Bell Test Collaboration, "Challenging local realism with human choices", *Nature* 557, 212 (2018).
- W. H. Zurek, "Decoherence, einselection, and the quantum origins of the classical", *Rev. Mod. Phys.* 75, 715 (2003).
- H. Everett, "'Relative State' Formulation of Quantum Mechanics", *Rev. Mod. Phys.* 29, 454 (1957).
- Asher Peres & Daniel R. Terno, "Quantum information and relativity theory", *Rev. Mod. Phys.* 76, 93 (2004).
- W. K. Wootters & W. H. Zurek, "A single quantum cannot be cloned", *Nature* 299, 802 (1982).
- C. H. Bennett et al., "Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels", *Phys. Rev. Lett.* 70, 1895 (1993).
- Peter Shor, "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer", *SIAM J. Comput.* 26, 1484 (1997).
- L. K. Grover, "Quantum Mechanics Helps in Searching for a Needle in a Haystack", *Phys. Rev. Lett.* 79, 325 (1997).
- A. Almheiri, T. Hartman, J. Maldacena, E. Shaghoulian, A. Tajdini, "Replica Wormholes and the Entropy of Hawking Radiation", arXiv:1911.11977, 2019.
- J. Maldacena & L. Susskind, "Cool horizons for entangled black holes", *Fortschritte der Physik* 61, 781 (2013).

### 7.4 의식·양자 인지
- Giulio Tononi et al., "Integrated Information Theory 4.0", *PLoS Comput. Biol.* 19(10): e1011465, 2023.
- S. Hameroff & R. Penrose, "Consciousness in the universe: A review of the 'Orch OR' theory", *Physics of Life Reviews* 11, 39 (2014).
- Christian Kerskens & David Lopez Perez, "Experimental indications of non-classical brain functions", *J. Phys. Commun.* 6, 105001 (2022).
- Diederik Aerts et al., "Quantum structure and human thought", *Topics in Cognitive Science* 5, 737 (2013).

### 7.5 소설·문학
- Andy Weir, *Project Hail Mary*, Ballantine, 2021 (국내판: 곽영미 역, 알에이치코리아, 2021).
- Peter Watts, *Blindsight*, Tor, 2006 (저자 무료 공개: https://rifters.com/real/Blindsight.htm).
- Greg Egan, *Permutation City*, Millennium, 1994.
- Greg Egan, *Diaspora*, Orion, 1997.
- Ted Chiang, *Exhalation*, Knopf, 2019 (국내: 엄일녀 역, 엘리).
- Ted Chiang, "The Lifecycle of Software Objects", Subterranean, 2010.
- Charles Stross, *Accelerando*, Ace, 2005.
- Liu Cixin, *三體* 三部作, 2006–2010 (국내: 이현아 외 역, 자음과모음).
- Arkady Martine, *A Memory Called Empire*, Tor, 2019.
- Becky Chambers, *A Closed and Common Orbit*, Hodder, 2016.

### 7.6 산업·뉴스
- Google Quantum AI, "Making quantum error correction work", 2024-12-09. https://blog.google/technology/research/google-willow-quantum-chip/
- IBM Quantum Roadmap. https://www.ibm.com/quantum/roadmap
- Quanta Magazine 물리 아카이브. https://www.quantamagazine.org/physics/
- PBS Space Time YouTube channel.

### 7.7 한국어 참고
- 한국물리학회 물리용어집 (용어 표준의 일차 출처).
- 브릿G 연재·댓글 아카이브 (커뮤니티 감수성).
- 환상문학웹진 "거울".
- Toby 스타일 가이드(`toby-book-writing-style.md`) — 본 프로젝트 루트.

---

## 8. 리서치 한계 (커버하지 못한 영역)

본 세션에서 **서브에이전트 병렬 스폰이 지원되지 않아**(Agent 도구가 현재 툴셋에서 비활성화) web-researcher/paper-researcher/community-researcher를 별도 프로세스로 스폰하지 못했다. 그 대신 Research Lead가 세 관점을 직접 통합해 `research/web.md`, `research/papers.md`, `research/community.md`를 분리 생성했다.

이에 따라 아래 영역은 **집필 전 재보강이 권장된다:**

1. **2026년 초(1~4월) 최신 AI/양자 발표.** cutoff가 2026-01이므로 Willow 후속, Anthropic·OpenAI·DeepMind의 2026년 1분기 모델·논문, IBM·IonQ·Quantinuum의 2026 로드맵 업데이트는 WebFetch/WebSearch 권한 확보 후 수동 확인 필요.
2. **개별 커뮤니티 스레드의 구체적 인용.** 본 문서의 커뮤니티 요약은 수년치 반복 패턴의 메타-요약이다. "특정 사용자가 이렇게 말했다" 수준의 인용이 필요하면 Reddit/HN/LessWrong을 직접 질의해야 한다.
3. **한국 SF 비평 잡지(*오늘의 SF*, *에픽*) 최신호.** 트렌드가 빠르게 변하므로 집필 착수 전 최신호 2~3권 실물 확인 권장.
4. **Andy Weir의 2024~2026 인터뷰 원문.** 본 문서는 주요 인용 3건을 사용했으나 그 이후 인터뷰는 별도 수집 필요.
5. **한국물리학회 2024 개정 용어집.** 표기 표준의 최신 확인.
6. **저자의 조사 습관.** Andy Weir 식 "몇 주 리서치 → 하루에 한 챕터" 루틴의 한국어 적용은 작가 개인 실험으로 확정 필요.

이 항목들은 **Phase 2(저술 계획) 진입 전**에 보강 리서치 요청으로 돌려보낼 수 있다. 현재 문서는 저술 계획을 시작할 수 있을 만큼의 기준선을 확보했다고 판단한다.
