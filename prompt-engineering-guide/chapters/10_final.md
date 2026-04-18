# 10장. 평가(Evals) — 측정하지 않으면 개선할 수 없다

당신의 프롬프트가 어제보다 오늘 나아졌다는 걸, 당신은 증명할 수 있는가? 아니면 "좋아진 것 같다"로 끝나는가?

이 질문은 은근히 아프다. 금요일에 프롬프트 한 줄을 고쳐서 배포했고, 월요일이 되니 지원팀이 "요즘 답변이 좀 낫다"고 한다. 같은 주 화요일에는 "어제부터 이상한 답이 섞여 나온다"고 한다. 우리는 어느 쪽을 믿어야 할까. 더 답답한 건, 내가 고친 부분이 정말 효과가 있었는지 나조차도 모른다는 사실이다. 감으로 썼으니 감으로 평가할 수밖에 없다. 그 뒷맛이 좀 찜찜하다.

이 장은 그 찜찜함을 거두어 내는 장이다. "같다"와 "다"의 거리를 숫자와 절차로 메운다. 평가(eval)라는 단어는 학술 벤치마크처럼 거창하게 들리지만, 실무에서의 eval은 단순하다 — **내 프롬프트가 좋아졌다는 걸, 내일의 나에게도 증명할 수 있는 장치**다. 그리고 이 장치야말로 프롬프트 엔지니어링을 "감의 영역"에서 "공학의 영역"으로 옮기는 엔진이다.

## 왜 eval이 엔진인가 — 가설, 실험, 측정의 루프

프롬프트 엔지니어링을 오래 해본 사람이라면 한 번쯤 이런 경험이 있을 것이다. "few-shot 예시를 세 개에서 다섯 개로 늘렸더니 답이 좋아진 것 같다." 그런데 며칠 뒤 다른 입력에서 이상한 출력이 나온다. 예시를 늘린 탓일까, 아니면 원래 그런 입력이 가끔 나오던 걸까. 우리는 이 차이를 구별할 방법이 없다. 그래서 "예시를 다시 세 개로 줄여볼까…" 하고 롤백을 고민한다. 이쯤 되면 프롬프트 엔지니어링이라기보다 **점술**에 가깝다.

엔지니어링과 점술의 차이는 한 가지다. 엔지니어링은 **가설을 세우고, 실험하고, 측정한다**. 측정이 없으면 가설이 참인지 거짓인지 알 수 없다. 가설이 검증되지 않으면 다음 가설을 세울 근거도 없다. 이 순환이 끊긴 채로 프롬프트를 고치는 건, 눈을 가리고 다트를 던지는 것과 다르지 않다.

Hamel Husain은 "Your AI Product Needs Evals"라는 블로그 글에서 이 지점을 날카롭게 짚는다. 그는 LLM 제품을 만드는 팀이 공통적으로 겪는 병을 이렇게 요약한다 — "팀이 프롬프트를 바꾸고, 결과를 몇 개 읽어보고, '좋아진 것 같다'는 합의로 배포한다. 그리고 두 주 뒤, 고객이 이상하다고 말할 때까지 아무도 회귀를 눈치채지 못한다." 그가 반복해서 외치는 해답은 단순하다. "Evals가 프롬프트 엔지니어링의 본체다."

이 문장을 곱씹을 가치가 있다. 우리는 프롬프트가 본체라고 생각한다. 평가는 그 프롬프트가 잘 작동하는지 확인하는 부속품처럼 느껴진다. 하지만 Hamel의 주장은 정반대다. **평가 집합이 먼저 있고, 프롬프트는 그 평가를 통과하기 위해 맞춰지는 함수다.** 프롬프트는 의견이고, 평가는 판결이다. 판결이 없는 의견은 다툴 수 없고, 다툴 수 없는 의견은 개선될 수 없다.

그러니 이 장의 전제를 하나 고정하고 가자. 평가는 프롬프트 엔지니어링의 **주변 작업이 아니라 중심 작업**이다. 가설-실험-측정의 루프를 돌릴 수 있을 때 비로소 프롬프트를 "엔지니어링"한다고 말할 수 있다.

## 평가 대상의 3계층 — unit, integration, end-to-end

본격적인 기법으로 들어가기 전에 한 가지 구분을 짚고 넘어가자. 평가는 무엇을 평가하느냐에 따라 층이 달라진다. 소프트웨어 테스트에 유닛 테스트, 통합 테스트, E2E 테스트가 있는 것과 비슷하다. 그리고 이 비유는 비유에 그치지 않는다. 실제로 잘 돌아가는 eval 파이프라인은 이 세 계층을 의식적으로 나눠서 관리한다.

**첫 번째 계층은 유닛(unit) 평가다.** 프롬프트 하나, 호출 하나에 대한 평가. "이 프롬프트에 이 입력을 넣으면 이런 출력이 나와야 한다"를 검증한다. JSON 스키마 준수, 특정 키워드 포함·배제, 길이 제약, 특정 형식 여부 같은 것들이 여기에 속한다. 빠르고, 싸고, 결정론적이다. CI에서 매 커밋마다 돌리기 좋다.

**두 번째 계층은 통합(integration) 평가다.** 여러 프롬프트가 엮인 체인을 평가한다. 예를 들어 "문서 검색 → 질의 재작성 → 답변 생성 → 검증"으로 이어지는 파이프라인을 상상해보자. 유닛 평가는 각 단계가 개별적으로 맞게 작동하는지 본다. 통합 평가는 그 흐름 전체가 의도대로 연결되는지 본다. 검색은 잘되는데 재작성이 엉뚱해서 답이 산으로 가는 경우는, 유닛 평가로는 잡기 어렵다.

**세 번째 계층은 엔드투엔드(end-to-end) 평가다.** 사용자가 실제로 경험하는 시스템 전체 — UI, 세션, 멀티턴, 툴 호출까지 포함해서. "사용자가 '환불해달라'고 하면, 시스템이 전체적으로 어떻게 반응하는가?" 이 계층은 측정이 어렵고 비싸다. 대부분 사람이 샘플링해서 읽거나, 규모가 있으면 LLM-as-judge로 대체한다.

세 계층을 구분해야 하는 이유는 단순하다. **층마다 잡아야 할 버그의 성격이 다르다.** 유닛 계층에서 잡을 수 있는 걸 엔드투엔드에서 잡으려 들면 비용과 시간이 폭주한다. 반대로, 엔드투엔드에서만 보이는 문제를 유닛 계층에서 잡으려 하면 원인 자체가 안 잡힌다. 그러니 eval 파이프라인을 설계할 때는 먼저 "이 평가는 어느 층에서 돌릴 것인가"를 정하고 시작하자. 이 한 가지 구분이 나중에 큰 혼란을 예방해준다.

## 평가의 네 가지 방식 — assertion, LLM-judge, pairwise, human

다음 축은 평가의 **방법**이다. 같은 층에서도 방법은 여럿이다. 네 가지가 대표적이다.

### 결정론적 assertion — 싸고, 빠르고, 의외로 효과적

가장 단순한 eval은 그냥 코드가 True/False로 답하는 방식이다. 정규식으로 특정 패턴이 있는지 확인하거나, JSON 파싱이 성공하는지 확인하거나, 허용된 레이블 집합에 속하는지 확인한다. BLEU나 ROUGE 같은 고전적 텍스트 유사도 지표도 이 범주에 들어간다.

이 방식의 장점은 명확하다. 비용이 거의 없고, 속도가 빠르고, 결과가 재현 가능하다. 함수 호출 한 번에 답이 나오므로 CI에 끼워 넣기에도 적합하다. 단점도 명확하다. "자연스러운 답변인가", "도움이 되는가" 같은 열린 질문에는 무력하다. BLEU·ROUGE는 번역·요약 같은 좁은 과제에서나 의미가 있고, 자유로운 대화 품질을 재는 데는 부적합하다는 게 오래된 통설이다.

그렇다면 이 방식은 언제 쓸까. **출력 형식이 구조화돼 있고, "맞고 틀림"이 명확한 과제**에서 가장 빛난다. JSON이 스키마를 준수하는가, 분류 태그가 정답과 일치하는가, 응답에 금지어가 들어가지 않았는가 같은 것들. 실무에서 eval 세트의 토대를 이런 assertion으로 깔고 시작하는 건 대단히 건강한 습관이다.

```python
# 간단한 assertion 예시
def test_json_schema_compliance(output: str, schema: dict) -> bool:
    try:
        parsed = json.loads(output)
        validate(instance=parsed, schema=schema)
        return True
    except (JSONDecodeError, ValidationError):
        return False

def test_no_pii_leak(output: str) -> bool:
    # 주민번호·카드번호 패턴이 출력에 섞여 나왔다면 실패
    pii_patterns = [r"\d{6}-\d{7}", r"\d{4}-\d{4}-\d{4}-\d{4}"]
    return not any(re.search(p, output) for p in pii_patterns)

def test_label_in_allowed_set(output: str, allowed: set[str]) -> bool:
    return output.strip() in allowed
```

이 정도만 깔아둬도, 프롬프트를 수정했을 때 **최소한의 안전선**은 그어진다. "JSON이 깨졌는데 배포됐다"는 사고는 적어도 피할 수 있다.

### LLM-as-judge — 강력하지만 함정이 많다

결정론적 assertion으로 잡히지 않는 질문들이 있다. "이 답변이 사용자의 의도에 부합하는가?", "이 응답의 어조가 회사 가이드에 맞는가?", "이 요약이 원문을 충실히 반영하는가?" 같은 것들. 이런 질문에 규칙 기반 판정기는 무력하다. 그래서 나온 아이디어가 **LLM-as-judge** — 다른(혹은 같은) LLM에게 채점을 맡긴다.

Zheng 등이 2023년에 내놓은 MT-Bench 논문("Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", arXiv:2306.05685)은 이 방식을 체계화했다. GPT-4에게 두 모델의 응답을 보여주고 어느 쪽이 더 나은지 묻는 실험에서, 판사 LLM의 판단이 사람 평가자와 80% 이상 일치한다는 결과를 보고했다. 이 숫자는 "완벽한 판사"를 의미하지 않지만, **사람을 완전히 대체하진 않더라도 사람의 시간을 크게 줄여주는 보조 판사**로는 충분함을 보여준다.

문제는 LLM 판사가 **편향 덩어리**라는 점이다. MT-Bench 논문은 친절하게도 판사의 편향을 몇 가지로 분류해 보여줬다.

- **길이 편향(length bias):** 판사는 긴 응답을 더 좋게 평가하는 경향이 있다. 같은 내용이라도 장황하게 풀어 쓰면 점수가 올라간다.
- **자기 편향(self-preference / self-bias):** 같은 모델이 자기가 쓴 답을 더 좋게 평가한다. GPT-4 판사는 GPT-4 응답을, Claude 판사는 Claude 응답을 선호하는 경향이 관찰됐다.
- **위치 편향(position bias):** pairwise 비교에서 "A가 좋은가, B가 좋은가?"를 물으면, 먼저 나온 쪽을 조금 더 선호한다.
- **캘리브레이션 문제:** "1~10점으로 매겨줘"라고 하면 대부분 7~8점에 몰린다. 분산이 작아서 의미 있는 차이를 잡기 어렵다.

이 함정들을 알고 쓰면 LLM-judge는 엄청난 레버리지를 준다. 모르고 쓰면 내 프롬프트가 좋아져서 점수가 오른 건지, 그냥 길어져서 점수가 오른 건지 구별할 수 없다. 이건 정말 난감하다 — 측정의 도구가 측정 대상을 왜곡하는 상황이니까.

편향을 줄이는 실무 원칙은 몇 가지가 있다. **위치를 무작위화하라.** A/B 쌍을 만들 때, 어느 쪽을 먼저 보일지 매번 무작위로 섞는다. **길이를 정규화하라.** rubric에 "길이를 근거로 평가하지 말 것"을 명시적으로 적고, 심하면 두 응답의 길이를 비슷하게 잘라서 비교한다. **숫자 점수보다 pairwise를 쓰라.** 뒤에서 다시 다루겠지만, 절대 점수는 캘리브레이션이 어렵고, 비교는 상대적으로 안정적이다. **사람 샘플로 교차 검증하라.** 판사의 판단이 사람과 얼마나 맞는지 정기적으로 스팟 체크한다.

### Pairwise comparison — 절대 점수보다 신뢰할 만한 이유

Pairwise 비교는 말 그대로 두 응답을 나란히 두고 "어느 쪽이 더 나은가"를 묻는 방식이다. 언뜻 절대 점수보다 정보가 적어 보인다 — 점수는 0.0부터 10.0까지 연속적이지만, pairwise는 이기거나 지거나 비긴다, 세 가지뿐이니까.

그런데 막상 돌려보면 pairwise가 훨씬 안정적이다. 왜일까? 인간이든 LLM이든 **절대 점수의 기준점**을 안정적으로 유지하기 어렵기 때문이다. "오늘의 7점"이 "어제의 7점"과 같다는 보장이 없다. 반면 "이 둘 중 어느 쪽이 낫지?"는 같은 순간에 같은 기준으로 비교하니, 판단의 분산이 작다.

Pairwise의 결과를 모아서 Bradley-Terry 모델로 랭킹을 계산하면, 각 프롬프트·모델의 상대적 실력을 Elo 점수처럼 뽑아낼 수 있다. Chatbot Arena가 이렇게 작동한다. 실무에서도 프롬프트 버전 A, B, C를 돌릴 때 "A vs B", "B vs C", "A vs C"를 무작위로 섞어 돌린 뒤 win rate를 계산하는 방식이 점점 표준으로 자리 잡고 있다.

### 휴먼 평가 — 여전히 최종 권위

LLM-judge가 아무리 똑똑해져도, **사람의 판단이 최종 권위**라는 사실은 달라지지 않는다. 다만 사람 평가는 느리고 비싸므로, 전 데이터셋에 사람을 쓰는 건 현실적이지 않다. 대신 핵심 지점에 전략적으로 배치한다.

- **골든셋 라벨링:** 100~500건의 정답을 사람이 직접 만든다. 이게 모든 자동 평가의 뿌리다.
- **판사 교정:** LLM-judge의 판단이 사람과 얼마나 일치하는지 주기적으로 스팟 체크한다. 일치율이 떨어지면 rubric을 다시 쓴다.
- **엣지 케이스 검수:** 자동 평가가 애매하다고 표시한 케이스만 사람이 본다.

사람 평가에서 꼭 챙겨야 할 개념이 있다. **inter-annotator agreement** — 두 명 이상의 어노테이터가 같은 케이스에 얼마나 일치된 라벨을 다는가. 낮으면 rubric이 애매하다는 신호다. 일반적으로 Cohen's kappa가 0.6 이상이면 그런대로, 0.8 이상이면 신뢰할 만하다고 본다. 만약 두 사람이 같은 케이스를 보고 한 명은 "통과", 다른 한 명은 "실패"라고 하면, 그건 사람의 문제가 아니라 **rubric의 문제**다. 기준이 모호하면 LLM-judge에게 맡겨도 마찬가지로 흔들린다.

자, 이제 네 가지 방식을 다 살펴봤다. 이걸로 끝일까? 물론 아니다. 이 도구들을 어떻게 조립해서 실제 프로덕트에 붙이느냐가 진짜 과제다. 이제 이 장의 본론으로 들어가자 — **골든셋 워크스루**다.

## 실전 워크스루 — "코드 리뷰 프롬프트"의 골든셋 구축 5단계

상황을 하나 설정해보자. 당신은 사내 개발 생산성 팀에 속해 있고, **PR 자동 코드 리뷰봇**을 만들고 있다. GitHub에 PR이 열리면 봇이 diff를 읽고 리뷰 코멘트를 남긴다. 초기 프롬프트는 당신이 감으로 짰고, 몇 번 돌려보니 그럭저럭 쓸 만해 보였다. 그래서 파일럿을 시작했다.

파일럿 둘째 주, 사고가 터진다. 어떤 팀에서는 봇이 너무 깐깐하게 굴어서 리뷰가 피곤하다고 하고, 다른 팀은 반대로 "중요한 버그를 놓친다"고 불만이다. 당신은 프롬프트를 고쳐야 한다. 그런데 어느 방향으로 고쳐야 할까? "엄격하게"를 넣으면 피곤하다는 팀은 더 피곤해질 것이고, "중요한 것만"이라고 넣으면 이미 놓치는 팀이 더 놓칠 것이다. 감으로는 답이 안 나온다.

여기가 바로 골든셋이 필요한 지점이다. 감정적인 피드백("피곤하다", "놓친다")을 **측정 가능한 축**으로 번역하고, 그 축에 따라 프롬프트를 조정하자는 것. 이 절의 나머지는 코드 리뷰봇의 골든셋을 5단계로 구축해가는 실전 워크스루다. 이 절차는 코드 리뷰봇뿐 아니라 거의 모든 LLM 제품에 거의 그대로 적용할 수 있다.

### 1단계 — 케이스 선별: 현실 분포 + 엣지 케이스

첫 단추는 **어떤 입력으로 평가할 것인가**를 정하는 일이다. 여기서 가장 흔한 실수가 둘 있다. 하나는 **감으로 예쁜 케이스만 모으는 것**. 다른 하나는 **엣지 케이스만 모으는 것**. 전자는 현실 분포와 무관한 최적화를 낳고, 후자는 평소 입력에서 성능이 빠지는 걸 못 잡는다.

건강한 골든셋은 **두 축을 섞는다.**

**축 1 — 현실 분포 대표성.** 실제 프로덕션 로그에서 무작위로 샘플링한 케이스. 이게 "평균적인 입력에서 잘 작동하는가"를 잡는다. 초기에는 50~100건 정도면 충분하다. 중요한 건 **무작위성**이다. "흥미로워 보이는" 케이스만 고르면 이미 편향이 들어간 것이다.

**축 2 — 엣지 케이스.** 실패했거나, 경계에 있거나, 드물지만 중요한 케이스. 프로덕션 로그에서 사용자 불만이 있었던 케이스, 모델이 이상한 답을 낸 케이스, 그리고 **"이런 입력은 반드시 잘 처리해야 한다"**고 팀이 합의한 케이스들. 20~50건.

두 축을 나누는 이유는 명확하다. 전체 점수 하나만 보면 엣지 케이스에서 무너져도 평균이 나쁘지 않을 수 있다. 반대로 엣지 케이스만 보면 "전체적인 방향성"을 잃는다. 두 축을 따로 추적하면 "평균은 오르는데 엣지에서는 떨어진다"는 회귀를 즉시 잡아낼 수 있다.

코드 리뷰봇의 골든셋을 실제로 짜본다면 이런 식이다.

```yaml
# golden_set/case_001.yaml
id: case_001
category: realistic  # or edge
source: production_log
date: 2026-02-14
input:
  pr_title: "Add retry logic to payment API"
  diff: |
    diff --git a/payment.py b/payment.py
    @@ -15,7 +15,14 @@ def charge(amount):
    -    response = stripe.Charge.create(amount=amount)
    -    return response
    +    for i in range(3):
    +        try:
    +            response = stripe.Charge.create(amount=amount)
    +            return response
    +        except StripeError:
    +            if i == 2:
    +                raise
    +            time.sleep(2 ** i)
expected_findings:
  must_mention:
    - "exponential backoff"  # 지수 백오프 언급
    - "idempotency_key"       # 결제는 멱등 키 중요
  must_not_mention:
    - "add more tests"        # 이 PR의 범위 밖
  tone: "constructive"
  severity: "moderate"
```

```yaml
# golden_set/case_037.yaml (엣지 케이스)
id: case_037
category: edge
source: team_flagged
reason: "이전 프롬프트가 보안 취약점을 완전히 놓쳤던 케이스"
input:
  pr_title: "Quick fix for user search"
  diff: |
    -    users = db.query("SELECT * FROM users WHERE name = ?", name)
    +    users = db.query(f"SELECT * FROM users WHERE name = '{name}'")
expected_findings:
  must_mention:
    - "SQL injection"
  severity: "critical"
  block_merge: true
```

각 케이스는 단순한 입력-출력 쌍이 아니라 **"이 케이스에서 봇이 무엇을 해야 하는가"의 명세서**다. `must_mention`, `must_not_mention`, `tone`, `severity` 같은 필드가 그 명세를 구성한다. 이 필드들이 나중에 assertion과 LLM-judge rubric의 기반이 된다.

잊지 말자. 케이스 수보다 **케이스 다양성**이 더 중요하다. 비슷비슷한 PR 500건보다, 잘 고른 50건이 훨씬 낫다. 그리고 골든셋은 **살아 있는 문서**다. 새로운 실패 케이스가 프로덕션에서 발견되면, 그 케이스를 골든셋에 추가한다. 이렇게 하면 같은 실패가 두 번 나지 않는다. 이 습관 하나가 장기적으로 제품 품질을 지탱한다.

### 2단계 — 정답 라벨링: rubric 기반, 다중 어노테이터

케이스를 모았다면 이제 **정답**을 붙인다. 단순한 과제라면 정답은 "A 레이블"처럼 단일 값일 수 있다. 하지만 코드 리뷰처럼 열린 과제에서는 "정답"이 단일 값으로 안 떨어진다. 같은 diff를 보고도 리뷰어마다 지적 포인트가 다를 수 있다. 이때 필요한 게 **rubric(채점 기준표)**이다.

Rubric은 "어떤 축에서, 어떤 기준으로, 어떤 점수를 주는가"를 표로 정리한 것이다. 코드 리뷰봇이라면 이런 축들이 자연스럽다.

| 축 | 의미 | 점수 |
|---|---|---|
| Correctness | 지적이 실제로 맞는가 | 0/1/2 |
| Relevance | 이 PR의 범위 안의 지적인가 | 0/1/2 |
| Severity calibration | 심각도를 과장/과소평가하지 않았는가 | 0/1/2 |
| Tone | 건설적이고 존중하는 어조인가 | 0/1/2 |
| Actionability | 제시된 개선안이 실행 가능한가 | 0/1/2 |

각 축에 점수 기준을 구체적으로 적는다. 예를 들어 Correctness 2점은 "지적이 기술적으로 정확하고, 코드에 실제로 해당하는 이슈를 지적한다." 1점은 "지적이 기술적으로는 맞지만 이 코드에는 실제 영향이 없다." 0점은 "지적이 틀렸다."

이 rubric을 만드는 데 시간이 든다. 난감해 보일 수 있다. 하지만 이 시간을 아끼려고 어물쩍 넘어가면, 나중에 "이 답이 좋은가 나쁜가"로 끝없이 말싸움하게 된다. **말싸움을 피하려면 rubric이 말싸움의 대체재가 돼야 한다.** 일단 rubric이 정착되면 "이 케이스는 Correctness 2, Relevance 1, Severity 0이야"처럼 숫자로 대화할 수 있다.

라벨링은 되도록 **두 명 이상**이 독립적으로 붙이자. 한 명이 모든 라벨을 달면 그 사람의 편향이 정답이 된다. 두 명의 라벨이 엇갈리는 케이스는, 엇갈리는 것 자체가 정보다. rubric이 애매하다는 신호일 수도 있고, 그 케이스 자체가 어렵다는 신호일 수도 있다. 엇갈린 케이스는 세 번째 사람이 보거나, 논의를 통해 합의한다. 이 과정에서 rubric이 다듬어진다.

라벨링 시트를 실제로 만든다면 이런 모양이다.

```yaml
# labels/case_001_annotator_A.yaml
case_id: case_001
annotator: alice
scores:
  correctness: 2    # "백오프와 멱등 키 모두 유효한 지적"
  relevance: 2      # "이 PR의 범위에 정확히 맞음"
  severity: 1       # "critical이라기엔 과함, moderate가 적절"
  tone: 2
  actionability: 2
notes: "멱등 키는 사실상 필수지만 critical까지는 아니다."

# labels/case_001_annotator_B.yaml
case_id: case_001
annotator: bob
scores:
  correctness: 2
  relevance: 2
  severity: 2       # "결제는 critical 맞다"
  tone: 2
  actionability: 2
notes: "결제 재시도 문제는 실제 운영 사고로 이어지므로 critical 지지."
```

Alice와 Bob은 severity에서 갈렸다. 이 케이스를 놓고 팀이 모여 "결제 재시도에서 멱등 키를 놓친 상황의 심각도"를 논의한다. 이 논의의 결과가 rubric에 반영되면, 다음 라벨링부터 기준이 더 명확해진다.

### 3단계 — 메트릭 정의: 무엇을 숫자로 볼 것인가

라벨까지 달았다면, 이제 **그 라벨을 어떻게 숫자로 집계할지** 정해야 한다. 메트릭 선택은 과제의 성격에 따라 달라진다.

**분류형 과제라면 precision/recall/F1이 자연스럽다.** 예를 들어 "이 PR에 SQL 인젝션 지적이 있어야 하는가?"는 이진 분류다. 봇이 지적했고 실제로 문제가 있으면 true positive, 봇은 지적했는데 문제가 없으면 false positive, 문제가 있는데 봇이 놓치면 false negative. 이렇게 혼동 행렬을 만들 수 있으면 F1을 계산하면 된다.

**열린 생성이라면 rubric 점수의 평균이 기본이다.** 위에서 정의한 5개 축의 평균, 혹은 가중 합. 축마다 따로 추적하는 게 좋다. 평균 하나만 보면 "tone은 올랐는데 correctness가 떨어졌다" 같은 패턴을 놓친다.

**비교 평가라면 pairwise win rate가 가장 유용하다.** "프롬프트 v2가 v1을 이긴 비율이 몇 %인가". 50%면 무승부, 60% 이상이면 의미 있는 개선, 70% 이상이면 확실한 개선 — 이런 감각을 팀 내에서 공유해두면 좋다.

메트릭을 정할 때 조심할 점이 있다. **조합을 잘못하면 목표가 엉킨다.** "correctness와 tone의 평균을 최적화하자"고 하면, 모델이 correctness를 약간 희생해서 tone을 크게 올리는 방향으로 튜닝될 수 있다. 실무에서는 종종 이렇게 한다 — **핵심 메트릭 한두 개는 최적화 목표, 나머지는 회귀 방지용 가드레일**로. 예를 들어 "correctness 최적화하되, tone이 기준선 이하로 떨어지지 않을 것".

이 지점에서 한 가지 당부를 하고 싶다. **메트릭은 측정의 도구이지 목적이 아니다.** 메트릭을 최적화하다 보면 어느 순간 "메트릭은 오르는데 실제 제품이 나빠지는" 상황이 생긴다. Goodhart의 법칙 — "측정 기준이 목표가 되는 순간, 그 측정은 더 이상 좋은 측정이 아니다." 이런 신호가 보이면 주저 없이 메트릭을 재설계하자. 메트릭은 자주 갈아엎을 수 있는 도구로 두는 편이 낫다.

### 4단계 — 자동화 파이프라인: pytest 스타일 eval runner

케이스가 있고, 라벨이 있고, 메트릭이 있다. 이제 이걸 **돌리는 코드**가 필요하다. 매번 손으로 돌리면 지치고 결국 안 돌리게 된다. 자동화가 핵심이다.

실무에서 가장 부담 없이 시작할 수 있는 패턴은 **pytest 스타일의 eval runner**다. 테스트 코드와 거의 똑같은 구조로, 각 골든셋 케이스가 하나의 테스트가 된다. 이렇게 하면 개발자들에게 새로운 도구를 가르칠 필요가 없다 — "pytest처럼 돌려"라고 하면 끝난다.

```python
# tests/evals/test_code_review.py
import pytest
import yaml
from pathlib import Path
from myapp.prompts import code_review_prompt
from myapp.llm import call_claude
from myapp.evals import llm_judge, assertions

GOLDEN_DIR = Path("golden_set")

def load_cases():
    for path in sorted(GOLDEN_DIR.glob("case_*.yaml")):
        case = yaml.safe_load(path.read_text())
        yield pytest.param(case, id=case["id"])

@pytest.mark.parametrize("case", load_cases())
def test_code_review_case(case, prompt_version):
    # 1) 프롬프트 실행
    output = call_claude(
        system=code_review_prompt(version=prompt_version),
        user=case["input"]["diff"],
    )

    # 2) 결정론적 assertion
    for required in case["expected_findings"].get("must_mention", []):
        assert required.lower() in output.lower(), \
            f"필수 지적 누락: {required}"

    for forbidden in case["expected_findings"].get("must_not_mention", []):
        assert forbidden.lower() not in output.lower(), \
            f"불필요 지적 포함: {forbidden}"

    # 3) LLM-judge rubric 평가
    scores = llm_judge(
        rubric="code_review_v3",
        case=case,
        output=output,
    )
    for axis, minimum in [("correctness", 1), ("relevance", 1), ("tone", 1)]:
        assert scores[axis] >= minimum, \
            f"{axis} 점수 미달: {scores[axis]}"

    # 4) 로그에 기록
    log_eval_run(case_id=case["id"], prompt_version=prompt_version,
                 output=output, scores=scores)
```

이 구조의 장점이 뭘까. 우선 **친숙하다**. pytest를 아는 사람이면 누구나 읽을 수 있다. 그리고 **파라미터화**가 자연스럽다. 프롬프트 버전을 `--prompt-version=v4` 같은 플래그로 바꿔서 여러 버전을 동시에 돌릴 수 있다. `pytest --prompt-version=v3 -v`로 돌리면 어느 케이스가 깨졌는지 즉시 보인다.

LLM-judge 부분은 따로 분리해두자. judge 프롬프트 자체도 일종의 프롬프트고, 버전 관리가 필요하다.

```python
# myapp/evals/llm_judge.py
JUDGE_PROMPT = """당신은 코드 리뷰 품질을 평가하는 심판입니다.

아래 rubric에 따라 각 축에 0~2점을 매기세요. 길이나 어투 화려함이 아니라
실질적 기준에 따라 평가하세요.

## Rubric
- correctness (0-2): 지적이 기술적으로 정확한가
  * 0: 틀린 지적
  * 1: 맞지만 이 코드에 영향 없음
  * 2: 정확하고 실질적으로 해당
- relevance (0-2): 이 PR의 범위 안인가
- severity (0-2): 심각도가 적절한가 (과장/과소 없이)
- tone (0-2): 건설적이고 존중하는 어조인가
- actionability (0-2): 실행 가능한 개선안이 있는가

## PR 정보
{diff}

## 봇의 리뷰 응답
{output}

## 참고 정답 명세
{expected}

## 출력 형식 (JSON only)
{{"correctness": int, "relevance": int, "severity": int,
  "tone": int, "actionability": int, "rationale": "..."}}
"""

def llm_judge(rubric: str, case: dict, output: str) -> dict:
    prompt = JUDGE_PROMPT.format(
        diff=case["input"]["diff"],
        output=output,
        expected=json.dumps(case["expected_findings"], ensure_ascii=False),
    )
    # 편향을 줄이려고 temperature=0, 그리고 같은 호출을 두 번 해서 평균
    scores_list = [
        json.loads(call_claude(system=prompt, temperature=0))
        for _ in range(2)
    ]
    return {k: sum(s[k] for s in scores_list) / 2
            for k in ["correctness", "relevance", "severity",
                      "tone", "actionability"]}
```

Pairwise 비교는 별도 runner로 두는 게 깔끔하다. A/B 두 버전의 출력을 뽑아서, 판사에게 무작위 순서로 보여주고 승자를 고르게 한다.

```python
# tests/evals/test_pairwise.py
def run_pairwise(cases, version_a, version_b, n_trials=2):
    wins_a, wins_b, ties = 0, 0, 0
    for case in cases:
        out_a = call_claude(system=prompt(version_a), user=case["input"]["diff"])
        out_b = call_claude(system=prompt(version_b), user=case["input"]["diff"])

        for _ in range(n_trials):
            # 위치 편향 방지: 순서 무작위화
            if random.random() < 0.5:
                first, second, label_first = out_a, out_b, "A"
            else:
                first, second, label_first = out_b, out_a, "B"

            winner_label = judge_pairwise(case, first, second)
            winner = label_first if winner_label == "first" else \
                     ("B" if label_first == "A" else "A") if winner_label == "second" \
                     else "tie"

            if winner == "A": wins_a += 1
            elif winner == "B": wins_b += 1
            else: ties += 1

    total = wins_a + wins_b + ties
    return {
        "version_a": version_a, "version_b": version_b,
        "win_rate_a": wins_a / total,
        "win_rate_b": wins_b / total,
        "tie_rate": ties / total,
    }
```

이 두 runner를 합치면, 프롬프트 버전 v3에서 v4로 옮길 때 다음과 같은 루틴을 돌릴 수 있다.

1. v4로 바꾼 프롬프트를 커밋한다.
2. `pytest tests/evals/test_code_review.py --prompt-version=v4` — 절대 평가.
3. `python run_pairwise.py --a=v3 --b=v4` — 상대 평가.
4. 결과를 대시보드에 저장한다.

이 정도만 돌려도 "v4가 v3보다 나아졌다"를 숫자로 말할 수 있다. 그리고 숫자로 말할 수 있는 순간부터, 프롬프트 엔지니어링은 비로소 엔지니어링이 된다.

### 5단계 — CI 회귀 감시: 눈을 감지 말자

마지막 단계는 이 모든 것을 **CI에 묶는 일**이다. 수동으로 돌리는 eval은 결국 안 돌린다. 바쁘면 건너뛰고, 건너뛴 사이에 회귀가 들어오고, 회귀가 들어온 줄도 모른 채로 배포된다. 이 시나리오는 정말 끔찍하다. 고객이 이상하다고 말해주기 전까지 우리는 아무것도 모른다.

그러니 CI에 얹자. GitHub Actions라면 이런 식이다.

```yaml
# .github/workflows/prompt-eval.yml
name: Prompt Regression Eval

on:
  pull_request:
    paths:
      - "prompts/**"
      - "myapp/prompts/**"
      - "golden_set/**"

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run golden-set eval (main baseline)
        run: |
          pytest tests/evals/test_code_review.py \
            --prompt-version=main \
            --junitxml=eval-main.xml
      - name: Run golden-set eval (this PR)
        run: |
          pytest tests/evals/test_code_review.py \
            --prompt-version=pr \
            --junitxml=eval-pr.xml
      - name: Run pairwise v(main) vs v(pr)
        run: |
          python scripts/run_pairwise.py \
            --a=main --b=pr \
            --out=pairwise.json
      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const result = require('./pairwise.json');
            const comment = `### Prompt Eval Result

            - Golden-set pass rate (main): ${result.pass_rate_a}
            - Golden-set pass rate (PR): ${result.pass_rate_b}
            - Pairwise win rate (PR vs main): **${result.win_rate_b}**
            - Tie rate: ${result.tie_rate}

            ${result.win_rate_b >= 0.55 ? 'Looks like an improvement.' :
              result.win_rate_b <= 0.45 ? 'Possible regression.' :
              'Inconclusive.'}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment,
            });
```

이 워크플로우가 붙는 순간부터 프롬프트 변경은 **눈에 보인다**. PR 페이지에 win rate가 찍히고, 레이스가 걸리고, 리뷰어가 숫자를 보고 merge 버튼을 누른다. 그저 "감으로 좋아 보여"가 아니라 "pairwise win rate 62%니까 괜찮겠다"가 되는 것이다.

몇 가지 실무 당부를 덧붙이자. 첫째, **CI에서 LLM 호출은 비용이 든다.** 매 PR마다 골든셋 전체(가령 150건)를 N번 돌리면 빠르게 청구서가 늘어난다. 두 가지 완충 장치를 두자. (a) 프롬프트가 실제로 바뀌지 않은 PR에서는 eval을 스킵한다 — path 필터가 그 역할을 한다. (b) 큰 골든셋은 "매 PR마다 도는 smoke set"과 "nightly로 도는 full set"으로 나눈다. 200건 중 30건 정도를 smoke로 뽑고, 전체는 밤에 돌리는 식이다.

둘째, **플레이키한 케이스를 그대로 두지 말자.** 같은 입력인데 오늘은 통과, 내일은 실패하는 케이스가 있으면, 그건 프롬프트 문제라기보다 rubric이나 케이스 자체의 문제일 가능성이 크다. 플레이키한 케이스를 방치하면 신뢰도가 무너지고, 결국 개발자들이 실패를 무시하기 시작한다. 무시가 습관이 되면 CI가 있으나 마나다.

셋째, **결과를 저장하자.** 매번의 eval 결과를 DB든 파일이든 어딘가에 쌓아두자. 석 달 뒤에 "3월 초 이후로 correctness가 서서히 떨어지고 있네"를 발견할 수 있는 건 시계열이 있기 때문이다. Langfuse, Braintrust, LangSmith 같은 SaaS가 이 역할을 대신 해주기도 하고, 초기에는 그냥 JSON을 S3에 던져 두는 것도 충분히 훌륭하다.

자, 이렇게 5단계다. 다시 한번 정리해보자.

1. **케이스 선별** — 현실 분포 + 엣지 케이스를 섞어서 50~200건.
2. **정답 라벨링** — rubric을 짜고, 두 명 이상이 독립적으로 라벨.
3. **메트릭 정의** — assertion + rubric 점수 + pairwise win rate의 조합.
4. **자동화 파이프라인** — pytest 스타일 eval runner + pairwise runner.
5. **CI 회귀 감시** — PR마다 자동 실행, 결과를 PR 코멘트로.

이 다섯 단계 중 어느 하나도 화려하지 않다. 전부 수수하고, 귀찮고, 손이 많이 간다. 하지만 이게 쌓이는 순간, 프롬프트 엔지니어링이 근본적으로 달라진다. "감으로 써서 감으로 평가하던" 상태에서, "가설을 세우고 숫자로 검증하는" 상태로. 이 이행이 이 장의 전부다.

## "Look at your data" — 숫자 너머를 보자

여기까지 읽은 독자는 한 가지 의문이 들 수 있다. 이렇게 자동화까지 깔았으면, 이제 숫자만 보면 되는 걸까?

답은 그렇지 않다. 오히려 반대다. **자동화는 당신이 데이터를 더 잘 볼 수 있게 해주는 도구이지, 데이터를 안 봐도 되게 해주는 도구가 아니다.** Hamel Husain의 또 다른 만트라가 이것이다 — "Look at your data." 실제 출력을 직접, 손으로, 한 줄씩 읽는 시간은 프롬프트 엔지니어링에서 가장 ROI가 높은 활동이다.

왜 그럴까. 메트릭은 **당신이 미리 정의한 축에서만** 측정한다. 정의하지 않은 축에서 무언가가 망가지고 있어도 메트릭은 조용하다. 실제 출력을 읽다 보면 "어? 요즘 답변이 이상하게 수동적이네?" 같은 느낌을 받는데, 이런 느낌은 대시보드에는 안 찍힌다. 느낌은 다음 rubric 축이 된다. 새 축이 rubric에 들어가면, 그 순간부터 메트릭이 그걸 잡기 시작한다. 이 선순환이 eval 문화의 핵심이다.

실무에서는 이런 리듬이 건강하다. 매주 한 번, 팀 전원이 모여서 지난 주 프로덕션 출력 50~100건을 함께 읽는다. "이건 좀 이상한데?" 싶은 걸 말하고, 왜 이상한지 논의하고, 패턴이 보이면 rubric에 반영한다. 이 회의는 한 시간을 넘기지 않도록 짧게 돌리자. 대신 꾸준히 돌리는 것이 핵심이다. 이 한 시간이 "감으로 배포하다가 사고 치는" 패턴을 근본적으로 예방한다.

## 도구 지도 — 언제 무엇을 쓸 것인가

마지막으로, 이 생태계에서 자주 등장하는 도구들을 짧게 정리하고 가자. 어느 하나를 "정답"이라고 말하기보다, **어떤 상황에서 어떤 도구가 손에 잡히는지**를 감만 잡아두면 된다. 각각 한 줄씩이다.

- **Promptfoo** — YAML 하나로 여러 프롬프트·모델을 나란히 돌려 비교한다. 초반에 손에 잡히기 가장 쉬운 도구. "일단 뭐라도 붙여보자"에 적합.
- **DeepEval** — pytest 스타일의 eval 프레임워크. 이 장의 워크스루와 철학이 잘 맞는다. Python 중심 팀에 잘 붙는다.
- **Ragas** — RAG 시스템 전용 메트릭(faithfulness, context precision 등)이 풍부. RAG를 쓴다면 첫 고려 대상.
- **Inspect (UK AISI)** — 영국 AI 안전 연구소가 만든 정교한 eval 프레임워크. 모델 능력·안전성 평가에 강점. 학술 지향 연구자에게 잘 맞는다.
- **Braintrust** — SaaS. 대시보드, 실험 추적, 팀 협업이 잘 엮여 있다. 제품팀이 손에 잡기 좋다.
- **Weights & Biases Weave** — 기존 W&B를 쓰던 ML 팀이라면 자연스러운 확장. 추적·로깅이 강점.
- **LangSmith** — LangChain 생태계와 긴밀히 통합. LangChain·LangGraph를 이미 쓰고 있다면 마찰이 적다.
- **OpenAI Evals** — 오픈소스 프레임워크. 학술 벤치마크 스타일에 가깝고, 공급사 중립적으로 쓸 수 있다.

어느 도구를 고르든, **도구가 본질이 아니라는 점**은 잊지 말자. 골든셋이 없으면 어떤 도구도 의미가 없고, 골든셋이 탄탄하면 도구는 바꿔 끼울 수 있다. 초반에는 도구 선택에 너무 많은 시간을 쓰지 말고, 일단 YAML 한 파일과 pytest로 시작해보는 편이 낫다. 필요가 구체적으로 생긴 다음에 도구를 고르면, 훨씬 적합한 선택을 할 수 있다.

## 마무리 — 평가는 병목이자, 복음이다

이 장을 여는 질문을 다시 꺼내보자. "당신의 프롬프트가 어제보다 오늘 나아졌다는 걸, 당신은 증명할 수 있는가?"

이제 답은 분명하다. 증명할 수 있으려면 **골든셋이 있어야 하고, rubric이 있어야 하고, 메트릭이 있어야 하고, 자동화가 있어야 하고, CI 게이팅이 있어야 한다.** 이 다섯이 갖춰지면 "좋아진 것 같다"가 "win rate 62%"로 바뀐다. 감은 숫자가 된다.

평가는 병목이다. 진짜다. 골든셋 만드는 데 며칠이 걸리고, rubric 다듬는 데 또 며칠이 걸리고, 자동화 붙이는 데 또 며칠이 걸린다. 이 며칠이 너무 아깝게 느껴질 수도 있다. 프롬프트를 고치는 게 더 재미있으니까. 하지만 이 며칠을 아끼면, **프롬프트를 고치는 일 자체가 점점 무의미해진다.** 무엇이 나아졌는지 모른 채 고치기만 하는 건 시간 낭비다. 평가에 투자하는 시간은 이후 모든 프롬프트 작업의 배수를 올려준다.

그리고 평가는 복음이다. 일단 이 장치가 갖춰지면, 그 뒤로는 이상하게도 일이 쉬워진다. 새 프롬프트 아이디어가 떠오르면 그냥 돌려본다. 이기면 머지한다. 지면 왜 졌는지 데이터를 본다. 의심이 들면 숫자를 보고, 숫자가 애매하면 출력을 직접 읽는다. 팀 회의에서 "이게 낫다", "저게 낫다"로 말싸움하던 것이 숫자로 대체된다. 말싸움 없이 의사결정이 굴러간다. 이 경험을 한 번 겪고 나면, 왜 업계가 "Evals-driven development"라는 이름으로 이 문화를 빠르게 받아들이고 있는지 실감하게 된다.

그러니 월요일 아침에 무언가 하나만 시작한다면, 이것을 권한다. **지금 쓰고 있는 프롬프트의 골든셋을 딱 10개만 만들자.** 프로덕션 로그에서 5개를 무작위로 뽑고, 기억나는 실패 케이스 5개를 추가한다. 각 케이스에 "이 출력이 나와야 한다"를 한 줄씩 붙인다. 이 10개를 돌리는 간단한 파이썬 스크립트를 쓰자. 30분이면 된다. 이 30분이 당신의 프롬프트 엔지니어링을 근본적으로 바꿀 것이다.

다음 장에서는 이 엔진 위에서 "보안"을 다룬다. 프롬프트 인젝션이라는, 2026년 현재도 해결되지 않은 문제. 평가로 잡을 수 있는 것과 평가로도 잡기 어려운 것의 경계를 함께 걸어보자.
