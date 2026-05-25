# 1장. 왜 우리는 ChatGPT를 직접 만들려 하는가

ChatGPT 창에 "안녕"이라고 한 줄 입력해본 적이 있는가? 답이 돌아온다. 너무 자연스럽게 돌아와서, 정작 그 안에서 *무슨 일이* 벌어지고 있는지 한 번도 진지하게 들여다본 적이 없다는 사실을 깨닫게 된다. 가중치 어딘가에서 행렬 곱이 일어나고, 토큰이 한 개씩 흘러나오고, 그것을 우리는 *대화*라고 부른다. 그런데 그 *어딘가*가 정확히 어디인지, *어떤 코드*가 그 일을 하는지, 우리는 대체로 모른다.

모른 채로 잘 쓰면 된다는 입장도 있다. 자동차의 내연기관을 분해해본 적 없는 운전자가 도로를 잘 달리듯, ChatGPT의 내부를 몰라도 멋진 글을 받아낼 수 있다. 하지만 어떤 사람들에게는 그 "잘 쓰면 된다"가 *몹시 찜찜한* 일이다. 도구를 손에 쥐고 나면 어쩐지 분해해보고 싶어진다. 내부가 보이지 않는 검은 상자를 매일 두드리는 게 *직업*이 된 사람이라면 더더욱.

이 책은 그 찜찜함에서 출발한다. ChatGPT가 어떻게 굴러가는지 *코드 한 줄 한 줄로* 손에 쥐고 싶은 사람을 위한 책이다. 그리고 그 일을 시켜줄 작품이 마침 한 편 있다 — 안드레이 카르파시(Andrej Karpathy)의 **nanochat**.

전체 약 8천 줄. 한 사람이 직접 손으로 쳤다. 그 안에 토크나이저부터 GPT 모델, 사전학습 루프, SFT, RL, 추론 엔진, ChatGPT 모양의 웹 UI까지 *전부 다* 들어 있다. 그리고 결정적으로 — 8XH100 한 노드에서 3시간을 굴리면 *진짜로 ChatGPT 비슷한 무언가가 튀어나온다*. 그게 nanochat이고, 우리가 한 챕터씩 분해해서 펴볼 작품이다.

먼저 그 도발의 *정확한 모양*부터 들여다보자.

## 1.1 "100달러로 살 수 있는 가장 좋은 ChatGPT"

2025년 10월, 카르파시는 GitHub에 nanochat이라는 리포지토리를 공개하면서 한 줄의 카피를 던졌다.

> *the best ChatGPT that $100 can buy.*

GitHub Discussion #1의 제목이다. 이 한 줄에 책 한 권의 무게가 담겨 있다고 해도 과언이 아니다. 차분히 풀어보자.

먼저 "$100"의 무게. GPT-2가 2019년에 학습된 비용은 약 4만 3천 달러로 추정된다. 카르파시는 그와 *동급의 능력을 가진 모델*을 8XH100 한 노드에서 약 3시간, 정가 기준 $48 안팎(스팟 인스턴스라면 $15까지도 내려간다)으로 만든다고 약속한다. 그러니까 *7년 전에 4만 3천 달러였던 것이 오늘 50달러*가 된다는 이야기다. 압축률만 따져도 800배다. 이게 한 사람이 한 노드에서 한 오후 동안 *재현 가능한 일*이 됐다는 뜻이다.

다음으로 "ChatGPT"의 무게. 사전학습된 *문장 완성기*만 만드는 게 아니다. nanochat은 토크나이저 학습부터 사전학습(pretraining), SFT, 그리고 RL까지 가서, 마지막에는 FastAPI로 띄우는 ChatGPT 모양의 웹 UI까지 *한 리포에 다 들어 있다*. "The capital of France is" 같은 말을 받아서 "Paris"로 *문장을 잇는* 모델이 아니라, "프랑스 수도가 어디야?"라고 물으면 *대답하는* 모델까지를 한 자리에서 만든다. 그게 *ChatGPT*다.

마지막으로 "$100 can buy"의 무게. 살 수 있는 게 추상적인 *모델 가중치*가 아니라 *전 과정*이라는 뜻이다. 코드는 약 8천 줄이고, 한 사람이 손으로 직접 쳤다고 카르파시는 [HN 댓글](https://news.ycombinator.com/item?id=45569350)에 적었다. 흥미로운 한 줄: *"코드 대부분을 손으로 직접 쳤다. claude/codex agent를 몇 번 써봤지만 잘 안 됐다 — 아마 이 리포가 학습 데이터 분포에서 너무 멀리 떨어져 있어서 그런 듯하다."*

이 자조 섞인 한 문장이 책 전체의 톤을 잡는다. *AI를 쓰는 도구는 만들 수 있다. 하지만 AI를 *만드는 코드*는 여전히 사람의 손가락이 짠다.* 우리는 그 손가락이 짜놓은 8천 줄을 따라가며, ChatGPT가 어떤 식으로 *지어지는지*를 본다.

여기서 한 가지 *기대치를 조정해두고 가자*. nanochat이 "GPT-2급"이라고 할 때, 그건 *DCLM CORE라는 평가 지표에서 GPT-2(1.6B 파라미터)의 점수 0.256525를 넘는다*는 *측정 가능한 의미*에서다. ChatGPT-4o의 자리를 위협하는 모델이 아니다. nanochat의 d24 모델 파라미터 수는 약 5억 6천만 — GPT-2의 1/3 수준이다. 그런데도 *능력*은 GPT-2와 같거나 약간 낫다. 그 사이의 *7년*에 무슨 일이 있었는지 — RoPE, RMSNorm, ReLU², Muon, FP8, FlashAttention 3, 더 좋은 데이터, 더 좋은 학습 레시피 — 가 이 책의 *진짜 내용물*이다.

또 한 가지. nanochat의 리더보드를 잠깐 들여다보면 신호가 더 분명해진다. README의 표를 그대로 옮겨오자.

| # | 시간 | val_bpb | CORE | 설명 | 시기 |
|---|---|---|---|---|---|
| 0 | 168시간 | - | 0.2565 | 원본 OpenAI GPT-2 체크포인트 | 2019 |
| 1 | 3.04시간 | 0.74833 | 0.2585 | d24 baseline, slightly overtrained | 2026.01 |
| 2 | 2.91시간 | 0.74504 | 0.2578 | d26 + **fp8** | 2026.02 |
| 3 | 2.76시간 | 0.74645 | 0.2602 | total batch size 1M tokens로 | 2026.02 |
| 4 | 2.02시간 | 0.71854 | 0.2571 | dataset을 NVIDIA ClimbMix로 | 2026.03 |
| 5 | 1.80시간 | 0.71808 | 0.2690 | autoresearch round 1 | 2026.03 |
| 6 | 1.65시간 | 0.71800 | 0.2626 | autoresearch round 2 | 2026.03 |

원본 GPT-2가 168시간 걸리던 일이 2026년 봄에는 1.65시간이 됐다. 100배 빨라졌다. 같은 코드가 *반 년 만에 두 배 빨라지고 있다*. 이 표가 *살아 움직이는 리포지토리*라는 사실을 잘 보여준다. 우리가 책을 읽는 시점에도 누군가는 이 리더보드에 새로운 줄을 추가하고 있을 것이다.

그 *살아 있음*이 이 책을 쓰기 *위험하고 즐거운* 일로 만든다. 위험한 이유는, 6개월 뒤에는 라인 번호가 다 어긋날 수 있어서다. 즐거운 이유는, 우리가 단순히 *완결된 옛 작품*을 들여다보는 게 아니라 *지금 자라고 있는 작품*의 한 단면을 잡고 있다는 점이다. 책의 어떤 라인 번호가 안 맞으면 *함수명과 클래스명으로 검색*해서 새 위치를 찾자. 그건 *책의 실수*라기보다 *코드가 살아 있는 증거*다.

리더보드를 보다 보면 한 가지 더 흥미로운 흐름이 보인다. *autoresearch*라는 항목. 카르파시가 LLM 에이전트로 *하이퍼파라미터 자동 탐색*을 시도해서 학습 시간을 더 줄인 결과다. AI를 *만드는* 코드에 AI를 *써본* 한 시도. 결과는 *부분적으로 성공*이고, 12장 마지막에 한 번 더 이 사례를 짚는다. AI가 AI를 만드는 코드를 짤 수 있게 되는 날이 어느 날 갑자기 올지, 아니면 *멀어 보였지만 결국 점진적으로* 올지 — 그게 nanochat을 둘러싼 흥미로운 *메타 질문* 중 하나다.

## 1.2 가계도 — nanoGPT → modded-nanoGPT → nanochat

nanochat은 *고아*가 아니다. 가계도가 있다.

가장 윗대는 **nanoGPT**다. 같은 저자(카르파시)가 2022년에 공개한, GPT-2를 *처음부터* 학습시켜 보여주기 위한 작은 리포다. 단, nanoGPT는 *사전학습만* 다룬다. base 모델이 나오면 거기서 끝이다. *대화하는 모델*이 아니다. 이름의 "nano"는 코드의 작음을, "GPT"는 사전학습된 트랜스포머를 가리킨다.

그 다음 세대가 **modded-nanoGPT**다. Keller Jordan을 중심으로 한 커뮤니티가 nanoGPT 위에 *각종 현대화 패치*를 얹어 GPT-2 학습 속도 경쟁(speedrun)을 벌이는 곳이다. RoPE, RMSNorm, value embedding, sliding window attention, 그리고 결정타로 **Muon 옵티마이저**가 여기서 나왔다. nanoGPT 124M 학습을 90초 만에 끝내는 기록이 거기서 세워졌다. 이 흐름이 "더 빠르게, 더 적은 토큰으로, 같은 품질의 GPT를"이라는 문화를 만들었고, 그 문화의 *코드적 산물*이 nanochat이다.

modded-nanoGPT의 *리더보드 문화*가 흥미롭다. 누군가 새로운 트릭으로 학습 시간을 단축하면 PR을 보내고, 그게 머지되면 *리더보드의 한 줄*이 새 기록으로 갱신된다. 90초가 70초가 되고, 다시 50초가 된다. 그 한 줄을 위해 누군가는 *몇 주를 갈아넣는다*. 그 결과 *현대 GPT 학습의 트릭 보따리*가 한 리포에 빠르게 축적됐다. nanochat은 그 보따리에서 *작은 모델에 적합한 것들*만 골라 흡수했다. ReLU²(SwiGLU 대신), QK norm, value embedding, smear, backout, logit softcap, Muon 옵티마이저, FP8 학습 — 4A와 4B와 5장에서 *모두 정확히* 본다.

흥미로운 한 가지 더. modded-nanoGPT는 *경쟁 문화*를 만들었지만, nanochat은 그 문화의 결과를 *교육 친화적인 모양*으로 다시 정렬했다. modded-nanoGPT의 코드는 *최단 시간*을 위해 트릭이 누적된 결과라 *읽기*가 그리 친절하지 않다. nanochat은 같은 트릭들을 *읽을 수 있는* 코드로 다시 짠 작품에 가깝다. *공부의 대상으로 쓸 수 있게* 정렬된 modded-nanoGPT라고 해도 좋다.

그래서 nanochat은 *nanoGPT의 다음 세대*이자 *modded-nanoGPT의 적자*다. 사전학습만 다루던 형(nanoGPT)에 대화 단계(SFT·RL)와 추론 엔진(KV cache·tool use)을 붙이고, 형의 친구들(modded-nanoGPT)이 발견한 트릭을 흡수해서 *완성된 가족*이 됐다. README의 한 줄이 그 정체성을 정확히 잡는다:

> *the simplest experimental harness for training LLMs.*

*하네스(harness)* — 도구를 묶어 한꺼번에 굴리는 *마구(馬具)*. 이 단어 선택이 의미심장하다. nanochat은 "ChatGPT 프레임워크"가 아니다. 거대한 설정 객체, 모델 팩토리, 끝없는 if-else 분기 같은 것이 *없다*. README의 다른 한 줄:

> *Accessibility is about overall cost but also about cognitive complexity.*

비용도 비용이지만, *인지적 복잡도*가 접근성의 핵심이라는 입장이다. 우리가 이 책에서 따라갈 코드가 8천 줄로 끝나는 이유다. *읽을 수 있는* 양이라는 뜻이기도 하다.

그런데 8천 줄이 *무엇으로 가능한가*. 그게 가능한 데에는 *한 개의 다이얼*이라는 디자인 결정이 있다. nanochat의 모든 학습 스크립트는 `--depth` 단 하나의 옵션으로 모델 크기를 결정한다. d4부터 d26까지. depth 외의 *모든* 하이퍼파라미터 — 트랜스포머의 width, head 수, learning rate 보정, 학습 토큰 수, weight decay까지 — 가 *자동으로 컴퓨트-옵티멀하게 결정된다*.

이 디자인이 얼마나 *과감한 것*인지 한 번 짚어두자. 보통의 LLM 학습 코드는 수십 개의 하이퍼파라미터가 설정 객체에 줄줄이 들어 있고, 그것들을 *어떻게 골라야 하는가*가 시니어 엔지니어의 *암묵지*다. 그 암묵지가 코드 바깥에서 떠도는 동안, 새로 들어온 사람은 *어디서부터 손을 대야 할지*가 도무지 보이지 않는다. 끔찍한 일이다.

nanochat은 그 모든 하이퍼파라미터를 *코드 안에 박아넣었다*. Chinchilla scaling laws, Power Lines paper의 batch size 공식, T_epoch framework의 weight decay 스케일링 — 이런 *논문에 흩어진 결정들*이 한 함수 `get_scaling_params(model)` 안에 한꺼번에 들어 있다. 사용자는 d12 또는 d24만 고르면, *그 depth에 컴퓨트-옵티멀한 모든 것*이 자동으로 결정된다.

그 결과가 nanochat이 *공부의 대상*으로 쓸 수 있는 작품인 이유다. 우리는 책을 따라가며 *왜 그 다이얼이 가능한가*를 한 단계씩 풀어본다. 6장에서 scaling laws의 *코드적 형태*를 정확히 본다.

## 1.3 이 책이 약속하는 것, 약속하지 않는 것

기술서가 가장 자주 저지르는 죄가 있다. *과한 약속*이다. 어떤 책은 한 권을 다 읽고 나면 LLM 박사가 된 것 같은 기분이 들게 만든다. 그 기분은 며칠 안 가서 무너진다. 이 책은 처음부터 약속의 *경계*를 분명히 그어두자.

**약속하는 것.**

- nanochat 코드 8천 줄을 *한 줄도 빠짐없이 따라 읽는다*. 토크나이저, GPT 모듈, 옵티마이저, 데이터로더, 추론 엔진까지. 책을 덮으면 "이 함수가 무엇을 하는지" 하나도 모르는 부분이 없게 한다.
- 각 학습 단계가 *무엇을 가르치는지*와 *무엇으로 검증하는지*를 한 문장으로 설명할 수 있게 한다. 사전학습은 무엇을, SFT는 무엇을, RL은 무엇을 가르치는가. CORE는 무엇을 측정하고, bits-per-byte는 어떻게 다른가.
- 직접 굴려본다. CPU/MPS에서 d6 모델로 정성 검증을 해보거나, GPU 한 노드에서 GPT-2급 d24를 학습시켜 본다. *책 안에 머무는 지식*이 아니라 *손에 쥔 산출물*로 끝난다.
- modded-nanoGPT의 현대화 트릭들 — RoPE, RMSNorm, ReLU², value embedding, sliding window, Muon, FP8까지 — 의 *직관*을 코드와 함께 잡는다. 왜 SwiGLU가 아니라 ReLU²인지, 왜 임베딩에 Muon을 쓰면 안 되는지를 동료에게 설명해줄 수 있게 한다.

**약속하지 않는 것.**

- *한국어* 챗봇 만들기. nanochat은 영어 위주다. FineWeb과 SmolTalk 모두 영어 중심 데이터셋이고, 학습된 모델에 한국어로 물으면 영어로 답하거나 깨진다. *그게 이상한 게 아니라 정상이다.* 다만 12장 마지막 절에서 "한국어로 가는 길"을 한 절 분량으로 정리한다.
- LLM 이론서. 트랜스포머의 수학적 유도, 어텐션 메커니즘의 정보 이론적 해석 같은 것은 다루지 않는다. 우리는 *코드를 읽는 책*이다. 이론은 *코드를 이해하는 데 필요한 만큼만* 곁들인다.
- 프로덕션 LLM 만들기. nanochat의 d24 모델은 GPT-2급이지 GPT-4급이 아니다. 그 차이는 단순한 *depth* 차이가 아니라 *수십억 달러의 인프라와 데이터 수집*의 차이다. 이 책을 읽고 나서 ChatGPT의 자리를 위협하는 모델을 만들 수는 없다. *대신* ChatGPT의 자리에 있는 사람들이 어떤 코드를 짜고 있는지를 정확히 안다.

이 약속의 경계가 *찜찜하다*고 느낀다면, 그게 이 책의 정직함이다. 잘 모르는 것을 모른다고 명시하는 책이 잘 아는 것을 *깊이* 다룬다.

*책의 차별점* 한 가지를 더 짚어두자. 비슷한 영역의 책들과 비교했을 때 이 책의 자리가 어디인가에 대한 이야기다.

LLM을 다루는 책은 크게 두 갈래로 나뉜다. *이론서*와 *프롬프트 엔지니어링 책*. 이론서는 트랜스포머의 수학과 어텐션 메커니즘의 정보 이론을 다루지만, *실제 코드*까지는 잘 안 내려간다. 프롬프트 엔지니어링 책은 *모델을 잘 쓰는 법*을 다루지만, *모델이 어떻게 만들어지는가*는 거의 안 다룬다. 그 사이가 비어 있다. 이 책은 그 빈자리를 채우려고 한다.

또 하나, *한 작품을 끝까지 따라가는* 책이 의외로 드물다. 보통의 ML 책은 여러 라이브러리·여러 모델·여러 코드 예제를 *발췌해서* 보여준다. 한 작품에 8천 줄이 들어 있고, 그 8천 줄을 *통째로 한 번 따라가는* 책은 *흔하지 않다*. 그게 가능한 작품(즉 "8천 줄로 ChatGPT를 만드는 한 리포")이 *2025년 가을에 비로소* 등장했다는 사실이 이 책의 *유일한 가능성*을 만들었다. 우리는 그 가능성을 잡는다.

## 1.4 사전 지식 점검 — 무엇을 알고 무엇을 모르고 오는가

이 책을 펴는 독자가 *이미 갖춰서 와야 하는 것*을 정리해두자. 모자라는 부분이 있다면 1장이 끝나기 전에 보강해도 늦지 않다.

PyTorch와 파이썬을 다룬다. `torch.nn.Module`을 상속해서 forward를 짜본 적이 있고, `torch.compile`이 무엇인지 들어봤다. autograd가 어떻게 backward를 만들어내는지 *대략* 안다. DDP(`DistributedDataParallel`)라는 단어를 *들어는* 봤다. 이 수준이다. *전문가일 필요는 없다.* 다만 `import torch`를 보고 손이 굳지는 않아야 한다.

GPU 환경에 어느 정도 익숙하다. `nvidia-smi`로 메모리 사용량을 확인해본 적이 있고, OOM 에러를 직접 한 번은 마주쳤다. bf16, fp16, fp32가 *어떻게 다른지*는 한 줄로 답할 수 있다. GPU가 없다면 노트북의 CPU나 Apple Silicon의 MPS로 *맛만 보기* 모드로 책을 따라갈 수 있다. 그 경로도 나란히 안내한다.

명령행을 두려워하지 않는다. `bash`, `screen`, 환경 변수 설정 같은 것이 *고문*이 아니라 *익숙한 도구*다. nanochat은 셸 스크립트로 파이프라인을 묶기 때문에, 터미널을 켜는 데 거부감이 없어야 한다.

ChatGPT는 써봤지만 내부는 모른다. 이 책의 *모든 챕터의 기반*이 되는 한 줄이다. 모른다는 사실 자체가 *동기*가 된다.

이 정도가 갖춰져 있다면 1장의 실습을 따라가는 데 무리가 없다. 만약 "PyTorch는 처음 본다"는 수준이라면 카르파시의 이전 강의 *Zero to Hero* 시리즈를 한 번 훑고 오는 편이 낫다. *이 책이 기초부터 다시 친절히 풀어주지는 못한다.* 모든 책이 그렇듯 어딘가에서 선을 그어야 하고, 우리는 그 선을 PyTorch 기본기에 둔다.

*새로 배워야 할 것*도 미리 정리해두자. 책을 다 덮을 즈음 우리가 손에 쥐고 있을 개념들이다.

- BPE 토크나이저가 *왜 필요한가*, vocab_size와 compression ratio가 모델 성능에 어떤 영향을 주는가 (2~3장)
- pretraining, midtraining, SFT, RL이 각각 *무엇을 가르치는가* (6, 8, 9장)
- Transformer의 최신 변종들 — RoPE, RMSNorm, SwiGLU vs ReLU², GQA, sliding window attention, value embeddings (4A·4B장)
- AdamW가 무엇이고 Muon이 *왜 등장했는가* (5장)
- 학습 인프라 — bf16/fp8, FlashAttention, BOS-aligned bestfit dataloader, ZeRO-2 스타일 분산 (6장)
- 평가 — CORE score, bits-per-byte, MMLU·ARC·GSM8K·HumanEval이 *무엇을 측정하는가* (7장)
- 추론 — KV cache, sampling temperature/top-k, tool use(calculator/Python) (10장)

이 목록이 *지금은 흐릿한 단어들의 모음*으로 보인다면, 그게 1장을 펴는 *정상적인 상태*다. 12장을 덮을 즈음 모든 단어가 *코드의 어느 함수와 연결되는지* 손에 잡힌다. 그게 이 책의 약속이다.

## 1.5 환경 구축 — 30분이면 끝난다

자, 이제 손을 더럽혀보자. 환경부터 잡는다.

nanochat은 [uv](https://docs.astral.sh/uv/)로 의존성을 관리한다. pip이나 conda가 아니다. 처음 쓰는 도구일 수 있는데, Rust로 짠 *몹시 빠른* 파이썬 패키지 매니저라고 생각하면 된다. `pyproject.toml` 한 파일로 모든 의존성과 가상환경을 통제한다.

리포를 받고 의존성을 까는 게 첫 단계다.

```bash
git clone https://github.com/karpathy/nanochat.git
cd nanochat
uv sync --extra gpu    # CUDA(A100/H100/...)가 있다면
# uv sync --extra cpu  # 없다면 (Mac MPS도 cpu extra로)
source .venv/bin/activate
```

`--extra gpu`와 `--extra cpu`가 *왜 따로* 있을까. `pyproject.toml`을 열어보면 답이 보인다.

```toml
[project.optional-dependencies]
cpu = [
    "setuptools>=65.0.0",
    "torch==2.9.1",
]
gpu = [
    "torch==2.9.1",
]

[tool.uv.sources]
torch = [
    { index = "pytorch-cpu", extra = "cpu" },
    { index = "pytorch-cu128", extra = "gpu" },
]
```

`pyproject.toml`의 47번 줄 부근에서 같은 `torch==2.9.1`이 *어느 인덱스에서 받느냐*에 따라 CPU 빌드가 되기도 하고 CUDA 12.8 빌드가 되기도 한다. 같은 버전 번호의 *다른 바이너리*다. uv는 이 분기를 한 명령으로 처리한다. 우아한 디자인이다.

다음으로, 작업 산출물을 둘 디렉토리를 정한다.

```bash
export NANOCHAT_BASE_DIR="$HOME/.cache/nanochat"
mkdir -p $NANOCHAT_BASE_DIR
```

`NANOCHAT_BASE_DIR`는 nanochat이 *모든 중간 산출물*을 쌓아두는 디렉토리다. 토크나이저, 데이터 셰드, 체크포인트, 리포트 모두 여기 들어간다. 기본값을 `~/.cache/nanochat`으로 잡았는데, 디스크 여유가 부족하다면 외장 SSD 같은 곳으로 옮기자. d24 풀 학습이면 수십 GB가 쌓인다는 점을 *잊지 말자*.

이 두 단계가 환경 구축의 전부다. *전부*다. 거대한 도커 이미지를 받거나, 빌드 시스템과 씨름하거나, 잘 안 되는 CUDA 드라이버를 한 시간씩 우회할 필요가 없다. uv가 `.venv`를 만들고, `torch`를 깔고, 우리는 `source .venv/bin/activate`만 누르면 된다.

다만 한 가지. GPU 환경이라면 CUDA 드라이버와 nvidia-smi가 *동작은 해야 한다*. uv가 *드라이버까지* 깔아주지는 않는다. `nvidia-smi`가 OS에서 잘 보이는지 한 번 확인하고 넘어가자.

`uv sync --extra cpu`로 CPU 빌드를 받았다가 나중에 GPU 환경으로 옮기면서 *바꿔 깔아야* 할 수도 있다. `pyproject.toml`을 보면 `[tool.uv]` 섹션 아래에 흥미로운 줄이 있다.

```toml
conflicts = [
    [
        { extra = "cpu" },
        { extra = "gpu" },
    ],
]
```

cpu와 gpu extras를 *동시에는* 깔 수 없다고 명시되어 있다. 한쪽을 깔면 다른 쪽이 제거된다. 우아한 디자인이지만, 옮길 때 `uv sync --extra gpu`를 *반드시 다시* 실행해야 한다는 점은 *잊지 말자*. 이 한 줄을 빼먹고 `python -m scripts.base_train`을 돌리면 토치가 CUDA를 못 찾아 *어리둥절한 에러*가 뜬다.

`source .venv/bin/activate`가 매번 번거롭다면 `.envrc`에 한 줄 박아 direnv를 쓰는 것도 방법이다. 작은 디테일이지만, 셸을 새로 열 때마다 가상환경을 다시 활성화하는 *번거로움*이 사라진다.

## 1.6 컴퓨트 환경의 단일 진실 — bf16, fp32, 그리고 MPS

nanochat이 우아하게 처리하는 부분이 한 가지 더 있다. *어떤 정밀도로 굴릴 것인가*에 대한 결정이다.

대부분의 PyTorch 학습 코드는 `torch.amp.autocast`로 mixed precision을 처리한다. 자동이라 편하지만 *어디서 어떤 정밀도가 쓰이는지*가 코드를 펴서 직접 보기 어렵다. 카르파시는 이걸 *쓰지 않는다*. 대신 `nanochat/common.py`에 `COMPUTE_DTYPE`이라는 전역 dtype을 하나 두고, 모듈이 임포트되는 시점에 자동 결정한다.

규칙은 단순하다.

| 하드웨어 | 기본 dtype | 이유 |
|---|---|---|
| CUDA SM 80+ (A100, H100, ...) | `bfloat16` | bf16 텐서 코어가 네이티브로 빠르다 |
| CUDA SM < 80 (V100, T4, ...) | `float32` | bf16 지원 없음, fp16은 `NANOCHAT_DTYPE=float16`으로 |
| CPU / MPS | `float32` | reduced-precision 텐서 코어가 없다 |

`NANOCHAT_DTYPE=bfloat16` 같은 환경 변수로 강제할 수도 있다. 이 *전역 단일 진실*이 모든 코드 경로의 dtype을 결정한다. 모델 weight는 fp32로 두되, 우리가 직접 짠 커스텀 `Linear` 레이어가 forward에서 `COMPUTE_DTYPE`으로 캐스팅한다. 임베딩은 메모리를 아끼려고 처음부터 `COMPUTE_DTYPE`으로 저장한다.

왜 이렇게 *수동으로* 잡았을까. autocast가 더 편할 텐데. 답은 README에 명시되어 있다 — *"어디서 어떤 정밀도가 쓰이는지 한눈에 보이는"* 정합성을 우선한 결정이다. 디버깅할 때, 그리고 *학습 코드를 *읽을 때**, 이 단순함이 큰 값을 한다. 우리도 이 책을 따라가며 *그 단순함의 보상*을 자주 받게 된다.

조금 더 깊이 들어가보자. autocast가 *왜 디버깅을 어렵게 하는가*. autocast는 *연산 단위로* dtype을 자동 결정한다. matmul은 bf16, layernorm은 fp32, softmax는 fp32, 식의 규칙이 자동 적용된다. 평소에는 잘 동작한다. 그런데 어느 날 loss가 발산한다고 해보자. *어디서 정밀도가 깨졌는지*를 추적하려면 autocast의 내부 규칙을 머리에 다시 떠올려야 한다. 그게 *번거롭다*. nanochat의 방식은 다르다 — 모델 weight는 fp32로 명시적으로 저장되고, `Linear`의 forward에서 `weight.to(x.dtype)`로 *눈에 보이는 캐스팅*이 일어난다. 코드를 펴면 *어디서 무엇이 캐스팅되는지*가 보인다.

이 디자인은 카르파시의 *반복되는 취향*을 보여준다. 똑똑한 자동화보다 *읽을 수 있는 명시*. 추상화의 우아함보다 *코드를 펴서 본 사람이 이해할 수 있는 직접성*. 우리는 책을 따라가며 이 취향이 곳곳에서 반복되는 걸 본다.

한 가지 더 짚어두면, nanochat은 *PyTorch DDP도 쓰지 않는다*. ZeRO-2 스타일의 옵티마이저 state sharding을 *직접 구현*했다. FSDP라는 PyTorch의 공식 솔루션이 있지만, *읽기에는 너무 무겁다*는 판단이었다. `nanochat/optim.py`의 `DistMuonAdamW`가 그 자체 구현체다 — 약 240줄로 ZeRO-2의 *읽을 수 있는 버전*을 다시 짰다. 5장에서 *박스로 분리*해서 한 번 펼쳐본다.

이 패턴이 한 번 더 반복된다. `nanochat/fp8.py`도 torchao의 약 2,000줄짜리 FP8 학습 구현을 *약 150줄*로 다시 짠 미니 버전이다. *작은 자체 구현이 큰 라이브러리보다 읽기 편하다*는 입장이다. 운영 환경의 일반화 가능성보다 *공부의 대상*으로서의 읽기 쉬움이 우선이라는 디자인 결정. 그래서 이 책이 가능해진다.

CPU나 MPS로 따라가는 독자에게 한 가지. 이 책의 풀 GPU 경로는 bf16을 기본으로 가정한다. CPU/MPS에서는 자동으로 fp32로 떨어지므로 *속도가 훨씬 느리다*. d24를 노트북에서 돌릴 생각은 *접자*. 대신 d6짜리 장난감 모델로 코드 경로를 다 *밟아보는* 데에는 큰 무리가 없다. 우리는 이 두 길을 함께 안내한다.

## 1.7 작품의 층위 — 라이브러리, 스크립트, 데이터, 셸

nanochat 리포의 디렉토리 트리를 한 번 펴서 *전체 모양*을 잡아두자. 8천 줄이 어떻게 *조직*되어 있는지 보는 게, 챕터를 펼치기 전에 우리가 가져야 할 첫 지도다.

리포의 모양은 이렇다.

```
nanochat/
├── nanochat/           # 라이브러리 (재사용 가능한 모듈)
│   ├── gpt.py              # GPT nn.Module
│   ├── tokenizer.py        # BPE: HF 호환 / rustbpe+tiktoken
│   ├── optim.py            # MuonAdamW (1GPU + ZeRO-2 distributed)
│   ├── dataloader.py       # BOS-aligned bestfit-crop dataloader
│   ├── dataset.py          # parquet 셰드 다운로드/iter
│   ├── engine.py           # KV-cache 추론 엔진 (+ tool use FSM)
│   ├── flash_attention.py  # FA3 / SDPA 디스패처
│   ├── fp8.py              # 자체 미니 FP8 학습 (~150줄)
│   ├── core_eval.py        # DCLM CORE 22-task 평가
│   ├── loss_eval.py        # bits-per-byte 평가
│   ├── checkpoint_manager.py
│   ├── common.py           # COMPUTE_DTYPE, ddp setup, GPU TFLOPS 테이블
│   ├── execution.py        # 샌드박스 Python 실행 (HumanEval용)
│   ├── report.py           # markdown 학습 리포트 생성
│   └── ui.html             # 챗봇 프론트엔드
├── scripts/            # CLI 진입점
│   ├── tok_train.py / tok_eval.py
│   ├── base_train.py / base_eval.py
│   ├── chat_sft.py / chat_rl.py / chat_eval.py
│   └── chat_cli.py / chat_web.py
├── tasks/              # 데이터셋·평가 정의
│   ├── common.py           # Task base class, TaskMixture
│   ├── arc.py mmlu.py gsm8k.py humaneval.py smoltalk.py
│   ├── spellingbee.py      # 합성 spelling/counting task
│   └── customjson.py       # jsonl 대화 파일을 task로
├── runs/               # 풀 파이프라인 쉘 스크립트
│   ├── speedrun.sh         # 8XH100, GPT-2급 d24
│   ├── runcpu.sh           # CPU/MPS d6 데모
│   ├── scaling_laws.sh
│   └── miniseries.sh
├── dev/                # 보조 도구
│   └── gen_synthetic_data.py
└── tests/test_engine.py
```

네 개의 *층위*가 있다. 이 구분이 책 전체의 *읽기 순서*와도 일치하므로 머리에 박아두는 편이 좋다.

가장 안쪽 층은 **`nanochat/` 라이브러리**다. *재사용 가능한 모듈*들이 모여 있다. `gpt.py`는 GPT 모델, `tokenizer.py`는 BPE, `optim.py`는 옵티마이저, 이런 식이다. 모듈끼리 서로 임포트하지만 *바깥에서 직접 실행되지는 않는다*. 책의 *핵심 챕터*들(4A, 4B, 5장)이 이 층을 다룬다.

그 위가 **`scripts/` CLI 진입점**이다. `python -m scripts.base_train` 같은 식으로 *직접 실행*되는 파일들이다. 각 스크립트는 argparse로 옵션을 받고, 라이브러리 모듈을 조립해서 *한 단계의 학습이나 평가*를 수행한다. 6장(사전학습)과 8장(SFT), 9장(RL)이 이 층을 펼친다.

세 번째는 **`tasks/` 데이터셋·평가 정의**다. ARC, MMLU, GSM8K, HumanEval, SmolTalk 같은 표준 벤치마크들이 *모두 같은 인터페이스*(`Task` 베이스 클래스)로 래핑되어 있다. `TaskMixture`는 이들을 비율로 섞어 SFT 데이터셋을 만든다. 8장에서 길게 다룬다.

가장 바깥이 **`runs/` 쉘 스크립트**다. `speedrun.sh`는 8XH100 풀 파이프라인, `runcpu.sh`는 CPU/MPS 데모, `miniseries.sh`는 d4부터 d26까지 여러 depth로 한꺼번에 학습. *셸 한 줄이 한 노드에서 3시간을 굴린다.* 이 층은 *오케스트레이션*이고, 정작 그 안에서 실제 일을 하는 것은 안쪽의 세 층이다.

이 네 층의 *경계*를 헷갈리지 않는 게 책을 따라가는 데 큰 도움이 된다. 어떤 코드를 펼 때 *내가 지금 어느 층에 있는가*를 늘 한 번 짚어두자. `nanochat.tokenizer`인지 `scripts.tok_train`인지 `tasks.gsm8k`인지 `runs/speedrun.sh`인지. 이게 흐릿하면 챕터 사이에서 *길을 잃기 쉽다*.

한 가지 흥미로운 관찰. 잘 짜인 ML 코드의 *디렉토리 구조*가 곧 그 코드의 *멘탈 모델*인 경우가 많다. nanochat의 네 층은 단순한 정리가 아니라 *책임의 분할*이다. `nanochat/`은 "재사용 가능한 단위", `scripts/`는 "한 번 실행되는 단위", `tasks/`는 "데이터셋의 단위", `runs/`는 "파이프라인의 단위". 책임이 흐릿한 코드는 *모듈끼리 서로 임포트가 얽혀 있는 코드*다. nanochat은 그 얽힘이 거의 없다 — `tasks/`는 `nanochat.tokenizer`를 임포트하지만 그 반대는 없다. `scripts/`는 `nanochat/`을 임포트하지만 그 반대는 없다. *방향이 일관된* 의존 그래프다.

처음 한 리포를 받아들고 *어디부터 봐야 할까*가 막막하다고 느낄 때, 이런 *방향성*을 머리에 그려두면 길 찾기가 한결 수월해진다. 다른 리포를 펼 때도 같은 질문을 던지자. *이 코드는 어디가 가장 안쪽(라이브러리)이고 어디가 가장 바깥(셸 스크립트)인가?* 그 답이 떠오르지 않는 코드는 *코드 자체에 문제가 있는 경우*가 많다.

## 1.8 셰드 한 개의 크기 — 데이터를 받아보자

이제 *처음으로 손을 더럽혀보자*. 사전학습 데이터의 셰드(shard) 두 개를 받아본다. nanochat 코드 경로를 *진짜로 한 번 통과*해보는 일이다.

데이터 다운로드를 담당하는 모듈은 `nanochat/dataset.py`다. 한 페이지짜리 짧은 파일이다. 의미만 짚자.

```python
BASE_URL = "https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle/resolve/main"
MAX_SHARD = 6542  # the last datashard is shard_06542.parquet
index_to_filename = lambda index: f"shard_{index:05d}.parquet"
```

`dataset.py` 23~25번 줄이다. *6542개의 parquet 셰드*가 HuggingFace에 올라가 있고, `shard_00000.parquet`부터 `shard_06542.parquet`까지의 일관된 이름 규칙으로 받을 수 있다. 흥미로운 건 이름이다 — *climbmix-400b-shuffle*. 본래 nanochat은 FinewebEdu-100B로 학습했는데, 2026년 3월에 NVIDIA의 ClimbMix-400B로 데이터셋이 *업그레이드*됐다. 같은 코드, 다른 데이터. README의 리더보드를 보면 그 업그레이드만으로 학습 시간이 2.76시간에서 2.02시간으로 *26% 빨라졌다*.

그러면 한 개의 셰드는 얼마나 큰가. `speedrun.sh`의 주석이 명시한다:

> *each data shard is ~250M chars ... so we download 2e9 / 250e6 = 8 data shards ... each shard is ~100MB of text (compressed)*

한 셰드가 *압축된 텍스트 약 100MB, 약 2억 5천만 글자*다. 8개를 받으면 약 800MB, 토크나이저 학습용 2B chars 분량이 된다. 우리는 한 번 *맛만 보려는* 거니까 두 개만 받자.

```bash
python -m nanochat.dataset -n 2
```

이 명령이 하는 일을 머리에 그려보자. 셰드 인덱스 `[0, 1, 6542]` (0, 1, 그리고 *항상 받는* validation 셰드 6542)를 4개의 워커 프로세스로 병렬 다운로드한다. 각 셰드를 임시 파일(`*.tmp`)에 받은 뒤 다 받으면 원본 이름으로 *원자적*으로 rename한다. 네트워크가 끊겨도 부분 파일이 남지 않게 하려는 작은 디테일이다.

빠른 네트워크에서 셰드 한 개당 약 30초, 두 개 + validation까지 *약 1분 안에* 끝난다. 끝나면 디렉토리는 이렇게 생긴다.

```
~/.cache/nanochat/base_data_climbmix/
├── shard_00000.parquet    # 약 100MB
├── shard_00001.parquet    # 약 100MB
└── shard_06542.parquet    # validation
```

세 개의 parquet 파일. 이게 *우리가 모델에게 먹일 식량*이다. parquet 안에 무엇이 들었는지 한 번만 들여다보자.

```python
import pyarrow.parquet as pq
pf = pq.ParquetFile("~/.cache/nanochat/base_data_climbmix/shard_00000.parquet".replace("~", os.path.expanduser("~")))
rg = pf.read_row_group(0)
texts = rg.column('text').to_pylist()
print(len(texts), len(texts[0]))   # 문서 개수, 첫 문서 글자 수
print(texts[0][:500])               # 첫 문서 앞 500자
```

`text` 컬럼 하나가 든 단순한 파일이다. 한 row가 한 문서(웹페이지나 책의 한 단락)이고, 한 셰드 안에 수만 개의 문서가 들어 있다. 5줄짜리 이 파이썬 코드가 작은 *aha*를 준다 — *우리가 모델에게 가르치려는 것은 결국 이런 텍스트들의 다음 토큰을 맞히는 일이다.* 모델은 이 잡다하고 풍부한 웹 텍스트들의 *통계적 패턴*을 흡수한다. 거기서 "지능"으로 보이는 무언가가 *창발*한다.

지금은 다운로드만으로 충분하다. 토크나이저를 학습시키고 토큰화하는 일은 2장과 3장에서 자세히 다룬다. 여기서는 *셰드의 무게감*만 손에 쥐자 — 100MB짜리 파일 하나가, 한 셰드, 약 2억 5천만 글자.

한 가지 흥미로운 디테일. `dataset.py` 38~58번 줄 어딘가에 *옛 사용자를 위한 안내문*이 박혀 있다.

```python
if not os.path.exists(data_dir):
    if warn_on_legacy:
        print()
        print("=" * 80)
        print("  WARNING: DATASET UPGRADE REQUIRED")
        print("=" * 80)
        print()
        print(f"  Could not find: {data_dir}")
        print()
        print("  nanochat recently switched from FinewebEdu-100B to ClimbMix-400B.")
        print("  Everyone who does `git pull` as of March 4, 2026 is expected to see this message.")
        ...
```

데이터셋을 FinewebEdu-100B에서 ClimbMix-400B로 *통째로 바꾸는* 결정이 있었는데, 이전에 학습한 사용자들이 *어느 날 갑자기* 데이터 디렉토리가 안 보인다고 당황하지 않도록, 친절한 안내문과 *복구 명령*까지 코드 안에 박아두었다. *카르파시 식 사용자 친화성*이라고 부를 만한 디테일이다. 8장에서 `tasks/customjson.py`를 볼 때 이 패턴이 한 번 더 나온다.

오픈소스 코드에서 *깨끗한 정렬*과 *너그러운 마이그레이션*이 동시에 잡혀 있는 사례는 의외로 드물다. 보통 둘 중 하나다 — 깨끗하지만 옛 사용자를 버리거나, 너그럽지만 코드가 누더기가 되거나. nanochat은 한 함수 안에 두 경로를 *명시적으로* 갈라두고, *명시적인 안내문*과 *명시적인 fallback*을 박아두었다. 흉내 낼 만한 패턴이다.

## 1.9 한 줄 인터랙션 — special token 한 번만 출력해보자

데이터를 받았으니, *우리가 만들 모델이 마지막에 무엇을 출력할 것인지* 한 가지만 미리 맛보자. 2장의 *aha*로 가는 사다리를 미리 한 칸 걸어둔다.

`nanochat/tokenizer.py`를 열어보면 13~25번 줄에 흥미로운 리스트가 있다.

```python
SPECIAL_TOKENS = [
    # every document begins with the Beginning of Sequence (BOS) token that delimits documents
    "<|bos|>",
    # tokens below are only used during finetuning to render Conversations into token ids
    "<|user_start|>", # user messages
    "<|user_end|>",
    "<|assistant_start|>", # assistant messages
    "<|assistant_end|>",
    "<|python_start|>", # assistant invokes python REPL tool
    "<|python_end|>",
    "<|output_start|>", # python REPL outputs back to assistant
    "<|output_end|>",
]
```

아홉 개의 *특수 토큰*이다. 각각 한 줄짜리 주석이 붙어 있는데, 천천히 읽어보면 이 리스트가 *책 전체의 줄거리*를 압축해서 보여준다는 사실이 보인다.

`<|bos|>`는 모든 문서의 시작에 박힌다. 사전학습(6장)에서 데이터로더가 매 row의 첫 토큰으로 BOS를 넣어주는 이유다.

`<|user_start|>`, `<|user_end|>`, `<|assistant_start|>`, `<|assistant_end|>` 네 개는 *대화*를 표현한다. base 모델이 SFT를 거쳐 *어시스턴트*가 되려면, 사용자의 발화와 자기 발화의 경계를 알아야 한다. 이 네 토큰이 그 경계를 *토큰 단위로 박아둔다*. 8장의 핵심이다.

`<|python_start|>`, `<|python_end|>`, `<|output_start|>`, `<|output_end|>` 네 개는 *도구 사용*이다. 어시스턴트가 "9 곱하기 8은?"이라는 질문을 받으면, 마음속으로 계산하는 대신 `<|python_start|>9*8<|python_end|>`를 출력할 수 있다. 그러면 추론 엔진(`engine.py`)이 그 사이의 표현식을 *직접 실행*해서 결과를 `<|output_start|>72<|output_end|>`로 *모델의 입력 스트림에 도로 끼워 넣는다*. 10장의 클라이맥스다.

여기서 *한 가지 중요한 사실*. 이 9개의 특수 토큰은 *토크나이저 단에 박혀 있다*. 모델이 학습되기도 전, 가장 첫 단계인 토크나이저 학습 시점부터 이 토큰들의 자리가 정해진다. 그게 의미하는 바가 있다 — *나중에 새로운 도구를 추가하려면 토크나이저를 다시 학습시켜야 한다.* 가볍게 끼워 넣을 수 있는 결정이 아니다.

이 사실이 *찜찜하게* 느껴진다면 정상이다. *모델보다 먼저 정해지는 결정들*이 LLM 설계에는 의외로 많다. 토크나이저의 어휘 크기, 특수 토큰의 종류, 컨텍스트 길이 — 이런 것들은 사전학습 *전에* 정해야 하고, 한 번 정하면 나중에 바꾸기가 *매우 번거롭다*. nanochat은 그 결정들의 *무게*를 한 리포에 그대로 노출해서 보여준다.

5줄짜리 *맛보기 인터랙션*을 하나 해보자. `tok_eval` 스크립트를 가볍게 띄워 첫 번째 special token이 어떤 ID로 매핑되는지 본다. 토크나이저가 아직 학습되어 있지 않은 시점이라면 이 단계는 *2장 끝*까지 미뤄도 좋다. 다만 이미 학습된 토크나이저가 있다면 한 줄로 확인할 수 있다.

```python
import tiktoken
# (2장에서 학습할) 32K vocab의 우리 토크나이저를 로드한 뒤
# enc = ...
# print(enc.encode_single_token("<|bos|>"))   # 예: 32768 - 9 = 32759
```

지금은 *그런 게 있다*는 것만 알자. 2장에서 이 토큰들이 *실제로 어떤 ID*를 받는지, 한국어 문장이 어떻게 *조각조각 쪼개지는지*를 가지고 본격적인 토크나이저 여행이 시작된다.

이 9개 토큰의 *목록 자체*를 다시 한 번 들여다보면, *책 12장의 줄거리*가 한 페이지에 압축돼 있다는 느낌이 든다.

| 토큰 | 역할 | 언제 학습되는가 | 어디서 다루는가 |
|---|---|---|---|
| `<|bos|>` | 문서 시작 표시 | 사전학습 데이터로더가 매 문서 앞에 prepend | 6장 |
| `<|user_start|>` / `<|user_end|>` | 사용자 발화 경계 | SFT에서 mask=0으로 학습 | 8장 |
| `<|assistant_start|>` / `<|assistant_end|>` | 어시스턴트 발화 경계 | SFT에서 mask=1으로 학습 | 8장 |
| `<|python_start|>` / `<|python_end|>` | 도구 호출 표현식 경계 | SFT에서 GSM8K 데이터로 학습 (mask=1) | 8장, 10장 |
| `<|output_start|>` / `<|output_end|>` | 도구 결과 경계 | 추론 시 엔진이 *강제로* 주입 (mask=0) | 10장 |

mask=1은 *모델이 그 토큰을 학습한다*는 뜻이고, mask=0은 *학습 신호에서 제외*된다는 뜻이다. 사용자 발화를 mask=0으로 두는 이유는, 우리가 모델에게 *어시스턴트가 답하는 법*을 가르치지 *사용자가 묻는 법*을 가르치는 게 아니기 때문이다. 도구 결과도 마찬가지로 mask=0이다 — 그건 모델이 *생성*하는 게 아니라 환경이 *주는* 토큰이다.

이 mask의 *의미*가 SFT의 핵심이고, 8장에서 `render_conversation` 함수의 mask 계산 로직을 한 줄 한 줄 따라간다. 지금은 *대화 능력은 mask로 가르친다*는 한 줄짜리 직관만 가져가자.

## 1.10 이 책의 코드 인용 규칙

코드를 읽는 책에는 *코드 인용을 어떻게 다루는가*가 중요한 문제다. 너무 많이 인용하면 책이 코드 덤프가 되고, 너무 적게 인용하면 *추상적 설명만 둥둥 떠다닌다*. 이 책은 다음 세 가지 규칙으로 균형을 잡는다.

**5줄 이하의 짧은 인용은 본문 안에 그대로 박는다.** 함수 시그니처, 한 줄짜리 정의, 핵심 한 줄 같은 것들이 여기 해당한다. 본문의 호흡을 끊지 않고 *지나가며* 읽힌다.

**5줄에서 20줄 사이는 코드 블록 박스로 분리한다.** 한 함수의 핵심부, 클래스 한 토막 같은 것이 여기 들어간다. 박스 앞에 *어디서 펴는지*(파일 경로와 라인 범위)를 명시하고, 박스 뒤에 *그 코드가 무엇을 하는지*를 한두 단락으로 풀어준다.

**20줄을 넘어가면 인용하지 않는다. 대신 *코드 펴기 신호*를 준다.** 이때 본문에는 한 줄만 들어간다: *"`nanochat/optim.py:299-535`를 펴자."* 그리고 그 함수의 *큰 그림*만 산문으로 설명한다. 책이 코드의 *완전한 복제본*이 아니라 *코드를 펴서 읽기 위한 동반자*가 되는 지점이다.

이 규칙에 *한 가지 예외*가 있다. `nanochat/loss_eval.py`처럼 *파일 전체가 한 페이지 미만*인 짧은 모듈은 통째로 인용하기도 한다. 7장에서 그렇게 한다. 짧은 파일은 *생략하는 게 더 번거롭다*.

코드를 인용할 때 *라인 번호는 신뢰의 화폐*다. 이 책의 모든 라인 번호는 카르파시의 nanochat 리포 특정 커밋 기준이고, 책 본문 작성 시 *직접 파일을 펴서 재검증*했다. master 브랜치가 빠르게 움직이기 때문에 라인 번호가 *살짝 어긋날 수 있지만*, 함수명·클래스명·핵심 키워드는 그대로 두고 라인 번호를 *근사값*으로 받아들이자. 각 챕터의 코드 인용 블록 위에는 *해당 커밋의 SHA*도 함께 표기한다.

*책과 코드의 관계*에 대해 한 가지 더. 우리는 이 책을 *코드를 펴는 동반자*로 만들려고 한다. 책을 한 손에 들고 다른 손으로 에디터를 열어두는 그림이 이상적이다. 책이 *모든 코드를 다 보여주지는 않는다*. 대신 책은 *그 코드를 *어떤 순서로*, *어떤 질문을 가지고*, *어떤 직관과 함께* 읽으면 되는지를 알려준다.

이 차이가 *기술서의 가치*라고 생각한다. 코드는 깃허브에 가면 다 있다. 책이 줄 수 있는 건 그 코드 안에서 *어디를 봐야 하는지*, *왜 그 디자인인지*, *그 결정이 다른 부분과 어떻게 얽혀 있는지*에 대한 *내러티브*다. 우리는 그 내러티브를 12장에 걸쳐 펼쳐본다.

## 1.11 두 가지 읽기 방식 — 풀 GPU 노드 vs 노트북 정성 검증

이 책은 두 종류의 독자를 *동시에* 가정한다.

**풀 GPU 노드를 가진 독자**는 `runs/speedrun.sh`를 *진짜로* 한 번 돌려본다. 8XH100을 빌릴 수 있는 형편이라면 가장 좋고, A100 1장이나 4090 1장으로도 *작은 nanochat*은 만들 수 있다. 책은 6장의 끝에서 "환경별 사다리 표"를 통해 *어떤 GPU에서 어떤 결과를 기대할 수 있는지* 정확히 알려준다. 진짜 GPT-2급 성능을 손에 쥐고 싶다면 이 길이 답이다.

**노트북만 가진 독자**는 `runs/runcpu.sh`로 *코드 경로를 다 밟아보는* 길을 간다. M3 Max 기준 약 40분 안에 토크나이저 학습 → d6 사전학습 5000 step → SFT 1500 step → chat_cli까지 *전 파이프라인*이 끝난다. 모델의 답변 품질은 *유치원생 수준*이다. README의 표현을 그대로 빌리면 *"kindergartener level"*. 그래도 책의 *모든 코드 경로*를 한 번 통과하고, 자기 노트북에서 *말하는 모델*이 한 번 깜빡이는 걸 보는 일은 그 자체로 큰 값이다.

두 길은 서로를 배제하지 않는다. 노트북에서 정성 검증을 한 뒤 GPU 한 노드를 빌려 풀 학습을 시도하는 게 *가장 권장되는 경로*다. 책의 챕터별 실습 박스에는 *(CPU/MPS X분)*과 *(GPU Y분)*이 *나란히* 적혀 있다. 둘 중 하나를 골라 따라가면 된다.

한 가지 *솔직한 당부*. CPU/MPS 경로의 결과로 "내 모델이 자연스럽게 대화한다"를 기대하지는 말자. 그건 d24 GPU 학습의 결과이지 d6 CPU 학습의 결과가 아니다. 8장에서 *기대치 조정 박스*를 통해 이 부분을 한 번 더 짚는다. 책이 정직하게 기대치를 그어두는 것 자체가 *기술서가 독자에게 줄 수 있는 가장 중요한 선물* 중 하나라고 생각한다.

GPU 한 노드를 *어떻게 빌리는가*에 대한 짧은 메모. nanochat README에서 카르파시는 Lambda Labs를 추천한다. 시간당 $24 안팎으로 8XH100 한 노드를 빌릴 수 있고, 스팟 인스턴스라면 절반 가까운 값에 잡힌다. RunPod, Vast.ai, CoreWeave 같은 다른 공급자들도 비슷한 가격대로 GPU를 빌려준다. *3시간만 빌려서 speedrun을 돌리고 반납*하는 패턴이면 한 번 시도하는 데 $50 안팎이다. 책을 다 읽고 *한 번은* 풀 GPU로 굴려보는 경험이 권장된다 — *말로만 듣던 것*과 *직접 한 번 굴려본 것*은 머릿속에 남는 무게가 다르다.

물론 GPU가 *영영 없는* 독자에게도 이 책은 의미가 있다. 코드를 읽는 것만으로도 *현대 LLM이 어떻게 구성되는지*에 대한 멘탈 모델은 완전히 잡힌다. d6 CPU 학습으로 작은 *말하는 모델*을 한 번 깜빡여보는 경험은 그 자체로 충분히 흥미롭다. "내가 학습시킨 모델이 답한다"는 *처음의 감각*은 d24든 d6든 똑같이 짜릿하다.

## 1.12 1장 실습 박스

이론은 충분히 깔았다. 손을 움직이자. 이 실습이 끝나면 nanochat의 *환경*과 *데이터의 무게*가 손에 쥐어진다.

> **[CPU/GPU 공통, 약 10분]**
>
> 1. nanochat 리포를 받고 환경을 잡는다.
>
>    ```bash
>    git clone https://github.com/karpathy/nanochat.git
>    cd nanochat
>    uv sync --extra cpu       # GPU가 있다면 --extra gpu
>    source .venv/bin/activate
>    export NANOCHAT_BASE_DIR="$HOME/.cache/nanochat"
>    mkdir -p $NANOCHAT_BASE_DIR
>    ```
>
> 2. 셰드 두 개와 validation 셰드를 받는다. 시간을 *직접 재본다*.
>
>    ```bash
>    time python -m nanochat.dataset -n 2
>    ```
>
>    빠른 네트워크에서 약 1분. 끝나면 `~/.cache/nanochat/base_data_climbmix/`에 세 개의 parquet이 있다.
>
> 3. 첫 셰드의 첫 문서를 *직접* 펴보자.
>
>    ```python
>    import os
>    import pyarrow.parquet as pq
>
>    path = os.path.expanduser("~/.cache/nanochat/base_data_climbmix/shard_00000.parquet")
>    pf = pq.ParquetFile(path)
>    rg = pf.read_row_group(0)
>    texts = rg.column("text").to_pylist()
>
>    print(f"row group 0 has {len(texts)} documents")
>    print(f"first doc has {len(texts[0])} characters")
>    print("--- first 500 chars ---")
>    print(texts[0][:500])
>    ```
>
>    출력의 형태에 익숙해지자. 이게 *모델에게 먹일 식량*이다.
>
> 4. 9개의 특수 토큰이 어떻게 정의되어 있는지 *코드를 직접 펴서 확인*한다.
>
>    ```bash
>    sed -n '13,25p' nanochat/tokenizer.py
>    ```
>
>    9개 토큰의 이름과 주석을 *눈으로* 한 번 훑어두자. 책 전체의 줄거리가 이 13줄에 압축되어 있다.

이 실습은 *환경 점검*인 동시에 *책 전체의 도입부*다. 다운로드 시간과 셰드 크기를 직접 손에 쥐어보고, 9개의 특수 토큰을 눈으로 한 번 훑어두는 일 — 이것이 본격적인 코드 여행을 떠나기 전 *손을 따뜻하게 하는 의식*이다.

실습이 잘 안 풀린다면 흔한 원인 두 가지. 첫째, `NANOCHAT_BASE_DIR` 환경 변수가 *현재 셸*에서 설정되어 있는지 확인하자. `echo $NANOCHAT_BASE_DIR`로 한 번 찍어본다. 비어 있으면 `export` 명령을 다시 실행. 둘째, `uv sync`가 성공했는지 `python -c "import torch; print(torch.__version__)"`로 한 번 확인한다. `2.9.1`이 떠야 한다. 두 가지 모두 정상이면 다운로드는 거의 항상 잘 된다 — HuggingFace 미러가 가끔 느려질 수는 있지만, 결국 받아진다.

## 1.13 마무리 — 2장에서 보자

여기까지가 1장이다. 우리가 무엇을 손에 쥐었는지 정리해보자.

카르파시의 "$100 ChatGPT"라는 도발이 *정확히 무엇을 약속하는지* — 8천 줄의 코드와 8XH100 한 노드 3시간으로 GPT-2급 ChatGPT를 *처음부터 끝까지* 만든다는 것 — 을 분명히 했다. 그게 nanoGPT → modded-nanoGPT → nanochat의 *가계도* 안에서 어떤 자리를 차지하는지도 보았다.

책의 *약속과 한계*도 그었다. nanochat 코드를 한 줄도 빠짐없이 따라 읽고, 직접 굴려보고, 각 단계가 *무엇을 가르치는지* 한 문장으로 설명할 수 있게 한다. 다만 한국어 챗봇은 약속하지 않고, 이론서도 아니며, 프로덕션 모델을 만드는 책도 아니다.

환경을 잡았다. `uv sync` 한 줄과 `NANOCHAT_BASE_DIR` 환경 변수 한 줄. 그게 끝이다. 그리고 데이터 셰드 두 개를 *진짜로* 받아봤다. 한 셰드가 약 100MB, 약 2억 5천만 글자라는 *무게*를 손에 쥐었다.

작품의 *네 층위* — `nanochat/` 라이브러리, `scripts/` CLI, `tasks/` 데이터, `runs/` 셸 — 도 머리에 박았다. 챕터를 펴며 *내가 지금 어느 층에 있는가*를 늘 한 번 짚는 습관을 들이자.

그리고 9개의 특수 토큰을 한 번 들여다보았다. `<|bos|>`, `<|user_start|>` 같은 것들이 *모델보다 먼저 정해지는 결정들*이라는 사실을 알았다. 토크나이저는 그저 *바이트를 토큰으로 쪼개는 모듈*이 아니라 *모델이 세상을 보는 단위*를 결정하는 모듈이라는 직관이 살짝 잡혔다.

그 직관이 바로 2장의 *aha*다.

2장에서는 같은 한 줄의 한국어 문장이 GPT-2(50K), GPT-4(100K), 그리고 우리의 32K nanochat 토크나이저에서 *얼마나 다르게* 쪼개지는지를 *직접 본다*. "안녕하세요, 저는 토비입니다"라는 짧은 문장이 어떤 토크나이저에서는 18개 토큰이 되고, 어떤 토크나이저에서는 8개가 된다. 그 차이가 *무엇을 의미하는지* — 모델 학습 비용, 추론 속도, 그리고 *한국어가 영어보다 두 배 비싸지는 이유*까지 — 가 2장에서 풀린다.

토크나이저는 *모델이 세상을 보는 단위*다. 그 단위를 어떻게 정했느냐에 따라 모델이 무엇을 *잘 보고* 무엇을 *잘 못 보는지*가 결정된다. 영어 위주로 학습된 토크나이저에서 한국어가 비싸지는 것도, GPT-4가 *strawberry의 r 개수를 못 세는* 것도, 결국 *토큰화 단계의 결정*이다. 모델 자체가 "멍청해서"가 아니다. 우리는 그걸 코드로 *직접 확인한다*.

*기억해두자.* nanochat은 *읽기 위해 짜인 코드*다. 운영 환경의 모든 엣지 케이스를 처리하려고 짜인 코드가 아니다. 그래서 책을 따라가다 보면 *너무 단순해 보이는 결정*들이 눈에 자주 띈다. 그게 약점이 아니라 *디자인*이다. 우리는 그 단순함을 *깊이 이해*하려고 책을 폈다.

코드를 펴고 함께 가자.
