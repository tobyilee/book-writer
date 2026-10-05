# Cloudflare를 나의 클라우드로

### 정적 사이트부터 Spring 백엔드까지, 무료로 시작해 안전하게 운영하기

> DNS와 CDN을 주는 곳으로만 알던 Cloudflare를, 내가 만든 앱과 서비스를 배포하고 운영하는 클라우드로 쓰는 법 — 무엇을 안에 두고 무엇을 밖에 둘지 판단하는 기준까지.

- **저자:** Toby-AI
- **버전:** v1.0.0
- **발행일:** 2026-10-03
- **언어:** 한국어 (ko)
- **분량:** 14개 장 + 부록 3종 / 본문 순수 산문 약 165,000자 (코드·표·다이어그램 제외), 다이어그램 14점
- **라이선스:** CC BY-NC-SA 4.0

## 이 책은 무엇인가

Cloudflare 계정을 가진 개발자는 많지만, 대부분 도메인 네임서버를 옮기고 프록시를 켠 뒤로는 다시 열어보지 않는다. 그 계정 안에는 코드를 실행하는 Workers, 관계형 데이터베이스 D1, 객체 저장소 R2, 상태를 가진 Durable Objects, 큐와 워크플로, 컨테이너, 포트를 열지 않고 서버를 공개하는 Tunnel, 팀의 내부 도구를 지키는 Cloudflare One이 들어 있다. 이 책은 그 계정을 "내 앱과 서비스를 배포하고 운영하는 클라우드"로 쓰는 실전서다.

책은 개발자 밋업 신청 서비스 `moim` 하나를 처음부터 끝까지 키운다. 정적 소개 페이지에서 시작해 React SPA, Hono API, D1·KV·Durable Objects·R2·Queues·Workflows, Next.js(vinext)로 자라고, Tunnel·Containers·Hyperdrive·Queues HTTP pull로 기존 Spring Boot 백엔드와 이어지며, Turnstile·WAF·레이트 리미팅과 Cloudflare One(Access·서비스 토큰·Spring Security의 Access JWT 검증)으로 보호된다. 마지막에는 세 가지 캐시 경로, 무료 티어 설계, 유료 계정의 다층 비용 방어를 거쳐 출시 점검에 이른다. 제품을 목록 순서가 아니라 "서비스에 다음으로 무엇이 필요해지는가"의 순서로 만나게 된다.

이 책은 제품별 사용법을 나열하지 않는다. D1이냐 Hyperdrive냐, Containers냐 Tunnel 뒤의 VM이냐, 존 캐시냐 Workers Cache냐처럼 같은 문제를 푸는 여러 선택지 사이에서 고르는 기준을 다룬다. 비용에 대해서도 정직하다. 2026년 10월 기준 Cloudflare에는 계정 전체의 지출 상한(하드캡)이 없다. 이 책은 "청구서 걱정 없이"라는 약속 대신, 무료 티어를 운영 전략으로 쓰는 법과 유료 계정에서 여러 장치를 겹쳐 비용 사고의 반경을 줄이는 법을 따로 다룬다.

모든 가격·한도·버전·제품 상태는 2026년 10월 3일 기준이며, 수치마다 기준이 된 문서와 날짜를 붙였다. 2026년에 이름이나 권장 경로가 바뀐 제품(WARP Client → Cloudflare One Client, Browser Rendering → Browser Run, 새 정적 사이트는 Pages 대신 Workers로 등)은 부록 C에 대조표로 정리했다.

## 누구를 위한 책인가

- **Java·Kotlin(Spring Boot) 개발자** — Workers에는 JVM이 없다. 이 책은 "Spring을 Workers로 옮기는 법"이 아니라 "Spring을 어디에 두고 Workers와 어떻게 잇는가"에 답한다. Spring Boot 서버는 Tunnel(6장), Containers·Hyperdrive·Queues pull(7장), SMTP·Pulumi Java(8장), Access JWT 검증(10장)에 걸쳐 서비스의 한 축으로 계속 등장한다.
- **JS/TS·React·Next.js·Node.js 개발자** — Vercel·AWS·VPS 사이에서 어디에 올릴지 고민하고 있다면, Workers 런타임이 Node 서버와 어떻게 다른지, Next.js를 Vercel 밖에서 운영할 때 어떤 위험을 지는지부터 짚는다.
- **사이드 프로젝트·사내 도구·작은 SaaS를 직접 배포하고 운영하려는 사람** — 웹 서비스를 한 번 이상 만들어 굴려본 중급 개발자를 전제한다. AWS 같은 클라우드를 깊이 알 필요는 없고, Cloudflare는 "DNS와 CDN을 무료로 주는 곳" 정도로만 알아도 충분하다.

책을 펴기 전의 독자는 무료라는 말에 끌리면서도 "갑자기 큰 청구서가 오면?"이 불안하고, Spring 개발자라면 "내 JVM 서버는 어디에 두지?"에 답을 찾지 못한 상태다. 책을 덮을 때는 정적 사이트에서 API, 데이터, 풀스택 앱, Spring 백엔드 연결, 외부 서비스 통합, 보안과 제로 트러스트, 캐싱, 비용 방어까지 직접 구성해 하나의 서비스를 출시할 수 있고, 무엇을 Cloudflare 안에 두고 무엇을 밖에 둘지 그 이유를 설명할 수 있게 된다.

## 무엇을 얻게 되는가

- Cloudflare 개발자 플랫폼의 지도 — isolate(Workers)·microVM(Containers)·VM으로 이어지는 격리 스펙트럼과 각 제품의 자리
- 데이터 종류별로 저장소(D1·KV·Durable Objects·R2·Queues·Workflows)를 고르는 기준과, 각 저장소의 비용이 터지는 지점
- 기존 Spring Boot 서비스를 상시 API·배치·데이터 공유 관점으로 나눠 착지점을 고르는 기준과 비용 계산법
- 결제·메일·외부 DB·AI·IaC를 붙일 때의 판단 틀과 검증된 연결 방법
- 공개 앱을 지키는 방어선 네 겹(Turnstile·WAF·레이트 리미팅·시크릿)과 각 층이 막는 것·못 막는 것
- 관리자 화면과 내부 서버를 Cloudflare Access로 닫고, Spring Security로 그 결과를 검증하는 완결된 흐름
- 콘텐츠 종류별 캐시 경로 선택표와 배포 후 캐시 문제를 층별로 진단하는 순서
- 무료 티어를 의도적으로 설계하는 계산법, 그리고 하드캡 없는 유료 계정에 겹쳐 둘 방어 장치 목록과 직접 만든 서킷 브레이커
- 바로 쓸 수 있는 가격·한도 치트시트와 출시 전 과금 안전 체크리스트

## 차례

**1부 올리기**

1. **Cloudflare를 나의 클라우드로 — 지도부터 펼치기** — CDN으로만 알던 Cloudflare 위에 앱 전체를 올린다는 것의 의미와, 되는 것·안 되는 것
2. **첫 배포 — 정적 사이트와 SPA를 Workers에 올리기** — Pages인가 Workers인가, 정적 자산을 무료로 남기는 구성 원칙
3. **Workers 런타임 — JVM 개발자의 멘탈 모델 바꾸기** — Workers가 Node 서버도 Spring 서버도 아닌 이유와, 그 위에서의 API 설계
4. **데이터와 상태 — D1·KV·Durable Objects·R2·Queues·Workflows 고르기** — "DB 하나에 스키마 하나"라는 전제를 넘어 엣지의 데이터 선택지 나눠 쓰기
5. **풀스택 앱 — React와 Next.js를 Workers에서** — 프레임워크를 Vercel 밖에서 운영할 때의 위험과 vinext·OpenNext·React Router 선택 기준

**2부 잇기**

6. **Cloudflare Tunnel — 포트를 열지 않고 서버를 세상에 내놓기** — 공인 IP도 열린 포트도 없이 Spring 서버를 포함한 오리진을 공개하는 법과 그 한계
7. **Spring Boot의 자리 — JVM 백엔드를 어디에 두고 어떻게 잇는가** — Tunnel 뒤 VM, Containers, 외부 DB 공유라는 세 착지점 비교
8. **Cloudflare 밖과 함께 — DB·결제·메일·AI·IaC 통합 전략** — 무엇을 안에서 하고 무엇을 밖에 맡길지, 밖에 둔 것을 잇는 방법

**3부 지키기**

9. **공개 앱 지키기 — Turnstile·WAF·레이트 리미팅·시크릿** — 누구나 들어오는 신청 폼과 API를 무료 범위 안에서 지키기
10. **Cloudflare One — 작은 팀을 위한 제로 트러스트** — 운영자 화면, Spring 서버, 팀원의 SSH를 VPN 없이 닫아두기

**4부 운영하기**

11. **캐싱 — 세 가지 캐시 경로와 무효화** — 존 캐시·Workers Cache·Cache API를 언제 쓰고, 바뀐 콘텐츠를 어떻게 내리는가
12. **무료로 어디까지 — 무료 티어를 설계 전략으로** — 사용량을 한도에 대조하고 무료로 버틸 구간을 의도적으로 설계하기
13. **유료 계정에서 안전하게 — 하드캡 없는 세상의 다층 방어** — 계정 지출 상한이 없는 상태에서 비용 사고를 막고 반경을 줄이는 장치들
14. **출시, 그리고 그 너머** — `moim` 출시 점검으로 전 과정을 되짚고, 장애·단일 벤더 리스크와 베타 제품의 전망까지

**부록**

- 부록 A. 가격·한도 치트시트 (2026-10-03 기준)
- 부록 B. 출시 전 과금 안전 체크리스트
- 부록 C. 명칭 변경 대조표와 도구 버전 (2026-10 기준)
- 참고문헌

## 저자 소개

Toby-AI는 개발자를 위한 기술서를 쓰도록 설계된 AI 저자 페르소나다. 독자와 함께 걸어가는 평어체 문장, 수사적 질문과 상황 가정으로 개념의 "왜"를 먼저 묻는 서술을 특징으로 한다. 이 책은 [book-writer](https://github.com/tobyilee/book-writer) 하네스 v2.0.0으로 리서치·계획·저술·사실 검증·편집·통권 수락 검수를 거쳐 만들어졌다.

공식 예제가 없어 직접 작성한 코드(Containers 위의 Spring Boot, Spring Security의 Access JWT 검증, 서킷 브레이커 `moim-guard` 등)는 본문에서 "저자 작성 예제"라고 밝혔다. 운영에 쓰기 전에 자기 환경에서 검증하기를 권한다.

## 책 정보

- 파일: `Cloudflare를-나의-클라우드로-v1.0.0.epub`
- 형식: EPUB 3 (ko)
- 식별자: `urn:uuid:7ae484e4-06ae-4ec0-8308-d14c91014f75`
- 라이선스: CC BY-NC-SA 4.0 (저작자표시-비영리-동일조건변경허락 4.0 국제)
- 표준 검증: epubcheck 통과 (0 errors / 0 warnings)
