# 1부. 패러다임의 전환 — 프롬프트에서 하네스로

> **부 인트로**

2026년 봄. 같은 결론을 외친 다섯 명의 목소리가 거의 동시에 도착했다.

2월, 미첼 하시모토(Mitchell Hashimoto)가 *My AI Adoption Journey*를 올렸다.[^hashimoto] HashiCorp 창업자이자 Terraform·Vault의 설계자인 그가, 자기가 어떻게 챗봇을 버리고 에이전트로 옮겨갔는지를 6단계로 정리한 글이다. 같은 달, OpenAI의 하네스 엔지니어링 팀이 *Harness engineering: leveraging Codex in an agent-first world*를 발표했다.[^openai-harness] 5개월간 100만 줄, 1,500개의 PR을 — *사람이 코드 한 줄도 안 쓰고* — 출하한 이야기였다. 그 한 달 전, 애디 오스마니(Addy Osmani)는 *Agent Harness Engineering*에서 한 문장을 박아 넣었다.[^osmani]

> "Agent = Model + Harness. If you're not the model, you're the harness."
>
> *에이전트 = 모델 + 하네스. 당신이 모델을 만드는 사람이 아니라면, 당신이 하는 일은 모두 하네스 엔지니어링이다.*

3월에는 Anthropic이 3-에이전트 하네스 사례를 공개했고[^anthropic-harness2], 4월에는 비르기타 뵈켈러(Birgitta Böckeler)가 Thoughtworks 사이트에 *Harness engineering for coding agent users*를 올려 Guides·Sensors 프레임워크를 결정판으로 정리했다.[^bockeler-main]

다섯 진영이 — 인디 블로거, 인프라 거장, 두 곳의 1차 모델 벤더, 컨설턴시의 거물 — 같은 시기에 같은 단어를 골랐다. 우연일까? 그렇지 않다. 우리가 마주한 문제가 같았기 때문이다.

문제는 이것이다. AGENTS.md를 백 줄 써도 에이전트는 같은 실수를 반복한다. Cursor를 켜고 Claude Code도 깔고 Codex CLI까지 써 봤지만, *왜* 어떤 줄은 효과가 있고 어떤 줄은 무시되는지 알 수가 없다. 모델 버전을 올렸더니 어떤 작업은 더 잘하는데 어떤 작업은 오히려 후퇴한다. 그래서 짜증을 내며 프롬프트를 다시 고친다. 다시 고치면 한 번은 잘 된다. 다음 날, 다시 같은 실수다.

이 책은 그 자리에서 시작한다. 그리고 1부는 그 자리에서 *왜 우리가 여기에 와 있는지*를 본다. 다섯 사람의 합의가 어떻게 만들어졌는지, 우리는 그 지도 위 어디에 서 있는지, 그리고 평가와 운영이 같은 마구를 쓴다는 사실을 받아들이는 데서부터 출발한다.

1부는 거울이다. 1장에서 산업이 합의한 정의를 받아들이고, 2장에서 자기 단계를 솔직하게 짚는다. 3장에서 평가 하네스와 런타임 하네스가 동형(同形)임을 본다. 4장에서 같은 모델이 다른 하네스 위에서 왜 다른 점수를 받는지를 Terminal-Bench 2.0으로 확인한다.

여기서 책 전체의 좌표계가 정해진다. 좌표가 잡히면, 그 다음은 척추를 세우는 일이다. 2부가 그 일을 한다. 일단 1부를 함께 걸어 보자.

[^hashimoto]: Mitchell Hashimoto, *My AI Adoption Journey*, 2026-02. https://mitchellh.com/writing/my-ai-adoption-journey
[^osmani]: Addy Osmani, *Agent Harness Engineering*. https://addyosmani.com/blog/agent-harness-engineering/
[^openai-harness]: OpenAI, *Harness engineering: leveraging Codex in an agent-first world*, 2026-02. https://openai.com/index/harness-engineering/
[^anthropic-harness2]: Anthropic Engineering, *Harness design for long-running application development*, 2026-03.
[^bockeler-main]: Birgitta Böckeler, *Harness engineering for coding agent users*, martinfowler.com, 2026-04.
