# 7장. 모델을 쓰는 일 — API, Java 서비스 연결, 프롬프트의 함정

같은 질문을 다섯 번 던졌는데 답이 매번 조금씩 다르다고 상상해보자. `temperature=0`으로 박았고, 프롬프트도 바꾸지 않았고, 모델도 같은 `gpt-4o-2024-11-20`이다. 그런데 한 번은 "사내 개발 문서 요약 시스템입니다."로 시작하고, 다음엔 "안녕하세요, 사내 개발 문서를"로 시작한다. 세 번째는 줄바꿈 위치가 다르다. 백엔드 개발자에게 이 상황은 낯설다. `Math.sqrt(2.0)`가 호출할 때마다 다른 값을 돌려주면 누구나 버그라고 할 것이다. 그런데 LLM API가 그런 "함수"다. 이게 버그가 아니라 설계라는 사실을 받아들이는 데서 이 장이 시작된다.

6장까지 우리는 "모델을 만든다"의 궤적을 걸어왔다. 4장에서 미니 GPT를 쌓고, 6장에서 Llama 3 8B를 QLoRA로 파인튜닝했다. 이제 관점을 한번 돌릴 때가 됐다. 7장과 8장에서 "모델을 쓴다"로 넘어간다. 공통 태스크 "사내 개발 문서 요약/Q&A"를 API 한 줄로 풀어보고, 그 함수를 Java 서비스 안에 콩(Bean)처럼 꽂는 법을 같이 배운다. 이 장을 덮을 때 독자가 얻는 것은 단순하다. **LLM을 함수처럼 호출하되, "신뢰할 수 없는 함수"로 다루는 법.** 같이 한 걸음씩 들어가보자.

---

## 7.1 지금 우리가 어디에 있나 — 여정 지도와 7장의 자리

매번 장을 열 때마다 같은 지도를 꺼내든다. 내가 지금 어디에 있는지를 잊지 않기 위해서다.

```text
[2장 토큰/임베딩] → [3장 어텐션/트랜스포머]
        ↓
[4장 미니 GPT from scratch + 디코딩 루프]
        ↓
[5장 스케일·정렬: Pretraining → Scaling Laws → RLHF]
        ↓
[6장 QLoRA 파인튜닝: Llama 3 8B를 사내 문서에 맞춘다]
        ↓
★ [7장 API·Spring AI·LangChain4j — 세 번째 답]  ← 지금 여기
        ↓
[8장 RAG — 네 번째 답]
        ↓
[9장 통합 결정 플로차트] → [10장 다음 걸음]
```

공통 태스크인 "사내 개발 문서 요약/Q&A"를 네 번 다르게 푼다고 약속했던 것을 기억해두자. 4장에서는 축소판 한국어 코퍼스로 모델을 from scratch로 학습시켜 답을 얻었고, 6장에서는 오픈 모델을 QLoRA로 파인튜닝해서 같은 문제를 풀었다. 이번 장은 그 시리즈의 **세 번째 답**이다. 이번엔 만들지 않는다. 이미 훈련된 SaaS 모델(GPT-4o, Claude 3.5 Sonnet 등)을 API로 부른다. "만든다"가 아니라 "쓴다"로 관점이 회전하는 바로 그 장면이다.

한 바퀴 도는 여정은 이렇다. Chat Completions API 스키마 해부 → 4장 디코딩 루프 ↔ API 파라미터 매핑 → "Temperature=0인데 왜 답이 다른가" 정면돌파 → 프롬프트 엔지니어링 기본기 → Python 실습(OpenAI/Anthropic) → 회고 콜아웃 → Java 실습(Spring AI + LangChain4j) → 의존성 한 줄로 provider 스왑 → 로컬 모델(Ollama) → 관측성(observability). 같이 가자.

---

## 7.2 Chat Completions API 스키마 해부

API 문서를 먼저 뒤지기 전에, 한 가지를 머릿속에 박아두고 가자. **LLM은 이제 "대화"의 모양으로 쓰인다.** 과거 GPT-3 API는 그냥 프롬프트 문자열 하나를 받아 "이어서 써라"라고 시키는 completion 방식이었다. 지금 우리가 쓰는 건 대부분 **Chat Completions** 계열이다. OpenAI, Anthropic, Google, Ollama, 심지어 대부분의 오픈소스 호환 서버까지 이 모양으로 수렴했다. 모양이 같다는 건 실무자에게 축복이다. 한 번 배우면 어디 가도 통한다.

Chat Completions API의 요청은 JSON 한 덩어리다. 아래 예시를 보자.

```json
{
  "model": "gpt-4o-2024-11-20",
  "messages": [
    {"role": "system", "content": "너는 사내 개발 문서를 요약하는 도우미다. 한국어로 3문단 이내로 답한다."},
    {"role": "user", "content": "아래 Spring Boot 3.3 릴리즈 노트를 요약해줘.\n\n..."},
    {"role": "assistant", "content": "Spring Boot 3.3은 ..."},
    {"role": "user", "content": "방금 요약에서 Observability 부분만 더 자세히 풀어줘."}
  ],
  "temperature": 0.3,
  "top_p": 0.9,
  "max_tokens": 1024,
  "stop": ["\n\n---\n\n"],
  "stream": false
}
```

핵심 필드를 하나씩 뜯어보자.

**`model`.** 어느 모델을 호출할지 지정한다. OpenAI라면 `gpt-4o-2024-11-20`, `gpt-4o-mini`, Anthropic이라면 `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-latest` 같은 형태다. 여기서 한 가지 주의할 점. **모델 별명(alias)보다 날짜 박힌 정식 ID를 쓰는 편이 낫다.** `gpt-4o`만 쓰면 OpenAI가 내부적으로 새 스냅샷으로 교체했을 때 어느 날 갑자기 출력이 미묘하게 달라진다. 프로덕션 서비스라면 이 변화가 재앙이다. 날짜 박힌 ID로 고정해두고, 교체 시기를 팀이 의식적으로 고른다. 그게 더 건강하다.

**`messages`.** 이 API의 심장이다. `role`이 셋 있다. `system`은 "이 모델에게 주는 성격과 규칙"을 적는 자리다. 한 번만 주는 게 보통이고 대화 처음에 둔다. `user`는 사용자의 입력, `assistant`는 모델이 과거 턴에서 한 말이다. 여기서 한 가지 머리에 박아둘 사실이 있다. **Chat Completions API는 상태를 기억하지 않는다.** 매 요청마다 지금까지의 대화 전체를 클라이언트가 다시 보내야 한다. "어제 이야기한 거 기억나?"가 통하지 않는다. 기억하고 싶으면 대화 히스토리를 내 서버에 쌓아두고, 매번 `messages` 배열에 전부 집어넣어서 보내야 한다. 이건 의외로 많은 초보자가 부딪히는 지점이다. "왜 세션이 안 이어지지?" 하는 찜찜함의 정체가 이것이다.

**`temperature`, `top_p`.** 4장에서 우리가 손으로 조립했던 바로 그 손잡이들이다. 뒤에 따로 한 절을 할애해 매핑한다.

**`max_tokens`.** 모델이 만들어낼 수 있는 **출력 토큰**의 상한이다. 입력 토큰은 별개다. 이 값이 작으면 긴 요약을 만들려다 중간에 칼같이 잘린다. 이 때 응답의 `finish_reason`이 `length`로 찍힌다. 반대로 너무 크게 잡으면 과금이 걱정이고, 응답 지연도 늘어난다. "요약 3문단이면 1,000토큰쯤"처럼 용도별로 감을 갖자.

**`stop`.** 특정 문자열이 나오면 거기서 생성을 멈춘다. "항상 `---END---`로 끝내라"고 시키고 `stop: ["---END---"]`를 주면 말미 군말을 막을 수 있다.

**`stream`.** true로 주면 서버가 SSE(Server-Sent Events)로 토큰을 하나씩 흘려보낸다. ChatGPT처럼 타이핑 느낌을 주거나 최초 지연(time-to-first-token) 기준으로 UX를 개선하고 싶을 때 켠다. 스트리밍 이야기는 잠시 뒤에 따로 한다.

응답은 이렇게 생겼다.

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1713330000,
  "model": "gpt-4o-2024-11-20",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Spring Boot 3.3은 관측성(Observability)을 한층 강화했다. ..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 842,
    "completion_tokens": 318,
    "total_tokens": 1160
  }
}
```

눈여겨볼 필드가 두 개 있다. **`finish_reason`**과 **`usage`**다.

`finish_reason`은 생성이 왜 멈췄는지를 말해준다. 실무에서 자주 보는 값은 네 가지다.

- `stop` — 정상 종료. 모델이 스스로 마침표를 찍었거나 `stop` 문자열을 만났다.
- `length` — `max_tokens`에 부딪혀 잘렸다.
- `content_filter` — 안전 필터에 걸렸다.
- `tool_calls` — 모델이 함수 호출을 요청했다.

서비스 코드에서 이 값을 챙겨두는 편이 낫다. "응답이 잘려 있는데 왜 뒷부분이 없지?"로 고생하는 사람 대부분은 `finish_reason`을 안 보고 `message.content`만 꺼내 쓰다 당한다. 번거로워도 로깅에 찍어두자.

`usage`는 요금 계산의 기준이다. OpenAI GPT-4o를 예로 들면 2026년 초 기준 입력 1M 토큰당 약 $2.50, 출력 1M 토큰당 약 $10.00이다(모델과 시점에 따라 바뀌니 공식 pricing 페이지로 재확인하자). 입력이 훨씬 싸고 출력이 비싸다. 입력은 병렬, 출력은 자기회귀라 GPU 시간이 더 든다(4장 디코딩 루프 복습). 이 비대칭을 이해하면 "프롬프트를 짧게 쓰는 것보다 출력을 짧게 받는 쪽이 비용 절감에 더 효과적"이라는 감각이 생긴다. 2장에서 본 "한국어 토큰 2배 먹는다"까지 더해보면 한국어 출력 단가는 체감 이상으로 비싸진다.

### 스트리밍과 SSE 한 꺼풀

`stream: true`로 요청하면 응답이 한 덩어리가 아니라 **여러 개의 이벤트**로 쪼개져 돌아온다. `Content-Type: text/event-stream`이고 한 이벤트는 이런 모양이다.

```text
data: {"id":"chatcmpl-...","choices":[{"delta":{"content":"Spring "},"index":0}]}

data: {"id":"chatcmpl-...","choices":[{"delta":{"content":"Boot "},"index":0}]}

... (중략) ...

data: [DONE]
```

각 이벤트의 `delta.content`를 이어붙이면 최종 문자열이 된다. 마지막 `[DONE]`이 종료 신호다. 스트리밍은 UX 이득이 크지만, **과금 집계와 에러 처리가 까다롭다.** 요청 하나가 수십~수백 이벤트로 쪼개져서 중간에 네트워크가 끊기면 어디까지 받았는지 확인해야 하고, 토큰 사용량도 보통 마지막 이벤트 근처에서만 내려온다. OpenAI는 `stream_options: {"include_usage": true}`로 usage를 박아준다. 초반엔 "대화 UX가 꼭 필요한 엔드포인트에만" 스트리밍을 쓰는 편이 낫다. 배치성 요약·분류는 한 방에 받는 쪽이 심플하다.

---

## 7.3 4장 루프의 API 매핑 — 설명이 아니라 연결

여기서부터는 **설명이 아니라 연결**이다. 4장 말미에서 우리는 미니 GPT 출력층에 `logits → softmax → sampling`의 파이프라인을 직접 꽂아놓고, Greedy / Temperature / Top-k / Top-p를 한 장면 안에서 돌려봤다. 개념은 거기서 이미 몸으로 잡았다. 그러니 여기서는 "그게 API 파라미터로 어떻게 이름을 바꿔 달고 나오는가"만 짚고 넘어가자.

| 4장에서 본 이름 | API 파라미터 이름 | 역할 |
|---|---|---|
| `greedy` (매 스텝 argmax) | `temperature=0` + `top_p=1.0` | 가장 확률 높은 토큰만 뽑는다. 이론상 결정론적. 실제는 7.4 참조 |
| `temperature=T` | `temperature` (0.0~2.0) | softmax 왜곡 정도. T가 낮으면 날카롭게, 높으면 평평하게 |
| `top_k` (상위 k개에서 샘플링) | **대부분 API는 노출 안 함** | OpenAI Chat Completions는 노출 X. Anthropic/Google/로컬 일부는 있음 |
| `top_p` (누적확률 p까지에서 샘플링) | `top_p` (0.0~1.0) | 확률 분포의 "허리"에서 컷 |
| `max_new_tokens` | `max_tokens` | 출력 상한 |
| EOS 토큰 만나면 종료 | `stop` + `finish_reason="stop"` | 생성 종료 조건 |

한눈에 보이듯이 4장의 손잡이가 이름만 바꿔 달고 그대로 올라와 있다. 한 가지 헷갈리기 쉬운 점은 **`top_k`가 대부분의 SaaS Chat Completions API에서 노출되지 않는다**는 사실이다. OpenAI는 top_k를 API 파라미터로 주지 않는다. Anthropic Messages API와 Google Gemini API, 그리고 Ollama처럼 로컬로 돌리는 호환 서버들은 `top_k`를 노출한다. 4장에서 본 Top-k 샘플링을 API에서도 그대로 쓰고 싶다면 provider 선택에 따라 가능 여부가 갈린다는 걸 기억해두자.

실무 기본값에 대한 감을 짧게 잡아두자. "일단 돌려보기" 디폴트는 `temperature=0.7`, `top_p=0.9`, `max_tokens`는 용도별로 명시다. 여기서 출발해서 용도에 맞게 조금씩 민다.

| 용도 | `temperature` 권장 | 이유 |
|---|---|---|
| 분류·추출·요약 | 0 ~ 0.2 | 사실성·재현성 우선 |
| 코드 생성 | 0.0 ~ 0.3 | 문법 실수 최소화 |
| 창작·브레인스토밍 | 0.7 ~ 1.2 | 다양성이 값어치 |

`top_p`는 대부분 0.9나 1.0을 써도 무방하다. 다만 `temperature`와 `top_p`를 둘 다 과격하게 흔들면 결과가 예측이 안 되니, **둘 중 하나만 주로 조절**하는 편이 낫다. OpenAI 문서도 같은 조언을 한다.

자, 이렇게 이름만 바꿔 달고 올라온 파라미터들에 얽힌 가장 큰 함정이 하나 있다. 바로 `temperature=0`을 줬는데도 답이 매번 미묘하게 다르다는 사실이다. 다음 절에서 정면으로 다뤄본다.

---

## 7.4 "Temperature=0 is a Lie" — 재현성의 배신

가장 먼저 인정하자. 이 제목은 2025년 Thinking Machines Lab의 블로그 포스트에서 그대로 가져왔다. 같은 프롬프트에 `temperature=0`을 다섯 번 찍어본 경험이 있는 사람이라면 그 블로그의 첫 문장에서 "아, 나만 그런 거 아니었구나" 싶었을 거다. 여기서는 왜 그런지, 그리고 실무에서 어떻게 다뤄야 하는지를 같이 풀어본다.

먼저 문제를 눈으로 확인하자. 아래 스크립트는 같은 프롬프트를 `temperature=0`으로 다섯 번 호출한다. `openai` 파이썬 SDK가 필요하다.

```python
# pip install openai
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def call_once():
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "한국어로 간결하게 답하라."},
            {"role": "user", "content": "사내 개발 문서 요약 시스템을 한 문장으로 설명하라."},
        ],
        temperature=0,
        max_tokens=100,
    )
    return resp.choices[0].message.content

for i in range(5):
    print(f"[{i+1}] {call_once()}")
```

실행하면 대충 이런 결과가 나온다. 정확한 문장은 실행 때마다 다르다.

```text
[1] 사내 개발 문서 요약 시스템은 내부 문서를 자동으로 분석하여 핵심 내용을 간결하게 정리해주는 도구입니다.
[2] 사내 개발 문서 요약 시스템은 회사 내부의 개발 관련 문서를 자동으로 분석하고 핵심 내용을 간추려 제공하는 도구입니다.
[3] 사내 개발 문서 요약 시스템은 내부 문서를 자동으로 분석하여 핵심 내용을 간결하게 정리해주는 도구입니다.
[4] 사내 개발 문서 요약 시스템은 회사 내부의 개발 문서를 자동으로 요약하여 제공하는 시스템입니다.
[5] 사내 개발 문서 요약 시스템은 내부 문서를 자동으로 분석하여 핵심 내용을 간결하게 정리해주는 도구입니다.
```

문장 세 개가 겹치고, 두 개가 달라졌다. `temperature=0`이면 argmax가 매번 같은 토큰을 골라야 하지 않나? 이론상으로는 그렇다. 그런데 실제로는 그렇지 않다. 이유는 두 층에 걸쳐 있다.

### 왜 그런가 — GPU 부동소수점 + 배치 효과

이유는 두 층으로 얽혀 있다. 첫째, GPU 행렬 곱셈에서 부동소수점 덧셈의 순서가 실행마다 조금씩 달라진다. `(a+b)+c`와 `a+(b+c)`가 수학적으로는 같아도 반올림 때문에 마지막 몇 비트가 다를 수 있고, CUDA 커널은 성능을 위해 여러 스레드의 부분합을 합치는 순서를 고정해두지 않는다. logits에서 1등과 2등 확률이 아주 가까울 때, 이 미세한 차이가 argmax를 뒤집는다.

둘째, 더 큰 원인은 **배치 효과(batching effect)**다. SaaS API 서버는 효율을 위해 여러 사용자의 요청을 한 배치로 묶어 GPU에 올린다. 내 요청이 어떤 다른 요청들과 같은 배치에 묶이느냐에 따라 패딩 길이·커널 dispatch·메모리 레이아웃이 달라지고, 같은 입력이라도 부동소수점 경로가 달라진다. Thinking Machines Lab의 글이 짚은 핵심이 이거다. **내가 보낸 요청의 결정성을 남이 보낸 요청이 흔든다.**

백엔드 개발자에게 "외부 상태가 내 함수의 결과를 바꾼다"는 건 있을 수 없는 일이다. 그런데 클라우드 GPU 위의 LLM 추론이 그렇다. 이 사실을 먼저 인정하고 시작하자.

### 그래서 어떻게 다뤄야 하나

완전한 결정성을 얻는 건 현실적으로 어렵다. 그래도 **재현성에 근접**하는 실무 전략은 있다.

**(1) `seed` 파라미터를 쓴다.** OpenAI Chat Completions는 2023년 말부터 `seed` 파라미터와 응답의 `system_fingerprint`를 지원한다. 같은 `seed` + 같은 `system_fingerprint` 하에서는 결정성을 **"최선을 다해"** 보장한다. 여전히 완벽하진 않지만 매번 다른 배치보다는 훨씬 낫다.

```python
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    temperature=0,
    seed=42,
)
print(resp.system_fingerprint)  # "fp_abc123..." 같은 값
```

이 `system_fingerprint`가 바뀌면 OpenAI가 내부 모델/커널/하드웨어를 뭔가 바꿨다는 신호다. 이때부터는 출력이 달라질 수 있다고 가정해야 한다. 테스트 코드에서 스냅샷 검증을 한다면 `system_fingerprint`도 같이 기록하는 편이 낫다.

**(2) 모델 ID를 날짜까지 박아 고정한다.** 7.2에서 언급한 것과 같은 이유다. `gpt-4o` 별명은 언제든 바뀐다.

**(3) 결정성을 정말로 원하면 로컬에서 배치 1로 돌린다.** Ollama나 vLLM으로 혼자 쓰는 배치 사이즈 1의 추론은 훨씬 결정적이다. 다만 속도와 비용이 별개 문제다.

**(4) 테스트는 정확 일치가 아니라 의미 일치로 짠다.** 이게 가장 근본적인 해법이다. `assertEqual(result, "예상 문자열")`로 짜면 재현성 배신에 당한다. 대신 "JSON 스키마를 만족하는가", "특정 키워드를 포함하는가", "LLM-as-a-judge로 의미가 일치하는가"로 검증한다. 8장과 9장에서 더 자세히 다룬다.

핵심은 이것이다. **LLM은 순수 함수가 아니다.** 백엔드 코드에서 LLM API를 호출하는 함수를 쓸 때, 그 함수의 반환값이 실행마다 조금씩 달라질 수 있다는 전제를 붙여두자. 호출부에서 이 전제를 잊으면, 아주 찜찜한 버그에 시달리게 된다.

> **박스 — "Temperature=0 is a Lie" 출처**
> Thinking Machines Lab (2025). "Defeating Nondeterminism in LLM Inference". https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
> 이 글은 배치 효과를 제거하는 커널 설계까지 파고든다. 커널 레벨에 관심 있는 독자에게 권한다.

---

## 7.5 프롬프트 엔지니어링 기본기 — 역할, 예시, 생각의 사슬

같은 모델을 쓰는데 누구는 좋은 답을 받고 누구는 엉뚱한 답을 받는다. 차이는 어디서 올까? `messages` 배열을 어떻게 채우느냐, 그 한 군데다. 이걸 **프롬프트 엔지니어링**이라는 거창한 이름으로 부르는데, 실무에서 쓰는 기본기는 몇 가지 되지 않는다. 하나씩 살펴보자.

### 역할 분담 — system / user / assistant

`system` 메시지는 "이 세션 전체의 배경 설정"이다. 모델의 성격, 응답 형식, 금지사항, 도메인 지식 요약을 담는다. `user`와 `assistant`가 왔다갔다 하는 동안 `system`은 기본적으로 한 번만 준다.

좋은 `system` 메시지의 특징을 세 가지 꼽자면 (1) **구체적인 역할 지정**, (2) **출력 형식 명시**, (3) **실패 시 행동 지정**이다. 세 번째가 특히 중요하다. 모델은 지시하지 않으면 모르는 걸 지어낸다(환각). "몰라도 된다"를 명시적으로 허락해야 모른다고 답한다.

안 좋은 예를 보자.

```text
System: 좋은 답을 해라.
```

이런 건 안 주느니만 못하다. 모델은 이미 "좋은 답"이 디폴트 목표다. 덧붙이는 게 없다.

좋은 예는 이렇다.

```text
System: 너는 사내 개발 문서 요약 도우미다.
- 출력은 한국어 JSON 한 덩어리. 키는 `summary`(string), `keywords`(array of string), `confidence`(0~1 float).
- 문서에서 근거를 찾지 못하면 `summary`를 빈 문자열, `confidence`를 0으로 둔다.
- 추측하지 말고, 문서에 있는 사실만 요약한다.
- 줄바꿈은 `\n`으로 이스케이프한다.
```

명시적이고 실행 가능하다. 코드에서 `json.loads()`로 파싱하는 게 부담 없다.

### Few-shot — "이렇게 답해라"의 시범

입력-출력 예시 두세 개를 `messages`에 섞어두면 모델이 패턴을 따라한다. 이걸 few-shot 프롬프팅이라고 부른다. GPT-3 논문(Brown et al., 2020)의 핵심 발견이 이거였다. 파라미터를 건드리지 않고 프롬프트에 예시만 넣어도 모델이 새 태스크를 배운다.

```python
messages = [
    {"role": "system", "content": "문서를 한 줄로 요약한다."},
    {"role": "user", "content": "Spring Boot 3.3 릴리즈 노트 ...(전문) ..."},
    {"role": "assistant", "content": "Spring Boot 3.3은 Observability 강화와 Java 21 완전 지원이 핵심이다."},
    {"role": "user", "content": "JPA 2.2 변경사항 ...(전문) ..."},
    {"role": "assistant", "content": "JPA 2.2는 스트림 쿼리와 CDI 주입 통합을 도입했다."},
    {"role": "user", "content": "이번 문서를 같은 형식으로 요약해줘.\n\n..."},
]
```

예시가 두세 개면 충분히 효과가 난다. 다만 예시가 길면 입력 토큰이 늘어 비용도 올라간다. 2장에서 본 한국어 토큰 효율 이야기가 여기서 살아난다. Few-shot을 한국어로 많이 깔면 입력 비용이 빠르게 불어난다. 짧게, 대표적으로.

### Chain-of-Thought (CoT) — 생각의 사슬

복잡한 추론이 필요한 문제에서는 "답만 내라"보다 "먼저 생각을 정리하고 답하라"가 훨씬 잘 먹힌다. Wei et al. (2022)의 CoT 논문이 이걸 공식화했다.

```text
System: 문제를 풀 때는 먼저 <thinking>...</thinking> 안에 생각을 정리하고,
마지막에 <answer>...</answer> 안에 최종 답만 담는다.

User: 한 서비스의 API 호출이 5분 동안 12만 건이었고, 이 중 3%가 실패했다.
실패 중 절반이 429(rate limit), 나머지는 500대다. 500대 건수는?
```

이렇게 시키면 모델은 `<thinking>` 안에 "12만 × 0.03 = 3,600. 3,600 × 0.5 = 1,800."처럼 계산을 풀어두고, `<answer>1,800건</answer>`만 최종 답으로 낸다. 응답 파싱은 정규식 한 줄. 사고 과정을 강제하면 산술이나 다단계 추론에서 정답률이 눈에 띄게 오른다. 다만 출력 토큰이 늘어나니 비용이 같이 오른다는 트레이드오프가 있다.

요즘은 한 발 더 나아간 흐름도 있다. OpenAI `o1`/`o3` 같은 reasoning 모델은 사용자가 `<thinking>` 태그를 시키지 않아도 내부에서 사고 토큰을 돌리고 청구한다. 다만 출력 토큰 단가가 일반 모델보다 비싸다. 산술·코드 디버깅처럼 추론이 필요한 태스크엔 reasoning 모델, 단순 요약·분류엔 일반 모델이 가성비가 좋다.

### ReAct — 도구 사용으로 한 발 더

CoT가 "혼자 머릿속으로 생각하기"라면 ReAct(Yao et al., 2022)는 "생각하면서 도구도 같이 쓰기"다. `Thought → Action → Observation → Thought ...` 루프를 돌며 검색·계산기·DB 같은 도구를 부르는 흐름이다. 이게 발전해서 오늘의 **함수 호출**과 **에이전트**가 됐다. 이 책의 범위를 넘어서니 이름만 짚고 간다. 10장 "다음 걸음"에서 다시 만난다.

### 한 줄 권장: 짧고 구체적으로

프롬프트 엔지니어링을 한 줄로 요약하면 이렇다. **모델이 짐작하지 않아도 되도록 짧고 구체적으로 적어라.** 후배에게 "잘 짜줘"라고 하면 결과가 안 좋다. "입력은 X, 출력은 Y, 예외는 이렇게 처리, 스타일은 팀 컨벤션"이라고 하면 좋아진다. 모델도 같다.

> **참고 자료**
> - Wei et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. arXiv:2201.11903
> - Wang et al. (2022). Self-Consistency Improves Chain of Thought Reasoning. arXiv:2203.11171
> - Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. arXiv:2210.03629
> - Anthropic Prompt Engineering Guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering

---

## 7.6 Python 실습 — 같은 태스크를 OpenAI와 Anthropic으로

이제 손을 움직여보자. 공통 태스크인 "사내 개발 문서 요약/Q&A"를 API로 한 번 풀어본다. Python부터 가고, 같은 일을 Java로 다시 짜는 흐름이다.

### OpenAI SDK 최소 버전

먼저 환경부터. Python 3.11 이상, 가상환경 안에서 시작한다.

```bash
pip install openai
export OPENAI_API_KEY="sk-..."
```

API 키는 코드에 박지 말자. 환경변수가 기본이다. 운영에서는 AWS Secrets Manager, HashiCorp Vault 같은 걸 쓰는 편이 낫다. 키가 코드에 박히면 GitHub에 한 번 푸시되는 순간 봇이 5분 안에 긁어가서 비싼 모델로 돌리기 시작한다. 끔찍한 일이다.

아래 스크립트는 사내 문서를 받아 요약을 돌린다. 출력은 JSON이다.

```python
# pip install openai
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SYSTEM_PROMPT = """\
너는 사내 개발 문서 요약 도우미다.
- 출력은 한국어 JSON 한 덩어리. 키는 `summary`(string, 3문장 이내), `keywords`(array of string, 최대 5개), `confidence`(0~1 float).
- 문서에서 근거를 찾지 못하면 `summary`를 빈 문자열, `confidence`를 0으로 둔다.
- 추측하지 말고, 문서에 있는 사실만 요약한다.
"""

def summarize(document: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"다음 문서를 요약하라.\n\n---\n{document}\n---"},
        ],
        temperature=0.2,
        max_tokens=512,
        response_format={"type": "json_object"},
    )
    finish = resp.choices[0].finish_reason
    if finish != "stop":
        raise RuntimeError(f"비정상 종료: finish_reason={finish}")
    raw = resp.choices[0].message.content
    return json.loads(raw)


if __name__ == "__main__":
    doc = """\
Spring Boot 3.3은 2024년 5월에 릴리즈됐다. 주요 변경은 Observability 강화, Java 21 가상 스레드 정식 지원, 
그리고 Spring AI 1.0 GA 호환이다. Micrometer 1.13과 함께 OpenTelemetry 1.36을 권장한다. ...
"""
    result = summarize(doc)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

몇 가지 짚어둘 점이 있다.

**`response_format={"type": "json_object"}`**는 OpenAI의 JSON 모드다. 모델이 valid JSON만 뱉도록 강제한다. 이걸 안 켜면 모델이 답 앞뒤로 ```json ... ``` 같은 마크다운 펜스를 붙이거나 "아래는 요약입니다."로 시작하는 군말을 붙여서 `json.loads()`가 깨진다. 끔찍한 일이다. JSON 모드는 그런 군말을 막아준다. 다만 키 이름과 타입까지 강제하진 않는다. 더 강한 강제가 필요하면 `response_format={"type": "json_schema", "json_schema": {...}}` 식의 Structured Outputs를 쓴다. OpenAI는 2024년부터 정식 지원한다.

**`finish_reason` 체크.** 위 코드에서 정상 종료가 아니면 예외를 던진다. 이게 7.2에서 강조한 그 이야기다. 운영 코드에선 **꼭** 챙겨두자.

**비용·지연 로깅.** 이 코드에는 빠져 있는데, 실제 운영에선 `resp.usage`와 `time.perf_counter()`로 잰 지연을 같이 로깅하는 편이 낫다. 7.10 관측성 절에서 다시 다룬다.

### Anthropic Claude로 같은 일을

같은 태스크를 Claude로 돌려보자. Anthropic의 SDK는 메시지 모양이 살짝 다르다. `system`이 `messages` 배열 안의 항목이 아니라 **별도 파라미터**로 분리돼 있다.

```python
# pip install anthropic
import json
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """..."""  # 위와 동일


def summarize(document: str) -> dict:
    resp = client.messages.create(
        model="claude-3-5-haiku-latest",
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"다음 문서를 요약하라.\n\n---\n{document}\n---"},
        ],
        temperature=0.2,
        max_tokens=512,
    )
    if resp.stop_reason != "end_turn":
        raise RuntimeError(f"비정상 종료: stop_reason={resp.stop_reason}")
    raw = resp.content[0].text
    # Claude는 JSON 강제 모드가 없어서 마크다운 펜스를 가끔 붙인다
    raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(raw)
```

OpenAI와 차이가 두 군데다. 첫째, `system`이 따로 빠져 있다. 둘째, JSON 강제 모드가 없어서 마크다운 펜스를 손으로 벗겨야 한다. 그리고 `finish_reason` 대신 `stop_reason`, 정상 종료 값은 `end_turn`이다.

이런 미세한 차이가 골치다. SDK 두 개를 다루다 보면 if 분기가 늘어나니 LangChain 같은 추상화가 나왔다. 짧게 얹어보자.

### LangChain으로 한 꺼풀 추상화

LangChain의 `ChatPromptTemplate`을 쓰면 프롬프트와 모델을 분리해서 관리할 수 있다. provider 교체도 한 줄이다.

```python
# pip install langchain langchain-openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 사내 개발 문서 요약 도우미다. JSON으로 답한다."),
    ("user", "{document}"),
])
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

chain = prompt | llm
result = chain.invoke({"document": "Spring Boot 3.3은 ..."})
print(result.content)
```

`prompt | llm`의 파이프 연산자는 LCEL(LangChain Expression Language)이다. 함수 합성처럼 자연스럽고, provider를 바꿔도 prompt 코드는 그대로다. 이게 추상화의 이득이다.

LangChain에는 메모리·출력 파서·RAG·에이전트 등 더 많은 기능이 있다. 다만 추상화 레이어가 두꺼워질수록 디버깅이 힘들어진다. 처음 입문할 땐 SDK 직접 쓰는 쪽이 학습에 좋다. 8장 RAG 실습에서 LangChain을 본격적으로 쓴다.

여기까지가 Python 쪽 기본기다. 이제 관점을 한 번 회전할 시간이다. 다음 절은 잠깐 코드에서 떨어져, 6장과 7장 사이에 일어난 변화를 정리하는 회고 콜아웃이다.

---

## 7.7 회고 콜아웃 — 지금까지 만든 것 vs 지금부터 쓰는 것

> **잠시 멈춤.** 이 책의 한가운데를 지나고 있다. 여기서 한 페이지 정도 시간을 써서 시야를 정리하고 가자. 익숙한 풍경에서 새 풍경으로 옮겨가는 길목이라, 한 번 발을 멈추는 게 낫다.

### 지금까지 우리가 "만든" 것

2장에서 6장까지의 궤적을 다시 펼쳐보자.

- **2장**에서는 토큰화와 임베딩을 손으로 만져봤다. `tiktoken`과 `minbpe`로 한국어가 어떻게 잘리는지 확인했고, 임베딩 공간에서 "도서관"과 "독서실"이 이웃이라는 사실을 눈으로 봤다.
- **3장**에서는 Q/K/V 어텐션과 트랜스포머 박스의 내부를 풀었다. 그림 100번 보고도 모르겠던 것들이 코드 10줄로 정리됐다.
- **4장**에서는 미니 GPT를 from scratch로 만들었다. Bigram에서 시작해 셀프 어텐션, 멀티헤드, 피드포워드, 레지듀얼을 차곡차곡 쌓았다. 마지막에는 디코딩 루프를 직접 짜서 Greedy / Temperature / Top-k / Top-p의 결과를 같은 모델 위에서 비교했다.
- **5장**에서는 Pretraining부터 Scaling Laws, RLHF, Constitutional AI까지의 5년사를 따라갔다. 작은 모델을 만들어본 경험이 "1.3B가 175B를 이긴" 사건을 가슴에 박히게 만들었다.
- **6장**에서는 Llama 3 8B를 QLoRA로 사내 개발 문서에 맞춰 파인튜닝했다. HF Hub에 본인 이름이 박힌 모델이 하나 올라갔을 것이다.

이게 우리가 **"만든"** 것의 궤적이다. 핵심은 "내부가 어떻게 생겼는지를 본 사람이 됐다"는 점이다. 토큰이 어떻게 잘리는지, 어텐션이 무엇을 보고 있는지, loss가 어떻게 떨어지는지, 파인튜닝이 어떤 weight를 건드리는지를 손으로 확인했다. 이제 LLM은 더 이상 블랙박스가 아니다.

### 지금부터 우리가 "쓰는" 것

7장과 8장은 관점이 회전한다. 만들지 않는다. 이미 누군가 잘 만들어 놓은 것을 **쓴다**. 호출하고, 조립하고, 서비스에 붙인다.

- **7장(지금)**: 만들어진 모델을 API로 부른다. Chat Completions 스키마, 파라미터, 프롬프트, Spring AI, LangChain4j. "외부 함수로서의 LLM."
- **8장**: 외부 지식(사내 문서)을 모델의 컨텍스트에 주입한다. 검색, 임베딩, 벡터 DB, 출처 인용. "RAG라는 우회로."

관점이 회전한다는 게 무슨 뜻일까. 만드는 관점에선 GPU 메모리·loss 곡선·학습률·토크나이저 어휘 같은 걸 신경 썼다. 쓰는 관점에선 응답 지연·토큰 비용·재현성·안전 필터·출력 검증·에러 처리·관측성이 들어온다. 백엔드 개발자에게 이쪽이 훨씬 익숙한 단어들이다. **만드는 사람의 고민은 데이터 사이언티스트의 것이고, 쓰는 사람의 고민은 백엔드 엔지니어의 것이다.** 이 책은 후자에 더 비중이 있다.

### 같은 태스크의 네 가지 답

서문에서 약속했던 공통 태스크 "사내 개발 문서 요약/Q&A"의 네 가지 답을 한 장면에 겹쳐보자.

| 장 | 해법 | 비용 | 지연 | 갱신성 | 적합한 상황 |
|---|---|---|---|---|---|
| 4장 | 축소판 from scratch | 학습: 무료~몇 달러 / 추론: 무료 | 매우 빠름 | 재학습 필요 | 학습용·실험용 |
| 6장 | Llama 3 8B QLoRA | 학습: $1~$10 / 추론: 자체 GPU | 중간 | 재파인튜닝 | 톤·스타일·도메인 학습 |
| 7장(지금) | API 호출 + 프롬프트 | 학습: 0 / 추론: 호출당 과금 | 모델 따라 | 즉시(프롬프트만 바꾸면) | 빠른 PoC, 일반 지식 |
| 8장 | RAG + 벡터 DB | 학습: 0 / 추론: 호출 + 검색 | 검색 추가됨 | 즉시(문서만 바꾸면) | 자주 갱신되는 사내 지식 |

이 표가 9장 결정 플로차트의 골격이 된다. 네 답이 같은 문제의 다른 모양이라는 사실을 한 장면에 겹쳐 보고 있는 게 핵심이다. **"파인튜닝 vs RAG"가 종교 전쟁이 아니라 트레이드오프**라는 감각, 그게 이 책의 가장 큰 자산이다.

자, 회고는 여기까지다. 다시 코드로 돌아가자. 이번엔 Java다. 이 장의 진짜 주공이 시작된다.

---

## 7.8 Java 실습 (1) — Spring AI로 LLM을 콩(Bean)처럼 다루기

지금까지의 Python 코드를 Spring 백엔드에 옮긴다고 해보자. `RestTemplate`이나 `WebClient`로 OpenAI HTTP API를 직접 부를 수도 있다. 안 될 건 없다. 다만 인증·재시도·토큰 카운팅·스트리밍·provider 교체를 직접 짜야 한다. 짜본 사람은 안다. 번거롭고 찜찜하다. 두 모델을 비교하려고 OpenAI 코드를 Anthropic 코드로 통째로 갈아엎고 있는 자신을 발견하게 된다.

Spring AI는 이 답답함을 푸는 라이브러리다. 한 줄로 요약하면 **"LLM을 Spring Bean처럼 주입받아 쓰는 표준 추상화"**다. 2024년 1.0 GA 이후 OpenAI·Anthropic·Vertex AI·Azure OpenAI·Ollama·Mistral·Groq 등 주요 provider를 모두 지원한다. 한 번 코드를 짜두면 의존성 한 줄 갈아 끼우는 걸로 provider가 바뀐다. 이 약속의 위력을 잠깐 뒤에 직접 확인한다.

### 프로젝트 세팅

Spring Boot 3.3, Java 21 기준이다. `pom.xml`에 의존성을 추가한다.

```xml
<!-- pom.xml -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.ai</groupId>
      <artifactId>spring-ai-bom</artifactId>
      <version>1.0.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
  </dependency>
</dependencies>
```

`application.yml`에 키를 박는다(환경변수에서 불러오자).

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      chat:
        options:
          model: gpt-4o-mini
          temperature: 0.2
```

Spring Boot가 시작되면 `OpenAiChatModel`이라는 빈이 자동으로 등록된다. 이걸 그대로 주입받아 써도 되지만, 보통은 한 단계 위 추상화인 `ChatClient`를 쓴다.

### `ChatClient`로 첫 호출

`ChatClient`는 fluent API로 프롬프트를 조립하고 호출하는 진입점이다. 아래는 가장 짧은 예시다.

```java
// SummaryConfig.java
@Configuration
public class SummaryConfig {

    @Bean
    public ChatClient chatClient(ChatClient.Builder builder) {
        return builder
            .defaultSystem("""
                너는 사내 개발 문서 요약 도우미다.
                - 출력은 한국어 JSON. 키는 summary, keywords, confidence.
                - 추측하지 말고 문서에 있는 사실만 요약한다.
                """)
            .build();
    }
}
```

```java
// SummaryService.java
@Service
public class SummaryService {

    private final ChatClient chatClient;

    public SummaryService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public String summarize(String document) {
        return chatClient.prompt()
            .user(u -> u.text("다음 문서를 요약하라.\n\n---\n{doc}\n---")
                       .param("doc", document))
            .call()
            .content();
    }
}
```

이 코드의 어디가 좋은가. 첫째, **API 키·HTTP 클라이언트·재시도·타임아웃 같은 인프라 코드가 사라졌다.** 자동 설정이 다 처리한다. 둘째, **프롬프트가 코드와 분리된다.** `defaultSystem`은 한 번 정의하고 호출부는 `user(...)` 한 줄. 셋째, **다른 Spring Bean처럼 주입·테스트된다.** Mockito로 `ChatClient`를 mock해두면 단위 테스트도 자연스럽다.

### 구조화된 출력 — Java POJO로 받기

`String`이 아니라 Java 객체로 받으면 더 좋다. Spring AI의 `entity()` 메서드가 이걸 지원한다. 모델 출력을 JSON으로 강제하고, Jackson으로 역직렬화해준다.

```java
public record Summary(String summary, List<String> keywords, double confidence) {}

public Summary summarize(String document) {
    return chatClient.prompt()
        .user(u -> u.text("다음 문서를 요약하라.\n\n---\n{doc}\n---")
                   .param("doc", document))
        .call()
        .entity(Summary.class);
}
```

이 코드가 하는 일은 단순하다. `Summary` 클래스의 구조를 보고 JSON 스키마를 자동 생성해 system 프롬프트에 붙이고, 모델이 뱉은 JSON을 Jackson이 `Summary` 객체로 역직렬화한다. **LLM 응답이 외부 REST API의 응답처럼** 다뤄지는 모양이다. 손으로 JSON을 파싱하는 끔찍한 일이 사라진다.

### Advisor로 메모리 끼우기

7.2에서 "Chat Completions API는 상태가 없다"고 했다. 대화 히스토리를 매번 보내야 한다고. Spring AI는 이걸 위해 **Advisor**라는 인터셉터 메커니즘을 제공한다. AOP의 advisor와 비슷한 발상이다. 호출 전후로 끼어들어 프롬프트를 가공하거나 응답을 후처리한다.

`MessageChatMemoryAdvisor`는 사용자별 대화 히스토리를 자동으로 쌓고, 매 호출마다 `messages` 배열에 끼워준다. 설정은 이렇게 한 줄이다.

```java
@Bean
public ChatClient chatClient(ChatClient.Builder builder, ChatMemory chatMemory) {
    return builder
        .defaultSystem("...")
        .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())
        .build();
}

@Bean
public ChatMemory chatMemory() {
    // 인메모리 구현. 운영에선 RedisChatMemory 등으로 교체
    return new InMemoryChatMemory();
}
```

호출부에서는 `advisors(a -> a.param(ChatMemory.CONVERSATION_ID, userId))`로 `conversationId`만 넘기면 대화가 알아서 이어진다. 매번 history를 손으로 만들어 넘기는 번거로움이 사라진다. 8장에서는 이 Advisor 메커니즘을 그대로 활용해 `QuestionAnswerAdvisor`로 RAG를 한 줄에 끼운다. 이런 일관된 추상화가 Spring AI의 진짜 매력이다.

### Maven 의존성 한 줄로 provider 스왑

이제 약속한 마술을 해보자. 위에서 짠 `SummaryService` 코드를 한 글자도 안 바꾸고 OpenAI에서 Anthropic으로 갈아탄다. `pom.xml`에서 의존성 한 줄만 바꾸면 된다.

```xml
<!-- 기존 -->
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
</dependency>

<!-- 변경 -->
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-anthropic-spring-boot-starter</artifactId>
</dependency>
```

`application.yml`도 한 섹션만 갈아 끼운다.

```yaml
spring:
  ai:
    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
      chat:
        options:
          model: claude-3-5-haiku-latest
          temperature: 0.2
```

이게 끝이다. `SummaryService`의 Java 코드는 한 글자도 안 바꿨다. 다시 빌드해서 돌리면 그대로 Claude로 호출된다. 같은 일을 Ollama로(즉, 로컬 모델로) 돌리고 싶으면 의존성을 `spring-ai-ollama-spring-boot-starter`로 바꾸고 yml을 다시 한 섹션 바꾸면 된다.

```yaml
spring:
  ai:
    ollama:
      base-url: http://localhost:11434
      chat:
        options:
          model: llama3.1:8b
          temperature: 0.2
```

같은 `SummaryService` 코드가 OpenAI, Anthropic, Ollama 위에서 모두 동작한다. **이게 Spring AI를 이 책의 7장 주공으로 둔 이유다.** Java 백엔드 개발자가 LLM 통합을 시작할 때 가장 큰 두려움이 "특정 provider에 락인되는 것"인데, 이 추상화 한 겹이 그 두려움을 풀어준다. PoC는 OpenAI로, 비용 검토 후 일부는 Claude로, 민감한 사내 데이터는 Ollama로 — 이런 운영을 같은 코드 베이스 안에서 한다.

물론 추상화의 한계도 있다. provider별 고유 기능(Claude의 긴 사고, OpenAI의 reasoning 모드, Gemini 멀티모달)을 풀로 쓰려면 `OpenAiChatOptions`·`AnthropicChatOptions` 같은 provider별 옵션 객체에 손이 간다. Spring AI는 `ChatClient.prompt().options(...)`로 이걸 끼울 수 있게 했다. 90%는 추상화로, 10%는 provider별 fine-tuning으로 — 이 정도가 현실적인 균형이다.

---

## 7.9 Java 실습 (2) — LangChain4j로 같은 일을

Spring AI만 있는 게 아니다. **LangChain4j**라는 또 다른 강력한 후보가 있다. Python LangChain의 정신적 후속이고, 2023년부터 자체 노선으로 빠르게 컸다. 핵심 추상화는 `ChatLanguageModel` 인터페이스 + `AiServices`의 두 축이다.

Spring AI와 LangChain4j 중 어느 걸 고를지는 팀 컨텍스트에 따라 다르다. **이미 Spring 생태계에 깊이 들어가 있다면 Spring AI가 자연스럽다.** 자동 설정, Bean 주입, Actuator 통합이 그대로 따라온다. **반대로 Spring 없이 가볍게 쓰거나 LangChain의 풍부한 통합을 그대로 받고 싶다면 LangChain4j가 매력적이다.** 둘 다 적극적으로 개발되고 있고, 어느 쪽도 죽은 라이브러리가 아니다. 둘 다 한 번 써보고 손에 맞는 걸 고르는 편이 낫다.

같은 요약 태스크를 LangChain4j로 짜보자.

### `ChatLanguageModel` 직접 쓰기

가장 단순한 방식. 의존성을 추가한다.

```xml
<dependency>
  <groupId>dev.langchain4j</groupId>
  <artifactId>langchain4j-open-ai</artifactId>
  <version>0.36.2</version>
</dependency>
```

```java
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;

public class SimpleSummary {

    public static void main(String[] args) {
        ChatLanguageModel model = OpenAiChatModel.builder()
            .apiKey(System.getenv("OPENAI_API_KEY"))
            .modelName("gpt-4o-mini")
            .temperature(0.2)
            .maxTokens(512)
            .build();

        String response = model.generate(
            "사내 개발 문서 요약 시스템을 한 문장으로 설명하라."
        );
        System.out.println(response);
    }
}
```

`OpenAiChatModel.builder()` 한 줄로 모델 객체를 만들고, `generate(...)`로 호출한다. 단순하다. 위 코드는 완전한 standalone Java 프로그램이다. Spring 없이도 LLM 호출이 된다. CLI 도구나 데이터 파이프라인 같은 데서 가볍게 쓰기에 좋다.

### `AiServices`로 한 단계 추상화

LangChain4j의 진짜 매력은 `AiServices`다. **자바 인터페이스를 선언하면 LangChain4j가 그 인터페이스의 구현체를 동적으로 만들어 LLM 호출을 끼워준다.** Spring Data JPA의 `JpaRepository`가 인터페이스만 선언해도 구현체가 자동으로 생기는 것과 같은 발상이다.

```java
// 1. 인터페이스만 선언
public interface DocumentSummarizer {

    @SystemMessage("""
        너는 사내 개발 문서 요약 도우미다.
        - 출력은 한국어 JSON. 키는 summary, keywords, confidence.
        """)
    Summary summarize(@UserMessage("다음 문서를 요약하라.\n\n---\n{{doc}}\n---")
                      String doc);
}

public record Summary(String summary, List<String> keywords, double confidence) {}
```

```java
// 2. 인스턴스 생성
DocumentSummarizer summarizer = AiServices.builder(DocumentSummarizer.class)
    .chatLanguageModel(model)
    .build();

// 3. 메서드 호출만 하면 끝
Summary result = summarizer.summarize("Spring Boot 3.3은 ...");
System.out.println(result.summary());
```

`@SystemMessage`와 `@UserMessage` 애너테이션으로 프롬프트를 박아두고, 메서드를 부르면 LLM 호출이 일어난다. 응답은 `Summary` POJO로 자동 역직렬화된다. **인터페이스 한 장이 LLM 호출 모듈이 되는** 모양이다. Spring 친화적인 백엔드 개발자에게 무척 자연스럽다.

LangChain4j도 provider 교체가 의존성 한 줄이다. `langchain4j-open-ai`를 `langchain4j-anthropic`이나 `langchain4j-ollama`로 갈아 끼우고, builder 클래스만 바꾸면 같은 인터페이스가 그대로 동작한다.

```java
// Anthropic으로
ChatLanguageModel model = AnthropicChatModel.builder()
    .apiKey(System.getenv("ANTHROPIC_API_KEY"))
    .modelName("claude-3-5-haiku-latest")
    .build();

// Ollama로
ChatLanguageModel model = OllamaChatModel.builder()
    .baseUrl("http://localhost:11434")
    .modelName("llama3.1:8b")
    .build();
```

`DocumentSummarizer` 인터페이스의 시그니처는 한 글자도 안 변한다. Spring AI와 같은 약속이다. 두 라이브러리가 비슷한 약속을 한다는 건 자바 LLM 생태계가 그쪽으로 수렴하고 있다는 신호다. 좋은 일이다.

---

## 7.10 Ollama로 로컬에서 돌리기

여기까지 SaaS API 위주로 이야기했다. 그런데 사내 데이터의 민감도, 비용, 또는 단순히 인터넷이 없는 환경에서는 **로컬 모델**을 돌리고 싶을 때가 있다. Mac M 시리즈에 8GB VRAM이면 Llama 3.1 8B가 현실적인 기본값이다. 도구는 **Ollama**가 가장 단순하다.

설치는 한 줄.

```bash
# macOS
brew install ollama
# 또는 https://ollama.com 에서 설치 파일 다운로드

# 모델 다운로드 + 첫 실행
ollama run llama3.1:8b
```

처음 실행하면 모델이 자동으로 다운로드된다. 8B 모델은 약 4.7GB. 한 번 받아두면 이후엔 즉시 뜬다. Ollama는 백그라운드에 OpenAI 호환 HTTP 서버를 11434 포트에 띄운다. 즉, **OpenAI SDK를 그대로 쓰되 base URL만 바꿔주면** Ollama 모델이 호출된다.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # 아무 값이나, 검증 안 함
)

resp = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "사내 개발 문서 요약을 한 문장으로."}],
)
print(resp.choices[0].message.content)
```

Spring AI에서는 7.8에서 본 그대로다. 의존성과 yml만 바꾸면 같은 `SummaryService` 코드가 로컬 모델로 돌아간다. 이게 Spring AI가 약속한 추상화의 진짜 가치다. **실제로 같은 코드가 OpenAI, Anthropic, Ollama 위에서 다 돌아가는 걸 한 번 손으로 확인하고 나면**, Java 서비스에 LLM을 넣는 일이 더 이상 막막하지 않다.

> **GPU 없을 때 박스**
> Mac M1 8GB 통합 메모리에서도 Llama 3.1 8B 4bit 양자화(`llama3.1:8b`는 기본 Q4_K_M)가 돈다. 응답 속도는 사람이 글을 쓰는 속도와 비슷하다. 더 가벼운 모델이 필요하면 `qwen2.5:3b`나 `phi3:mini`(3.8B), 더 빠른 응답이 필요하면 클라우드 API를 섞어 쓰는 하이브리드도 좋다. "로컬에서 빠르게 PoC, 트래픽 늘면 클라우드"가 흔한 패턴이다.

로컬 모델을 짧게 정리하자. **장점**: 데이터가 외부로 안 나간다, API 비용 0, 오프라인 동작, 응답 지연이 일정. **한계**: GPT-4o급 품질 대비 떨어진다(8B 기준), 동시 요청 한계, 모델 업데이트는 직접 관리. 사내 민감 문서 PoC나 폐쇄망에서 가장 빛난다. **"일단 일주일 써보고 결정하라"** — r/LocalLLaMA의 격언이다. 머리로 고르지 말고 손으로 고르자.

---

## 7.11 관측성 — 신뢰할 수 없는 함수에는 로그가 필요하다

"프롬프트 한 줄 바꿨는데 응답 품질이 왜 떨어졌지?" 이 질문이 나온 순간이 관측성을 미루지 말아야 할 신호다. LLM은 신뢰할 수 없는 함수고, 입력이 같아도 출력이 달라지고, 내부에서 무슨 일이 일어났는지 우리는 모른다. 백엔드 개발자에게 익숙한 처방이 있다. 로그·메트릭·트레이스. 잘 쌓아두면 디버깅도 평가도 가능해진다. LLM 개발에서는 일반 백엔드보다 **더 일찍, 더 깊게** 필요하다는 점만 기억해두자.

Python 진영에는 **LangSmith**(LangChain 팀의 SaaS)와 **Langfuse**(오픈소스 자체 호스팅 가능)가 널리 쓰인다. 둘 다 OpenAI/Anthropic SDK 호출을 자동으로 hooking해서 트레이스를 쌓아주는 방식이고, 클라이언트 import 한 줄 갈아 끼우는 수준으로 켠다.

Java/Spring 진영에는 더 익숙한 손잡이가 있다. **Spring AI Observation**이다. Spring Boot의 `Micrometer` + `Tracing`(Brave/OpenTelemetry) 위에 자연스럽게 올라간다. 의존성 추가만으로 LLM 호출 한 건마다 (a) 입력/출력 토큰 수, (b) 지연 시간, (c) 모델명, (d) finish_reason이 자동으로 메트릭과 트레이스로 쌓인다.

```xml
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
  <groupId>io.opentelemetry</groupId>
  <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

```yaml
spring:
  ai:
    chat:
      observations:
        include-prompt: true       # 프롬프트도 트레이스에 포함 (보안 검토 후 켜자)
        include-completion: true   # 응답도 포함
management:
  tracing:
    sampling:
      probability: 1.0
```

이 설정이 켜지면 `spring.ai.chat.client` 메트릭과 `chat ${provider}` 트레이스가 Actuator로 흘러나온다. Grafana, Tempo, Loki 같은 기존 백엔드 관측성 스택에 그대로 꽂힌다. **LLM 호출이 일반 RPC처럼 다뤄진다.** 백엔드 개발자에게 이건 어마어마한 친숙함이다.

한 가지 주의할 점. **프롬프트와 응답을 트레이스에 그대로 담으면 PII·기밀 데이터가 트레이스 저장소로 흘러간다.** Spring AI Observation이 제공하는 마스킹 콜백을 써서 운영 진입 전에 한 번 정리하자. 첫 PoC에선 다 켜고 보고, 그다음에 다듬는 흐름이 무난하다.

---

## 7.12 돌아보며 — 우리가 같이 걸어온 길

긴 길이었다. 한 번 뒤를 돌아보자. 지금까지 같이 짚어온 것들을 머릿속에 지도로 다시 펴두면, 다음 장으로 넘어가는 발걸음이 한결 가볍다.

Chat Completions API의 스키마를 해부하는 것에서 출발했다. `messages`·`temperature`·`top_p`·`max_tokens`·`stop`·`stream`·`finish_reason`·`usage`. 어느 provider를 가도 거의 똑같은 이 이름들을 4장 디코딩 루프의 손잡이와 1:1로 매핑해 봤다. 개념은 4장에서 이미 익혔으니, 여기서는 연결만 하면 됐다.

그 뒤에 가장 뼈아픈 장면이 있었다. **"Temperature=0 is a Lie"의 정체**. GPU 부동소수점의 비결정성과 배치 효과 때문에 같은 입력이 다른 출력을 낸다는 사실. `seed`와 `system_fingerprint`로 최선을 다하되, 테스트는 정확 일치가 아니라 의미 일치로 짜야 한다는 결론까지 같이 왔다. 프롬프트 엔지니어링의 기본기(역할 분담, few-shot, CoT, ReAct)를 챙긴 뒤, Python으로 OpenAI/Anthropic SDK를 다뤘고 LangChain으로 한 꺼풀 추상화하는 모양도 봤다.

회고 콜아웃에서는 "만든다"에서 "쓴다"로 관점이 회전하는 장면을 정리했고, 공통 태스크의 네 답을 한 표에 겹쳐 봤다. 그런 다음 이 장의 진짜 주공인 Java 쪽으로 건너와서 Spring AI의 `ChatClient`·Advisor·`entity()`, 그리고 LangChain4j의 `AiServices`까지 같은 태스크를 두 번 짜봤다. Maven 의존성 한 줄로 OpenAI ↔ Anthropic ↔ Ollama 스왑이 정말로 되는 것, 로컬 모델(Ollama)이 PoC의 든든한 한 축이 된다는 것, Spring AI Observation으로 호출 한 건마다 관측성이 붙는다는 것까지 손으로 확인했다.

여기까지 오면 한 가지 실력이 생겼다. **LLM을 함수처럼 호출하되, 그 함수가 신뢰할 수 없다는 사실을 인정하고 다루는 법.** 같은 함수가 매번 조금씩 다른 답을 내고, 가끔은 환각을 하고, 토큰 비용이 호출당 청구되고, provider가 바뀌면 미세한 행동도 바뀐다. 이런 함수를 백엔드 서비스에 안전하게 끼우려면 (a) 출력 검증, (b) 재시도 정책, (c) 비용 상한, (d) 관측성, (e) provider 추상화가 필요하다. 이 장에서 그 도구들을 다 짚었다.

그런데 여기까지 와도 한 가지 큰 문제가 남는다. **사내 개발 문서를 모델은 모른다.** GPT-4o든 Claude든 Llama든, 학습 데이터에 우리 회사 내부 위키가 들어 있을 리 없다. 프롬프트에 통째로 붙여 넣자니 컨텍스트 윈도우와 비용이 터진다. 6장처럼 파인튜닝해서 모델 안에 박아 넣을 수도 있지만, 문서는 매주 갱신된다. 갱신될 때마다 재학습할 수도 없다. 그래서 또 다른 길이 필요하다.

다음 장에서 그 길을 같이 걷는다. **검색을 먼저 하고, 검색 결과를 컨텍스트에 끼워서, 모델에게 답을 시킨다.** 이름은 RAG(Retrieval-Augmented Generation). 공통 태스크의 **네 번째 답**이다. 7장에서 익힌 Spring AI `ChatClient` 위에 `QuestionAnswerAdvisor` 한 줄을 더 끼우는 것만으로 RAG가 동작하는 모양을 보게 될 것이다. 같이 가자.