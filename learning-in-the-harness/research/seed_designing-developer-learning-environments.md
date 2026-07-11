![에이전트의 실행 환경만이 아니라, 개발자의 학습 환경도 설계 대상이다](https://image.codex.epril.com/covers/2289c6d6-74bc-434e-9f7b-502a574fa3ac.jpg)

# 에이전트의 실행 환경만이 아니라, 개발자의 학습 환경도 설계 대상이다

developer-skillshuman-ai-collaborationdeliberate-practice

![Toby](/icons/toby-avatar.png)![AI](/icons/ai-avatar.png)

Toby/AI·![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiI+PHJlY3QgeD0iMyIgeT0iNCIgd2lkdGg9IjE4IiBoZWlnaHQ9IjE4IiByeD0iMiIgcnk9IjIiIC8+PGxpbmUgeDE9IjE2IiB5MT0iMiIgeDI9IjE2IiB5Mj0iNiI+PC9saW5lPjxsaW5lIHgxPSI4IiB5MT0iMiIgeDI9IjgiIHkyPSI2Ij48L2xpbmU+PGxpbmUgeDE9IjMiIHkxPSIxMCIgeDI9IjIxIiB5Mj0iMTAiPjwvbGluZT48L3N2Zz4=)Jul 1, 2026·![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiPjwvY2lyY2xlPjxwb2x5bGluZSBwb2ludHM9IjEyIDYgMTIgMTIgMTYgMTQiPjwvcG9seWxpbmU+PC9zdmc+)10min read·![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiI+PHBhdGggZD0iTTEgMTJzNC04IDExLTggMTEgOCAxMSA4LTQgOC0xMSA4LTExLTgtMTEtOHoiIC8+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMyI+PC9jaXJjbGU+PC9zdmc+)607 views[![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTMiIGhlaWdodD0iMTMiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiI+PHBhdGggZD0iTTIxIDE1djRhMiAyIDAgMCAxLTIgMkg1YTIgMiAwIDAgMS0yLTJ2LTQiIC8+PHBvbHlsaW5lIHBvaW50cz0iNyAxMCAxMiAxNSAxNyAxMCI+PC9wb2x5bGluZT48bGluZSB4MT0iMTIiIHkxPSIxNSIgeDI9IjEyIiB5Mj0iMyI+PC9saW5lPjwvc3ZnPg==).md](/api/posts/designing-developer-learning-environments-for-ai-agents/download.md "Markdown 다운로드")

하네스 엔지니어링을 다루면서 나는 줄곧 에이전트 쪽을 바라보고 있었다. 에이전트가 안전하게 달릴 수 있는 실행 환경, maker/checker 루프, 서브 에이전트 오케스트레이션, 컨텍스트 핸드오프. 어떻게 하면 에이전트가 실패로부터 빠르게 피드백을 받고, 검증 가능한 산출물을 내놓게 할 것인가.

그런데 최근 몇 가지 데이터를 들여다보다가 하나의 비대칭이 눈에 들어왔다. 우리는 에이전트의 피드백 루프는 집요하게 설계한다. 컴파일러, 테스트, 린터, 리뷰 에이전트까지 겹겹의 검증 계층을 깔아준다. 반면 그 에이전트의 출력을 최종 승인하는 인간의 역량이 어떻게 형성되고 유지되는지는, 적어도 내가 아는 한 어떤 하네스 설계 문서에도 등장하지 않는다.

이 글의 주장은 하나다. **하네스 엔지니어링의 설계 대상에는 에이전트의 실행 환경뿐 아니라 개발자의 학습 환경이 포함되어야 한다.** 이 주장을 세 단계로 논증하겠다. 첫째, 업계는 이미 '피드백 루프의 품질이 산출물의 품질을 결정한다'는 원리를 에이전트 쪽에 대규모로 적용하고 있다(전제의 확립). 둘째, 같은 원리를 인간 쪽에 적용하지 않았을 때 무슨 일이 벌어지는지 보여주는 실증 데이터가 나오기 시작했다(문제의 실증). 셋째, 따라서 인간의 학습 루프를 하네스의 설계 요소로 편입해야 하며, 그것은 실제로 설계 가능하다(처방).

## 1. 전제: 업계는 이미 '피드백 환경 설계'에 베팅했다

AI 시대의 언어 선택 논쟁을 자세히 들여다보면, 그것은 언어 취향의 문제가 아니라 **피드백 환경 설계의 문제**로 수렴하고 있다.

GitHub Octoverse 2025에서 TypeScript는 Python과 JavaScript를 제치고 처음으로 GitHub 최다 사용 언어가 됐다. 월간 기여자가 전년 대비 66% 늘어난, 10년 만의 가장 큰 언어 순위 변동이다. GitHub이 제시한 해석이 의미심장하다. 타입 언어가 에이전트 보조 코딩을 프로덕션에서 더 신뢰할 수 있게 만든다는 것, 그리고 LLM이 생성한 컴파일 에러의 대부분이 타입 체크 실패였다는 연구가 그 해석을 뒷받침한다는 것이다. 개발자들이 문법이 좋아서 TypeScript로 옮겨간 게 아니다. 타입 시스템이라는 공짜 checker를 에이전트 루프에 끼워 넣기 위해 옮겨간 것이다.

에이전트 인프라 계층의 Rust 수렴도 같은 문법으로 읽힌다. OpenAI는 TypeScript로 만들었던 Codex CLI를 1년도 안 돼 95% Rust로 재작성했고, 에이전트 런타임과 샌드박스를 만드는 팀들이 일제히 Rust를 택하고 있다. 여러 이유(메모리 안전, 샌드박싱, 배포) 중 이 글의 맥락에서 중요한 것은 하나다. borrow checker가 제공하는 촘촘한 컴파일 타임 피드백. 인간에게 Rust 컴파일러의 깐깐함은 마찰이지만, 지치지 않고 무한 재시도하는 에이전트에게 그것은 "이건 틀렸다, 고쳐라"를 밀리초 단위로 돌려주는 무료 검증 오라클이다.

여기서 용어 하나를 정확히 하고 넘어가자. 나는 이것을 에이전트의 '학습 환경'이라고 부르지 않겠다. 에이전트는 세션 안에서 학습하지 않는다. 컴파일러 피드백으로 에이전트가 얻는 것은 학습이 아니라 반복 루프 내의 오류 교정이고, 세션이 끝나면 그 교정의 흔적은 증발한다. 정확한 명칭은 **피드백 환경**이다.

그런데 바로 이 구분이 논지의 핵심 비대칭을 드러낸다. 루프의 반대편에 있는 인간에게는 정반대의 성질이 있다. **인간의 피드백 루프는 세션을 넘어 누적된다.** 오늘 스택 트레이스를 파고든 경험은 3년 뒤의 장애 대응 역량이 된다. 에이전트 쪽 피드백 환경은 아무리 정교해도 산출물 하나의 품질만 높이지만, 인간 쪽 피드백 환경은 경력 전체에 복리로 작용한다. 우리는 증발하는 쪽의 루프는 정교하게 설계하면서, 누적되는 쪽의 루프는 방치하고 있는 셈이다.

방치하면 무슨 일이 생기는가. 이제 데이터를 보자.

## 2. 실증: 인지 작업을 위임하면, 위임한 만큼 배우지 못한다

Anthropic이 발표한 통제 실험을 보자. 개발자들을 두 그룹으로 나눠 낯선 라이브러리로 동일한 코딩 과제를 수행하게 했다. 한쪽은 AI 지원을 받았고, 다른 쪽은 직접 코딩했다. 과제 후 디버깅, 코드 읽기, 개념 이해를 묻는 퀴즈를 봤다. 결과: AI 그룹은 약 2분 빨랐지만 통계적으로 유의하지 않았다. 퀴즈 점수는 AI 그룹 50%, 수동 그룹 67%. 격차가 가장 컸던 영역은 디버깅이었다. 속도는 유의미하게 얻지 못했는데 이해는 확실히 잃었다.

이 연구의 더 중요한 발견은 평균이 아니라 분산에 있다. AI 그룹 내부에서 결과를 가른 것은 상호작용 방식이었다. 개념적 질문을 던지고, 코드와 함께 설명을 요구하고, 자기 이해를 검증하는 용도로 AI를 쓴 개발자들은 65% 이상을 기록했다. 코드 생성을 통째로 위임한 개발자들은 40% 미만이었다. 참고로 가장 *빠른* 패턴은 완전 위임이었고, 그 패턴은 학습을 완전히 희생했다.

**이 근거의 한계부터 정직하게 밝힌다.** 단일 실험이고, 과제는 단기적이며, "낯선 라이브러리를 처음 배우는 상황"이라는 특정 국면을 다뤘다. 연구진 스스로도 상호작용 패턴과 학습 결과 사이의 관계는 상관이지 인과 입증이 아니라고 명시했다. 완전 위임을 택한 사람들이 애초에 학습 동기가 낮았을 가능성도 배제할 수 없다.

그럼에도 이 결과를 진지하게 받아야 할 이유가 두 가지 있다. 첫째, 결과가 학습과학의 확립된 원리와 정확히 합치한다. 생성 효과(generation effect) — 스스로 답을 생성하려 애쓴 뒤 확인하면 학습이 일어나고, 답을 먼저 받아버리면 일어나지 않는다 — 는 수십 년간 재현된 견고한 발견이며, 이 실험은 그 원리가 AI 코딩 국면에서도 작동함을 보여주는 하나의 사례로 읽는 것이 가장 보수적인 해석이다. 둘째, 격차가 가장 컸던 영역이 하필 디버깅이라는 점이다. 디버깅은 코드가 왜 그렇게 동작하는지에 대한 인과 모델을 요구하는 활동이고, 인과 모델은 정확히 '스스로 생성해 본 경험'에서 나온다. 다시 말해 이 결과는 우연한 패턴이 아니라 이론이 예측하는 바로 그 자리에서 나왔다.

내가 전에 '역량의 착각(illusion of competence)'이라 불렀던 현상이 이것이다. AI가 만든 코드가 술술 읽히니까 내가 그것을 만들 수 있다고 착각한다. 읽어서 이해되는 것과 백지에서 생성할 수 있는 것의 간극은 평소에는 보이지 않다가, 스택 트레이스가 떨어지는 새벽 2시에 드러난다.

노동 시장 데이터도 짧게 언급해 둔다. Stanford의 급여 데이터 분석에 따르면 22~25세 개발자 고용은 2022년 말 이후 20% 가까이 감소한 반면 26세 이상은 유지되거나 늘었다. 시기가 AI 코딩 도구의 대중화와 겹치지만, 금리 인상과 팬데믹기 과잉 채용의 되돌림 같은 교란 변수가 있어 인과를 단정할 수는 없다. 이 데이터에서 내가 취하는 것은 인과 주장이 아니라 위험 구조다. 원인이 무엇이든 신입의 협상 지위는 이미 약해졌고, 그런 환경에서 역량 성장까지 실패하면 그것은 '성장이 느려지는 것'이 아니라 "당신은 AI보다 나은 판단을 제공하는가"라는 질문에 답하지 못하게 되는 것이다. 하방이 깊을수록 학습이라는 보험의 가치는 커진다.

## 3. 논지: 인간의 학습 루프는 하네스의 설계 요소다

이제 두 절을 연결하자. 1절의 교훈은 피드백 루프의 품질이 산출물의 품질을 결정하며, 업계는 이 원리를 에이전트 쪽에 이미 대규모로 적용하고 있다는 것이다. 2절의 교훈은 인간 쪽 루프를 방치하면 — 정확히는 인지 작업의 소유권을 무분별하게 넘기면 — 역량 형성이 실제로 손상된다는 것이다.

이 둘을 잇는 마지막 고리는 이 질문이다. 인간의 역량이 손상되면, 하네스에는 무슨 문제가 생기는가.

maker/checker 구조에서 검증이 생성보다 쉬운 경우는 많다. 테스트가 그 증거이고, 그래서 이 구조가 성립한다. 컴파일 가능성, 테스트 통과, 린트 규칙 — 형식화할 수 있는 속성은 기계 checker에게 맡기면 되고, 인간이 그보다 잘할 이유도 없다. 문제는 형식화되지 않는 속성들이다. 이 추상화가 도메인에 맞는가. 이 경계 설정이 6개월 뒤의 변경을 감당하는가. 이 코드가 우리 팀이 유지보수할 수 있는 물건인가. 이런 속성의 검증은 체크리스트로 환원되지 않고, 유사한 것을 만들어 보고 실패해 본 경험에서 오는 판단력을 요구한다. 하네스의 기계 검증 계층이 아무리 두꺼워져도 이 판단은 남고, 이것이 인간이 루프에서 맡는 마지막 직무다.

그렇다면 그림이 이렇게 그려진다. 하네스의 최종 품질 게이트는 인간의 판단력이다. 그런데 2절의 데이터가 시사하듯, 그 하네스 안에서 일하는 기본 방식(완전 위임)이 판단력의 원료인 생성 경험을 고갈시킨다. 엄밀히 말하면 Anthropic 실험은 학습 과제 상황이었고 실무 하네스에서의 장기 침식을 직접 측정한 것은 아니다 — 이것은 외삽이다. 그러나 방향을 의심할 이유는 없다. 실무는 실험보다 마감 압박이 크고, 마감 압박은 정확히 가장 빠른 패턴, 즉 완전 위임 쪽으로 사람을 민다. **시스템이 자신의 최종 품질 게이트를 마모시키는 기본값 위에 서 있다면, 그것은 개인의 의지 문제가 아니라 설계 결함이다.** 그리고 설계 결함은 설계로 고친다.

여기서 예상되는 가장 강한 반론을 정면으로 받자. **"모델이 계속 좋아지면 인간 검증 자체가 불필요해지는 것 아닌가. 사라질 역량을 왜 기르는가."** 세 가지로 답하겠다. 첫째, 이 반론이 옳더라도 시점 문제가 남는다. '인간 검증이 불필요해지는 시점'이 언제인지 아무도 모르는 상황에서, 그 시점 전까지 검증 역량 없이 일하는 것은 도착 시각을 모르는 채 낙하산 없이 뛰어내리는 것이다. 둘째, 역량의 내용은 바뀌어도 구조는 남는다. 어셈블리 디버깅은 사라졌지만 '시스템의 인과 모델을 세우고 가설을 검증하는 능력'은 계층을 옮겨가며 살아남았다. AI가 코드 계층을 흡수하면 판단은 설계와 스펙 계층으로 올라가는데, 상위 계층의 판단력은 하위 계층을 겪어본 경험 위에 서는 경향이 있다. 셋째, 이 반론은 조직 관점에서만 성립한다. "인간 검증이 불필요해진다"가 참이 되는 세계에서 손해 보는 것은 정확히 역량을 기르지 않은 개인이다. 반론이 맞을수록, 개인에게는 남는 역량을 길러둘 유인이 커진다.

## 4. 처방: 학습 루프를 하네스에 설계해 넣기

처방은 세 겹이고, 각 겹은 2절의 근거에 대응한다.

### 4-1. 흐름 안에서: 기본 상호작용 모드를 바꾼다

Anthropic 연구에서 학습 결과를 가른 변수는 'AI 사용량'이 아니라 '상호작용 패턴'이었다. 그렇다면 첫 번째 개입 지점은 별도의 학습 시간이 아니라 일하는 방식의 기본값이다. 다음 패턴들은 모두 같은 원리 — 인지 작업의 첫 시도를 인간이 소유한다 — 의 변주이며, 추가 시간이 거의 들지 않는다.

- **선(先)설계, 후(後)생성.** 코드를 받기 전에 내 접근을 한 문단으로 먼저 쓰고, 에이전트의 결과와 비교한다. 생성 효과를 확보하는 가장 싼 방법이다.
- **실행 전 예측.** 생성된 코드를 돌리기 전에 동작을 예측하고 확인한다. 예측이 틀린 지점이 정확히 내 멘탈 모델의 구멍이며, 학습과학에서 예측 오류는 가장 강한 학습 신호 중 하나다.
- **설명 동봉 요구.** "왜 이 방식인지, 어떤 대안을 기각했는지"를 함께 받는다. 연구에서 높은 점수를 낸 집단의 패턴이 정확히 이것이었다.
- **설명 가능성 게이트.** diff를 승인하기 전에 자문한다. 이 코드를 동료에게 설명할 수 있는가. 못 하면 아직 승인할 자격이 없는 것이다.

이 패턴들의 장점은 하네스에 직접 인코딩할 수 있다는 것이다. CLAUDE.md의 규칙으로, 훅으로, 커스텀 커맨드로. 예컨대 인간이 테스트(스펙)를 쓰고 에이전트가 구현하는 분업은 생산성과 학습을 동시에 확보하는 구조인데, 실패 조건을 정의하는 행위가 도메인에 대한 생성적 사고를 강제하기 때문이다. TDD Red-Green-Refactor 에이전트 팀에서 Red를 인간이 소유하는 것은 품질 장치인 동시에 학습 장치다.

### 4-2. 흐름 밖에서: 취약 지점을 겨냥한 AI-오프 의도적 연습

상호작용 패턴 개선만으로 충분한가. 아니다. 데이터가 최대 격차 지점으로 지목한 디버깅은 승인 루프 안에서 충분히 훈련되지 않는 활동이다. 잘 돌아가는 코드를 검토하는 일과 무너진 시스템에서 원인을 추적하는 일은 다른 근육을 쓴다. 그래서 두 번째 겹은 흐름 밖의 의도적 연습(deliberate practice)인데, 방점은 '수동 코딩 일반'이 아니라 '표적화'에 있다. 데이터가 짚어준 취약 지점에 집중한다.

- AI 없이 버그를 잡는다. 스택 트레이스만 들고 원인까지 걸어 내려간다.
- 에이전트가 만든 코드를 일부러 깨뜨리고, 어디가 어떻게 무너지는지 관찰한다.
- 작은 모듈 하나를 백지에서 구현한 뒤 에이전트 버전과 비교한다. 차이가 나는 지점이 배울 지점이다.

지게차가 있어도 코어 근육은 따로 기른다. 다만 하루 종일 맨손으로 짐을 나르라는 얘기가 아니다. 필요한 것은 총량이 아니라 규칙성과 표적이다. 분량은 각자의 취약 지점에 따라 다르겠지만, 캘린더에 박제된 짧은 블록이 '언젠가 하겠다'는 다짐보다 낫다는 것만은 분명하다.

### 4-3. 메타 계층: 위임 다이얼을 영역별로 다르게 놓는다

여기서 상충하는 근거 하나를 정직하게 다뤄야 한다. CHI 2023에 실린 연구에서는 입문 학습자에게 AI 코드 생성기가 좌절을 줄이고 수행을 높이면서도, 이후 AI 없는 상황에서의 수행이나 수동 코드 수정 능력을 저하시키지 않았다. AI가 학습의 스캐폴딩이 될 수 있다는 결과다. Anthropic 연구와 정반대처럼 보인다.

그러나 두 연구는 조건이 다르다. 대상(입문 학습자 vs 현업 개발자), 도구 세대(제안을 보여주는 코드 생성기 vs 통째로 위임 가능한 에이전트), 과제 맥락(교육 환경 vs 업무형 과제). 이 차이들을 관통하는 가장 그럴듯한 해석은 이렇다. **도구가 해로운 것이 아니라, 이해를 건너뛴 수용이 기본값으로 굳는 국면이 해롭다.** CHI 연구의 환경은 학습자가 코드를 읽고 수정하도록 구조화되어 있었고, Anthropic 연구의 저성과 집단은 그 구조 없이 완전 위임을 선택할 수 있었다. 같은 도구라도 수용 방식이 구조화되어 있는가가 갈림길이라는 것이다.

이 해석이 맞다면 처방은 금지도 방임도 아닌 다이얼이다. 새 도메인, 새 언어, 새 아키텍처 — 내 멘탈 모델이 아직 없는 영역에서는 위임 비율을 의도적으로 낮추고 설명과 직접 작성 중심으로 간다. 이미 숙달한 영역에서는 공격적으로 위임해 속도를 뽑는다. 다이얼의 손잡이는 하나의 질문이다. "나는 지금 생산 모드인가, 학습 모드인가." 이 메타 인지가 앞의 두 겹을 하나로 묶는다.

## 맺으며: 설계 대상의 확장

논증을 요약한다. 피드백 루프의 품질이 산출물의 품질을 결정한다는 원리를, 업계는 에이전트 쪽에 이미 대규모로 적용했다(1절). 같은 원리를 인간 쪽에 적용하지 않은 채 인지 작업을 통째로 위임하면 역량 형성이 손상된다는 실증 신호가 나왔고, 그 신호는 학습과학의 확립된 원리가 예측하는 자리에서 정확히 나왔다(2절). 하네스의 최종 품질 게이트는 형식화되지 않는 속성을 판단하는 인간의 역량인데, 하네스의 기본 작업 방식이 그 역량의 원료를 고갈시킨다면 이는 설계 결함이다(3절). 따라서 상호작용 패턴, 표적 연습, 위임 다이얼이라는 세 겹의 학습 루프를 하네스에 명시적으로 설계해 넣어야 한다(4절).

AI 시대의 개발자에게 위험한 것은 코드를 안 쓰는 것이 아니라 생각을 안 하는 것이고, 역량의 성장을 결정하는 것은 투입 시간이 아니라 인지 작업의 소유권이다. 하네스 엔지니어링을 나는 에이전트가 잘 달리는 트랙을 까는 일이라고 생각해 왔다. 그러나 트랙 위를 달리는 것은 에이전트만이 아니다. 그 옆에서 최종 판단을 내리는 인간이 있고, 에이전트의 루프는 세션과 함께 증발하지만 인간의 루프는 경력에 복리로 쌓인다. 좋은 하네스는 좋은 코드를 뽑아내는 환경이면서, 동시에 좋은 엔지니어를 길러내는 환경이어야 한다.

------------------------------------------------------------------------

*참고 자료*

- Anthropic, "How AI assistance impacts the formation of coding skills" — [https://www.anthropic.com/research/AI-assistance-coding-skills](https://www.anthropic.com/research/AI-assistance-coding-skills)
- InfoQ, "Anthropic Study: AI Coding Assistance Reduces Developer Skill Mastery by 17%" — [https://www.infoq.com/news/2026/02/ai-coding-skill-formation/](https://www.infoq.com/news/2026/02/ai-coding-skill-formation/)
- GitHub, "Octoverse 2025" — [https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- InfoQ, "Another Rust Rewrite: OpenAI's Codex CLI Goes Native" — [https://www.infoq.com/news/2025/06/codex-cli-rust-native-rewrite/](https://www.infoq.com/news/2025/06/codex-cli-rust-native-rewrite/)
- Kazemitabaar et al., "Studying the Effect of AI Code Generators on Supporting Novice Learners in Introductory Programming" (CHI 2023) — [https://dl.acm.org/doi/10.1145/3544548.3580919](https://dl.acm.org/doi/10.1145/3544548.3580919)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiI+PHBhdGggZD0iTTE0IDlWNWEzIDMgMCAwIDAtMy0zbC00IDl2MTFoMTEuMjhhMiAyIDAgMCAwIDItMS43bDEuMzgtOWEyIDIgMCAwIDAtMi0yLjN6TTcgMjJINGEyIDIgMCAwIDEtMi0ydi03YTIgMiAwIDAgMSAyLTJoMyIgLz48L3N2Zz4=)3 Likes

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0iY3VycmVudENvbG9yIj48cGF0aCBkPSJNMTguMjQ0IDIuMjVoMy4zMDhsLTcuMjI3IDguMjYgOC41MDIgMTEuMjRIMTYuMTdsLTQuNzE0LTYuMjMxLTUuNDAxIDYuMjMxSDIuNzQ4bDcuNzMtOC44MzVMMS4yNTQgMi4yNUg4LjA4bDQuMjU5IDUuNjN6bS0xLjE2MSAxNy41MmgxLjgzM0w3LjA4NCA0LjEyNkg1LjExN3oiIC8+PC9zdmc+)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0iY3VycmVudENvbG9yIj48cGF0aCBkPSJNMjQgMTIuMDczYzAtNi42MjctNS4zNzMtMTItMTItMTJzLTEyIDUuMzczLTEyIDEyYzAgNS45OSA0LjM4OCAxMC45NTQgMTAuMTI1IDExLjg1NHYtOC4zODVINy4wNzh2LTMuNDdoMy4wNDdWOS40M2MwLTMuMDA3IDEuNzkyLTQuNjY5IDQuNTMzLTQuNjY5IDEuMzEyIDAgMi42ODYuMjM1IDIuNjg2LjIzNXYyLjk1M0gxNS44M2MtMS40OTEgMC0xLjk1Ni45MjUtMS45NTYgMS44NzR2Mi4yNWgzLjMyOGwtLjUzMiAzLjQ3aC0yLjc5NnY4LjM4NUMxOS42MTIgMjMuMDI3IDI0IDE4LjA2MiAyNCAxMi4wNzN6IiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0iY3VycmVudENvbG9yIj48cGF0aCBkPSJNMjAuNDQ3IDIwLjQ1MmgtMy41NTR2LTUuNTY5YzAtMS4zMjgtLjAyNy0zLjAzNy0xLjg1Mi0zLjAzNy0xLjg1MyAwLTIuMTM2IDEuNDQ1LTIuMTM2IDIuOTM5djUuNjY3SDkuMzUxVjloMy40MTR2MS41NjFoLjA0NmMuNDc3LS45IDEuNjM3LTEuODUgMy4zNy0xLjg1IDMuNjAxIDAgNC4yNjcgMi4zNyA0LjI2NyA1LjQ1NXY2LjI4NnpNNS4zMzcgNy40MzNhMi4wNjIgMi4wNjIgMCAwMS0yLjA2My0yLjA2NSAyLjA2NCAyLjA2NCAwIDExMi4wNjMgMi4wNjV6bTEuNzgyIDEzLjAxOUgzLjU1NVY5aDMuNTY0djExLjQ1MnpNMjIuMjI1IDBIMS43NzFDLjc5MiAwIDAgLjc3NCAwIDEuNzI5djIwLjU0MkMwIDIzLjIyNy43OTIgMjQgMS43NzEgMjRoMjAuNDUxQzIzLjIgMjQgMjQgMjMuMjI3IDI0IDIyLjI3MVYxLjcyOUMyNCAuNzc0IDIzLjIgMCAyMi4yMjIgMGguMDAzeiIgLz48L3N2Zz4=)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0iY3VycmVudENvbG9yIj48cGF0aCBkPSJNMTEuOTQ0IDBBMTIgMTIgMCAwMDAgMTJhMTIgMTIgMCAwMDEyIDEyIDEyIDEyIDAgMDAxMi0xMkExMiAxMiAwIDAwMTIgMGgtLjA1NnptNC45NjIgNy4yMjRjLjEtLjAwMi4zMjEuMDIzLjQ2NS4xNGEuNTA2LjUwNiAwIDAxLjE3MS4zMjVjLjAxNi4wOTMuMDM2LjMwNi4wMi40NzItLjE4IDEuODk4LS45NjIgNi41MDItMS4zNiA4LjYyNy0uMTY4LjktLjQ5OSAxLjIwMS0uODIgMS4yMy0uNjk2LjA2NS0xLjIyNS0uNDYtMS45LS45MDItMS4wNTYtLjY5My0xLjY1My0xLjEyNC0yLjY3OC0xLjgtMS4xODUtLjc4LS40MTctMS4yMS4yNTgtMS45MS4xNzctLjE4NCAzLjI0Ny0yLjk3NyAzLjMwNy0zLjIzLjAwNy0uMDMyLjAxNC0uMTUtLjA1Ni0uMjEycy0uMTc0LS4wNDEtLjI0OS0uMDI0Yy0uMTA2LjAyNC0xLjc5MyAxLjE0LTUuMDYxIDMuMzQ1LS40NzkuMzMtLjkxMy40OS0xLjMwMi40OC0uNDI4LS4wMDgtMS4yNTItLjI0MS0xLjg2NS0uNDQtLjc1Mi0uMjQ1LTEuMzQ5LS4zNzQtMS4yOTctLjc4OS4wMjctLjIxNi4zMjUtLjQzNy44OTMtLjY2MyAzLjQ5OC0xLjUyNCA1LjgzLTIuNTI5IDYuOTk4LTMuMDE0IDMuMzMyLTEuMzg2IDQuMDI1LTEuNjI3IDQuNDc2LTEuNjM1eiIgLz48L3N2Zz4=)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiI+PHBhdGggZD0iTTEwIDEzYTUgNSAwIDAgMCA3LjU0LjU0bDMtM2E1IDUgMCAwIDAtNy4wNy03LjA3bC0xLjcyIDEuNzEiIC8+PHBhdGggZD0iTTE0IDExYTUgNSAwIDAgMC03LjU0LS41NGwtMyAzYTUgNSAwIDAgMCA3LjA3IDcuMDdsMS43MS0xLjcxIiAvPjwvc3ZnPg==)Link

Tags:[\#developer-skills](/tag/developer-skills)[\#human-ai-collaboration](/tag/human-ai-collaboration)[\#deliberate-practice](/tag/deliberate-practice)

## 댓글

불러오는 중...

Subscribe

### 새 글을 이메일로 받아보세요

새로운 블로그 포스트나 위키 페이지가 게시되면 알려드립니다. 스팸 없이, 가치 있는 콘텐츠만 전달합니다.

구독하기

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ2YXIoLS1jb2xvci1hY2NlbnQpIiBzdHJva2Utd2lkdGg9IjIiPjxsaW5lIHgxPSI4IiB5MT0iNiIgeDI9IjIxIiB5Mj0iNiI+PC9saW5lPjxsaW5lIHgxPSI4IiB5MT0iMTIiIHgyPSIyMSIgeTI9IjEyIj48L2xpbmU+PGxpbmUgeDE9IjgiIHkxPSIxOCIgeDI9IjIxIiB5Mj0iMTgiPjwvbGluZT48bGluZSB4MT0iMyIgeTE9IjYiIHgyPSIzLjAxIiB5Mj0iNiI+PC9saW5lPjxsaW5lIHgxPSIzIiB5MT0iMTIiIHgyPSIzLjAxIiB5Mj0iMTIiPjwvbGluZT48bGluZSB4MT0iMyIgeTE9IjE4IiB4Mj0iMy4wMSIgeTI9IjE4Ij48L2xpbmU+PC9zdmc+)목차

- [1. 전제: 업계는 이미 '피드백 환경 설계'에 베팅했다](#1-전제-업계는-이미-피드백-환경-설계-에-베팅했다)
- [2. 실증: 인지 작업을 위임하면, 위임한 만큼 배우지 못한다](#2-실증-인지-작업을-위임하면-위임한-만큼-배우지-못한다)
- [3. 논지: 인간의 학습 루프는 하네스의 설계 요소다](#3-논지-인간의-학습-루프는-하네스의-설계-요소다)
- [4. 처방: 학습 루프를 하네스에 설계해 넣기](#4-처방-학습-루프를-하네스에-설계해-넣기)
- [4-1. 흐름 안에서: 기본 상호작용 모드를 바꾼다](#4-1-흐름-안에서-기본-상호작용-모드를-바꾼다)
- [4-2. 흐름 밖에서: 취약 지점을 겨냥한 AI-오프 의도적 연습](#4-2-흐름-밖에서-취약-지점을-겨냥한-ai-오프-의도적-연습)
- [4-3. 메타 계층: 위임 다이얼을 영역별로 다르게 놓는다](#4-3-메타-계층-위임-다이얼을-영역별로-다르게-놓는다)
- [맺으며: 설계 대상의 확장](#맺으며-설계-대상의-확장)
