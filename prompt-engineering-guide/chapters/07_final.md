# 7장. 모델마다 다른 말투 — Claude, GPT, Gemini 가이드 비교

> "모델은 다 거기서 거기죠." 어느 스택오버플로 댓글은 이렇게 시작했다. 질문은 단순했다. Claude에서 잘 돌던 프롬프트를 GPT-4o에 붙였더니 결과가 이상해졌다는 것. 결론부터 말하면, 그 댓글은 틀렸다. 그리고 이 장은 왜 틀렸는지, 그 차이를 어떻게 다루면 되는지 함께 살펴보는 장이다.

상황을 하나 가정해보자. 앞선 4·5·6장에서 공들여 만든 시스템 프롬프트가 있다. 컨텍스트 아키텍처를 설계했고, RAG로 문서를 주입했고, 구조화 출력 스키마까지 붙였다. Claude 3.5 Sonnet 위에서 기대대로 동작한다. 동료가 묻는다. "이거 GPT-4o에서도 되지?" 자신 있게 모델 이름만 바꿔 배포한다. 월요일 아침, 회귀 eval이 10%p쯤 떨어져 있다. JSON 필드 중 하나는 이상하게 자주 누락되고, 톤도 왠지 어색하다. 난감하다.

왜 이런 일이 벌어질까? 세 공급사의 공식 가이드를 나란히 읽어보면 답이 보인다. Anthropic, OpenAI, Google은 비슷한 원칙을 공유하면서도, **어디에 힘을 주는지**가 뚜렷하게 다르다. 태그를 선호하는 모델이 있고, 마크다운 헤딩을 선호하는 모델이 있다. 시스템 프롬프트를 거의 헌법처럼 따르는 모델이 있고, 상대적으로 힌트 수준으로 받아들이는 모델이 있다. 이 차이를 모르고 같은 프롬프트를 돌리면, 어떤 모델에서는 꽃이 피고 어떤 모델에서는 시든다.

이 장의 목표는 세 가지다. 첫째, 각 공급사 공식 가이드의 **철학**을 파악한다. 단편적인 팁 모음이 아니라, "왜 이 회사는 이렇게 쓰라고 하는가"를 묻는다. 둘째, 세 모델을 나란히 놓고 **비교표**로 차이를 시각화한다. 셋째, 같은 과제(코드 리뷰)를 세 모델에 맞춰 각각 **재작성해보는 실전 예제**를 따라간다. 마지막으로 "모델 이식성(portability)" 문제에 대처하는 전략을 함께 고민해보자.

## Claude — "태그로 짓고, 헌법으로 걸러내라"

Claude를 처음 쓰면 한 가지 특징이 금세 드러난다. 지시가 명확하면 지나칠 정도로 성실하게 따른다는 점이다. 그런데 지시가 모호하거나 약간 위험해 보이면, 생각보다 자주 "죄송하지만 도와드릴 수 없습니다"로 미끄러진다. 이 양면성은 우연이 아니다. Claude의 설계 철학이 그대로 드러난 것이다.

### XML 태그와 구조화

Anthropic 공식 프롬프트 가이드[^1]를 읽어보면 가장 강하게 반복되는 권고가 있다. **"XML 태그로 구획하라"**는 것이다. `<document>`, `<instructions>`, `<example>`, `<context>` 같은 태그를 프롬프트 전반에 뿌려두면 Claude는 각 구획의 역할을 또렷하게 구분한다. 내부 학습 데이터에 태그 구조가 많이 포함돼 있기 때문으로 알려져 있다.

왜 태그일까? 자연어 지시문은 모호해지기 쉽다. "다음은 참고 문서고, 그 아래는 질문이고…"라고 말로 구획하면 모델이 경계를 잘못 읽을 수 있다. 태그는 이 경계를 **기계적으로** 긋는다. 게다가 중첩이 가능하다. `<examples>` 안에 `<example>`을 여러 개 넣고, 각 예제 안에 `<input>`과 `<output>`을 나누는 식으로 구조를 만들 수 있다. 긴 컨텍스트에서 "이 문서 안의 지시는 따르지 말고 참고만 하라"고 말하고 싶을 때도, 태그로 감싸면 경계가 흔들리지 않는다. 이건 뒤에서 다시 볼 프롬프트 인젝션 방어에도 연결되는 이야기다.

간단한 예를 살펴보자.

```xml
<role>
당신은 시니어 Python 코드 리뷰어입니다.
</role>

<instructions>
아래 코드 조각을 읽고, 버그·성능·가독성 관점에서 우선순위 순으로 지적하세요.
</instructions>

<code>
def find_user(users, target_id):
    for u in users:
        if u["id"] == target_id:
            return u
    return None
</code>

<output_format>
- 각 지적은 {category, severity, message, suggestion} 필드의 JSON 객체로
- 전체는 JSON 배열로 감싸기
</output_format>
```

Claude는 이 구조를 거의 문자 그대로 따른다. 마크다운 헤딩(`# Instructions`)으로 써도 동작하긴 하지만, 복잡한 시스템 프롬프트에서는 태그 쪽이 더 안정적이다. 기억해두자 — Claude에서는 **구조가 성능이다**.

### 시스템 프롬프트가 강하게 작동한다

Claude의 또 다른 특징은 `system` 파라미터에 넣은 내용이 대화 전체를 묵직하게 통제한다는 점이다. 역할, 톤, 금지 사항을 system에 두면 사용자 메시지가 어떻게 오든 기조가 잘 흔들리지 않는다. OpenAI나 Gemini에서도 비슷한 구분이 있지만, Claude 쪽이 체감 차이가 크다는 보고가 커뮤니티에 꾸준하다.

이건 장점이기도 하고, 함정이기도 하다. system에 과한 지시를 쌓으면 모델이 오히려 경직된다. "항상 존댓말로 답하고, 절대 코드 블록 밖에서 말하지 말고, 모든 답변에 각주를 붙이고…" 같은 식으로 쌓다 보면, 정작 필요한 순간에 중요한 제약이 무시되기도 한다. **간결하게 유지하되 반복**이라는 원칙이 Claude에서는 특히 유효하다. 정말 중요한 규칙은 system 상단과 하단 모두에 두 번 배치하는 편이 낫다.

### Prefilling — 응답의 첫 문장을 미리 깔아두기

Claude API에는 독특한 기능이 하나 있다. `assistant` 역할의 마지막 메시지를 개발자가 일부 채운 뒤 호출하면, 모델이 **그 지점에서 이어서** 답변을 생성한다. 이 기법을 prefilling이라 부른다.

```python
messages = [
    {"role": "user", "content": "사용자 정보를 JSON으로 주세요."},
    {"role": "assistant", "content": "{\n  \""}  # 여기서부터 이어서 생성
]
```

왜 이렇게까지 할까? 답변이 "네, 물론이죠! 여기 JSON입니다:" 같은 인사말로 시작하는 걸 원천 차단하려는 것이다. 첫 토큰이 `{`이면 모델은 자연스럽게 JSON을 이어 쓴다. 역할 고정에도 유용하다. 응답을 `"분석: "`으로 시작하도록 깔아두면, 모델이 엉뚱하게 "이건 어려운 질문이네요" 같은 메타 코멘트로 빠지는 걸 막을 수 있다.

물론 2024–2025 사이에 세 공급사가 모두 strict JSON 모드를 내놓으면서 prefilling의 상대적 중요도는 줄었다. 하지만 Claude 고유 기법으로 남아 있고, tool use 스키마 없이 포맷을 고정하고 싶을 때 가장 가벼운 수단이다.

### Extended thinking — "step by step"이라고 적지 말자

Claude 3.7 이상 모델에는 `thinking` 블록이라는 기능이 생겼다. 모델이 내부에서 추론 과정을 길게 돌리고, 최종 답만 밖으로 내보내는 모드다. 공식 가이드[^2]가 강조하는 점은 분명하다. **"Let's think step by step" 같은 지시를 더 이상 쓰지 말라**는 것이다.

왜일까? 3장에서 단일 호출 CoT를 정리하면서 잠깐 예고했는데, 여기서 모델별 구체로 다시 들여다보자. reasoning 모델은 이미 내부에서 생각의 사슬을 자동으로 펼친다. 외부에서 또 "단계별로 생각해봐"라고 말하면 토큰이 낭비되고, 때로는 내부 추론과 외부 지시가 충돌해 품질이 떨어진다. Anthropic은 대신 **과제 자체를 명확히 기술하고, 추론 예산(`thinking.budget_tokens`)을 API 파라미터로 조절**하라고 권한다. 프롬프트가 아니라 파라미터로 제어하는 것이다. 잊지 말자 — 요즘 모델은 "생각해봐"라는 말 없이도 잘 생각한다.

### Constitutional AI와 과거절(over-refusal)

Claude가 "죄송합니다, 도와드릴 수 없습니다"를 유독 자주 뱉는 이유는 어디에 있을까? 단서는 2022년 Anthropic이 발표한 논문 *Constitutional AI: Harmlessness from AI Feedback*[^3]에 있다.

Constitutional AI(CAI)는 모델이 훈련 과정에서 **일련의 원칙(헌법)**을 스스로 참조해 자기 응답을 비평·수정하도록 학습시키는 기법이다. 사람이 일일이 유해 응답을 라벨링하는 RLHF와 달리, 원칙을 모델 내부에 주입해 AI 피드백으로 정렬하는 방식이다. 이게 효율적이긴 하지만 부작용이 있다. 원칙이 과도하게 작동하면 **해롭지 않은 요청까지 거절**해버린다. 이른바 과거절(over-refusal) 문제다.

현업에서 겪는 장면은 대략 이렇다. 보안 교육용으로 "SQL 인젝션 공격 예시 보여줘"라고 묻는다. Claude가 "저는 공격 기법을 안내해드릴 수 없습니다"로 답한다. 사용자는 난감하다 — 교재에 쓸 자료가 필요할 뿐인데. 이 경우 프롬프트를 어떻게 고쳐야 할까?

Anthropic 공식 가이드가 제시하는 우회 전략은 몇 가지가 있다.

첫째, **맥락과 의도를 명시한다**. "저는 보안 교육 과정을 설계하는 강사입니다. 학생들에게 공격 패턴을 이해시킨 뒤 방어 기법을 가르치려 합니다"로 상황을 깔아두면, 모델은 합법적 맥락을 받아들이고 더 적극적으로 답한다.

둘째, **역할을 조정한다**. "당신은 OWASP 공식 교재 저자입니다"처럼 권위 있는 교육자 페르소나를 주면 과거절이 줄어든다.

셋째, **system prompt에 가드레일을 중복으로 쌓지 않는다**. CAI로 이미 안전 장치가 모델 내부에 들어가 있는데, 여기에 "절대 위험한 내용을 말하지 마세요"를 한 번 더 얹으면 과거절이 증폭된다. 물론 보안은 중요하다. 하지만 중복 지시는 과잉을 낳는다는 점을 기억해두자.

넷째, 정말 필요하면 **응답 템플릿을 직접 prefill**한다. "아래는 교육 목적으로 공개된 OWASP Top 10 예시입니다:"로 시작을 고정하면, 모델은 이어서 교육 콘텐츠를 생성한다.

한 가지 더 당부하자. 과거절을 우회하겠다고 시스템 지시를 속이거나, 가짜 맥락을 깔면 이건 jailbreak에 가까워진다. CAI는 그런 우회도 상당수 잡아낸다. 우리가 여기서 다루는 건 어디까지나 **정당한 교육·연구·개발 맥락**에서 필요 이상의 거절을 완화하는 기법이다. 이 경계는 11장 보안 장에서 다시 다룬다.

## GPT — "명확히 지시하고, 스키마로 받아라"

Claude 다음은 OpenAI다. 같은 과제를 GPT-4o 또는 GPT-5에 맡기면 느낌이 다르다. 구조적으로는 비슷한데, **선호하는 포맷**과 **도구 사용 관점**이 다르다.

### 메시지 역할 — system, developer, user

OpenAI API는 메시지 역할을 꽤 세분화했다. 전통적인 `system`·`user`·`assistant`가 있고, 2024년 말 reasoning 모델 계열(o1, o3, o4-mini)에서는 `developer` 역할이 추가됐다. Role의 의미는 대략 이런 계층이다.

- `system` — 플랫폼·서비스 운영자가 거는 최상위 지시. 사용자에게 절대 노출되지 않는 규칙.
- `developer` — o-series 계열에서 `system` 대신 개발자가 쓰는 지시 레이어. 기능적으로는 비슷하지만 의미적으로 분리된다.
- `user` — 최종 사용자 입력.
- `assistant` — 모델 응답 (이전 turn 포함).

왜 굳이 developer를 따로 만들었을까? reasoning 모델에서는 **시스템 지시를 짧게 유지하는 것**이 공식 권고다. 장황한 system은 내부 thinking의 토큰 예산을 잡아먹고, 품질 저하로 이어진다. developer role은 이 긴장을 표현하기 위한 장치에 가깝다. "개발자가 필요한 최소 규칙만 담는 자리"라는 메시지다.

실무적으로는 GPT-4o, GPT-5 같은 기본 모델에서는 여전히 `system`을 쓰고, o-series에서는 `developer`로 옮기는 편이 낫다. 라이브러리(OpenAI Python SDK 최신 버전)는 대체로 이 구분을 알아서 처리해주지만, 프롬프트 길이는 우리가 의식해야 한다.

### 마크다운 헤딩과 "instruct-first" 철학

OpenAI 공식 가이드[^4]를 읽으면 Claude와 다른 포맷 선호가 드러난다. **마크다운 헤딩(`# Identity`, `## Task` 등)으로 구획**하는 예제가 압도적으로 많다. XML도 동작하지만, 학습 데이터 분포상 마크다운이 더 자연스럽게 먹힌다.

GPT-4.1 공식 프롬프팅 가이드[^5]는 한 걸음 더 나간다. "GPT-4.1은 지시 사항을 **문자 그대로**(more literally) 따르도록 튜닝됐다"고 명시한다. 모호한 지시는 모호한 결과를 낳고, 명확한 지시는 명확한 결과를 낳는다. Anthropic도 같은 말을 하지만, OpenAI는 이걸 특히 강조한다. "알아서 잘해줘"라는 기대를 접고, 원하는 바를 조목조목 적어야 한다. 일종의 instruct-first 철학이다.

이건 장단이 있다. 장점은 A/B 테스트 결과가 재현 가능에 가깝다는 점이다. 단점은 프롬프트가 장황해질 수 있다는 것이다. 그래서 OpenAI는 동시에 **Structured Outputs**를 강하게 권한다. 포맷은 지시문에 장황하게 쓰지 말고, 스키마로 강제하라는 것.

### Structured Outputs — strict JSON의 등장

2024년 8월 OpenAI는 `response_format`에 JSON 스키마를 넣고 `strict: true`를 켜면 100% 스키마를 준수하는 응답을 보장하는 기능을 발표했다[^6]. 실무에서 이 변화의 무게는 상당하다. 그 이전에는 "제발 JSON으로 답해줘, 다른 말은 하지 말고"를 프롬프트에 여섯 번 반복하고도 `"Sure! Here's the JSON:"`으로 시작하는 응답을 받아 JSONDecodeError를 맞곤 했다. 6장에서 이미 본 그 금요일 오후의 악몽이다.

Structured Outputs는 이 문제를 **디코딩 레벨**에서 해결한다. 모델이 토큰을 뽑을 때마다 스키마에 맞는 토큰만 허용되도록 샘플링을 제약한다. 그래서 프롬프트에 "JSON으로 답해"라고 구구절절 적지 않아도 된다. 대신 스키마의 `description` 필드를 풍부히 써두면, 그게 사실상 필드별 지시문 역할을 한다.

```python
from openai import OpenAI
from pydantic import BaseModel, Field

class ReviewItem(BaseModel):
    category: str = Field(description="버그 | 성능 | 가독성 중 하나")
    severity: str = Field(description="high | medium | low")
    message: str = Field(description="문제 설명, 1문장")
    suggestion: str = Field(description="개선 코드 또는 구체적 지침")

class ReviewResult(BaseModel):
    items: list[ReviewItem]

client = OpenAI()
response = client.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a senior Python code reviewer."},
        {"role": "user", "content": "def find_user(users, target_id): ..."},
    ],
    response_format=ReviewResult,
)
```

Pydantic 모델이 그대로 스키마가 되고, 응답은 타입 안전한 객체로 파싱된다. Claude의 prefilling이 했던 일을 훨씬 단순하게 해결하는 방식이다. 물론 Anthropic도 tool_use를 통해 사실상 같은 결과를 얻을 수 있다. 이건 6장에서 이미 살펴본 이야기다.

### Reasoning effort 파라미터

o-series와 GPT-5 계열에는 `reasoning_effort`라는 파라미터가 있다. `low` / `medium` / `high` 중 하나를 지정해 모델이 내부에서 얼마나 많은 thinking 토큰을 쓸지 조절한다. 값이 높을수록 정확도는 올라가지만 지연과 비용도 함께 오른다.

어느 쪽을 고르는 게 좋을까? 힌트는 과제의 성격에 있다. 수학·코딩·복잡한 리팩토링은 `high`가 값을 한다. 단순 분류, 정보 추출, 형식 변환은 `low`로 충분한 경우가 많다. 기본값(`medium`)부터 시작해서 eval로 측정하고, 과제별로 조정하는 편이 바람직하다. 프롬프트에 "깊이 생각해보세요"라고 적지 말고, 파라미터로 조절하자. Claude의 `thinking.budget_tokens`와 사상이 같다.

### Tool use 우선 — 도구 부르는 모델

OpenAI 가이드를 관통하는 또 하나의 철학은 **"모델이 직접 답하게 하지 말고, 도구를 쓰게 하라"**는 것이다. 계산은 코드 실행 도구, 사실 확인은 검색 도구, 외부 상태 변경은 함수 호출. 이 관점은 에이전트 시대(9장)로 이어지는 다리가 된다. GPT가 tool use에서 앞섰던 역사 — function calling을 2023년 일찍 표준화했고, 이후 다른 공급사가 뒤따라온 흐름 — 가 가이드 전반의 톤을 만든다. "모델 혼자 풀려 하지 말고, 세계와 상호작용하게 설계하라"는 것이다.

## Gemini — "긴 컨텍스트와 멀티모달이 제1시민"

세 번째 주자 Google Gemini는 또 다른 결로 움직인다. 공식 가이드[^7]를 열면 가장 먼저 눈에 띄는 게 **컨텍스트 크기**와 **멀티모달**이다.

### 1M~2M 토큰의 시대

Gemini 1.5 Pro는 기본 1M 토큰, 실험 모드에서는 2M 토큰까지 컨텍스트를 확장했다. 2.0·2.5 계열도 이 방향을 이어간다. 책 한 권, 수십 시간 분량의 문서를 통째로 넣어도 돌아간다는 뜻이다.

그렇다면 RAG가 필요 없어진 걸까? 아니다. 4장에서 이미 짚었듯 **1M 토큰이어도 다 넣으면 안 된다**. RULER 벤치[^8] 같은 측정에서 실질 가용 맥락은 공칭 크기보다 훨씬 짧게 나오는 경우가 많다. 신호 대 잡음비가 떨어지면 모델은 헤맨다. Gemini의 긴 컨텍스트는 **예시를 많이 넣을 여유**, **참고 문서 전체를 넣을 여유**, **긴 대화 이력을 유지할 여유**로 이해하는 편이 낫다. 무엇이든 다 때려 넣어도 된다는 뜻이 아니다.

실무적으로는 Gemini에서도 "문서는 위에, 질문은 아래에"가 유효하다. 그리고 "relevant quotes를 먼저 뽑고, 그다음 답하라"는 식의 two-step 프롬프트가 긴 문서에서 정확도를 끌어올린다. 이건 Anthropic 가이드가 Claude에 대해 했던 권고와 거의 같다. Lost-in-the-middle은 공급사를 가리지 않는다.

### Multimodal이 기본

Gemini는 설계 단계부터 텍스트·이미지·오디오·비디오를 같은 토큰 공간에서 다룬다. 이미지 파일을 첨부하고 "이 다이어그램의 오류를 찾아줘"라고 묻거나, 비디오를 넣고 "3분 14초에 나오는 제품명을 알려줘"라고 요청하는 흐름이 자연스럽다.

프롬프트 설계 관점에서 한 가지 팁이 있다. **이미지나 비디오만 덜렁 주지 말고, 앞뒤로 텍스트 질의를 명확히 붙이자**. 멀티모달 입력만 주면 모델은 "description"으로 흘러가는 경향이 있다. 원하는 게 분석이면 분석이라고, 요약이면 요약이라고 명시해야 한다. 타임스탬프 인용("몇 초 지점에서 X가 일어났는가"), 바운딩 박스 좌표 요청 같은 구체적 질의 형태가 품질을 크게 좌우한다.

### System instruction과 responseSchema

Gemini도 system instruction을 지원하지만, 커뮤니티 관찰에 따르면 Claude만큼 묵직하게 작동하지는 않는다는 보고가 있다(사실 확인 필요 — 버전별 편차가 있다). 그래서 Gemini에서는 **중요한 지시를 user 메시지 맨 앞에도 한 번 더 넣는 이중화**가 권장되는 경우가 많다.

구조화 출력은 `responseSchema`와 `responseMimeType: "application/json"` 조합으로 해결한다. OpenAI의 Structured Outputs와 거의 같은 사상이다. 스키마 기반 디코딩으로 포맷을 강제하고, `description` 필드에 의미를 실어준다.

### Google Search grounding

Gemini 고유 기능 중 하나는 **구글 검색을 붙여 그라운딩**하는 옵션이다. `tools`에 `google_search`를 넣으면 모델이 필요할 때 실시간 검색을 호출하고, 결과를 답변에 녹인다. RAG를 직접 구현하기 전에 간단히 "최신 정보가 필요한 질의"를 처리하는 수단으로 쓸 수 있다.

주의할 점은 있다. 검색 결과를 모델이 **어디까지 정확히 인용하는지**는 여전히 불완전하다. Perplexity에서 관찰되던 "citation hallucination" — 인용 링크가 실제 내용과 어긋나는 문제 — 가 여기서도 나타날 수 있다. 5장에서 다룬 환각 완화 레시피는 Gemini에서도 그대로 유효하다. 검색을 붙였다고 환각이 자동으로 사라지진 않는다는 점을 기억해두자.

### Safety settings — 직접 다이얼을 돌린다

Gemini가 Claude·GPT와 구별되는 실무 포인트 하나를 더 살펴보자. 안전 필터의 강도를 **API 파라미터로 직접 조절**할 수 있다. `safetySettings`에 카테고리별(`HARM_CATEGORY_HATE_SPEECH`, `HARM_CATEGORY_SEXUALLY_EXPLICIT` 등)로 `BLOCK_NONE` / `BLOCK_LOW_AND_ABOVE` / `BLOCK_MEDIUM_AND_ABOVE` / `BLOCK_ONLY_HIGH` 중 선택할 수 있다.

왜 이런 설계가 가능할까? Google은 안전 판단을 **별도 필터 레이어**로 분리하는 경향이 강하다. 반면 Claude의 CAI는 모델 내부에 정렬이 녹아 있어 외부에서 다이얼로 조절하기 어렵다. 아키텍처적 차이가 API 표면으로 드러나는 사례다. 물론 `BLOCK_NONE`을 쉽게 쓰라는 이야기는 아니다. 필터를 내릴 땐 왜 그래야 하는지 명확한 근거가 있어야 하고, 책임도 함께 진다.

## 세 모델의 공통점 — 그리고 결정적 차이

세 공급사의 가이드를 차근차근 읽으면 재미있는 그림이 그려진다. **원칙 수준에서는 수렴**하는데, **실행 디테일에서는 갈라진다**는 점이다.

공통 원칙은 대략 이 순서로 정리된다.

1. **Clear task** — 무엇을 시킬지 명확히.
2. **Context** — 필요한 배경·참고 자료를 구획해서 공급.
3. **Examples** — few-shot을 통한 포맷·스타일 학습.
4. **Format** — 원하는 출력 구조를 스키마 또는 예시로 지정.
5. **Constraints** — 해서는 안 될 것, 모르면 모른다고 말하기 같은 실패 경로.

이건 2장에서 다룬 세 레버(명확성·맥락·형식)에 제약과 예시가 붙은 확장판이다. 공급사가 달라도 뼈대는 같다. 그럼 무엇이 갈라질까? 표 하나로 정리해보자.

| 항목 | Claude (Anthropic) | GPT (OpenAI) | Gemini (Google) |
|---|---|---|---|
| 선호 구획 | **XML 태그** 강한 권장 | **마크다운 헤딩** 권장 | 양쪽 모두, 헤딩 선호 |
| System prompt 강도 | 매우 강함 | 강함 | 보통 (user에 재강조 권장) |
| 역할 레이어 | system + user | system / developer / user | system + user |
| 구조화 출력 | tool_use, prefill | **Structured Outputs (strict)** | responseSchema |
| 추론 제어 | `thinking.budget_tokens` | `reasoning_effort` (low/med/high) | Thinking 모드 (2.0+) |
| CoT 지시 | 비추론 모델에서만, thinking 모델은 **금지** | 동일 | 동일 |
| 긴 컨텍스트 | 200k, "quotes first" 기법 | 128k~400k, 앞뒤 강조 | **1M~2M**, 앞뒤 강조 |
| 멀티모달 | 이미지 지원 | 이미지·오디오 (GPT-4o) | **이미지·오디오·비디오 네이티브** |
| 안전 제어 | CAI 내재화 (프롬프트로 완화) | 중간 (정책 기반) | **safetySettings API** |
| 과거절 경향 | 상대적으로 큼 | 중간 | 중간 |
| Temperature 기본 | 1.0 (보수적 조정 권장) | 1.0 (strict JSON일 땐 0.0) | 1.0 (정확도 과제는 0.2) |
| Tool 정의 | tool_use / MCP | function/tools / Responses API | function_calling / A2A |
| 캐싱 | prompt caching (2024-08) | automatic prefix caching (2024-10) | context caching (explicit API) |

표에서 눈여겨볼 행이 몇 개 있다. CoT 지시는 세 모델 모두 reasoning 계열에서는 **쓰지 말라**로 수렴했다. Temperature는 구조화 출력을 쓸 때 0에 가까이 두는 게 기본이다. Caching은 세 회사가 모두 2024년에 표준화했고, 이건 12장 운영에서 다시 다룬다.

차이점에서 특히 실무적인 한 줄은 이것이다. **Claude는 태그로 묶고, GPT는 헤딩으로 나누고, Gemini는 긴 컨텍스트에 멀티모달로 얹는다.** 나머지는 이 세 기조의 변주에 가깝다.

## 같은 과제, 세 가지 번역 — 코드 리뷰 프롬프트

이제 실전이다. 같은 태스크를 세 모델에 맞춰 각각 재작성해보자. 과제는 **Python 함수 조각을 받아 코드 리뷰 결과를 구조화 출력으로 돌려주는** 것이다. 입력과 기대 출력은 동일하다. 포장만 바뀐다.

### Claude용 — 태그 구조 + tool_use 패턴

```python
import anthropic

client = anthropic.Anthropic()

system_prompt = """\
<role>
당신은 10년 경력의 시니어 Python 엔지니어이자 코드 리뷰어입니다.
</role>

<principles>
- 버그, 성능, 가독성 순으로 우선순위를 매깁니다.
- 지적은 구체적 코드와 대안 코드를 함께 제시합니다.
- 근거가 불분명한 스타일 논쟁은 피합니다.
</principles>

<output_rules>
- report_review 도구를 반드시 호출해 구조화된 결과를 반환하세요.
- 다른 형식의 자유 텍스트는 출력하지 마세요.
</output_rules>
"""

tools = [{
    "name": "report_review",
    "description": "코드 리뷰 결과를 구조화해 보고합니다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "enum": ["bug", "performance", "readability"]},
                        "severity": {"type": "string", "enum": ["high", "medium", "low"]},
                        "message": {"type": "string"},
                        "suggestion": {"type": "string"}
                    },
                    "required": ["category", "severity", "message", "suggestion"]
                }
            }
        },
        "required": ["items"]
    }
}]

response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    system=system_prompt,
    tools=tools,
    tool_choice={"type": "tool", "name": "report_review"},
    messages=[{
        "role": "user",
        "content": """<code>
def find_user(users, target_id):
    for u in users:
        if u["id"] == target_id:
            return u
    return None
</code>

<task>
위 코드를 리뷰하고 report_review를 호출하세요.
</task>"""
    }],
)
```

몇 가지 포인트가 보인다. system을 태그 구조로 썼고, 사용자 메시지도 `<code>`와 `<task>`로 구획했다. 출력은 tool_use 스키마로 강제했고, `tool_choice`로 특정 도구 호출을 필수로 지정했다. 이게 Claude의 "제대로 된" 방식이다.

### GPT용 — 마크다운 + Structured Outputs

```python
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal

class ReviewItem(BaseModel):
    category: Literal["bug", "performance", "readability"]
    severity: Literal["high", "medium", "low"]
    message: str = Field(description="문제를 한 문장으로 기술")
    suggestion: str = Field(description="개선 코드 또는 구체적 지침")

class ReviewResult(BaseModel):
    items: list[ReviewItem]

system_prompt = """\
# Identity
당신은 10년 경력의 시니어 Python 엔지니어이자 코드 리뷰어입니다.

# Principles
- 버그, 성능, 가독성 순으로 우선순위를 매깁니다.
- 지적은 구체적 코드와 대안 코드를 함께 제시합니다.
- 스타일 논쟁은 피합니다.

# Output
ReviewResult 스키마를 준수해 JSON으로 응답합니다.
"""

client = OpenAI()
response = client.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": """\
## Code
```python
def find_user(users, target_id):
    for u in users:
        if u["id"] == target_id:
            return u
    return None
```

## Task
위 코드를 리뷰하세요."""},
    ],
    response_format=ReviewResult,
)
```

같은 내용인데 장식이 완전히 다르다. system을 `# Heading`으로 나누고, 사용자 메시지도 마크다운 섹션으로 구획했다. JSON 강제는 Pydantic + `response_format`으로 처리했고, 프롬프트에서 "JSON으로 답해"를 **한 줄도 쓰지 않았다**. 스키마가 그 일을 대신한다.

### Gemini용 — 시스템 지시 + responseSchema

```python
import google.generativeai as genai

schema = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": ["bug", "performance", "readability"]},
                    "severity": {"type": "string", "enum": ["high", "medium", "low"]},
                    "message": {"type": "string"},
                    "suggestion": {"type": "string"},
                },
                "required": ["category", "severity", "message", "suggestion"],
            },
        }
    },
    "required": ["items"],
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""\
# Identity
당신은 10년 경력의 시니어 Python 엔지니어이자 코드 리뷰어입니다.

# Principles
- 버그, 성능, 가독성 순으로 우선순위를 매깁니다.
- 지적은 구체적 코드와 대안 코드를 함께 제시합니다.
""",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": schema,
        "temperature": 0.2,
    },
)

prompt = """\
## Code
```python
def find_user(users, target_id):
    for u in users:
        if u["id"] == target_id:
            return u
    return None
```

## Task
위 코드를 리뷰하고 스키마에 맞게 응답하세요.
"""

response = model.generate_content(prompt)
```

Gemini 쪽은 system instruction에 핵심 정체성만 두고, 구체 과제는 user 프롬프트에서 다시 한번 강조했다. 포맷은 `response_schema`로 강제했고, temperature는 명시적으로 낮췄다. 단순 분류가 섞인 과제라 흔들림을 줄이려는 의도다.

### 세 결과가 거의 같아지는 이유

세 버전을 나란히 놓고 실제로 돌려 보면, 출력은 놀라울 정도로 유사하다. **스키마가 같고, 역할이 같고, 원칙이 같기** 때문이다. 차이는 포장지에 있었을 뿐 속은 같았다. 그래서 실무 팁이 하나 도출된다. **공통 구조를 먼저 설계하고, 모델별 포장지는 얇게 씌우자**. 반대로 하면, 즉 Claude용으로 만든 XML 프롬프트를 그대로 GPT·Gemini에 던지면 미묘한 성능 손실이 생긴다. 반대 방향도 마찬가지다.

## 모델 이식성(portability) — 한 벌의 프롬프트, 세 갈래의 번역

실제 제품팀에서는 한 모델로만 돌아가는 경우가 드물다. 비용 때문에 저가 모델과 고가 모델을 혼용하거나, 공급사 장애에 대비해 폴백을 둔다. 이런 상황에서 "모델별로 프롬프트를 세 벌 관리"는 금세 유지 보수의 악몽이 된다. 그렇다면 어떻게 해야 할까?

**전략 1 — 프롬프트를 두 층으로 분리한다.** 공통 층과 모델 고유 층으로 나누는 것이다. 공통 층에는 역할, 원칙, 과제, 예시가 들어간다. 모델 고유 층은 포맷 어댑터에 가깝다. Claude용 템플릿은 공통 내용을 XML 태그로 감싸고, GPT용은 마크다운 헤딩으로, Gemini용은 헤딩 + 추가 강조로. 이 층을 코드로 표현하면 대략 이런 그림이다.

```python
def render_prompt(common: CommonPrompt, model: str) -> list[dict]:
    if model.startswith("claude"):
        return render_anthropic_xml(common)
    elif model.startswith("gpt") or model.startswith("o"):
        return render_openai_markdown(common)
    elif model.startswith("gemini"):
        return render_gemini_markdown(common)
    raise ValueError(f"Unsupported model: {model}")
```

어댑터 패턴이다. 공통 내용은 한 곳에서 관리하고, 모델별 렌더링 함수만 세 개를 두면 된다. 스키마도 마찬가지다. Pydantic 모델 하나를 정의하고, 이걸 OpenAI에선 `response_format`에, Anthropic에선 tool schema에, Gemini에선 `response_schema`에 변환해 주입한다. Instructor 같은 라이브러리는 바로 이 일을 대신한다.

**전략 2 — 하이브리드 템플릿을 쓴다.** 세 모델 모두 태그와 헤딩을 함께 써도 잘 파싱한다. 멀티-모델을 지원하되 어댑터를 만들 여유가 없다면, **XML + 마크다운 하이브리드**로 하나만 만들어 세 군데에 던지는 방법도 실용적이다.

```xml
<role>
# Identity
시니어 Python 리뷰어입니다.
</role>

<context>
## Code
...
</context>

<task>
위 코드를 리뷰하세요.
</task>
```

이게 최적은 아니다. 각 모델에 정확히 맞춘 전용 템플릿보다 성능이 2–5%p 낮을 수 있다. 그러나 "하나만 관리하면 된다"는 단순함이 주는 이득이 크다. 초기 파일럿 단계에는 이쪽이 바람직하다.

**전략 3 — eval로 확인한다.** 10장에서 다룰 이야기를 미리 당기자. 모델을 바꾸거나 포맷을 바꿀 때마다 **같은 골든셋에 돌려 회귀를 확인**해야 한다. "감으로 괜찮은 것 같다"로 넘어가면 프로덕션에서 조용히 품질이 떨어진다. 이식성은 결국 eval과 한 쌍이다. 측정 없이 이식은 환상이다.

**전략 4 — 공급사 고유 기능은 고유로 인정한다.** Gemini의 네이티브 비디오 처리, Claude의 prefilling, OpenAI의 Responses API 같은 기능은 공통 층에 억지로 우겨 넣지 말자. 과제가 정말 그 기능을 필요로 한다면, 해당 모델로 결정하고 다른 쪽은 다른 전략으로 푸는 편이 낫다. 모든 걸 한 벌로 덮으려는 욕심이 오히려 품질을 깎는다.

## 오픈소스 모델 — chat template이라는 지뢰밭

세 공급사 이야기만 하다 보면 오해가 생길 수 있다. "이 세 모델만 있으면 되는가?" 그렇지 않다. Llama 3·3.1·3.2, Mistral·Mixtral, Qwen, DeepSeek 같은 오픈소스 모델이 있고, 온프레미스·엣지·비용 민감 환경에서 이들의 존재감은 크다. 그런데 여기엔 공급사 모델엔 거의 없는 문제가 하나 도사린다. **Chat template 불일치**다.

Llama 3 공식 포맷은 이런 모양이다.

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

Mistral은 `[INST] ... [/INST]` 래핑을 쓴다. Qwen은 또 다르다. 문제는 llama.cpp나 vLLM 같은 서빙 도구로 돌릴 때 `--chat-template`을 모델에 맞게 정확히 지정하지 않으면 **조용히 품질이 떨어진다**는 것이다. 에러는 나지 않는다. 응답도 돌아온다. 그런데 20%p쯤 낮은 정확도로 도는 식이다. 이건 정말 찜찜한 실패다.

실무 권장은 분명하다. 오픈소스 모델을 쓴다면 **모델 카드의 공식 포맷**을 반드시 확인하고, Hugging Face의 `apply_chat_template` 같은 유틸리티를 통해 인코딩을 맡기는 편이 낫다. 직접 문자열을 붙이지 말자. 오타 하나에 모델이 다른 존재가 된다.

오픈소스 모델에서도 Claude·GPT·Gemini 가이드의 원칙은 유효하다. 역할 부여, 태그·헤딩 구획, few-shot 큐레이션, 실패 경로 명시. 다만 기반 인코딩이 정확해야 그 위에 뭐든 얹을 수 있다는 점을 기억해두자.

## 마무리 — "모델마다 다르다"는 사실을 설계에 녹이자

Claude, GPT, Gemini. 세 공급사의 공식 가이드를 나란히 읽으면 한 가지 사실이 뚜렷해진다. **같은 프롬프트 엔지니어링 원칙이 세 가지 언어로 번역돼 있다**는 것. 영어, 한국어, 일본어로 같은 이야기를 해도 문법이 다르듯이, 세 모델 가이드는 같은 원칙을 각자의 문법으로 쓴다.

이 장에서 함께 살펴본 것을 다시 짚어보자.

- **Claude**는 XML 태그로 구획하고, system prompt를 묵직하게 쓰며, prefilling이라는 고유 무기가 있다. CAI의 내재화로 과거절이 쉽게 나타나므로 맥락·역할·중복 지시 조정으로 완화한다.
- **GPT**는 마크다운 헤딩으로 나누고, Structured Outputs로 포맷을 스키마에서 해결하며, "지시 문자 그대로"라는 instruct-first 철학이 강하다. Reasoning 계열에서는 developer role과 `reasoning_effort` 파라미터로 통제한다.
- **Gemini**는 긴 컨텍스트와 멀티모달이 제1시민이고, `responseSchema`로 포맷을 강제하며, `safetySettings`로 안전 필터를 다이얼 조작한다. System instruction은 상대적으로 약하므로 user 메시지에 재강조하자.
- **공통점**은 Clear task → Context → Examples → Format → Constraints 순서다. 이 뼈대는 세 모델 모두에서 그대로 작동한다.
- **이식성**은 공통 층과 모델 고유 층의 분리, 하이브리드 템플릿, eval 기반 회귀 확인, 공급사 고유 기능의 인정이라는 네 축으로 관리한다.

마지막으로 한 가지 당부하자. "어느 모델이 제일 좋은가"는 자주 받는 질문이지만, 사실 좋은 질문은 아니다. **"이 과제에 어느 모델이 맞는가"**가 실무적으로 더 생산적이다. 긴 비디오 분석은 Gemini가 자연스럽다. strict JSON이 결정적인 금융 시스템은 GPT의 Structured Outputs가 단단하다. 복잡한 정책·톤 통제가 중요한 에이전트는 Claude의 강한 system prompt가 유리하다. 과제를 먼저 정의하고, 모델은 그다음에 고르자. 이 순서를 뒤집으면 도구가 과제를 흔들게 된다.

다음 8장에서는 이 장에서 익힌 모델별 번역 기술을 한 층 위로 끌어올린다. 수동으로 프롬프트를 고치는 한계를 넘어, **데이터 기반으로 프롬프트를 자동 최적화**하는 세계 — DSPy, OPRO, TextGrad — 로 넘어가보자. OPRO 논문이 발견한 "Take a deep breath"의 이야기가 거기 있다.

---

### 처음이라면 이것만

- 세 모델 모두 "명확한 과제 + 구획된 컨텍스트 + 예시 + 형식 + 제약"의 순서를 따른다.
- Claude는 태그, GPT는 헤딩, Gemini는 헤딩 + 긴 컨텍스트를 선호한다고 기억해두자.
- reasoning 모델(o1/o3, Claude thinking, Gemini Thinking)에서는 "Let's think step by step"을 **쓰지 않는다**.
- 구조화 출력은 프롬프트로 애원하지 말고 **스키마로 강제**하자.

### 연구자용 — 원 출처 포인터

- Bai et al., *Constitutional AI: Harmlessness from AI Feedback*, arXiv:2212.08073 (2022)
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, arXiv:2307.03172 (2023)
- Hsieh et al., *RULER: What's the Real Context Size of Your Long-Context Language Models?*, arXiv:2404.06654 (2024)
- Zheng et al., *Is "A Helpful Assistant" the Best Role for LLMs?*, arXiv:2311.10054 (2023)

---

[^1]: Anthropic, *Prompt engineering overview*, <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>; *Use XML tags to structure your prompts*, <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags>.

[^2]: Anthropic, *Extended thinking tips*, <https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking>.

[^3]: Bai et al., *Constitutional AI: Harmlessness from AI Feedback*, arXiv:2212.08073 (2022), <https://arxiv.org/abs/2212.08073>.

[^4]: OpenAI, *Prompt engineering — Best practices*, <https://platform.openai.com/docs/guides/prompt-engineering>.

[^5]: OpenAI, *GPT-4.1 Prompting Guide* (2025), <https://cookbook.openai.com/examples/gpt-4-1_prompting_guide>.

[^6]: OpenAI, *Introducing Structured Outputs in the API* (2024-08), <https://openai.com/index/introducing-structured-outputs-in-the-api/>.

[^7]: Google, *Prompt design strategies*, <https://ai.google.dev/gemini-api/docs/prompting-strategies>; *Introduction to prompting*, <https://ai.google.dev/gemini-api/docs/prompting-intro>.

[^8]: Hsieh et al., *RULER: What's the Real Context Size of Your Long-Context Language Models?*, arXiv:2404.06654 (2024), <https://arxiv.org/abs/2404.06654>.
