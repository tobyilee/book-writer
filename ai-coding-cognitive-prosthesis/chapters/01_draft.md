# 1장. 5초마다 결정해야 한다 — 감독관이 된 개발자의 피로

> *"I'm experiencing severe cognitive overload combined with serious mental burnout."*  
> — Hacker News, *"Ask HN: I feel several times more fatigue when coding with AI"* [1]
>
> *"I find myself being [like] a lazy babysitter that's just doing enough to keep the kids from hurting themselves."*  
> — 같은 스레드의 다른 개발자 [2]

이 두 문장 앞에서 잠깐 멈춰서자. 한 사람은 "심각한 인지 과부하와 정신적 번아웃"을 겪고 있다고 말하고, 다른 한 사람은 자기를 "아이들이 다치지 않을 정도로만 봐주는 게으른 베이비시터"에 비유한다. 두 사람 다 코드를 안 짠다는 게 아니다. *AI와 함께 코드를 짠다.* 그런데 끝나면 더 지친다. 어떤 개발자라도 이 문장을 보고 어딘가 익숙한 자리에서 자기 표정을 발견한다. 분명 더 빨리 끝냈는데, 왜 더 텅 빈 채로 의자에서 일어나는가?

같은 스레드를 조금 더 내려가면 비슷한 결의 토로가 줄을 잇는다. 어떤 개발자는 자기 일과를 *"끊임없이 작은 작업과 LLM 기다림 사이를 오가는 일"* 이라고 묘사하고, 또 다른 개발자는 *"하루에 여섯 개 프로젝트를 의미 있게 진척시키지만 하루가 끝나면 탈진해 있다"*고 적었다. 빨라졌다는 말과 더 지친다는 말이 같은 사람의 입에서 나온다. 그것도 한두 명이 아니라 수백 개의 댓글이 비슷한 문장을 반복한다. 익명 게시판이라 더 솔직하다.

분명히 짚어두자. 이건 게으름이나 의지의 문제가 아니다. 이건 *구조*의 문제다. 그리고 그 구조는 지난 1년 사이 우리가 알아채지 못한 사이에 바뀌었다.

## 바이브 코딩에서 에이전틱 엔지니어링까지 — 자리가 바뀐 사람

2025년 2월 2일, Andrej Karpathy가 X에 한 줄을 던졌다.

> "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists." [3]

본인 말로는 *"a shower of thoughts throwaway tweet that I just fired off"* — 샤워 중에 떠오른 잡념을 그냥 던졌다는 — 한 줄이었는데, 4백 5십만 회 노출되며 산업의 명칭이 됐다. 코드를 *느낌*으로 짠다. 코드가 존재한다는 사실조차 잊는다. 가벼운 표현이지만 그 가벼움이 정확히 그 시점의 분위기였다. *AI에게 맡기고, 흐름을 즐기고, 결과를 받는다.*

그로부터 약 1년이 지난 2026년의 Sequoia AI Ascent에서 같은 사람이 다른 단어를 꺼냈다.

> "I'm not writing the code directly 99% of the time, you are orchestrating agents who do and acting as oversight." [4]

*99%.* 직접 코드를 쓰지 않는다. 에이전트들을 *조율*하고 *감독*한다. 그가 새로 선호한 용어는 *agentic engineering*. *agentic*은 직접 작성하지 않고 에이전트를 부린다는 뜻이고, *engineering*은 그래도 거기에 art와 science가 남아 있다고 강조하기 위해 붙였다.

*executor에서 orchestrator로*, *작성자에서 감독자로*. 1년 사이에 일어난 일을 한 줄로 줄이면 그 정도다. 그리고 이 한 줄이 우리 어깨에 얹은 무게가 — 1장에서 함께 들여다볼 그 피로의 정체다.

여기서 한 가지 짚고 가자. 감독관 자리는 작성자 자리보다 *편한* 자리가 아니다. 1983년 항공 자동조종 콕핏을 연구한 사람들이 이미 지적했던 사실인데, 4장에서 다시 만난다. 지금 우리가 짚어둘 건 단순하다. *코드를 적게 쓰게 됐다는 사실이 곧 머리를 적게 쓴다는 뜻은 아니다.* 오히려 그 반대일 수 있다.

## 빨라졌다고 *느꼈을 뿐* — METR이 측정한 19%의 진실

그러면 진짜로 묻자. AI가 우리를 *빨라지게 했나*?

2025년 7월, METR이라는 비영리 평가 기관이 한 편의 무작위 대조 시험(RCT) 결과를 공개했다 [5]. 표본은 16명의 숙련된 오픈소스 기여자 — 자기 프로젝트에서 평균 5년 이상 코드를 짠 사람들이었다. 246개의 실제 이슈를 두 그룹으로 나눠서 한쪽에는 AI 도구(Cursor Pro + Claude 3.5/3.7 Sonnet)를 허용했고, 다른 쪽에는 허용하지 않았다. 그러고 시간을 쟀다.

먼저 *예측*. 작업 시작 전 개발자 본인들은 AI를 쓰면 *24% 빨라질 것* 이라고 답했다. 외부 전문가들은 더 낙관적이었다 — 경제학자들은 -39%, ML 연구자들은 -38%. 누구나 빨라질 거라고 봤다.

작업이 *끝난 뒤* 본인들에게 다시 물었다. *어느 정도 효과를 봤습니까?* 대답은 *-20%* — 여전히 빨라졌다고 *느꼈다*.

그런데 실측 결과는 정반대였다. **+19%.** AI 도구를 허용했더니 작업 완료 시간이 19% *늘었다*. 논문 초록 한 줄을 그대로 옮기면 이렇다.

> *"allowing AI actually increases completion time by 19% — AI tooling slowed developers down."* [5]

이 숫자를 처음 접한 자리에서 멈춰 서서 한 번 더 음미할 만하다. 본인 *예측*은 -24%, *느낌*은 -20%, *측정*은 +19%. 예측·체감·실제 사이에 거의 *40 퍼센트 포인트*의 골이 패어 있다. 이게 의미하는 건 단순하다. **우리는 빨라졌다고 느끼지만, 그 느낌은 시계와 일치하지 않는다.** 끔찍한 건 빨라졌다고 *느낀* 그 시간 동안 우리가 *덜 피곤했냐* 하면, 그것도 아니다. METR 본문은 그 부분도 따로 짚는다 — 시간은 더 걸리고, 인지 부담은 더 컸다.

여기서 흔한 반론이 따라온다. *"표본이 16명인 연구 하나 가지고 일반화는 좀 그렇지 않나?"* 정당한 지적이다. 이 책도 한 편의 RCT만 들고 결론을 내리지는 않는다. 다만 METR 결과의 의미는 *숫자 그 자체*가 아니라 *느낌과 측정이 갈라진다*는 사실에 있다. 그 갈라짐은 다른 모집단·다른 도구에서도 반복적으로 관찰되었고, 책 뒷부분에서 그 보강 데이터를 차례로 만나게 된다. 한 줄로 요약하자면 — *빨라졌다는 느낌 자체를 의심해본 적이 있는가*가 이 책의 첫 질문이다.

자, 여기서 한 박자 쉬자. *그래서 AI는 다 사기였단 말인가?*

그렇지 않다.

## 그럼 +21%, +98% 는 거짓말인가 — 두 진실 사이에서

DORA 2025 *State of AI-Assisted Software Development* 보고서를 같이 펴 보자 [6]. 같은 해, 다른 모집단, 정반대 방향으로 생긴 숫자가 두 개 있다.

- 개인 단위 작업 완료: **+21%**
- 머지된 풀 리퀘스트 수: **+98%**

거의 *두 배*다. AI 채택률은 90%를 넘었고, 80% 이상이 "생산성이 올랐다"고 *느꼈다*. METR과 DORA, 둘 다 신뢰할 만한 출처고, 둘 다 2025년의 데이터다. 한쪽은 19% 느려졌다고 하고, 한쪽은 두 배 가까이 빨라졌다고 한다.

*같은 도구를 쓰는데 왜 결과가 갈릴까?*

DORA 2025가 1년 전 보고서와 결정적으로 달라진 지점이 여기다. 보고서는 AI를 *증폭기(amplifier)*로 본다. *"AI doesn't fix a team; it amplifies what's already there."* 강한 팀에서는 더 강해지게 만들고, 흔들리는 팀에서는 흔들림을 더 크게 만든다는 것이다. 사실 두 보고서 다 같은 가속에 동의한다 — 다만 그 가속이 *어디로 흘러가느냐*가 모집단에 따라 다르다. 강한 팀에서는 처리량으로 흘러가고, 약한 팀에서는 검증 큐와 결함률과 피로감으로 흘러간다. 그 자세한 해부는 5장에서 다시 만난다. 지금은 한 가지만 기억해두자. *METR의 -19% 와 DORA의 +21~98%, 둘 다 사실이다.* 모순은 데이터에 있지 않고, *어떤 모집단에서 어떤 조건으로 측정했는가*에 있다. 이 책은 둘 다 사실로 받아들이고 시작한다.

여기서 솔직하게 한 가지 더 짚자. DORA가 같은 시기에 "빨라졌다"고 보고한 그 팀들조차 — 조직 전체의 SW 전달 지표는 *정체* 상태였다. 개인은 빨라졌는데 조직은 그대로다. 가속의 일부가 어딘가로 *증발*했다는 뜻이다. 그 증발의 정체가 — 다음 절의 주제다.

## 5초마다 결정해야 한다 — 마이크로 결정의 누적

다시 처음의 두 인용으로 돌아가자. *"lazy babysitter."* 왜 *베이비시터*라는 비유였을까. 같은 HN 스레드의 또 다른 답변자가 그 감각을 더 짧게 정리한다.

> *"It's the constant switching between doing a little bit of work/coding/reviewing and then stopping to wait for the LLM to generate something."* [7]

조금 작업하다가, 멈추고, LLM이 뱉어주기를 기다리고, 받은 걸 본다. 또 조금 작업하다가, 또 멈추고, 또 받은 걸 본다. 5초쯤 마다. 200줄짜리 패치가 5초 만에 도착한다. 머지할 것인가, 읽을 것인가, 일부만 받을 것인가, 다시 시킬 것인가. 결정이 필요하다. 그것도 *순간적인* 결정이.

이 결정 하나하나는 작다. 하지만 한 시간 동안 그게 백 번이면, 백 번의 미시 결정이 머리에 차곡차곡 쌓인다. 그러는 동안 옆에서는 새 출력이 또 도착해 있다. 같은 스레드의 또 다른 댓글은 이걸 가장 정확하게 정리한다.

> *"The bandwidth of the info channel to the brain doesn't increase no matter what AI or anything else magically does."* [8]

마법 같은 도구가 와도 머리로 들어가는 정보 채널의 *대역폭*은 늘지 않는다. AI가 더 많이 만들어준다고 해서 우리가 더 많이 검토할 수 있게 되지는 않는다는 뜻이다. 물론 도구는 좋아졌다. 하지만 *받는 쪽*은 그대로다.

이게 1장의 핵심 메타포다. **5초마다 결정해야 한다.** 작성자였을 때는 한 시간에 결정의 큰 단위가 한두 개였다. 어떤 자료구조를 쓸 것인가, 어떤 패턴을 따를 것인가. 손은 그 결정을 *수행*하느라 바빴고, 머리는 그 사이에 자연스럽게 *호흡*했다. 감독관이 된 지금은 결정의 단위가 잘게 쪼개져서 끊임없이 들이친다. 호흡할 자리가 없다.

상황을 한 번 떠올려보자. 점심 직후에 자리에 앉아 Cursor를 열고 *"이 함수에 페이지네이션 추가해줘"* 라고 던졌다. 5초 뒤 200줄 패치가 도착한다. 변수명이 우리 컨벤션과 다르다 — 하나 결정. 새로 쓴 헬퍼가 실은 옆 모듈에 이미 있는 것 같다 — 두 번째 결정. 테스트가 같이 왔는데 모킹이 어색하다 — 세 번째 결정. 그러는 사이 다른 탭에서 또 다른 에이전트가 별개 작업의 결과를 던져둔다. 네 번째, 다섯 번째 결정. 한 시간 뒤 우리는 PR 두세 개를 *진척*시켰다. 그런데 머릿속에는 *읽다 만 컨텍스트의 잔재*가 다섯 종 쌓여 있다. 일이 끝났는데도 머리는 계속 어딘가 *살피고* 있다.

같은 스레드에 이런 줄이 있다.

> *"I can make meaningful progress on half a dozen projects in the course of a day now but I end the day exhausted."* [9]

하루에 여섯 개 프로젝트를 *의미 있게* 진척시킨다. 그런데 하루가 끝나면 *탈진*한다. 빨라졌다는 말과 지친다는 말이 *동시에 사실*인 자리 — 그 자리가 지금 우리 자리다. METR의 -19%와 DORA의 +98%가 *한 사람 안에서도* 동시에 작동한다.

찜찜하지 않은가. 일은 분명 더 많이 했는데, 끝나고 나면 머리가 저녁을 맞이할 준비가 안 돼 있다. 책상 앞을 떠나고 나서도 한참 동안 잔재가 남는다. *"코드 검토하던 모드"*가 저녁 식탁까지 따라온다. 이 잔재의 학술적 이름이 *attention residue*인데, 이것도 4장에서 정식으로 만난다.

## 이 책이 약속하는 것 — 그리고 약속하지 않는 것

여기까지 읽었다면 한 가지는 확실해졌을 것이다. *이건 나만의 문제가 아니다.* HN 스레드의 베이비시터도, METR의 16명의 숙련 기여자도, DORA가 측정한 강한 팀과 약한 팀도, 다 같은 시대를 같이 통과하고 있다. 어떤 사람은 가속하고 어떤 사람은 추락하지만, 누구도 *예전처럼* 일하지 않는다.

이 책은 그 피로감에 *언어*를 주려고 한다. 이름 없는 피로보다 이름 있는 피로가 견디기 쉽다. 9장에 걸쳐 우리는 다음 세 가지 자리를 거친다. 첫째, *내가 무엇을 겪고 있는가* — 1·2장에서 통증의 주관·객관을 직시하고. 둘째, *왜 그런가* — 3·4장에서 인지부하 이론과 자동화의 역설로 메커니즘을 해부하고. 셋째, *그러면 무엇을 손보면 되는가* — 5·6·7장에서 팀 차이와 하네스 엔지니어링의 도구를 손에 쥐고, 8·9장에서 다시 사람으로 돌아온다.

미리 말해둘 게 있다. 이 책은 *Cursor를 어떻게 쓰는지* 알려주는 매뉴얼이 아니다. 도구는 매월 바뀐다. 이 책이 다루는 건 도구가 바뀌어도 남는 *원리* 쪽이다. 그리고 *AI를 쓰지 말자*는 러다이트 선언도 아니다. 그 반대다 — *더 잘 쓰자*는 책이다. *단일 정답을 약속하지도 않는다.* METR의 -19%와 DORA의 +21~98%는 *모두* 사실이고, 어느 쪽이 *내 팀에* 적용되는지는 책 한 권으로 결정해줄 수 없다. 이 책이 줄 수 있는 건 그 판단을 위한 *지표*와 *어휘*다.

마지막으로 한 가지 더. 이 피로감엔 *얼마나* 비싸다는 가격표가 붙어 있을까? 1.7배 결함, 4배 클론, 신뢰 11퍼센트 포인트 하락, 디버깅 시간 증가 — 다음 장에서 같이 그 청구서를 펼쳐보자.

---

[각주 / 참고]

[1] Hacker News, *"Ask HN: I feel several times more fatigue when coding with AI"*, item id=44486289. [https://news.ycombinator.com/item?id=44486289](https://news.ycombinator.com/item?id=44486289)

[2] 같은 스레드의 베스트 답변 댓글 — *"lazy babysitter"* 표현. 출처 동일.

[3] Andrej Karpathy, X(Twitter) 게시글, 2025-02-02. *"Vibe Coding"* 명명 트윗. [https://x.com/karpathy/status/1886192184808149383](https://x.com/karpathy/status/1886192184808149383)

[4] Andrej Karpathy, *Sequoia AI Ascent 2026* fireside chat. *"99% of code I don't write directly anymore"*. 정리 자료: [thenewstack.io](https://thenewstack.io/vibe-coding-is-passe/), [aiagentssimplified.substack.com](https://aiagentssimplified.substack.com/p/from-vibe-coding-to-agentic-engineering).

[5] Becker, Rush, Barnes, Rein. *"Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"*, METR (2025). arXiv:2507.09089. [https://arxiv.org/abs/2507.09089](https://arxiv.org/abs/2507.09089). 표본 16명 숙련 OSS 기여자, 246 태스크, RCT 설계, Cursor Pro + Claude 3.5/3.7 Sonnet. *예측 -24% / 사후 평가 -20% / 측정 +19%.*

[6] DORA / Google Cloud, *2025 State of AI-Assisted Software Development*. [https://dora.dev/dora-report-2025/](https://dora.dev/dora-report-2025/). *"AI doesn't fix a team; it amplifies what's already there."* 인용 출처: itrevolution.com 분석 — *AI's Mirror Effect*.

[7] Hacker News, *"AI fatigue is real and nobody talks about it"*, item id=46934404. [https://news.ycombinator.com/item?id=46934404](https://news.ycombinator.com/item?id=46934404)

[8] 같은 스레드의 답변자 joules77.

[9] 같은 스레드의 다른 답변자 — *하루 6개 프로젝트, 그리고 탈진*.
