# Web Research: 바이브 코딩하는 홈 베이커

수집 목적: 학술 인용이 아닌 "에세이 본문에 녹여 쓸 감각적 디테일·은유·통계·실제 사례"의 카탈로그.

---

## 1. AI 에이전틱 코딩의 워크플로우 변화 (2024~2026)

### 1-1. "vibe coding"이라는 말의 출처
- 2025년 2월 2일, Andrej Karpathy가 X에 올린 트윗에서 "vibe coding"이라는 표현이 처음 등장. 4.5M회 이상 조회. 본인은 "샤워 중 떠오른 생각을 그냥 던졌다(shower of thoughts throwaway tweet)"고 후일 회고. (출처: x.com/karpathy/status/1886192184808149383)
- 원문 핵심 구절(인용 가능):
  > "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists."
  > "I'm building a project or webapp, but it's not really coding — I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works."
- Karpathy는 SuperWhisper로 음성 입력만 하고 키보드는 거의 만지지 않는다고도 적었다. → 에세이 모티프: "코드를 짜지 않는 코더, 말하는 코더."

### 1-2. agentic engineering vs vibe coding 구분
- 2026년 현재 기술 커뮤니티의 통상적 구분: **vibe coding**은 코드 소유권을 AI에 내주는 것이고, **agentic engineering**은 엔지니어 판단을 운전석에 둔 채 AI에게 잡일을 위임하는 것이다. (출처: voitanos.io/blog/vibe-coding-vs-agentic-engineering)
- 본 책에서 차용 가능한 어휘 카드: "맡기는 코딩 / 검수하는 코딩 / 함께 듣는 코딩."

### 1-3. 워크플로우의 실제 변화
- Claude Code: "터미널 우선" 경험. 코드베이스를 읽고, 다중 파일에 걸친 변경을 계획하고, 테스트를 돌리고, 커밋까지 한다. 가장 자율적인 옵션. (출처: builder.io/blog/claude-code, builder.io/blog/cursor-vs-claude-code)
- Cursor: 에디터 안에서 빠른 왕복. 매번 diff를 보고 accept/reject. "fast, tight, control of every change"가 키워드.
- Devin: "위임형". 작업을 정의하고 plan을 승인한 뒤 실행이 끝나면 돌아온다. "define work, approve plan, check back when done." (출처: builder.io/blog/devin-vs-claude-code)
- 통상 패턴: Claude Code로 새 기능 스캐폴드·테스트·복잡한 리팩터를 자율로 돌리고, Cursor로 디테일 편집을 한다.
- 에세이 화면 묘사: "터미널의 회색 배경, 깜빡이는 커서, '⏺'와 함께 5분째 멈춰 있는 진행 표시. 오른쪽 위에 토큰 카운터가 작은 시계처럼 늘어나는 것이 보인다."

### 1-4. 장시간(long-running) 작업과 백그라운드
- Anthropic 자체 문서: "긴 호라이즌 작업이 가능해지면서 며칠/몇 주 걸릴 프로젝트를 몇 시간으로 압축할 수 있게 되었다." (출처: anthropic.com/research/long-running-Claude, anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Claude Code는 sub-agent를 백그라운드로 보낼 수 있고(Ctrl+B), 한 세션에 최대 50개의 스케줄링된 작업을 동시에 돌릴 수 있다. (출처: claudefa.st/blog/guide/agents/async-workflows, mindstudio.ai/blog/claude-code-routines-scheduled-cloud-tasks)
- /loop 같은 native command로 self-referential 루프를 돌리는 패턴이 이미 일반화되었다. (출처: tessl.io/blog/anthropic-adds-routines-to-claude-code-for-scheduled-agent-tasks)
- 본 책에 쓸 수치 카드: 한 작업 단위가 "수 분 ~ 수 시간". 이것이 베이킹의 폴딩 인터벌(30분)·벌크 발효(3~5시간)·콜드 리타드(12~24시간)와 거의 같은 시간 척도다.

### 1-5. 토큰 비용·속도
- Simon Willison은 본인의 일일 Claude Code 토큰 사용을 약 $15~$20 상당으로 추정. 헤비 유저의 표지표. (출처: simonwillison.net/tags/claude-code)
- 2026년 3월, Anthropic은 Claude Code의 사용량 한도가 너무 빨리 소진된다는 비판을 인정. (출처: theregister.com/2026/03/31/anthropic_claude_code_limits)
- 에세이 모티프: "한도가 차가워지는 시간 — 빵이 식는 시간과 닮아 있다."

---

## 2. 무라카미 하루키 에세이 스타일 노트

### 2-1. "small but certain happiness"의 발생
- 1986년 에세이 「랑겔한스섬의 오후」에서 무라카미가 처음 만들어낸 표현. 일본어로 小確幸(쇼카쿠코), 한국어로 "소확행". (출처: en.wiktionary.org/wiki/小確幸, lolo-xinchen.medium.com/小確幸-shōgakkō)
- 본 책에 직접 인용 가능한 그가 든 예시들 — **베이킹 모티프와 직결**:
  - "갓 구워낸 빵을 손으로 뜯어 먹는 것"
  - "서랍 속에 잘 개켜놓은 속옷을 보는 것"
  - "가을 오후의 햇살을 바라보며 브람스 실내악을 듣는 것"
  - "잡지를 읽으며 혼자 맥주를 마시는 것"
- 핵심 구절(인용 후보):
  > "이런 작지만 확실한 행복이 없다면, 인생은 메마른 사막에 지나지 않는다."

### 2-2. 무라카미 에세이 문장의 특징 (외부 비평 종합)
- "짧고 단순한 문장. 문체가 한 차선을 벗어나지 않는다. 천천히 움직이므로 독자가 충분히 음미할 시간을 가진다." (medium.com/@shifasarguru4/haruki-murakami-for-beginners)
- "일상과 구체를 균형 잡아, 평범한 것이 마술적으로 느껴지게 한다. 한 남자가 스파게티를 삶고 있는데 한 통의 전화가 인생을 송두리째 바꾼다 — 식의 장면 구성." (medium 위와 동일)
- "음식, 음악, 일상의 디테일을 굉장히 많이 적는다. 재즈나 클래식을 들으며 파스타나 맥주를 마시는 인물이 자주 나온다. 마술적 사건 한복판에도 이런 디테일이 현실감을 떠받친다." (medium)

### 2-3. The Millions: "Haruki Murakami and the Art of the Day"
- 핵심 통찰: "큰 것(소설을 쓰는 일)을 작은 것(매일 몇 시에 자는가)과 한 자리에 놓는 능력." (themillions.com/2010/05/haruki-murakami-and-the-art-of-the-day)
- 본 책의 구조 원칙으로 채택 가능: AI라는 거대한 변화를 "오븐 예열 220도"라는 사소함과 같은 평면에 둘 것.

### 2-4. 『달리기를 말할 때 내가 하고 싶은 이야기』에서 차용 가능한 문장 장치
- 명상으로서의 루틴: "아무리 평범해 보이는 행동도 충분히 오래 계속하면 명상이 된다." (Goodreads quotes / 다수 출처)
- 멈춤의 미학: "더 쓸 수 있다고 느끼는 바로 그 순간에 멈춘다. 그래야 다음 날의 작업이 매끄럽게 이어진다." → 빵 굽기에도 그대로 적용 가능: 폴딩을 더 할 수 있을 때 멈추는 것, AI 프롬프트를 더 다듬을 수 있을 때 일단 보내는 것.
- 1인칭의 거리감: "달리는 사람들은 대부분 더 오래 살려고 달리는 게 아니라, 사는 동안 충분히 살고 싶어서 달린다."

### 2-5. 본 에세이집에 차용할 수 있는 구체적 장치 7가지
1. **시간으로 호흡하기**: "오전 6시", "10분 후", "1시간이 지났다" 같이 시각·시간으로 단락을 끊는다.
2. **고유명사의 결정성**: 음악·책·요리 이름은 두루뭉술하지 말고 정확히 적는다 (Brahms 6중주, 푸가타, 통밀 30%, Claude Sonnet 등).
3. **자기 객관화의 농담**: "나는 그때 부엌에서 약간 멍청해 보이는 표정으로 서 있었다." 식의 자기 응시.
4. **결론의 비낌**: 큰 깨달음 직전에 다른 디테일로 빠져나간다 — "라디오에서 빌 에반스가 흘러나왔다. 그게 전부였다."
5. **사물에게 마음 주기**: 반죽·노트북·오븐을 인격화하지 않되, 마치 동료처럼 다룬다 — "오븐이 제 할 일을 하고 있었다."
6. **두 평면의 대비**: 한 단락은 부엌, 다음 단락은 책상. 두 공간의 시간이 같이 흐른다.
7. **숫자와 감각의 병치**: "75% 가수율, 끈적함이 손가락에 살짝 묻는다." 식으로 정량과 촉각을 한 줄에 둔다.

---

## 3. 사워도우 굽기 — 본문에 녹일 기술 디테일 30+개

### 3-1. 발효 시간·온도
1. 24°C(74~76°F) 실온에서 벌크 발효는 평균 4시간. (theperfectloaf.com/guides/the-ultimate-guide-to-bread-dough-bulk-fermentation)
2. 일반적 사워도우 벌크 발효 폭: **2시간~5시간**.
3. 도우 온도가 1°C 오를 때마다 발효 속도가 눈에 띄게 빨라진다. 29°C(85°F)를 넘기면 지나치게 빠르다.
4. 벌크가 끝나는 신호: 반죽이 처음보다 20~50% 부피 증가, 표면에 작은 거품, 가장자리가 살짝 돔 모양으로 부푼다.
5. 콜드 리타드(냉장 발효): 36~38°F에서 12~36시간. 더 오래 두면 acetic acid가 강해져 신맛이 깊어진다. (kingarthurbaking.com/recipes/extra-tangy-sourdough-bread-recipe, sourdoughhome.com/retarding-dough-for-flavor-enhancement-and-process-control)
6. 24시간을 넘기면 풍미가 망가지기 시작한다 — "기다림에도 한도가 있다."
7. 호밀(rye)이 4%만 들어가도 벌크 발효가 1~2시간 늘어난다. (thefreshloaf.com 다수 스레드)
8. 호밀 르뱅은 14~16시간, 밀 르뱅은 12시간이 표준 발효 시간.
9. 50% 호밀 사워도우는 73°F(약 23°C)에서 3~4시간이면 충분히 부푼다.

### 3-2. 폴딩과 글루텐
10. Stretch and fold: 30분 간격으로 3세트가 표준. 약한 반죽은 15분 간격으로 시작해 점차 간격을 늘린다. (theperfectloaf.com/how-to-stretch-and-fold-sourdough-bread-dough)
11. "30분"이라는 숫자는 반죽이 긴장을 풀고 다시 펼쳐지기에 정확히 알맞은 시간이다.
12. 가수율 70%는 손에 거의 묻지 않는 매끈함, 78%는 적당한 끈적함, 85%는 손가락 사이로 흘러내릴 정도의 슬랙(slack)함.
13. 고가수율 반죽은 짧은 폴딩(15분 간격)을 초반에 여러 번 반복해 빠르게 강화한다.
14. 오토리즈(autolyse): 물과 밀가루만 섞어 30분~수 시간 두는 휴지. 그 사이 효소가 글루텐의 기초를 자동으로 짠다.

### 3-3. 스코어링(scoring) — 빵에 칼집 내기
15. lame은 프랑스어로 "면도날". 칼날을 안전하게 잡기 위한 손잡이가 달린 도구. (kingarthurbaking.com/blog/2017/08/04/scoring-bread-dough)
16. 곡선 칼날(curved blade)은 "ear"라 부르는 들리는 귀 모양을 만든다. 직선 칼날은 밀 이삭(wheat stalk) 같은 기하학 무늬에 쓴다.
17. ear를 내려면 칼을 표면에 45도 각도로 댄다. 장식 무늬는 90도(수직).
18. 옛 공동 화덕에서는 모든 빵에 자기만의 스코어링이 있었다 — 빵의 서명. (makeitdough.com/sourdough-scoring)
19. 좋은 스코어는 단 한 번의 자신 있는 자국. 망설이면 칼이 끌려 반죽을 찢는다.

### 3-4. 굽기 — 오븐 안의 처음 10분
20. 오븐에 들어간 직후 10~12분 동안 빵은 약 20% 더 부푼다. 이를 oven spring이라 한다. (busbysbakery.com/oven-spring-guide, busbysbakery.com/sourdough-oven-spring)
21. 효모가 마지막 발열을 하며 알코올과 CO2를 폭발적으로 내뿜고, 그것이 글루텐 그물에 갇혀 부피로 변한다.
22. 10~12분이 지나면 수분이 증발하면서 표면이 굳고 crust가 고정된다.
23. 240°C 안팎에서 굽되, 처음 20분은 뚜껑을 덮어(또는 더치 오븐으로) 증기를 가둔다.

### 3-5. 향과 소리
24. crust의 깊은 향은 Maillard 반응의 결과 — 표면이 140°C(280°F)를 넘으면 아미노산과 환원당이 만나 수백 종의 향 분자를 만든다. (bakeryinsider.com/the-biological-and-chemical-drivers-of-bread-aroma, intechopen.com/chapters/89529)
25. 2-acetyl-1-pyrroline이라는 분자가 우리가 "갓 구운 빵 냄새"라 부르는 그 정확한 향이다 — 팝콘이나 크래커에서도 같은 분자가 난다.
26. 사워도우는 pH가 낮아 caramelization이 더 빠르게 일어난다 — 그래서 표면이 더 검붉게, 향이 더 복잡하게 난다.
27. fermentation 과정에서 나는 알코올과 ester는 과일·용제 같은 향을, aldehyde와 ketone은 버터·맥아·풀 같은 향을 만든다.
28. 오븐에서 꺼내자마자 빵은 "노래한다(singing)" — 식으면서 crust가 수축하며 잘게 갈라지는 소리. (foodpairing.com/the-science-behind-the-aroma-of-sourdough, busbysbakery.com)
29. 식는 동안의 작은 crackling은 잘 구워진 빵의 표지. 천으로 덮으면 갇힌 증기가 crust를 즉시 무르게 한다.

### 3-6. 크럼과 마무리
30. 오픈 크럼(open crumb): 큰 구멍이 불규칙하게 퍼진 단면 — 고가수율·잘 발달된 글루텐의 결과. 타이트 크럼(tight crumb): 균일하고 작은 구멍 — 통밀·호밀에 흔하다.
31. 갓 구운 빵은 자르지 말고 적어도 1시간은 식혀야 한다 — crust 안에서 수분이 재분배되며 crumb가 마저 익는다.
32. 사워도우 starter의 정상적인 향은 요거트 같은 시큼함. 아세톤(매니큐어 리무버) 냄새가 나면 굶주린 상태 — 더 자주 먹여달라는 신호다. (sourdougharchive.com/sourdough-starter-smells-like-acetone-fix)

---

## 4. 디지털 노동과 손노동의 문화적 흐름

### 4-1. 팬데믹 사워도우 붐 — 통계
- 2020년 봄, 미국 효모 매출 +457%, 베이킹 파우더 +178%, 밀가루 +155%. (en.wikipedia.org/wiki/Pandemic_baking, bakingbusiness.com/articles/55024)
- 2020년 한 해 r/Sourdough에 16,800명 이상의 사용자가 40,525건의 글을 올렸다. 4~5월에 정점.
- 미국 성인의 37%가 팬데믹 절정기에 집에서 빵을 구웠다고 응답(National Restaurant Association 2020).
- 영국 성인 1/3이 2020년에 처음 빵을 굽기 시작했고, 그중 절반이 25~34세.
- 이유 응답 분포: "마음을 진정시켜준다(46%) / 성취감(42%) / 늘어난 시간을 채워준다(40%)."
- 2024년 NPR 보도: "팬데믹발 사워도우 열풍은 끝나지 않았다." 베이킹 클래스 수요는 2023년 10월 기준으로도 여전히 높음. (npr.org/2024/02/18/1232335116)

### 4-2. Matthew Crawford, Shop Class as Soulcraft
- 핵심 논지: 지식노동만 떠받드는 교육은 "생각과 행동의 분리"라는 잘못된 전제 위에 서 있다. (thenewatlantis.com/publications/shop-class-as-soulcraft)
- 인용 후보:
  > "수공은 종종 컨설팅보다 인지적으로 더 까다롭다. 추상적 규칙으로 환원되지 않기 때문이다."
  > "우리는 우리의 소유물이 어떻게 만들어지는지, 어떻게 작동하는지로부터 소외되어 있다."
- 본 책 모티프: 코드는 점점 더 추상적 규칙으로 위임되어 가는데, 빵 굽기는 끝까지 환원되지 않는 노동으로 남는다.

### 4-3. Cal Newport, Digital Minimalism / Slow Productivity
- 핵심 한 줄: "성공한 디지털 미니멀리스트들은 나쁜 디지털 습관을 끊기 *전에* 자유 시간을 무엇으로 채울지부터 새로 짠다." (calnewport.com/on-digital-minimalism)
- "인간은 깊은 곳에서 craftsman이다. 존재하지 않던 가치 있는 것을 만들 때 우리는 깊이 만족한다." (medium.com/@RationalBadger/my-7-takeaways-from-digital-minimalism)
- 본 책의 입론 근거: "AI가 코드를 짜는 동안 무엇을 할 것인가"라는 질문은 곧 "자유 시간을 무엇으로 채울 것인가"이며, Newport의 처방과 정확히 같은 형태의 질문이다.

### 4-4. cottagecore·craft revival의 부상
- 팬데믹 직후 인스타그램·TikTok에서 사워도우 굽기 영상, "starter 챌린지"가 바이럴 콘텐츠가 되었다. (en.wikipedia.org/wiki/Pandemic_baking)
- 2026년 현재까지도 home baking 관심도는 팬데믹 이전보다 높은 수준 유지.
- 본 책에서 짚을 점: 이 흐름은 단순한 트렌드가 아니라 "스크린 시간을 보충하는 신체 시간"으로서의 의미를 가진다.

---

## 5. 본문 직접 인용 후보 짧은 문구

> "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes... and forget that the code even exists." — Andrej Karpathy, 2025-02-02

> "I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works." — Karpathy, 같은 글

> "이런 작지만 확실한 행복이 없다면, 인생은 메마른 사막에 지나지 않는다." — 무라카미 하루키, 「랑겔한스섬의 오후」 (1986)

> "아무리 평범해 보이는 행동도 충분히 오래 계속하면 명상이 된다." — 무라카미 하루키, 『달리기를 말할 때 내가 하고 싶은 이야기』

> "더 쓸 수 있다고 느끼는 바로 그 순간에 멈춘다." — 무라카미, 같은 책

> "수공은 종종 컨설팅보다 인지적으로 더 까다롭다." — Matthew Crawford, *Shop Class as Soulcraft*

> "성공한 디지털 미니멀리스트는 나쁜 습관을 끊기 전에 자유 시간을 무엇으로 채울지부터 새로 짠다." — Cal Newport, *Digital Minimalism*

> "Loaves sing to you as they crackle whilst cooling." — Sourdough baking lore (Busby's Bakery)

> "Each baker had a signature scoring design so they could identify their loaves in the community oven." — Make It Dough, scoring guide

> "마음을 진정시켜준다 — 46%. 성취감 — 42%. 늘어난 시간을 채워준다 — 40%." — 2020 팬데믹 베이킹 동기 조사

---

## 6. 참고 URL 목록

### AI 코딩
- https://x.com/karpathy/status/1886192184808149383
- https://www.anthropic.com/research/long-running-Claude
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/product/claude-code
- https://code.claude.com/docs/en/best-practices
- https://www.builder.io/blog/claude-code
- https://www.builder.io/blog/cursor-vs-claude-code
- https://www.builder.io/blog/devin-vs-claude-code
- https://claudefa.st/blog/guide/agents/async-workflows
- https://simonwillison.net/tags/claude-code/
- https://www.voitanos.io/blog/vibe-coding-vs-agentic-engineering/
- https://www.coderabbit.ai/blog/a-semantic-history-how-the-term-vibe-coding-went-from-a-tweet-to-prod
- https://www.theregister.com/2026/03/31/anthropic_claude_code_limits/
- https://tessl.io/blog/anthropic-adds-routines-to-claude-code-for-scheduled-agent-tasks/

### 무라카미 하루키
- https://en.wiktionary.org/wiki/%E5%B0%8F%E7%A2%BA%E5%B9%B8
- https://lolo-xinchen.medium.com/%E5%B0%8F%E7%A2%BA%E5%B9%B8-sh%C5%8Dgakk%C5%8D-small-but-certain-happiness-in-life-3990c15bd06a
- https://lithub.com/whats-needed-is-magic-writing-advice-from-haruki-murakami/
- https://themillions.com/2010/05/haruki-murakami-and-the-art-of-the-day.html
- https://www.penguin.co.uk/discover/articles/murakami-writing-process-novelist-as-a-vocation
- https://www.turnerstories.com/blog/2021/7/20/haruki-murakamis-writing-routine-and-running-habits
- https://medium.com/@shifasarguru4/haruki-murakami-for-beginners-aa8cab6cd939
- https://www.goodreads.com/work/quotes/2475030-hashiru-koto-ni-tsuite-kataru-toki-ni-boku-no-katar
- https://quillette.com/2022/11/24/murakami-on-writing/

### 사워도우
- https://www.theperfectloaf.com/guides/the-ultimate-guide-to-bread-dough-bulk-fermentation/
- https://www.theperfectloaf.com/how-to-stretch-and-fold-sourdough-bread-dough/
- https://www.theperfectloaf.com/the-importance-of-dough-temperature-in-baking/
- https://www.theperfectloaf.com/spelt-rye-and-whole-wheat-sourdough-bread/
- https://www.theperfectloaf.com/beginners-sourdough-bread/
- https://www.kingarthurbaking.com/blog/2019/07/22/bulk-fermentation
- https://www.kingarthurbaking.com/recipes/extra-tangy-sourdough-bread-recipe
- https://www.kingarthurbaking.com/blog/2017/08/04/scoring-bread-dough
- https://www.kingarthurbaking.com/blog/2015/10/14/artisan-sourdough-bread-tips-part-2
- https://thesourdoughjourney.com/faq-bulk-fermentation-timing/
- https://thesourdoughjourney.com/faq-scoring/
- https://www.busbysbakery.com/sourdough-oven-spring/
- https://www.busbysbakery.com/oven-spring-guide/
- https://makeitdough.com/sourdough-scoring/
- https://bakeryinsider.com/the-biological-and-chemical-drivers-of-bread-aroma/
- https://www.intechopen.com/chapters/89529
- https://www.foodpairing.com/the-science-behind-the-aroma-of-sourdough/
- https://sourdougharchive.com/sourdough-starter-smells-like-acetone-fix/
- https://breadtopia.com/sourdough-rye-country-bread/

### 디지털 노동·craft·문화
- https://en.wikipedia.org/wiki/Pandemic_baking
- https://www.bakingbusiness.com/articles/55024-baking-boom-of-2020-had-lasting-effect-on-yeast-demand
- https://www.npr.org/2024/02/18/1232335116/the-pandemic-fueled-sourdough-frenzy-isnt-over
- https://www.thenewatlantis.com/publications/shop-class-as-soulcraft
- https://calnewport.com/on-digital-minimalism/
- https://medium.com/@RationalBadger/my-7-takeaways-from-digital-minimalism-by-cal-newport-715ef0115865

---

## 수집 한계
- 한국어 무라카미 평론 원문(『하루키 문학의 풍경』 같은 단행본 내용)에는 검색으로 직접 접근하지 못함. 영어권 비평·인터뷰로 대체.
- "developer 'AI is writing code' boredom waiting hobby" 키워드에서는 직접 일치 글이 검색되지 않았음 — 커뮤니티 리서처가 r/ExperiencedDevs·HN에서 일화를 채워야 한다.
- Tartine Bread의 원본 챕터 인용은 책 내부 텍스트라 웹에서는 단편적으로만 확인. 일반화된 기법 설명만 채택.
