# 4장. ReAct 너머 — 루프 모양의 변종들

같은 모델로 같은 문제를 풀어도 점수가 18배 차이 나는 경우가 있다. Game of 24를 단순 CoT(Chain-of-Thought)로 풀게 시키면 정답률이 4%, Tree of Thoughts로 풀게 시키면 74%다 (Yao et al. 2023). 모델은 똑같다. 바뀐 건 모델 위에 씌운 "루프 모양" 뿐이다.

3장에서 우리는 `mini_agent.py`라는 작은 ReAct 루프를 손으로 짰다. while 한 줄로 round-trip을 감싸고, tool 결과를 다시 모델에 먹이는 패턴. 단순하지만 강력했다. 일반적인 도구 사용 작업의 70~80% 정도는 이 작은 루프로 충분히 풀린다. 그런데 ReAct가 모든 문제에 통할까? 나머지 20~30%는 어디로 가야 할까?

한 번 솔직하게 따져보자. 사용자가 "이 데이터를 분석해서 요약해 줘"라고 했다고 해보자. ReAct는 한 스텝씩 생각하고, 한 스텝씩 도구를 부른다. 그런데 만약 작업이 일곱 단계로 쪼개져야 하고, 두 번째 단계의 결과가 다섯 번째 단계의 입력이라면? ReAct는 매 스텝마다 "지금 뭘 해야 하지?"를 다시 묻는다. 큰 그림이 없다. 그래서 자주 길을 잃는다. 도중에 엉뚱한 도구를 부르거나, 같은 단계를 반복하거나, 끝났다고 착각하고 멈춘다. 난감한 상황이다.

또 다른 경우. 모델이 답을 한 번 틀렸을 때, *그 실패에서 배워서* 다음 시도에 반영하길 바란다고 해보자. ReAct는 다음 시도에 들어가는 순간 깨끗하다. 어제 무엇을 잘못했는지 모른다. 사람은 시험을 망치면 오답 노트를 쓰는데, ReAct에는 오답 노트가 없다. 찜찜하다. 같은 함정에 매번 새 마음으로 다시 빠진다.

마지막 경우. "여러 가능성을 펼쳐 보고, 그중 가장 그럴듯한 길을 골라라"가 본질인 문제. 수학 퍼즐, 게임의 다음 수, 전략 의사 결정 같은 것들. ReAct는 직선이다. 한 길로 쭉 간다. 갈림길이 있어도 한쪽만 본다. 막다른 길에 도달해도 백트래킹할 줄 모른다. 그저 "더는 진전이 없네"라고 적고 멈춰 버린다.

이 세 가지 결함을 각각 다른 방식으로 메우려고 등장한 학술 패턴이 Plan-and-Solve, Reflexion, Tree of Thoughts다. 여기에 Voyager와 LATS를 곁들이면, 2023년 이후 "ReAct 너머"에서 시도된 루프 변종들의 거의 전부를 짧게 훑을 수 있다. 한 번 살펴보자.

## 큰 그림을 먼저 그리자 — Plan-and-Solve

먼저 떠오르는 가장 단순한 보완책은 무엇일까. "한 스텝씩 생각하지 말고, 전체 계획을 먼저 세운 다음 그 계획을 따라가게 하자." 사람이 일을 할 때 자연스럽게 하는 그것이다.

Wang et al.이 2023년에 발표한 Plan-and-Solve(PS) prompting이 이 발상을 그대로 옮긴다 (Wang et al. 2023, [arXiv:2305.04091](https://arxiv.org/abs/2305.04091)). 단순 CoT의 "let's think step by step" 한 줄을 두 단계로 분해한다. 먼저 *plan을 만들고*, 그다음 *plan에 따라 풀어라*. 논문의 동기는 단순 CoT가 자주 빠뜨리는 missing-step 오류 — 중간 단계를 통째로 건너뛰는 실수 — 를 줄이자는 데 있다.

코드로 옮기면 의외로 작다. `mini_agent.py`의 루프 시작 직전에 plan 단계 하나만 끼우면 된다. 정본 mini_agent는 손대지 않고, 별도 demo 파일을 만들자.

```python
# plan_and_solve_demo.py
from mini_agent import call_llm, run_agent  # 3장의 정본을 그대로 가져온다

PLAN_PROMPT = """\
You are a planner. Given the user task, break it down into 3~6 concrete
subtasks. Output each subtask as a single line, prefixed with a number.
Do not solve any subtask here — only plan.
Task: {task}
"""

def make_plan(task: str) -> str:
    messages = [{"role": "user", "content": PLAN_PROMPT.format(task=task)}]
    return call_llm(messages)

def run_plan_and_solve(task: str) -> str:
    plan = make_plan(task)
    augmented = (
        f"Task: {task}\n\n"
        f"Plan to follow (do not deviate):\n{plan}\n\n"
        f"Now execute the plan one subtask at a time."
    )
    return run_agent(augmented)  # 기존 ReAct 루프 재사용

if __name__ == "__main__":
    print(run_plan_and_solve("오늘 서울 날씨를 알아보고, 우산이 필요한지 알려줘"))
```

루프 모양 자체는 그대로다. 바뀐 건 단 하나, ReAct 루프에 들어가기 전에 "이 일을 어떻게 쪼갤 것인가"의 텍스트가 시스템 컨텍스트에 한 번 박힌다는 점이다. 그러면 모델은 매 스텝 "지금 뭐 하지?"를 다시 묻는 대신, 미리 박힌 plan을 참조하며 진행한다. 다섯 번째 스텝에서 두 번째 스텝의 결과를 가져와야 한다는 사실도 plan에 적혀 있다.

물론 단점도 있다. plan이 틀리면 그대로 틀린다. 첫 단추가 어긋난 채로 루프가 그 위를 충실히 따라가니, 잘못된 길로 더 길게 걸어가게 된다. 또 plan을 만드는 데 LLM 호출이 한 번 더 들어간다. 작업이 단순할수록 이 추가 호출은 손해다. ReAct가 한 호출로 끝낼 일을 두 번에 나눠 푸는 셈이다.

그래서 ReAct로 충분한 단순 작업에까지 Plan-and-Solve를 끼울 필요는 없다. 본격적으로 효과를 보는 건 "작업이 명백히 다단계인데, ReAct가 자꾸 중간 단계를 빠뜨릴 때"다. 다섯 단계 이상의 절차, 단계 간 의존성이 또렷한 작업, 사용자가 입력에 이미 "먼저 A 한 다음 B" 같은 순서를 쓴 경우가 후보다. 이런 신호가 보이면 plan 단계 하나만 끼워 보자. 30줄짜리 변형으로 missing-step 오류가 줄어드는 경우가 의외로 많다.

한 가지 더, plan을 따로 만들지 않고 시스템 프롬프트에 "먼저 plan을 적고, 그다음 plan을 따라 실행하라"라고 한 줄만 추가하는 더 가벼운 변형도 가능하다. 호출 수가 늘지 않는 대신, 모델이 plan을 *진지하게* 따르도록 강제하기는 어렵다. 둘 중 무엇이 나은지는 작업마다 다르니, 한 번씩 비교해 보고 고르는 편이 좋다.

## 실패에서 배우게 하자 — Reflexion

Plan-and-Solve가 "큰 그림을 먼저 그리자"였다면, Reflexion은 "틀렸을 때 왜 틀렸는지를 기록하자"다. Shinn et al. 2023의 Reflexion 논문이 던진 한 줄짜리 아이디어가 이것이다 (Shinn et al. 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)).

발상을 그대로 옮기면 이렇다. 에이전트가 한 번 시도해서 실패하면, 그 trial 전체를 모델에게 다시 보여준 뒤 "이번에 왜 실패했는지, 다음 시도에 무엇을 다르게 할지 한 문단으로 적어라"라고 시킨다. 그렇게 만들어진 자기 반성(self-reflection) 텍스트를 *다음 시도의 시스템 프롬프트*에 끼운다. 모델은 자기가 어제 무엇을 잘못했는지를 들고 두 번째 시도에 들어간다.

논문이 보인 숫자가 인상적이다. HumanEval에서 GPT-4 baseline의 pass@1이 80%였는데, Reflexion을 두르자 91%로 올라간다 (Shinn et al. 2023, 3.4). 같은 모델인데, "지난번에 인덱스를 헷갈렸으니 다음엔 0-base 확인부터 하자" 같은 자기 메모 한 단락이 11퍼센트 포인트의 차이를 만든다는 이야기다.

코드로 옮기자. 이번에도 `mini_agent.py`는 손대지 않는다. demo 파일 하나만 추가하면 충분하다.

```python
# reflexion_demo.py
from mini_agent import run_agent, call_llm

REFLECT_PROMPT = """\
You just attempted the task below and failed. Trial transcript:
{transcript}

Write ONE short paragraph that:
1) names the concrete mistake you made,
2) states what you will do differently next time.
"""

def reflect(transcript: str) -> str:
    messages = [{"role": "user",
                 "content": REFLECT_PROMPT.format(transcript=transcript)}]
    return call_llm(messages)

def run_reflexion(task: str, max_trials: int = 3) -> str:
    memo = ""
    for trial in range(max_trials):
        system = "Reflections from past trials:\n" + memo if memo else ""
        result, transcript, succeeded = run_agent(task, system_prefix=system)
        if succeeded:
            return result
        memo += f"\n[Trial {trial+1}] " + reflect(transcript)
    return result  # 최종 trial 결과 반환
```

`run_agent`가 transcript와 성공 여부를 함께 돌려준다는 가정이 들어가 있다. 3장에서 짠 정본이 이 두 가지를 돌려주도록 *조금만* 손보면 된다. 정본 자체의 루프 모양은 그대로다.

흥미로운 건 이 패턴이 "메모리"의 한 변종이라는 점이다. 보통 LLM 에이전트의 메모리라고 하면 대화 history를 떠올리는데, Reflexion의 자기 메모는 그것과 결이 다르다. trial 사이에 살아남는, *과거 실패의 추상화*다. 메모리 분류학에서는 이걸 episodic memory라고 부른다. 이 이야기는 5장에서 본격적으로 다시 꺼낼 것이다.

당장 실무에 끼울 때 주의할 점도 있다. 자기 메모가 누적되면 시스템 프롬프트가 점점 길어진다. 그래서 trial 수를 적당히 제한하거나(보통 3~5회), 오래된 메모는 요약으로 압축하는 손질이 필요하다. 또 자기 메모가 *틀린* 진단을 내놓을 수도 있다. 모델이 "내가 이번에 X 때문에 틀렸다"고 적었는데 실은 다른 이유였다면, 다음 trial은 엉뚱한 방향으로 흐른다. 자기 진단의 오류를 자기가 또 진단하는 식의 메타 함정에 빠지면, 메모는 점점 시처럼 추상화되고 실효는 없어진다. 이 경우엔 자기 메모 대신 외부에서 주어진 ground-truth 오류 정보 — 예를 들어 테스트 실패 로그, 사용자 피드백 — 를 끼우는 변형이 낫다.

또 하나 짚어둘 점. Reflexion이 빛나는 자리는 *성공/실패의 신호가 명확한 작업*이다. 코드를 짜고 테스트가 돌면 성공, 안 돌면 실패, 같은 식의 검증 신호가 있을 때 trial 사이의 학습이 의미를 갖는다. 반대로 "이 글 잘 썼나?"처럼 성공 기준이 모호한 작업에서는 Reflexion의 자기 메모가 자기 위안에 그치기 쉽다. 끼우기 전에 "이 작업의 성공을 무엇으로 판정할 것인가"부터 정해 두자.

## 한 길 말고 여러 길을 펼치자 — Tree of Thoughts

이제 가장 화려한 변종, Tree of Thoughts(ToT)다. Yao et al. 2023의 같은 그룹이 ReAct 다음 해에 내놓은 후속 작업 (Yao et al. 2023, [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)).

발상은 이렇다. CoT와 ReAct는 한 번에 하나의 "생각"만 펼친다. 직선이다. 그런데 사람이 어려운 문제를 풀 때를 떠올려보자. 우리는 머릿속에서 여러 가능성을 *동시에* 띄워 놓고, 각각을 짧게 시뮬레이션해 본 다음, 가장 그럴듯한 한두 가지만 더 깊이 파고든다. 갈림길에서 한쪽이 막다른 길로 보이면 다른 쪽으로 백트래킹하기도 한다. ToT는 이걸 LLM에게 그대로 시킨다. 한 thought를 노드로 보고, 다음 thought 후보를 *여러 개* 생성하고, 각 후보를 self-evaluation으로 점수를 매기고, 가장 유망한 가지만 확장하는 트리 탐색을 돈다.

Game of 24의 정량 차이가 이 발상의 가치를 가장 잘 보여준다. 같은 GPT-4로 단순 CoT를 시키면 4%, ToT를 시키면 74%다 (Yao et al. 2023, 3.1). 같은 모델로 18배의 격차가 난다. ReAct를 처음 짜 봤을 때의 흥분과는 또 다른 충격이다.

코드를 다 옮기진 않는다. 본격적인 ToT 구현은 trial state, 평가 함수, beam search 같은 부속이 붙어 한 챕터 분량을 가뿐히 넘긴다. 대신 의사코드로 모양만 보자.

```text
function ToT(task, branching_factor=3, depth=4, beam=2):
    frontier = [empty_thought]
    for step in 1..depth:
        candidates = []
        for thought in frontier:
            # 한 노드에서 branching_factor개의 다음 thought를 생성
            next_thoughts = LLM.propose(task, thought, n=branching_factor)
            for t in next_thoughts:
                score = LLM.evaluate(task, t)   # self-evaluation
                candidates.append((thought + [t], score))
        # 상위 beam개만 살려서 다음 깊이로
        frontier = top_k(candidates, k=beam, by=score)
    return best(frontier)
```

이 의사코드만 봐도 비용이 어떻게 폭증하는지 보인다. branching factor 3, depth 4, beam 2면 한 task당 LLM 호출이 수십 번 들어간다. propose 호출에 evaluate 호출까지 곱해진다. ReAct가 한 task에 4~8회 호출하던 것과 비교하면 한 자리수 차이가 난다. 토큰 비용도 그대로 곱해진다. ReAct 한 번 돌릴 돈으로 ToT는 한 스텝만 펼치고 끝날 수도 있다.

게다가 self-evaluation이 항상 신뢰할 만한 것도 아니다. 모델이 자기 후보를 자기가 채점하는 구조라, "내가 만든 게 제일 좋아 보여요"라는 편향이 자주 나타난다. 평가 prompt를 깐깐하게 짜고, 여러 평가를 평균 내고, 때로는 외부 검증을 끼우는 손질이 필요하다. 이쯤 되면 단순 ReAct에 비해 코드량과 운영 비용 둘 다 한 자리수 늘어난다.

그래서 ToT를 진짜로 꺼낼 자리는 매우 좁다. "탐색과 평가 사이의 trade-off"가 본질인 문제 — 수학 퍼즐, 게임의 다음 수, 창의적 글쓰기에서 후보 출력을 비교 평가하는 경우 — 에 한해서다. 일반 작업에 ToT를 무차별 적용하면 비용만 잡아먹는다. 끔찍한 일이다. 입문 단계에서는 "ToT라는 모양이 존재한다"는 사실만 머릿속에 박아두고, 실제 적용은 정말 필요할 때까지 미루는 편이 낫다.

물론 ToT 발표 이후 여러 후속 작업이 이 비용을 줄이려고 시도한다. 그중 하나가 곧이어 살펴볼 LATS다.

## 영감으로만 기억해 두자 — Voyager

Voyager는 Wang et al. 2023의 또 다른 작업이다 (Wang et al. 2023, [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)). 우리 책의 본문에서는 한 단락으로 충분하지만, "디자인 영감"의 자리에서 꼭 한 번은 언급해 두는 편이 낫다.

Voyager의 핵심 발상은 skill library다. 에이전트가 Minecraft 안에서 어떤 작업을 성공시킬 때마다, 그 성공 경로를 *재사용 가능한 함수*로 추상화해 라이브러리에 누적한다. 다음 작업에서 비슷한 패턴이 필요하면 라이브러리의 함수를 호출해 재사용한다. 사람이 손에 익은 기술을 쌓아가듯, 에이전트도 자기 기술을 쌓는다.

루프 모양으로 보면 Reflexion의 친척이다. 둘 다 "과거 경험을 다음 시도에 이식한다." 다른 점은 이식의 단위다. Reflexion은 *자기 반성 텍스트*를, Voyager는 *코드 함수*를 이식한다. Reflexion이 episodic memory라면 Voyager는 procedural memory다.

실무에서 곧장 베껴 쓸 건 아니다. 도메인이 너무 특수하기 때문이다. 다만 "과거의 성공을 어떻게 미래에 재사용할 것인가"라는 질문이 던져졌을 때, Voyager의 모양을 떠올리면 설계 선택지가 한 칸 늘어난다. 예컨대 사내 코드 에이전트를 만든다고 해보자. 자주 쓰이는 작업의 성공 경로를 함수로 추출해 라이브러리에 저장하고, 다음 비슷한 요청에서 호출 가능한 도구로 제공하는 식. 모양은 Voyager에서 온 것이지만 적용 도메인은 전혀 다르다. 그래서 기억만 해 두자.

## 위치만 잡아두자 — LATS

LATS(Language Agent Tree Search)는 Zhou et al. 2023의 작업이다 (Zhou et al. 2023). 이름에서 짐작되듯, ToT의 트리 탐색과 Reflexion의 자기 반성을 결합한 패턴이다. 트리의 각 노드에서 평가만 하는 게 아니라, 실패한 경로에서 *반성*을 뽑아 다음 탐색에 반영한다. 비용은 ToT보다 더 든다. 대신 탐색의 품질이 한 단계 올라간다.

본문에서는 위치만 잡아 둔다. ToT를 알고 Reflexion을 알면, LATS는 "두 개의 합성"으로 머릿속에 들어온다. 따로 한 챕터를 할애해 분해할 만한 가치가, 입문서 단계에서는 아직 없다. 더 깊이 들어가고 싶다면 원 논문을 직접 보자.

## 그래서 언제 무엇을 꺼낼까

다섯 가지 변종을 훑었다. 그런데 정말 매번 어떤 걸 골라야 할지 고민될 텐데, 결정 기준은 의외로 단순하다.

먼저, 작업 성공률이 안정적이라면 굳이 변종을 꺼낼 필요가 없다. ReAct 그대로 가는 편이 낫다. 비용도 적고, 디버깅도 편하다. ReAct로 90%가 풀린다면, 마지막 10%를 잡으려고 ToT를 끼우는 건 보통 손해다. "더 화려한 패턴이 더 나은 패턴은 아니다"라는 점을 기억해두자. 학술 논문에서 멋져 보인 것과 우리 손에서 잘 도는 것은 다르다.

작업이 명백히 다단계이고, ReAct가 자꾸 중간 단계를 빠뜨린다면 Plan-and-Solve를 끼우는 편이 낫다. 30줄 변형으로 큰 그림을 한 번 잡아주는 것만으로 missing-step 오류가 줄어든다.

작업이 실패할 때, *그 실패에서 학습이 필요하다*면 Reflexion이다. 코드 생성, 문제 풀이, retry가 의미 있는 작업이 여기에 해당한다. trial 사이에 자기 메모를 누적하는 모양만 잘 짜면 된다.

탐색과 평가의 trade-off가 본질인 문제 — 게임, 퍼즐, 의사 결정 — 라면 Tree of Thoughts다. 다만 비용을 미리 각오하자. 일반 작업에 ToT를 들이밀면 토큰 비용이 폭증한다. 시작 전에 한 번 계산기를 두드려 보는 편이 좋다. branching factor × depth × beam의 곱이 한 task당 LLM 호출 수다. 거기에 토큰 단가를 곱하면 월 청구서가 어림된다. 그 숫자가 감당 가능한가? 감당 불가능하다면 ToT는 옵션에서 빼자.

마지막으로, 과거 성공을 자산으로 누적하고 싶다면 Voyager의 skill library 발상을 빌리자. LATS는 ToT + Reflexion이 둘 다 필요해진 단계에서 꺼내면 된다.

조합도 가능하다는 점을 잊지 말자. Plan-and-Solve로 큰 그림을 그리고, 그 안의 각 subtask는 ReAct 루프로 돌리고, 전체 trial이 실패하면 Reflexion 메모를 남겨 다음 trial에 끼우는 식의 합성이 자연스럽다. 변종들은 배타적이지 않다. 각각이 다른 결함을 메우는 패치라서, 결함이 둘 이상이면 패치도 둘 이상 붙이면 된다. 다만 매번 "지금 이 변종을 왜 끼우는가"의 답이 명확해야 한다. 답이 흐릿하면 그건 그냥 ReAct로 돌려도 될 자리다.

## 결국 루프 모양의 변형이다

여기까지 따라온 독자라면 한 가지가 보였을 것이다. 다섯 가지 변종이 결국 *루프 모양의 변형*이라는 사실이다. ReAct가 한 바퀴 round-trip을 while로 감싼 것이라면, Plan-and-Solve는 루프 앞에 plan 단계를 한 번 끼운 것이고, Reflexion은 루프 바깥에 trial 메모리를 둔 것이고, ToT는 루프의 한 스텝을 트리 분기로 펼친 것이다. Voyager는 루프 결과를 함수 라이브러리로 누적한 것이고, LATS는 둘 이상의 모양을 합성한 것이다. 각 패턴이 손대는 자리 — 루프 앞, 루프 바깥, 루프 안의 한 스텝, 루프 결과 — 가 모두 다르다는 점이 흥미롭다.

이 관찰이 왜 중요할까. 앞으로 우리가 만날 프레임워크들이 이 변종들을 어떻게 흡수하는지 보여주기 때문이다. 7장에서 LangChain을 살펴볼 때, 8장에서 LangGraph를 살펴볼 때, 그리고 10장에서 멀티 에이전트로 넘어갈 때, 우리는 같은 루프 모양들을 *추상화의 옷*을 입은 형태로 다시 만나게 된다. LangGraph의 `StateGraph`에 사이클을 그리는 순간, 그건 결국 Reflexion이나 Plan-and-Solve의 자리가 된다. LangChain Agent의 retry·fallback도 변종 루프의 한 표현이다. 정체를 알면 추상화가 덜 무섭다.

## 다음 장으로

다섯 패턴 모두에서 한 가지 공통의 골칫거리가 남는다. 매 iteration마다 history가 길어진다. ReAct는 매 round-trip마다 prior message가 누적되고, Plan-and-Solve는 plan 텍스트가 시작부터 박혀 있다. Reflexion은 trial 메모가 쌓이고, ToT는 트리의 후보 thought가 폭증한다. 컨텍스트 윈도우는 유한한데, 모양이 무엇이든 토큰은 자란다.

그래서 다음 5장에서는 "에이전트의 기억"을 정면으로 다룬다. 메모리의 네 분류 — short-term / long-term / episodic / semantic — 가 코드로 내려오면 결국 "리스트를 어떻게 자르느냐"의 문제로 환원된다는 사실, sliding window·summary buffer·외부 spillover의 세 가지 단순한 전략, 그리고 Reflexion에서 만났던 episodic memory가 다시 어디로 흘러가는지를 짚는다. 기억해두자. 루프의 모양이 무엇이든, history는 결국 길어진다.
