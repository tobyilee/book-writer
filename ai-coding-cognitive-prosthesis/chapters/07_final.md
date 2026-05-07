# 7장. Guides + Sensors — 일주일 안에 세울 최소 하네스

6장에서 이름과 짝을 익혔다. 그런데 이름만 쥐고 월요일 아침에 사무실에 앉으면 막상 무엇부터 손대야 할지 막막하다. 두꺼운 청사진 말고 *내일 출근해서 손댈 다섯 가지* 가 있다면, 그 다섯 가지는 어떤 모습이어야 할까.

일주일 안에 세울 최소 하네스 — 다섯 줄로 먼저 적어보자.

1. 저장소 루트에 `AGENTS.md` 한 페이지를 넣는다.
2. lint + format을 CI에 묶는다.
3. PR 템플릿에 *"AI 보조 여부"* 체크박스 한 줄을 추가한다.
4. 핵심 모듈 한두 곳에 ArchUnit 룰을 다섯 줄만 박는다.
5. 주 1회 30분, *"하네스 진단"* 회고를 잡는다.

다섯 줄 안에 6장에서 익힌 두 축이 모두 들어 있다. (1)·(3)은 *Guides* 다 — 행동이 일어나기 *전* 에 방향을 잡아주는 안내. (2)·(4)는 *Sensors* 다 — 행동이 끝난 *뒤* 에 잘못을 짚어주는 피드백. (5)는 둘을 같이 들여다보는 시간이다. 왜 하필 이 다섯인지 — 가이드 축부터 한 칸씩 들여다보자.

## Guides — 피드포워드

가이드의 첫 자리에 굳이 `AGENTS.md` 한 장을 두는 이유가 있다. 2025년 들어 Sourcegraph, OpenAI, Google, Cursor, Factory가 *공동 표준* 으로 합의했고, 곧 Linux Foundation에 위탁되어 *벤더 중립적인* 한 페이지 규약이 됐다.[^1] 30종이 넘는 코딩 에이전트가 이 한 파일만 보면 같은 컨벤션을 따라줄 수 있다는 뜻이다.

찜찜한 구석은 한 군데 있다. Claude Code 자체는 아직 `AGENTS.md` 를 직접 읽지 않고 `CLAUDE.md` 를 본다. 그렇다면 어떻게 해야 할까. 표준 워크어라운드는 한 줄짜리 심볼릭 링크다 — `ln -s AGENTS.md CLAUDE.md`. 한 파일로 두 도구를 동시에 먹인다. 한 번 깔아두면 신경 쓸 일이 없다.

내용은 길게 쓰지 않는 편이 낫다. 한 페이지를 넘기면 모델도, 사람도 끝까지 읽지 않는다. 같이 짜보자.

```markdown
# AGENTS.md

## 프로젝트 개요
- 한 줄 설명, 주요 도메인, 핵심 디렉터리 트리 5줄 이내.

## 빌드·테스트·실행
- `make build` / `make test` / `make run` — 명령은 *복사 가능* 하게.
- 자주 깨지는 명령과 그 이유를 짧게 메모.

## 코딩 컨벤션
- 언어별 포매터·린터 이름과 실행 명령.
- 우리 팀이 *유독* 신경 쓰는 한두 가지 규칙만 (예: "도메인 이벤트는 과거형").

## 금지 사항
- 절대 수정하지 말 것: `migrations/`, `legacy/`.
- 절대 새로 만들지 말 것: 전역 싱글톤, sleep 기반 테스트.

## 모르면 멈춰라
- 위 규칙과 충돌하는 변경이 필요하면 *PR을 열기 전에* 사람에게 묻는다.
```

왜 이렇게 짰을까. 핵심은 *모델이 추측하지 않게* 만드는 것이다. *프로젝트 개요* 와 *빌드·테스트·실행* 은 모델이 가장 먼저 시도해보는 상식의 자리다. 여기를 비워두면 모델이 자기 학습 데이터의 *평균치* 로 짐작해서 움직인다. *금지 사항* 은 더 중요하다. *해야 할 것* 은 무한히 많지만, *하면 안 되는 것* 은 손에 꼽을 수 있다. 짧은 부정형 한 줄이, 긴 권장형 한 페이지보다 행동을 더 잘 잡아준다. 마지막의 *모르면 멈춰라* 는 한 줄이 가장 큰 일을 한다 — 자율성의 한계선을 명시적으로 그어주는 것만으로, 모델은 *맘대로 진행하다가 큰 사고를 내는* 모드에서 *합의 점에서 잠깐 멈추는* 모드로 옮겨간다.

이 한 페이지를 더 잘 채우고 싶다면 1차 자료 세 편을 짝지어 읽는 편이 좋다. HumanLayer의 *Writing a good CLAUDE.md*, Anthropic의 *Effective context engineering for AI agents*, Martin Fowler의 *Context Engineering for Coding Agents* — 세 글이 권하는 항목을 추려보면 일곱 갈래로 묶인다.[^2] 하나, 디렉터리 지도를 주되 *왜 그렇게 나뉘었는지* 한 줄 의도를 같이 적는다. 둘, 빌드·테스트 명령은 *복사해서 그대로 실행 가능한 형태* 로 둔다. 셋, *우리 팀의 특수 어휘* — 도메인 용어와 약어 — 를 작은 사전처럼 정리한다. 넷, *피해야 할 패턴* 을 *해야 할 패턴* 보다 먼저 적는다. 다섯, 외부 의존성과 비밀 키 정책을 *어디서 받아오는지* 만 짚는다. 여섯, *코드 리뷰에서 자주 지적되는 한두 가지* 를 명시적으로 박는다. 일곱, *사람을 호출해야 하는 경계선* — 데이터베이스 스키마 변경, 외부 API 추가 같은 것들 — 을 분명히 그어둔다. 일곱이 다 채워지지 않아도 좋다. 한두 항목부터 채우고, 나머지는 회고 때 한 줄씩 추가해보자.

가이드가 `AGENTS.md` 한 장으로 끝나는 건 아니다. *부트스트랩 스크립트* 는 새 환경에서 의존성을 한 번에 깔아주는 *행동 전 안내* 다. *코드 모드* 는 자주 반복되는 변경을 자동 적용해 모델이 매번 같은 보일러플레이트를 짜지 않게 막아준다. *LSP 통합* 은 모델이 코드를 *문자열* 이 아닌 *심볼* 로 읽게 해, 잘못된 함수 이름을 부르거나 존재하지 않는 메서드를 만들어내는 일을 줄여준다. 셋 다 *행동 전* 의 안내라는 점에서 같은 가족이다. 분량상 한 줄씩만 짚고 넘어가지만, *내가 매번 똑같은 설명을 반복하고 있다* 싶을 때 — 그 자리가 가이드를 한 칸 더 박을 자리다.

## Sensors — 피드백

가이드를 잘 깔아도 모델은 가끔 어긋난다. 그때 어긋남을 *조용한 사고* 로 만들지 않으려면, 행동 *뒤* 를 봐주는 센서가 필요하다. 6장에서 말한 두 어휘를 다시 꺼내자 — *계산형(computational)* 과 *추론형(inferential)*.

계산형 센서는 결정적이고 빠르다. 같은 입력에 같은 출력을 돌려주고, 밀리초에서 수 초 안에 끝난다. 린터, 포매터, 컴파일러, ArchUnit, 단위 테스트, 뮤테이션 테스트 — 모두 계산형이다. 추론형 센서는 의미를 본다. 느리지만 풍부하다. *"이 코드가 우리 컨벤션과 어울리는가"* 같은 질문은 정규식으로 잡히지 않는다. 코드 리뷰 스킬, LLM 기반 정적 분석, 보안 의도 검사 같은 도구가 여기에 속한다. 한쪽은 *사실* 을 말하고, 다른 한쪽은 *의견* 을 말한다.

센서를 깔 때 잊지 말아야 할 원칙이 하나 있다 — *성공은 침묵하고 실패만 노출하라.* 잘 돌아간 항목까지 일일이 체크 표시를 띄우면, 정작 깨진 한 줄이 화면 어딘가에 묻혀버린다. 정보 과부하는 *센서를 더 다는 것* 으로 풀리지 않고, *침묵의 기준선* 을 분명히 잡는 것으로 풀린다. 통과한 검사는 조용히 통과시키고, 실패한 한 줄만 빨갛게 띄우는 편이 바람직하다.

가장 먼저 깔 계산형 센서는 lint와 format을 CI에 묶는 일이다. 두 도구 다 십수 년의 누적이 있고, 새로 배울 것이 거의 없다. 같이 한 번 짜보자.

```yaml
# .github/workflows/lint.yml
name: lint
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npx prettier --check .   # 포맷 어긋난 줄만 빨갛게.
      - run: npx eslint . --max-warnings=0  # 경고 한 줄도 통과 안 시킨다.
```

왜 이렇게 짰을까. 두 가지 의도가 박혀 있다. 첫째, `--check` 와 `--max-warnings=0` 으로 *통과 기준을 0으로 못 박는다.* 0이 아니면 어디까지가 허용인지 사람마다 해석이 갈리고, 그 틈으로 *작은 어긋남* 이 한 주씩 누적된다. 둘째, 출력은 *깨진 줄* 만 보여준다. 100개 파일이 통과하면 화면에 한 줄도 뜨지 않는다. *침묵* 이 *통과의 신호* 가 되도록 둔다. 이 한 줄 원칙이 지켜지면, 빨간 줄 하나가 떴을 때 사람의 시선이 즉시 그쪽으로 간다.

다음 자리는 구조를 봐주는 센서다. 코드가 *문법적으로 맞는가* 가 아니라 *우리가 정한 경계를 지키는가* 를 묻는 자리. ArchUnit이 그 자리에 잘 어울린다. 다섯 줄이면 충분하다.

```java
// src/test/java/.../ArchitectureTest.java
@Test
void domainShouldNotDependOnInfra() {
    noClasses().that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAPackage("..infra..")
        .check(new ClassFileImporter().importPackages("com.acme"));
}
```

이 다섯 줄이 무엇을 막는가. *도메인 코드가 인프라 패키지를 import하는 순간* 빌드를 깬다. 사람이 코드 리뷰에서 *"여기 도메인이 인프라를 알면 안 되지 않나요"* 라고 매번 적는 대신, 빌드가 그 한 줄을 자동으로 짚어준다. 모델에게도 같은 효과가 있다 — 모델이 도메인 안에서 *임시방편* 으로 인프라 클래스를 끌어다 쓰려는 순간, CI가 빨간색을 띄운다. 가이드(`AGENTS.md` 의 *금지 사항*) 와 센서(ArchUnit 룰) 가 같은 규칙을 *말로 한 번, 코드로 한 번* 박아두는 형태다. 같은 규칙을 두 번 박는 게 번거로워 보여도, 한쪽이 무너졌을 때 다른 한쪽이 잡아주는 *이중 안전망* 이 된다.

세 번째 자리에 PR 템플릿의 한 줄이 들어간다 — *"AI 보조 여부 체크박스"*. 계산형도 추론형도 아닌, *사람의 메타데이터* 다. 그런데 이 한 줄이 회고를 가능하게 만든다. 한 달치 PR을 모아놓고 *AI가 손댄 코드* 와 *그렇지 않은 코드* 의 결함률·리뷰 시간을 비교할 수 있게 되는 순간, 그동안 *느낌* 으로 다투던 *AI 효과* 가 *측정 가능한 숫자* 로 바뀐다. 측정이 가능해지면 토론이 짧아진다.

추론형 센서를 한 가지 더 짚고 가자. CHI 2024에서 발표된 *Ivie* 는 IDE 안에서 LLM이 갓 만든 코드 옆에 *닻처럼* 인라인 설명을 붙여주는 도구다.[^3] 흥미로운 발견은 *해석 레이어를 더하면 인지부하가 늘 것* 이라는 직관과 정반대였다는 점이다. 사용자들은 baseline 대비 코드 이해는 좋아지고 산만함은 늘지 않았다 — *"highly useful, low distraction"*. 함의는 묵직하다. *인지부하를 줄이는 길* 은 *AI를 덜 쓰는 게 아니라 AI 출력에 해석 레이어를 더하는 것* 일 수도 있다. 인라인 설명도 *피드백 센서* 의 한 종류다. 다만 이 자리는 추론형이라, 깔기 전에 *우리 팀의 노이즈 내성* 을 한 번 가늠해보는 편이 낫다. 의견이 너무 많이 떠다니면, 그 자체가 새로운 과부하가 된다.

마지막으로 한 단락만 — Educative의 파힘 울 하크(Fahim ul Haq)는 *"trust but verify"* 라는 짧은 어구로 같은 자리를 가리켰다.[^4] *AI가 분포의 중심에는 강하지만 엣지 케이스와 암묵 가정에는 약하다* 는 명제 위에서, 그가 권한 처방은 *작은 테스트 하네스* 였다. 거창한 통합 테스트가 아니라 *그 함수가 진짜로 그 엣지에서도 무너지지 않는지* 를 묻는 짧은 케이스 묶음. 위에서 짠 lint·ArchUnit·체크박스가 모두 같은 가족이다. *암묵 가정을 실행 가능한 진실로 옮긴다* — 그게 센서가 하는 일의 한 줄 요약이다.

다섯 가지를 다 깔았으면, 마지막 한 가지는 도구가 아니라 시간이다. 주 1회 30분, *"하네스 진단"* 회고를 잡는 편이 좋다. *지난주에 모델이 같은 실수를 두 번 이상 했는가? 그 실수는 가이드의 빈칸 때문인가, 센서의 빈칸 때문인가?* 두 질문이면 충분하다. 하네스는 한 번 깔고 끝나는 것이 아니라, 매주 *한 줄씩 자라는* 살아있는 문서다.

이 책의 자동화 리포도 같은 두 센서를 짝으로 쓴다. `style-guardian` 은 챕터 문체를 추론적으로 본다. `epubcheck` 은 EPUB 표준을 결정적으로 본다. 한쪽은 의견을 말하고, 한쪽은 사실을 말한다 — 그 둘이 짝을 이뤄야 한 권의 책이 통과한다.[^5]

도구는 깔았다. 그런데 *사람들이* 여전히 지친다. AGENTS.md를 잘 써놓고, lint를 0으로 못 박고, ArchUnit으로 경계를 지켜도 — 팀 단위에서 무언가가 어긋날 때가 있다. 다음 장에서 같이 *팀 단위 회복 설계* 를 들여다보자.

---

[^1]: AGENTS.md는 2025년 Sourcegraph, OpenAI, Google, Cursor, Factory가 공동으로 합의한 코딩 에이전트용 단일 페이지 규약이며, 이후 Linux Foundation에 위탁되어 벤더 중립적 표준으로 운영되고 있다. CLAUDE.md와의 관계 및 `ln -s AGENTS.md CLAUDE.md` 워크어라운드는 hivetrail의 비교 글에 정리되어 있다. <https://hivetrail.com/blog/agents-md-vs-claude-md-cross-tool-standard>. Claude Code 측 공식 가이드는 <https://code.claude.com/docs/en/best-practices> 참조.

[^2]: 본문의 7항목 체크리스트는 다음 세 글의 권고를 종합한 본문 저자의 정리다. HumanLayer, *Writing a good CLAUDE.md*, <https://www.humanlayer.dev/blog/writing-a-good-claude-md>; Anthropic Engineering, *Effective context engineering for AI agents*, <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>; Martin Fowler, *Context Engineering for Coding Agents*, <https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html>. Computational/Inferential, Guides/Sensors 분류는 6장에서 인용한 Birgitta Böckeler의 *Harness engineering for coding agent users* (<https://martinfowler.com/articles/harness-engineering.html>) 의 어휘를 그대로 따랐다.

[^3]: Litao Yan et al., *Ivie: Lightweight Anchored Explanations of Just-Generated Code*, CHI 2024. ACM DL <https://dl.acm.org/doi/10.1145/3613904.3642239>, arXiv <https://arxiv.org/html/2403.02491>. 본문의 *"highly useful, low distraction"* 평가와 *"인지부하를 줄이는 길은 AI를 덜 쓰는 게 아니라 AI 출력에 해석 레이어를 더하는 것"* 이라는 함의는 이 논문의 lab study 결과를 풀어 옮긴 것이다.

[^4]: Fahim ul Haq, *Trust but verify: A simple test harness for AI-suggested code*, Medium, 2026-02. <https://medium.com/@fahimulhaq/trust-but-verify-a-simple-test-harness-for-ai-suggested-code-aaae491dd284>. *AI는 분포의 중심에 강하지만 엣지 케이스·암묵 가정에 약하다* 는 명제와 *"tiny test harness"* 처방, *"unstated assumptions를 executable truth로 전환"* 표현 모두 이 글에서 가져왔다.

[^5]: 본문에서 짧게 언급한 *style-guardian* / *epubcheck* 짝은 본 책을 만든 자동화 리포 *book-writer* 의 실제 구성이다. 리포 구조와 에이전트·스킬 구성은 6장 각주의 셀프 인용을 참조. <https://github.com/tobyilee/book-writer>.
