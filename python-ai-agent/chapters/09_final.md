# 9장. LangChain의 그늘 — 비판, 옹호, 그리고 골라 쓰기

LangChain에 대해 처음 인터넷 검색을 해본 사람의 표정을 한번 상상해 보자. 한쪽 탭에는 *"production 표준이다, 안 쓰면 손해다"*라는 글이 떠 있고, 바로 옆 탭에는 *"LangChain은 망했다, 우리는 갈아엎고 다시 짰다"*라는 회고가 떠 있다. 같은 라이브러리에 대한 평이 맞나 싶을 정도로 진폭이 크다. 어느 쪽 말을 믿어야 할까? 둘 다 거짓말은 아니다. 단지 두 사람이 *서로 다른 깊이*에서 LangChain을 만져봤을 뿐이다.

8장에서 우리는 LangChain의 빛나는 자리를 살펴봤다. 100여 개의 벡터 DB 어댑터, 도구 카탈로그, 그리고 LangSmith. "사용자에게 광적으로 귀를 기울인다"는 Hamel Husain의 옹호도 인용했다. 그런데 같은 Hamel이 *"처음엔 LC에 짜증냈다"*고 시작한 트윗이라는 사실도 기억해 두자. 옹호조차도 마지못한 옹호였다. 짜증이 어디서 왔는지 정직하게 들춰보지 않고서는 LangChain을 *얼마나 받아들이고 어디서 거절할지* 결정할 수 없다.

이번 장에서 하려는 일은 단순하다. LangChain 비판을 *진지하게* 한 줄씩 검증한다. 어디까지 사실이고, 어디부터 과장인가. 그리고 그 검증의 끝에서 이 책의 입장을 한 번 더 단단히 못 박는다 — "LangChain은 골라 쓰는 라이브러리, 통째로 삼키는 종교가 아니다."

## 3개 이상의 소스에서 반복되는 6가지

LangChain 비판은 인터넷에 차고 넘친다. 그러나 개인의 한순간 분노로 끝나는 글도 적지 않다. 진지하게 다루려면 *반복되는 패턴*만 골라 보자. Designveloper, Woyera, Shashank Guda, safjan, TechTide, Latenode 커뮤니티 — 이 여섯 소스를 가로질러 일관되게 등장하는 비판은 다음 여섯 가지다.

1. **추상화 과잉** — OpenAI 한 줄 호출이 클래스 세 개를 거친다.
2. **breaking change의 잦은 빈도** — minor 버전 사이에서도 API가 깨진다. 한 달 전 튜토리얼이 안 돈다.
3. **문서와 실제의 불일치** — 공식 예제를 그대로 복사해 붙여도 동작하지 않는 경우가 있다.
4. **로깅·디버깅의 어려움** — 어떤 프롬프트가 *실제로* 모델에 나갔는지 추적이 답답하다.
5. **숨은 비용** — `with_retry()`, `with_fallbacks()` 같은 "내장된 회복력"이 사실은 *내장된 토큰 청구서*다.
6. **production 수준 에러 핸들링 부재** — try/catch와 재시도를 결국 우리 손으로 다시 짠다.

각 항목을 한 줄씩 정직하게 검증해 보자. 어떤 비판은 100% 사실이고, 어떤 비판은 절반은 사실, 절반은 오해다. 구분하는 시선을 길러야 한다.

### 추상화 과잉 — 사실, 그러나 의도된 측면이 있다

OpenAI SDK로 한 줄 호출하면 `client.chat.completions.create(...)`다. 같은 일을 LangChain으로 하면 `ChatPromptTemplate`, `ChatOpenAI`, `StrOutputParser` 세 객체를 거친다. 코드 줄 수가 1줄에서 7~8줄로 늘어난다. 처음 본 사람의 첫 반응은 "왜 이렇게 복잡하게 만들었어?"이고, 그 반응은 **사실 맞다**.

다만 한 가지 자문해 보자. 만약 우리가 짜는 코드가 영원히 *한 번의 모델 호출*에서 끝난다면 LangChain은 분명한 과잉이다. 그런데 그게 prompt 합성, 도구 호출, 출력 파싱, 스트리밍, 배치, 비동기, 재시도, fallback의 *조합*으로 진화한다면? 그때부터는 클래스 세 개를 거치는 비용이 *합성 가능성*이라는 보상으로 돌아온다.

비판 그대로 받아들이되, 단서를 달자. *예제 크기에서 보면 추상화 과잉*이지만, *production 크기에서 보면 합성 가능성*이라는 동전의 두 면이다. 한 번의 호출이라면 SDK를 직접 쓰자. 합성과 스트리밍이 곳곳에서 필요한 시스템이라면 LangChain의 표면적 복잡도가 결국 단순함을 만들어 준다. 어느 쪽 무게가 더 큰지는 *프로젝트 규모*가 결정한다.

### Breaking change — 사실, 그리고 가장 아픈 비판

이 항목은 균형을 잡을 여지가 별로 없다. 2024년부터 2026년 사이의 LangChain은 두 번의 큰 정리(0.1 → 0.2 → 0.3)를 거쳤다. 그 사이에 패키지가 `langchain_core`, `langchain`, `langchain_community`, `langchain_<provider>`로 쪼개졌고, 옛 chain 클래스가 LCEL로 갈아엎혔고, 옛 memory 클래스가 LangGraph로 이주를 강요받았다.

구체적인 예 하나만 짚어 보자. 0.1 시절의 LangChain 튜토리얼은 거의 모두 이런 모양이었다.

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([("human", "{q}")])
chain = LLMChain(llm=llm, prompt=prompt)
chain.run(q="hi")
```

이걸 0.3 환경에서 그대로 실행하면 어떻게 될까? 우선 `langchain.chat_models`가 deprecation warning을 띄우며 `langchain_openai`로 옮기라고 요구한다. 다음으로 `LLMChain`은 LCEL의 `prompt | llm`으로 갈아끼우라고 권고한다. `.run()`은 `.invoke()`로 바뀐다. import 한 줄, 클래스 한 줄, 메서드 한 줄 — 세 군데가 동시에 깨졌다. 한 달 전 블로그 글이라도 호환이 안 된다.

이게 LangChain 사용자가 가장 자주 토로하는 분노의 핵심이다. 같은 일을 *세 번째 방식*으로 다시 배우는 피로감. 게다가 deprecation 정책이 친절한 편도 아니다. 경고 메시지는 띄우지만, *언제까지* 호환되는지는 분명히 못 박지 않는 경우가 잦다. 회사 코드베이스가 한 번 LangChain에 의존하면, *분기마다* 의존성 업그레이드 비용이 따라온다. 끔찍한 일이다.

이 비판은 옹호의 여지가 거의 없다. 우리가 할 수 있는 대처는 두 가지다. 첫째, `langchain.xxx`로 시작하는 옛 import 경로는 일단 의심하고 `langchain_core` 또는 `langchain_<provider>` 경로로 옮긴다. 둘째, 가능하다면 *우리 코드의 LangChain 의존 표면을 좁힌다*. LangChain이 어디서 깨질지 미리 알 수 없다면, 적어도 우리 코드의 어느 한 모듈에 깨짐을 가둬 두는 편이 낫다.

### 문서와 실제의 불일치 — 절반은 사실, 절반은 다음 항목의 그림자

"공식 예제 복사해서 붙였는데 안 돈다"라는 불평을 들춰 보면, 그중 상당수가 *위에서 본 breaking change*의 후폭풍이다. 문서가 최신 코드를 따라잡지 못한 상태로 잠시 머문 동안 작성된 글이라는 뜻이다. 그러니까 비판 3번은 비판 2번의 부산물에 가깝다.

다만 100% 부산물은 아니다. LangChain은 통합 어댑터의 수가 워낙 많아서, *덜 인기 있는 통합*의 문서는 자체적으로 오래된 채로 방치되는 일이 있다. 인기 있는 OpenAI·Anthropic 통합은 빠르게 갱신되지만, 변두리 벡터 DB나 마이너 retriever는 사정이 다르다. 통합의 *수*가 강점인 동시에 *문서 품질의 분산*이라는 약점을 낳는다. 어느 통합을 선택할 때 GitHub의 마지막 커밋 시점을 한 번 들여다보는 습관이 안전한 이유다.

### 로깅·디버깅의 어려움 — 사실이었으나, LangSmith로 해소된다

이 비판은 6가지 중에서 가장 *시점*에 민감한 항목이다. 2023년 초까지는 100% 사실이었다. LangChain이 어떤 프롬프트를 실제로 모델에 보냈는지, 어떤 결과가 돌아왔는지, 추적이 진짜로 답답했다. `verbose=True`로 표준 출력에 흩뿌리는 것이 디버깅의 전부였던 시절이 있었다.

그런데 LangSmith가 등장하면서 이야기가 달라졌다. 8장에서 우리가 본 그대로, LangSmith를 켜면 매 LLM 호출, 매 도구 호출, 매 LCEL 단계의 입출력이 trace 트리로 시각화된다. 우리가 직접 `print()`로 흩뿌리지 않아도 된다. 이 비판은 *해소되었지만, LangSmith 없이는 여전히 사실*이라는 단서를 달아 둬야 한다.

그러니까 받아들임은 이렇다. LangChain 본체만 쓰고 LangSmith는 쓰지 않는 경로? 디버깅 답답함을 그대로 안고 가야 한다. LangChain + LangSmith의 묶음? 비판이 거의 무력화된다. *그리고 흥미로운 사실*은, 8장 끝에서 짚었듯 LangSmith는 LangChain 본체와 *묶이지 않은 채로도* 우리 코드에 붙는다. 이게 다음 절에서 다룰 *골라 쓰기* 입장의 기술적 뒷받침이다.

### 숨은 비용 — 가장 슬며시 다가오는 비판

LangChain의 친절한 헬퍼 함수들 — `with_retry()`, `with_fallbacks()` — 은 코드를 한 줄짜리로 깔끔하게 만들어 준다. 그런데 그 한 줄 뒤에서 *토큰이 얼마나 더 쓰이는지* 가시화해 본 적 있는가? 한 번 들춰보면 답답해진다. 이 책 7장의 끄트머리에서 슬쩍 예고했던 회수를 이제 해보자.

```python
import tiktoken
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import UsageMetadataCallbackHandler

base_llm = ChatOpenAI(model="gpt-4o-mini")
retry_llm = base_llm.with_retry(stop_after_attempt=3)

cb = UsageMetadataCallbackHandler()
# 일부러 모델이 깨지는 입력을 주거나, 5xx 시뮬레이터를 끼우는 환경이라면
# retry가 발동하면서 동일 프롬프트가 1~3회 재호출된다.
retry_llm.invoke("긴 문서를 요약해줘: ..." * 500, config={"callbacks": [cb]})

print(cb.usage_metadata)
# {'gpt-4o-mini': {'input_tokens': 6000*3, 'output_tokens': ...}}  ← 재시도 3회면 토큰 3배
```

LangChain의 `with_retry()`는 *같은 프롬프트로 다시 호출*하는 동작이다. 5xx 같은 일시적 네트워크 오류라면 정당한 비용이다. 그런데 *모델이 답을 못 만들거나 형식이 안 맞아서* retry가 발동되는 경우라면? 동일하게 망가질 프롬프트를 두 번, 세 번 더 보내고 결국 같은 실패를 받는다. 입력 토큰만 그대로 곱절로 청구된다.

`with_fallbacks()`는 한술 더 뜬다. 한 모델이 실패하면 다음 모델로 같은 프롬프트를 다시 보낸다. 코드 한 줄로 깔끔하지만, *5xx 에러가 아니라 모델의 답이 마음에 안 들어서* fallback이 도는 흐름이라면 토큰은 두 모델치를 다 쓴다. 게다가 fallback 모델이 더 크고 비싼 모델이라면 비용 그래프가 추가로 한 번 더 튄다.

LangChain이 잘못 짰다는 뜻은 아니다. 친절한 한 줄 뒤에 있는 *동작의 본질*을 모르고 쓰면 비용이 다음 달 청구서에 묻혀 온다는 뜻이다. 이 비판은 사실이되, *알면 피할 수 있는 비판*이다. retry 정책을 쓰기 전에 *어떤 종류의 실패를 재시도할 가치가 있는지* 한 번은 생각해 보자. 5xx와 rate limit은 재시도하되 모델의 형식 위반에는 *재시도가 아닌 다른 처치*를 한다는 정책이 토큰을 아낀다.

### Production 에러 핸들링 — 절반은 사실, 절반은 누구나 그렇다

"LangChain은 production 수준의 에러 핸들링이 없다"라는 비판은 자주 들린다. 그런데 한 발 떨어져서 생각해 보자. 어떤 라이브러리가 *모든 production 시나리오에 맞는 에러 핸들링을 미리 짜 줄* 수 있는가? 결국 회사 정책, 도메인 요구, 사용자 경험의 결합이 에러 처리 모양을 결정한다. 라이브러리가 그걸 미리 알 수 없다.

다만 LangChain의 기본 동작이 *덜 친절한* 측면은 있다. 예외가 나면 LCEL 파이프 한가운데서 그대로 던져지고, 어느 단계에서 터졌는지 stack trace만 가지고는 가늠하기 어려운 경우가 있다. 도구 호출이 실패했을 때 LLM에게 "에러를 봤으니 다시 시도하라"고 자연스럽게 알려 주는 기본 동작도, 라이브러리가 일률적으로 정해 두지 않는다. 결국 우리가 try/except로 감싸고 LLM에 다시 던지는 로직을 직접 짠다.

이 비판은 *기대치 조정*으로 받아들이는 편이 낫다. LangChain은 우리 시스템의 *합성 추상*과 *통합 어댑터*를 제공하지, 도메인 특화 에러 정책을 제공하지 않는다. 그 부분은 우리 손으로 짜야 한다는 점, 미리 알고 쓰자.

## Breaking change의 실제 모양, 조금 더 가까이

위에서 한 줄로 짚은 deprecation을 한 번 더 가까이서 들여다보자. 0.1 → 0.2 → 0.3 사이에서 가장 자주 깨진 자리 두 곳을 고른다.

첫째, **memory 모듈의 이주**. 0.1 시절 LangChain은 `ConversationBufferMemory`, `ConversationSummaryMemory` 같은 memory 객체를 chain에 붙여 쓰라고 권했다. 0.2 후반부에 와서 공식 문서가 톤을 바꿨다. *"short-term/long-term memory가 필요하면 LangGraph + checkpointer로 가라"*로 권고가 옮겨 갔다. 0.3에서는 옛 memory 클래스에 deprecation warning이 정식으로 붙었다.

문제는 이 이주가 *단순 import 경로 변경*이 아니라는 점이다. 사고방식 자체가 다르다. 옛 memory는 *chain 내부의 변수*였고, LangGraph checkpointer는 *상태 그래프 위의 영속 저장소*다. API뿐만 아니라 멘탈 모델까지 새로 학습해야 했다. 한 번 쓰던 코드를 안 깨고 옮길 방법이 *없는* 종류의 breaking change다.

둘째, **chain의 LCEL 이주**. 0.1 시절의 `LLMChain`, `ConversationChain`, `RetrievalQA.from_chain_type` 같은 고수준 chain 클래스는 0.2/0.3에서 모두 *권장되지 않는 흐름*으로 분류되었다. 같은 일을 LCEL로 표현하라는 권고가 따라붙었다. 단순한 한 줄 호출은 그래도 어떻게든 갈아치울 수 있지만, `RetrievalQA.from_chain_type` 같은 고수준 추상은 *내부 동작을 재현하기 위해 여러 LCEL 노드를 직접 합성*해야 옮겨진다. 한 줄짜리 마법이 사라지고 다섯 줄짜리 명시적 파이프가 그 자리에 들어선다. 명시성을 얻는 대신 코드 복사 비용을 치른다.

이 두 사례가 LangChain의 breaking change가 어떤 *결*인지 보여 준다. 단지 함수 이름이 바뀐 게 아니라, *추천하는 멘탈 모델 자체*가 옮겨 다닌다. 이게 사용자 입장에서 가장 짜증나는 형태의 깨짐이다. 라이브러리에 발을 깊게 담그면 담글수록 손해가 누적된다는 뜻이기도 하다.

## 옹호의 자리 — 그래도 다들 쓰는 이유

비판 여섯 줄을 길게 들춰봤으니, 균형을 위해 옹호도 정직하게 한 번 더 정리해 두자. Hamel Husain이 마지못해 했던 옹호의 핵심은 한 문장이다. *"업계 사람들과 일해 보니 다들 langchain을 쓰고 있더라."* 왜 다들 쓰는가? 추상화가 우아해서? 아니다. *시장 속도에 맞춰 통합을 쏟아내는 라이브러리가 사실상 유일했기 때문*이다.

새로운 벡터 DB가 등장한 다음 주에 어댑터가 들어와 있고, 새로운 모델 provider가 공개된 같은 주에 `langchain_<provider>` 패키지가 나오고, "trace에서 X 정보가 필요해요" 한 줄을 issue에 남기면 다음 minor 버전에 들어와 있다. 라이브러리가 사용자 요청에 광적으로 응답한다 — Hamel이 본 LangChain의 진짜 강점은 이것이다. 추상화의 우아함이 아니라 *반응 속도*다.

그리고 표준화의 가치. 우리 회사에서 새로 합류한 동료가 LangChain 코드를 본 경험이 있다면, 첫날부터 코드를 읽을 수 있다. SDK 직접 호출이라면 회사별 자작 추상을 한 번씩 다시 학습해야 한다. *공통 어휘*가 주는 가치는 라이브러리의 미적 우아함과 별개로 인정해야 한다. 코드 리뷰 속도, 신규 입사자 온보딩, 외부 컨설턴트 협업 — 이 모든 자리에서 LangChain은 "어디 가나 같은 모양"이라는 미덕을 발휘한다.

한 가지 더 짚어 둘 옹호가 있다. *생태계의 중력*이다. 새로운 도구가 등장했을 때 그 도구의 첫 통합이 거의 항상 LangChain 어댑터로 먼저 나온다는 사실, 무시할 수 없다. 모델 provider, 벡터 DB, 임베딩 서비스, retrieval 도구 — 모두 LangChain을 *기본 진입 채널*로 삼는다. 우리가 직접 SDK 추상을 짜는 경우에도, "다른 사람들이 어떻게 그 도구를 호출하나"의 *참조 구현*으로 LangChain 어댑터를 들춰보는 일이 적지 않다. 라이브러리를 직접 import하지 않더라도, *생태계의 좌표*로서의 가치는 인정해 둘 만하다.

## 이 책의 입장 — 골라 쓰기

비판도 옹호도 정직하게 들어 봤다. 그렇다면 결론은? 둘 중 하나를 *통째로* 받아들이는 건 답이 아니다. 이 책의 입장을 한 문장으로 명문화하자.

> **LangChain은 골라 쓰는 라이브러리, 통째로 삼키는 종교가 아니다.**

8장 끝에서 짚었듯이 LangChain 생태계는 사실상 세 겹이다. 가장 안쪽에 `langchain_core`(Runnable, LCEL, tool 추상), 그 위에 `langchain`(고수준 chain·agent, 빠르게 deprecate되는 옛 API 다수), 가장 바깥에 `langchain_community` 및 provider별 패키지(통합 어댑터). 옆에 LangSmith와 LangGraph가 독립된 도구로 떨어져 산다. 우리가 받아들일지 거절할지를 *겹별로* 정할 수 있다.

가장 단단한 *hybrid 패턴*이 하나 있다. `langchain_core`의 Runnable 추상만 빌려 와 합성의 골격으로 쓰고, 모델 호출은 SDK로 직접, 도구는 우리 손으로 짠 함수, 관찰은 LangSmith로. 한번 모양을 그려 보자.

```python
from langchain_core.runnables import RunnableLambda
from openai import OpenAI
import os

client = OpenAI()  # LangChain의 ChatOpenAI를 쓰지 않는다

def call_model(prompt: str) -> str:
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

def parse_summary(text: str) -> dict:
    # 우리가 직접 짠 파서. LangChain의 OutputParser를 쓰지 않는다.
    return {"summary": text.strip(), "length": len(text)}

# 합성 추상만 LangChain의 것을 빌린다. 그러면 LangSmith trace가 그대로 붙는다.
pipeline = RunnableLambda(call_model) | RunnableLambda(parse_summary)

# 환경 변수에 LANGSMITH_TRACING=true가 켜져 있으면
# 별도 코드 한 줄 없이 LangSmith 대시보드에 trace가 쌓인다.
result = pipeline.invoke("긴 문서를 짧게 요약해줘")
```

이 ~15줄짜리 패턴이 보여 주는 것은 분명하다. LangChain의 `ChatOpenAI`도, `with_retry()`도, `StrOutputParser`도, `LLMChain`도 쓰지 않는다. 그런데 LangSmith 대시보드에는 *합성 파이프의 모든 단계*가 trace로 떠 있다. 추상화 과잉의 비판도 피하고, breaking change의 위험 표면도 좁히고, 숨은 토큰 비용도 우리가 직접 통제한다. 동시에 LangChain 생태계의 가장 큰 강점(LangSmith)은 그대로 챙긴다. 한 끼 식사로 *반찬만 골라 담는* 방식이다.

물론 이 패턴이 모든 자리에 맞지는 않다. 통합 어댑터 100여 개의 혜택을 누리고 싶다면 `langchain_community`나 provider별 패키지의 도움을 받는 편이 낫다. RAG 파이프라인이 *벡터 DB 다섯 개를 옮겨 다니며 비교*하는 작업이라면 어댑터의 동질성이 우리가 직접 짤 추상보다 빠르다. 결정의 기준이 단 하나다 — *우리가 직접 짤 마음이 드는 자리인가, 아닌가.*

## 결정 트리 — 이 기능이면 LangChain, 이 기능이면 직접 짜자

비유와 입장 표명만으로는 실무 결정에 충분치 않다. 한 페이지 결정 트리를 손에 쥐고 가자. 새 기능을 추가할 때마다 이 표를 한 번씩 들여다보면 *어느 겹의 LangChain*을 쓸지 빠르게 답이 나온다.

| 우리에게 필요한 기능 | 권장 결정 |
|---|---|
| 단발성 모델 호출 한 줄 | SDK 직접 호출 (LangChain 없이) |
| Prompt + LLM + 파서의 합성, 스트리밍·배치 자동화 | `langchain_core`의 LCEL |
| 여러 단계의 호출 trace를 한눈에 보기 | **LangSmith** (LangChain 본체 없이도 가능) |
| 새로운 벡터 DB(예: Qdrant, Weaviate)에 빠르게 붙기 | `langchain_community` 또는 provider별 패키지 |
| 100개 문서 RAG 인덱싱 + Retriever 합성 | `langchain_core` + `langchain_<provider>` |
| 자동 retry, 자동 fallback (토큰 비용 감수) | `with_retry()`, `with_fallbacks()` (정책 사전 검토 필수) |
| 사이클이 있는 흐름, 사람의 개입(HITL), 상태 영속화 | **LangGraph** (LangChain 본체는 거의 사용 안 함) |
| 옛 `ConversationBufferMemory` 류로 대화 이력 관리 | **쓰지 말자**. LangGraph checkpointer로 |
| 옛 `LLMChain`, `RetrievalQA.from_chain_type` 류 | **쓰지 말자**. LCEL로 갈아끼우자 |
| 회사 표준이 "다른 동료도 읽을 수 있어야 한다" | LangChain (어휘의 표준화 가치) |
| 토큰 비용이 가장 큰 변수인 production 환경 | SDK + `langchain_core`의 hybrid 패턴 |
| 마이너 통합(잘 안 알려진 벡터 DB, 잘 안 알려진 retriever) | 우리가 직접 어댑터 짜는 편이 낫다 |

표 한 장이지만 짚는 메시지는 단순하다. *기능 단위로 결정하자.* "LangChain을 쓸 것인가?"가 아니라 "*이 기능에* 어느 도구가 맞는가?"로 질문을 바꾸자. 같은 시스템 안에서 어떤 기능은 LangChain으로, 어떤 기능은 SDK로, 어떤 기능은 LangGraph로 — *섞어 쓰는 게 default*다.

## smolagents — 너무 무거우면 어디로 갈 수 있나

LangChain의 무게가 부담스럽다는 결론에 이른 사람을 위해, 미니멀 대안을 한 페이지 분량으로 짚어 두자. 가장 자주 거론되는 보기가 Hugging Face의 [smolagents](https://github.com/huggingface/smolagents)다. 코드베이스 전체가 ~1,000줄이다. LangChain의 코드 분량과 비교하면 한 자릿수 줄어든다.

smolagents의 핵심 발상은 흥미롭다. 도구를 JSON 호출로 표현하지 않고 *파이썬 코드 자체를 액션*으로 다룬다. ReAct 루프에서 모델이 내놓는 "Action: search(query=...)" 대신 "Action: `search('langchain criticism')`"이라는 *실행 가능한 파이썬 표현식*이 나온다. 이걸 샌드박스 안에서 실행하고, stdout이 다음 turn의 Observation으로 들어간다. JSON 도구 호출 패러다임 대비 *단계 수와 LLM 호출이 약 30% 줄어든다*는 주장이 HF 블로그에 실려 있다.

hello-world는 정말로 짧다.

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel(),  # 기본 모델 자동 선택
)

result = agent.run("LangChain 비판이 가장 많이 다뤄지는 GitHub issue를 찾아줘")
print(result)
```

여덟 줄 안에 *검색 도구를 가진 ReAct 에이전트*가 한 번 돈다. 같은 일을 LangChain의 `AgentExecutor`로 짜면 import만 다섯 줄이 더 필요하다.

언제 smolagents가 맞는 선택인가? 단일 목적 에이전트, 도구 카탈로그 통합이 필요 없는 상황, 코드 의존 표면을 최소화하고 싶은 OSS 프로젝트, 보안 샌드박스가 이미 갖춰진 환경에서 *실행 가능한 액션 패러다임*의 효율을 누리고 싶을 때. 반대로 RAG + 벡터 DB + 다양한 provider 통합이 필요한 production이라면, smolagents의 단순함이 *우리가 직접 짤 어댑터 분량*으로 되돌아온다는 점도 기억해 두자.

smolagents가 LangChain을 *대체*한다고 단정할 자리는 아니다. 다만 "프레임워크는 LangChain뿐이다"라는 인상의 정정으로 한 페이지 분량을 내 줄 가치는 분명하다. 미니멀 대안이 *존재한다*는 사실 자체가 LangChain을 *통째로 삼키지 않을* 결심을 단단하게 만든다.

## 마무리 — Part 3로 가는 길목에서

이번 장의 한 줄을 한 번 더 새겨 두자. **LangChain은 골라 쓰는 라이브러리, 통째로 삼키는 종교가 아니다.** 추상화 과잉도, breaking change도, 숨은 토큰 비용도 정직하게 인정하되, 그렇다고 LangChain을 통째로 버리지도 않는다. 우리는 `langchain_core`의 합성 추상과 LangSmith의 관찰성이라는 *반찬*을 골라 담고, 나머지 자리는 SDK와 우리가 짠 함수로 채운다. 그게 6장에서 본 mini_agent의 정신과도 가장 자연스럽게 맞는다.

여기까지가 Part 2의 결산이다. 7장에서 LCEL의 표면을 다시 본 우리, 8장에서 생태계의 강점을 확인한 우리, 9장에서 비판을 정직하게 들춰본 우리. 이제 한 가지 자문이 남는다 — *LangChain의 LCEL만으로는 풀 수 없는 진짜 영역*은 어디에 있는가?

LCEL은 본질적으로 *DAG*다. 한 방향으로 흘러가는 화살표의 모음. 그런데 우리가 실제 에이전트를 짜다 보면 곧장 부딪히는 자리가 있다. *한 번 더 시도해야 한다*, *사람에게 물어보고 답을 기다려야 한다*, *상태를 디스크에 저장해 두고 내일 이어서 진행해야 한다*. 사이클, HITL, persistence. LCEL은 이 셋 중 어느 하나도 자연스럽게 표현하지 못한다.

그래서 LangChain의 같은 회사가 *별도 라이브러리*로 LangGraph를 내놓았다. 이름부터 다르다 — chain이 아니라 graph. 1장에서 "에이전트는 루프"라고 단언했던 우리의 정의가, Part 3을 거치며 자연스럽게 한 단어 확장된다. *"에이전트는 상태를 가진 그래프 위의 루프"*로. 그리고 mini_agent를 마지막으로 한 번 더 다시 짠다.

10장에서 만나자. LCEL이 사이클 앞에서 어떻게 무너지는지, 그리고 그래프가 그 자리를 어떻게 메우는지 — 이번에는 비판의 균형 잡기 없이, 순도 100%의 *기술적 필연*만 가지고 풀어 보자.
