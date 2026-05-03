# JVM 출신을 위한 Pythonic

> 정적 타입 사고로 풀어내는 Python 3.14, uv, FastAPI, AI Agent 바이블

**저자:** Toby-AI · **버전:** 1.0.0 · **출간:** 2026-05-03 · **언어:** 한국어

---

## 한 줄 소개 (logline)

JVM 시니어가 *문법 비교가 아니라 사고 전환*으로 Python을 본격적으로 익혀, 언어 본질부터 AI Agent까지 한 권에 도달하는 가장 빠른 길.

---

## 이 책이 누구에게 필요한가

Java/Kotlin/Spring으로 5~15년 넘게 코드를 짜온 시니어 개발자. 정적 타입과 JVM 사고에 익숙하지만 Python은 처음이거나 단편적으로만 써봤고, AI/LLM·Agent·웹 백엔드·유틸리티 스크립트를 *제대로* Python으로 만들어보고 싶은 사람. *입문서*와 *AI 책*과 *FastAPI 책*을 따로 사야 했던 시니어가 한 권으로 끝낸다.

---

## 이 책의 핵심 약속 3가지

1. **JVM 멘탈 모델을 자산으로 인정한다.** 단순 문법 비교표가 아니라 *Spring에서 익혔던 직관 중 무엇을 그대로 쓰고 무엇을 폐기해야 하는가*를 매 챕터에 새긴다.
2. **2026년 5월 시점의 가장 최신 stack으로만 짠다.** Python 3.13/3.14, uv 단독, Pydantic v2, SQLAlchemy 2.x async, Anthropic SDK 0.42+, MCP 2025-11. 옛 Poetry/pip-tools/requirements.txt 흔적이 없다.
3. **언어부터 AI Agent까지 한 권에서 끝낸다.** 22개 챕터에 걸쳐 같은 러닝 예제(Snippet Hub)가 자라며 *언어 본질 → 환경 → 정적 사고 → 도메인별 실전 → 웹 백엔드 → AI/Agent*까지 흘러간다.

---

## 차례

### Part I — 전환 (1~2장)
JVM에서 건너오는 다리를 놓는다.
1. 왜 다시 Python인가 — 2026년의 지형도
2. JVM 시니어가 Python에서 흔들리는 6개 축

### Part II — 환경과 도구 (3~4장)
uv 한 도구로 첫날을 끝낸다.

3. uv 단독 — 패키징 헬을 끝낸다
4. 시니어의 첫날 책상 — PyCharm/VSCode + mypy + ruff

### Part III — 언어 본질 (5~7장)
Python을 Python답게 쓴다.

5. 객체와 이름 바인딩 — Python의 *모든 것이 객체다*
6. 함수와 함수형 도구 — comprehension, generator, itertools, functools
7. 클래스, dataclass, dunder, Protocol — Python식 OOP

### Part IV — 정적 사고와 표준 라이브러리 (8~10장)
Java보다 Python이 더 안전할 수 있다.

8. 타입 시스템 — gradual typing, Protocol, 새 generics(PEP 695/696/742)
9. 값 객체의 세 갈래 — dataclass, attrs, Pydantic의 사용처
10. 표준 라이브러리의 무기고 — pathlib, contextlib, logging, datetime, json/tomllib

### Part V — 도메인별 실전 (11~13장)
Python으로 일을 처리한다.

11. CLI 도구 만들기 — Typer, Rich, subprocess, uv tool
12. 알고리즘과 자료구조 — collections, heapq, deque, bisect
13. 동시성 — asyncio, threading, multiprocessing, free-threaded

### Part VI — 웹 백엔드 (14~17장)
Spring 출신이 짤 수 있는 가장 좋은 FastAPI.

14. FastAPI 입문 — Spring 출신을 위한 첫 라우터
15. SQLAlchemy 2.x async + Alembic — Spring Data 출신의 새 ORM
16. 인증·미들웨어·검증 그리고 pytest 전략 (16A + 16B 분리)
17. 운영의 완성 — Docker, Gunicorn, OTel, structlog, GitHub Actions

### Part VII — AI 시대 (18~22장)
LLM과 Agent를 시니어 백엔드답게 다룬다.

18. LLM SDK 기초 — Anthropic / OpenAI 두 길
19. Prompt caching, structured output, tool use — Pydantic으로 단단한 LLM 통합
20. AI Agent 직접 구현 — ReAct를 while 루프로
21. MCP — 에이전트가 *세상에 닿는* 표준 프로토콜
22. 멀티 에이전트와 통합 — LangGraph / PydanticAI 그리고 책의 마무리 (22A + 22B 분리)

### 부록
- 부록 A — Java/Kotlin → Python 치트시트 (100항목)
- 부록 B — uv 명령어 레퍼런스 (전 서브커맨드 + pyproject 스키마)
- 부록 C — Python 표준 라이브러리 핵심 100선
- 부록 D — Spring → Python 라이브러리 매핑
- 부록 E — pytest 레시피 모음 (JUnit 5 출신용 30패턴)
- 부록 F — 챕터별 심화 학습 가이드

---

## 다 읽고 나서 만들 수 있게 되는 것 5가지

1. **uv 단독 워크플로**로 모노레포·라이브러리·CLI 도구를 처음부터 끝까지 짤 수 있다 — `uv init`부터 `uv tool install` 배포까지.
2. **mypy strict가 켜진 FastAPI 백엔드** 한 채를 PostgreSQL/SQLAlchemy 2.x async + Alembic + JWT + OpenTelemetry로 *운영 수준*으로 띄울 수 있다.
3. **운영용 유틸리티 스크립트**(로그 분석·헬스체크·git 통계·이미지 일괄 처리)를 Typer + httpx + asyncio로 30분에 짜고 `uv tool install`로 배포한다.
4. **Anthropic SDK + prompt caching + structured output + tool use**를 비용 의식적으로 설계한다. 토큰 회계, 캐시 prefix 정책, 스트리밍이 손에 익는다.
5. **MCP 서버를 직접 만들고** Claude Desktop과 연결하며, **LangGraph 또는 PydanticAI**로 멀티 에이전트 워크플로를 그래프로 설계한다.

---

## 차별점 (왜 이 책인가)

- **JVM 멘탈 모델을 자산으로 인정하는 거의 유일한 한국어 Python 책.** 매 챕터에 *Spring에서 익혔던 직관 중 무엇을 그대로 쓰고 무엇을 폐기해야 하는가*가 새겨진다.
- **2026년 5월 시점의 가장 최신 stack으로만 구성.** 옛 Poetry/pip-tools/requirements.txt 흔적 없음.
- **한 권에서 언어부터 AI Agent까지.** 같은 러닝 예제(Snippet Hub)가 3장 uv workspace에서 22장 멀티 에이전트가 붙은 백엔드까지 자라며 흐른다.

---

## 이 책이 *약속하지 않는 것*

데이터/ML 깊이(NumPy/Pandas/PyTorch), Django 깊이, 모바일/임베디드 — 본 책의 야망 외 영역이다. 이 도메인이 필요한 독자에게는 별도 자료가 더 풍부함을 명시한다.

---

## 분량

본문 22 챕터 + 부록 6개. 통합 원고 약 567,000자 (한국어 산문 기준 약 250,000자). A5 판형 환산 약 760~800페이지. 바이블 두께.

---

## 저자

**Toby-AI** — JVM 사고와 Pythonic 사고의 *경계*에서 코드를 짜는 AI 저자. *Toby의 문체 가이드*를 토대로 평어체와 청유형, 수사적 질문을 통해 시니어 독자와 *함께 고민하는 동료*의 자세로 글을 쓴다.

---

## 책 정보

- **형식:** EPUB 3
- **파일:** `JVM-출신을-위한-Pythonic-v1.0.0.epub` (약 428 KB)
- **언어:** 한국어 (ko)
- **출간일:** 2026-05-03
- **저자:** Toby-AI
- **검증:** epubcheck FATAL 0 / ERROR 0
