# 커뮤니티 리서치 2차 (표적 gap-fill): `01_reference.md` §7-3 공백 겨냥

> **작성:** 2026-07-25 / **genre:** tech-book / **대상 독자:** 자바·스프링 백엔드 개발자, Apple Silicon 맥 사용자
> **성격:** 1차 `research/community.md`의 **보완 파일**이다. 1차 파일은 수정하지 않았다.
> **중복 회피:** 1차가 이미 확보한 30개 URL(docker/for-mac#7849·#7075·#7172·#3677, paketo-buildpacks/spring-boot#491, spring-boot#33119·#46665, testcontainers-java#5034, colima#365, rancher-desktop#4457 등, HN 22491170·41421846·41578274·35056594, velog @___pepper 등)은 **의도적으로 재수집하지 않았다.** 아래는 전부 신규다.

---

## 📋 이 파일의 인용 규율 (저술가·fact-checker 필독)

| 등급 | 의미 | 본문에서 허용되는 것 |
|------|------|---------------------|
| **축자 인용 가능** | 원문 텍스트를 API/페이지에서 직접 받아 이 파일에 그대로 옮겼다 | 따옴표 인용 OK |
| **요약 경유(인용 불가)** | 검색 스니펫·요약만 봤다 | 따옴표 인용 금지. "그런 주장이 있다" 수준까지만 |
| **📒 제목·상태만** | 이슈 번호·제목·등록일·조회 시점 상태 네 가지만 확인. 본문 미열람 | 분포·존속기간 근거로만. 원인·해석 붙이면 창작 |

**수집 도구:** HN은 Algolia 공식 API(`hn.algolia.com/api/v1/items/{id}`)로 스레드 전문을 받았다 — 따라서 HN 인용문은 **전부 축자**다. GitHub은 `gh` CLI. 검색 시점은 전부 **2026-07-25**.

⛔ **Reddit은 이번 세션에서 접근 실패했다.** `reddit.com/*.json`이 봇 차단 HTML을 반환했다(User-Agent 위장 포함 2회 시도). r/kubernetes·r/devops·r/java 자료는 **이 파일에 0건**이며, 이는 "레딧에 자료가 없다"가 아니라 **도구 실패**다. 본문에서 "레딧에서는 ~"이라고 쓰지 말 것.

---

# 🔴 1순위 — 시점이 낡은 논쟁의 최신화

## A. Kubernetes 도입 논쟁 — 2025~2026년 판본

> §7-3 #8은 "K8s 도입 논쟁이 2020년 스레드 중심(6년 전)이고 2024~2026 최신 스레드는 빈약했다"고 신고했다. **이 판정은 뒤집힌다.** 아래 두 스레드가 최신 판본이며, 무엇보다 **논쟁의 축 자체가 옮겨갔다.**

### A-1. ⭐⭐⭐ "2025년에도 초기 스타트업에 K8s는 여전히 금기인가" — 질문자가 이미 반박을 깔고 시작한다

- **출처:** Hacker News — https://news.ycombinator.com/item?id=44976292 (작성: 2025-08-21, 27 points, 50 comments, 검색: 2026-07-25)
- **인용 등급:** 축자 인용 가능 (Algolia API 전문 수신)
- **원문(질문 본문, `herval`, 2025-08-21):**
  > "It's a commonly-repeated comment that early stage startups should avoid K8s at all cost. As someone who had to manage it on a baremetal infrastructure in the past, I get where that comes from - Kubernetes has been historically hard to setup, you'd need to spend a lot of time learning the concepts and how to write the YAML configs, etc.
  > However, hosted K8s options have improved significantly in recent years (all cloud providers have Kubernetes options that are pretty much self-managed), and I feel like with LLMs, it's become extremely easy to read & write deployment configs."

  (번역: "초기 스타트업은 무슨 수를 써서라도 K8s를 피해야 한다 — 흔히 반복되는 말이다. 과거에 베어메탈 인프라에서 그걸 직접 굴려야 했던 사람으로서, 그 말이 어디서 나왔는지는 안다. 쿠버네티스는 역사적으로 셋업이 어려웠고, 개념과 YAML 설정 작성법을 배우는 데 시간을 많이 써야 했다. 그런데 **호스팅형 K8s 선택지가 최근 몇 년 사이 크게 좋아졌고**(모든 클라우드 제공자가 사실상 자체 관리되는 쿠버네티스 옵션을 갖고 있다), **LLM 덕에 배포 설정을 읽고 쓰는 게 굉장히 쉬워졌다**고 느낀다.")

- **맥락:** 2020년 HN 22491170("Let's use Kubernetes. Now you have eight problems")의 정확히 5년 뒤, 같은 커뮤니티에서 같은 질문이 다시 던져졌다. **차이는 질문자가 이미 두 개의 새 변수(managed K8s 성숙, LLM)를 논거로 들고 나온다는 것**이다.
- **쓸 곳:** K8s 챕터 오프닝 — "6년 전 논쟁이 아직 안 끝났다"가 아니라 **"논쟁의 전제가 바뀌었다"**로 열 수 있다. §4-1의 2020년 자료와 나란히 놓을 것.

### A-2. ⭐⭐ 관점 B의 최신 근거 — "EKS는 그냥 알아서 굴러간다"

- **출처:** Hacker News — https://news.ycombinator.com/item?id=44976744 (작성: 2025-08-21, 검색: 2026-07-25)
- **인용 등급:** 축자 인용 가능
- **원문(`tnjm`):**
  > "While I wouldn't dream of standing up k8s on a bare metal cluster without a devops team, I set up managed k8s using EKS several years ago for a client and... it just chugs along, self-healing, with essentially zero maintenance. ... At this stage I consider managed k8s my default go-to unless it's something so lightweight I just want to push it to Vercel and forget about it."

  (번역: "데브옵스 팀 없이 베어메탈 클러스터에 k8s를 세울 생각은 꿈도 안 꾸겠지만, 몇 년 전 어떤 고객사에 EKS로 managed k8s를 셋업해줬는데… **그냥 알아서 굴러간다.** 자가 치유되고, 유지보수가 사실상 0이다. … 이 시점에는 **managed k8s가 내 기본 선택**이다. 그냥 Vercel에 던져놓고 잊어버려도 되는 아주 가벼운 것이 아니라면.")

- **맥락:** 2020년 논쟁의 핵심 논거였던 "K8s는 운영이 지옥"에 대한 2025년의 직접 반박. **"베어메탈 자체 운영"과 "managed"를 명시적으로 분리**한다.
- **쓸 곳:** §4-1 관점 B 보강. 이 책의 독자(맥에서 로컬 개발하는 자바 개발자)가 실제로 마주할 K8s는 대개 EKS/GKE라는 점과 연결.

### A-3. ⭐⭐ 관점 A의 최신 근거 — "7년째 EKS를 굴렸고, 이제 ECS로 내려간다"

- **출처:** Hacker News — https://news.ycombinator.com/item?id=44978566 (작성: 2025-08-21, 검색: 2026-07-25)
- **인용 등급:** 축자 인용 가능
- **원문(`therealfiona`):**
  > "After 7 years, and me wanting to move off EKS since I got the job 4 years ago, we are moving to ECS (I rose to power of Lead recently, but my engineers also thought it was a great move as they're sick of all the K8s BS).
  > The time sink required for the care and feeding just isn't worth it. **I pretty much have to dedicate one engineer about 50% of the year to keeping the dang thing updated.**"

  (번역: "7년이 지났고, 입사 4년 전부터 EKS에서 벗어나고 싶었는데, 이제 ECS로 옮기는 중이다(최근에 리드가 됐는데, 우리 엔지니어들도 K8s 헛짓거리에 질려서 좋은 결정이라고 봤다). **돌보고 먹이는 데 드는 시간 소모가 그만한 값을 못 한다. 사실상 엔지니어 한 명을 1년의 절반쯤 그 물건 업데이트에만 붙여놔야 한다.**")

- **맥락:** A-2와 **정면으로 충돌**한다. 같은 스레드, 같은 날. 한쪽은 "유지보수 0", 다른 쪽은 "인력 0.5명/년". 둘 다 managed(EKS) 이야기다.
- **쓸 곳:** ⭐ **이 충돌 자체가 본문의 핵심 논지가 될 수 있다** — "managed면 괜찮다"는 명제조차 합의가 아니다. 비교 대조형 챕터의 "흔한 오해" 절에 A-2/A-3을 나란히 배치.

### A-4. ⭐ 손익분기점에 대한 2025년 판정 기준들 (§4-1 H8 보강)

전부 같은 스레드(44976292), 전부 축자 인용 가능, 전부 2025-08-21~22.

| 발언자 | 원문 | 번역 | 링크 |
|---|---|---|---|
| `more_corn` | "Do you benefit enough from the three things K8S does well to pay the cost in increased complexity, reduced visibility, and increased toil? **If you can't immediately rattle off those three things, you don't need it.**" | "K8s가 잘하는 세 가지에서, 복잡도 증가·가시성 저하·잡일 증가라는 값을 치를 만큼 이득을 보는가? **그 세 가지를 즉석에서 술술 못 읊으면, 당신은 그게 필요 없는 것이다.**" | [44976970](https://news.ycombinator.com/item?id=44976970) |
| `ruuda` | "probably Kubernetes is a solution to problems that you don't have, while it creates new problems that you don't currently have." | "쿠버네티스는 아마 당신에게 없는 문제의 해법이면서, 지금 당신에게 없는 새 문제를 만들어낸다." | [44976694](https://news.ycombinator.com/item?id=44976694) |
| `xyzzy123` | "There aren't really any huge gotchas imho in 2025, just watch out that you don't get sidetracked delivering awesome developer infrastructure (preview environments! blue/green! pristine iac! its fun!) if there are actually more important things to be working on (there usually are)." | "2025년 기준으로 큰 함정은 딱히 없다. 다만 정말 더 중요한 일이 있는데(대개 있다) 근사한 개발자 인프라(프리뷰 환경! 블루/그린! 깔끔한 IaC! 재밌다!)를 만드느라 옆길로 새지 않도록 조심하라." | [44978752](https://news.ycombinator.com/item?id=44978752) |
| `tdsanchez` | "Best advice is if you have to rearchitect your system JUST to run it on Kubernetes you probably don't know enough about it yet." | "최고의 조언은 이거다 — 쿠버네티스에서 돌리기 **위해서만** 시스템을 재설계해야 한다면, 아직 쿠버네티스를 충분히 모르는 것이다." | [44982847](https://news.ycombinator.com/item?id=44982847) |
| `dangus` | "**'Avoid k8s' shouldn't mean 'avoid containers'** because they have major velocity and reliability benefits for small teams with no ops engineers." | "**'k8s를 피하라'가 '컨테이너를 피하라'를 뜻해서는 안 된다.** 컨테이너는 운영 엔지니어가 없는 소규모 팀에게 속도와 안정성 면에서 큰 이득이 있다." | [44985447](https://news.ycombinator.com/item?id=44985447) |

- **쓸 곳:** ⭐⭐ **`dangus`의 마지막 문장이 이 책 전체의 포지셔닝 문장에 가장 가깝다.** 서문 또는 K8s 챕터 마무리에 배치 후보.

### A-5. ⭐⭐ 2026년 판본 — "쿠버네티스는 과했다, 도커 컴포즈로 내려와 60시간을 아꼈다"

- **출처:** Hacker News — https://news.ycombinator.com/item?id=46576224 (제출: 2026-01-11, 22 points, 17 comments, 검색: 2026-07-25) / 원문 기사는 Medium 링크
- **인용 등급:** 축자 인용 가능 **(HN 댓글에 한함)** — ⚠️ Medium 원문 기사는 열지 않았다. 기사 본문 인용 금지, **기사 제목과 HN 댓글만** 쓸 것
- **원문(`austin-cheney`, 2026-01-11) — 기사에서 인용한 대목을 재인용:**
  > "That article is magic. Here is the most important part:
  > "But what about when we scale to 100,000 users?"
  > "Then we'll have the revenue to hire a dedicated infrastructure team. Right now, we have eight engineers and we're spending 60 hours a week managing Kubernetes instead of shipping features.""

  (번역: "그 글은 마법이다. 가장 중요한 부분은 이거다. — '그런데 우리가 사용자 10만 명으로 커지면요?' / '그때는 전담 인프라 팀을 고용할 매출이 있을 거다. 지금 우리는 엔지니어 여덟 명인데, 기능을 출시하는 대신 **주당 60시간을 쿠버네티스 관리에 쓰고 있다.**'")

  ⚠️ **주의:** 이 "주당 60시간"은 **HN 댓글 작성자가 Medium 기사에서 옮긴 문장**이다. 이 리서치는 기사 원문을 열지 않았으므로 **"어떤 팀이 그렇게 말했다"가 아니라 "그런 주장을 담은 기사가 2026년 1월 HN에 올라왔고 댓글이 이 대목을 인용했다"**로만 쓸 것. 수치를 사실로 단정 금지.

- **⭐ 같은 스레드의 반대편(`halfmatthalfcat`, 2026-01-11):**
  > "Sounds like an overreaction by the OP out of frustration by not understanding how something works and how to debug it. Instead of learning and accepting the growing pains, decides to throw the baby out with the bath water, shame."

  (번역: "무언가가 어떻게 동작하고 어떻게 디버깅하는지 이해하지 못한 좌절에서 나온 과잉반응 같다. 배우고 성장통을 받아들이는 대신, 목욕물과 함께 아기까지 버리기로 한 것이다. 안타깝다.") — https://news.ycombinator.com/item?id=46577298

- **⭐⭐ 가장 쓸모 있는 댓글(`elthor89`, 2026-01-11) — 기술 논쟁이 아니라 조직 논쟁이라는 §4-10과 연결:**
  > "However there are some good nuggets in this article like this one: "That's when I realized: we'd built a dependency on one person's specialized knowledge. And that knowledge had nothing to do with our actual product."
  > I see that at more smaller orgs, where they want to have technology X but fail to realize it requires a small team. Not because its a 3 man job to operate but because **if 1 leaves or is unavailable the knowledge is gone.**"

  (번역: "다만 이 글엔 좋은 알맹이가 있다. '그때 깨달았다. 우리는 **한 사람의 특수 지식에 대한 의존성**을 만들어놨고, 그 지식은 우리 제품과 아무 상관이 없었다.' / 작은 조직에서 이런 걸 자주 본다. 기술 X를 쓰고 싶어 하지만 그게 작은 팀 하나를 요구한다는 걸 못 깨닫는다. 운영에 3명이 필요해서가 아니라, **한 명이 나가거나 자리를 비우면 지식이 사라지기 때문**이다.") — https://news.ycombinator.com/item?id=46577325

- **쓸 곳:** K8s 챕터. **A-5는 "2026년에도 이 논쟁이 살아 있다"의 증거**이며, 동시에 논쟁의 무게중심이 "기술이 복잡하다"에서 **"조직이 그 지식을 감당할 수 있는가"**로 옮겨간 증거다.

---

## B. Alpine vs Debian slim 논쟁의 **현재 상태**

> §7-3 #9: "Alpine 논쟁이 2023년 자료다. 핵심 논거(musl DNS-over-TCP 부재)가 그 시점에 이미 수정 중이었다 → 1차 소스 재확인 없이 쓰면 오보 위험."
> **판정: 논쟁이 사라진 게 아니라 논거가 교체됐다.** 2025년의 중심 논거는 DNS가 아니라 **musl의 기본 할당자(allocator) 성능**이다.

### B-1. ⭐⭐⭐ 2025년의 새 논거 — "musl 기본 할당자는 성능에 유해하다"

- **출처:** Hacker News — https://news.ycombinator.com/item?id=45143347 ("Default musl allocator considered harmful to performance", 제출 2025-09-05, 104 points, 검색: 2026-07-25). 원문 블로그는 nickb.dev
- **인용 등급:** 축자 인용 가능 **(HN 댓글에 한함)**. ⚠️ 블로그 원문 미열람 — 블로그 본문 인용 금지
- **⭐ 컨테이너 실무자 시점의 핵심 댓글(`jauntywundrkind`, 2025-09-08) — 전문:**
  > "Alas this is a huge foot gun that ensnares many orgs. **Because engineers seem drawn like moths to the flame to Alpine container images. Yes they are small, but the ramifications of Alpine & using musl are significant.**
  > Optimizing for size & stdlib code simplicity is probably not the best fit for your application server! **Container size has always struck me as such a Goodhart's Law issue** (and worse, already a bad measure as it measures only a very brief part of the software lifecycle). Goodhart's Law:
  > > When a measure becomes a target, it ceases to be a good measure
  > This particular musl/Alpine footgun can be worked around. It's not particularly hard to install and use another allocator on Alpine or anywhere really. Ruby folks in particular seem to have a lot of lore around jemalloc, with various versions preferences and MALLOC_CONFIGs on top of that. But in general I continue to feel like **Alpine base images bring in quite an X factor**, even if you knowingly adjust the allocator: the prevalence of Alpine in container images feels unfortunate & eccentric.
  > Going distorless is always an option. A little too radical for my tastes though usually."

  (번역: "안타깝게도 이건 많은 조직을 옭아매는 거대한 지뢰다. **엔지니어들이 불에 뛰어드는 나방처럼 Alpine 컨테이너 이미지에 끌리는 것 같기 때문이다. 그렇다, 작다. 하지만 Alpine과 musl 사용이 남기는 파급은 상당하다.** / 크기와 표준 라이브러리 코드 단순성을 최적화하는 건 당신의 애플리케이션 서버에는 아마 최선의 궁합이 아니다! **컨테이너 크기는 나에게 늘 굿하트의 법칙 문제로 보였다**(게다가 소프트웨어 생애주기의 아주 짧은 한 토막만 재는, 이미 나쁜 척도다). 굿하트의 법칙: '측정치가 목표가 되는 순간, 그것은 좋은 측정치이기를 멈춘다.' / 이 musl/Alpine 지뢰는 우회할 수 있다. Alpine에서든 어디서든 다른 할당자를 설치해 쓰는 게 특별히 어렵지 않다. 특히 루비 쪽은 jemalloc에 대한 구전 지식이 많다… 하지만 대체로 나는 **Alpine 베이스 이미지가 상당한 X 팩터를 끌고 들어온다**고 계속 느낀다. 할당자를 알고 조정하더라도 말이다. 컨테이너 이미지에서 Alpine이 이만큼 흔한 건 유감스럽고 별나게 느껴진다. / distroless로 가는 건 언제나 선택지다. 다만 대체로 내 취향엔 좀 과격하다.")
  — https://news.ycombinator.com/item?id=45164869

- **반대편(`flohofwoe`, 2025-09-08):**
  > "It only matters when your threads allocate with such a high frequency that they run into contention. A too high access frequency to a shared resource is not a "general case", but simply poorly designed multithreaded code"
  (번역: "스레드가 경합에 걸릴 만큼 높은 빈도로 할당할 때에만 문제가 된다. 공유 자원에 대한 지나치게 높은 접근 빈도는 '일반적 경우'가 아니라 그냥 잘못 설계된 멀티스레드 코드다.") — https://news.ycombinator.com/item?id=45166368

- **재반박(`masklinn`, 2025-09-08):**
  > "**In 2025 an allocator not cratering multi-threaded programs is the opposite of specialisation.**"
  (번역: "**2025년에, 멀티스레드 프로그램을 곤두박질치게 만들지 않는 할당자는 '특수화'의 반대말이다.**") — https://news.ycombinator.com/item?id=45166312

- **⚠️ 자바 독자에게의 함의 — 신중하게 쓸 것:**
  이 스레드는 **Rust/C 맥락**이다. 스레드 안에 JVM 언급은 없다. 다만 **"멀티스레드 애플리케이션 서버"**라는 조건은 스프링 부트 애플리케이션에 정확히 해당한다. 본문에서는 **"musl 할당자 논쟁이 JVM에서 이렇다"라고 단정하지 말고**, "2025년 커뮤니티의 Alpine 논거가 DNS에서 할당자 성능으로 옮겨갔으며, 그 논거의 조건(고빈도 할당·멀티스레드)이 자바 서버에 해당하는지는 독자가 자기 워크로드로 확인해야 한다"로 쓸 것.

- **⛔ §8-3과의 충돌 점검:** 이 스레드에는 "Alpine JDK는 Java API 부분집합"류 주장이 **없다.** §8-3의 반증 판정과 충돌하지 않는다. (1차 리서치가 잡았던 그 주장은 이번 2차 수집분에 재등장하지 않았다.)

- **쓸 곳:** 베이스 이미지 선택 챕터의 "논쟁" 절. §8-3(1차 소스 기반 선택 기준)이 **무엇을 고를지**를 준다면, B-1은 **왜 이 논쟁이 안 끝나는지**를 준다.

### B-2. musl 성능 열위에 대한 다른 시점 증언들 (2025)

- **출처/인용 등급:** 전부 Hacker News, 축자 인용 가능

| 발언자·시점 | 원문 | 번역 | 링크 |
|---|---|---|---|
| `tombl` 2025-03-22 | "musl values portability over performance (great for my usecase), which makes it often significantly slower than glibc." | "musl은 성능보다 이식성을 중시하고, 그래서 glibc보다 상당히 느린 경우가 많다." | [43444592](https://news.ycombinator.com/item?id=43444592) |
| `saagarjha` 2025-09-08 | "glibc is faster in basically every usecase, though." | "그래도 glibc가 사실상 모든 용례에서 더 빠르다." | [45167248](https://news.ycombinator.com/item?id=45167248) |
| `userbinator` 2025-09-08 | "I believe musl is supposed to be optimised heavily for size, not speed." | "musl은 속도가 아니라 크기에 강하게 최적화된 것으로 안다." | [45164728](https://news.ycombinator.com/item?id=45164728) |
| `stonogo` 2025-09-08 | "Specifically its goals are low memory overhead and hardening. Safe defaults, and easy to swap to a performance-oriented malloc for those apps that want it." | "구체적으로 musl의 목표는 낮은 메모리 오버헤드와 하드닝이다. 안전한 기본값, 그리고 원하는 앱은 성능 지향 malloc으로 쉽게 갈아끼울 수 있게." | [45165234](https://news.ycombinator.com/item?id=45165234) |

- **쓸 곳:** "Alpine이 작다"는 한 줄 옆에 붙일 **트레이드오프의 다른 항목**. 커뮤니티 다수 의견 표시로 사용하되, **수치 근거는 없다**(전부 정성 증언).

---

## C. Docker Desktop 대안의 **현재 판세** (2025~2026)

> §7-3 #11: "Podman 후기가 2021~22년 것뿐."
> **판정: 뒤집힌다.** 2026-07-02 Podman v6.0.0 HN 스레드(648 points)가 있고, 2026-07-07 Apple Containers UI 스레드(389 points)가 대안 4종을 직접 비교한다.

### C-1. ⭐⭐⭐ Podman v6.0.0 스레드 — 2026년 7월의 대안 런타임 지형도

- **출처:** Hacker News — https://news.ycombinator.com/item?id=48762098 (제출 2026-07-02, **648 points**, 검색: 2026-07-25). 원문 링크는 blog.podman.io
- **인용 등급:** 축자 인용 가능 (HN 댓글에 한함). ⚠️ Podman 블로그 원문 미열람

**⭐⭐ 자바 독자 정조준 — Podman + Testcontainers 실패 증언 (`tsfenwick`, 2026-07-02):**
> "I ran into an issue I couldn't figure out how to solve with podman. Some of the testcontainers my test suites would run wouldn't start in time causing tests to fail locally. Switching back to docker desktop solved the problem."

(번역: "podman에서 해결법을 못 찾은 문제를 만났다. 내 테스트 스위트가 돌리는 **테스트컨테이너 중 일부가 제때 시작되지 않아 로컬에서 테스트가 실패**했다. **도커 데스크톱으로 되돌아가니 해결됐다.**")
— https://news.ycombinator.com/item?id=48766152

- **바로 아래 댓글(`gkhartman`, 2026-07-02):**
  > "This except in production. Nothing helped. I actually stopped using containers for a bit after that."
  (번역: "이건데 프로덕션에서였다. 아무것도 도움이 안 됐다. 그 뒤로 한동안 컨테이너 쓰기를 아예 그만뒀다.") — https://news.ycombinator.com/item?id=48766672
- **쓸 곳:** ⭐ Testcontainers 챕터 오프닝 후보. 1차의 A13(Colima 이주 후 Ryuk 소켓)과 **같은 패턴, 4년 뒤, 다른 런타임**이다. "런타임을 바꾸면 자바 테스트가 먼저 안다"는 논지의 두 번째 증거.

**⭐⭐ 맥에서의 판세 요약 (`spockz`, 2026-07-02) — 이번 수집에서 가장 밀도 높은 한 댓글:**
> "I think a stronger brand name. Also on macOS I found Docker Desktop to be more straightforward. **Also lately it has been very error prone. Randomly failing at mounting files, or cleaning up networking rules, or suddenly becoming bog slow so I have to restart the VM.**
> **Podman on macOS feels miles less refined. Orbstack is a way better choice.**
> I only use podman on Linux and there it is blazing fast. Even so, most features seem to be geared to be able to replace kubernetes in combination with systemd. And then something simple as docker compose support is flaky and it's TUI/ux lags behind the original."

(번역: "브랜드 이름이 더 강해서인 것 같다. 그리고 macOS에서는 Docker Desktop이 더 직관적이었다. **다만 최근엔 오류가 아주 잦다. 파일 마운트가 무작위로 실패하거나, 네트워킹 규칙 정리가 안 되거나, 갑자기 지독하게 느려져서 VM을 재시작해야 한다.** / **macOS의 Podman은 완성도가 한참 떨어지게 느껴진다. Orbstack이 훨씬 나은 선택이다.** / 나는 Podman을 리눅스에서만 쓰는데 거기선 엄청나게 빠르다. 그렇더라도 대부분의 기능이 systemd와 결합해 쿠버네티스를 대체하는 쪽으로 맞춰져 있는 것 같다. 그러다 보니 docker compose 지원 같은 단순한 것이 불안정하고, TUI/UX가 원본에 뒤처진다.")
— https://news.ycombinator.com/item?id=48766238

**⭐⭐ 자바 빌드 성능 증언 (`spockz`, 2026-07-03) — §7-3 #7의 인접 자료:**
> "Build as in building images or as in building a project when mounted in a container? **I notice 3-4x performance degradation of our maven builds in containers.** With golang I haven't noticed much performance degradation, but that may be because it is fast enough anyway."

(번역: "이미지를 빌드한다는 건가, 아니면 컨테이너에 마운트한 상태로 프로젝트를 빌드한다는 건가? **컨테이너 안에서 돌리는 우리 메이븐 빌드는 3~4배 성능 저하를 체감한다.** golang은 성능 저하를 크게 못 느꼈는데, 어차피 충분히 빨라서일 수도 있다.")
— https://news.ycombinator.com/item?id=48771765

- ⚠️ **이건 "수치"가 아니다.** 측정 방법·머신·런타임·마운트 방식이 전부 불명인 **단일 체감 증언**이다. §7-3 #7("Gradle/Maven 볼륨 마운트 성능 수치 없음")은 **여전히 미해소**다. 본문에서는 "한 개발자는 3~4배 저하를 체감한다고 말한다" 형태로만, 반드시 "체감"과 "단일 증언"을 병기할 것.
- **쓸 곳:** 볼륨 마운트/빌드 성능 절 — **자바 독자에게 처음으로 자바 워크로드로 말하는 증언**이라는 점에서 값이 있다.

**OrbStack 빌드 속도 증언 (`SOLAR_FIELDS`, 2026-07-02):**
> "Now that Apple has containerization api's probably the gap closed but when I ran benchmarks a couple years ago Orbstack would on average perform the same build at 4x faster wall clock time as docker desktop"

(번역: "이제 애플이 컨테이너화 API를 내놨으니 격차가 좁혀졌을 수도 있는데, 몇 년 전 내가 벤치마크를 돌렸을 땐 **OrbStack이 같은 빌드를 평균 4배 빠른 실측 시간에** 해냈다.")
— https://news.ycombinator.com/item?id=48768392
- ⚠️ **"a couple years ago"** — 본인이 시점을 흐리게 말했다. **수치 근거로 쓰지 말 것.** "그런 체감이 커뮤니티에 있다" 수준까지만.

**Docker CLI vs Docker Desktop 라이선스 구분 (`ifwinterco` / `pjmlp`, 2026-07-02) — §3-1(2021년 라이선스 공지)의 5년 뒤:**
> `ifwinterco`: "Docker CLI is free for commercial use, it's only docker desktop you have to pay for"
> `pjmlp`: "I know, but companies legal or IT department make it easier, no docker of any kind being installed from https://www.docker.com. Microsoft also is finally adding their own docker cli (wslc), due to having had enough pressure that many companies don't want to instal third party tools... Apple is doing a similar approach on top of their virtualisation framework."

(번역: — "도커 CLI는 상업적 사용이 무료다. 돈을 내야 하는 건 도커 데스크톱뿐이다." / — "안다. 그런데 회사 법무나 IT 부서는 더 간단하게 처리한다. **docker.com에서 받는 건 무엇이든 설치 금지다.** 마이크로소프트도 마침내 자체 docker CLI(wslc)를 넣고 있다. 서드파티 도구를 설치하기 싫어하는 회사가 많다는 압력을 충분히 받아서다… 애플도 자기 가상화 프레임워크 위에 비슷한 접근을 하고 있다.")
— https://news.ycombinator.com/item?id=48766350 / https://news.ycombinator.com/item?id=48766561
- **쓸 곳:** ⭐ §4-10(조직 정치) 보강. **"기술 논쟁이 아니라 구매 정책 논쟁"의 2026년 판본**이며, 1차의 2021년 라이선스 스레드가 6년 뒤 어떻게 착지했는지를 보여준다. 이 책의 독자가 회사에서 실제로 마주할 상황.

**Podman을 포기한 이유 (`trollbridge`, 2026-07-02) — 맥 사용자 시점:**
> "There were other problems although it's been a few years so I've forgotten them… **macOS had a seperate set of problems. I ended up just going with buildx and Colima on macOS. (We don't use Docker Desktop.)**"
(번역: "다른 문제들도 있었는데 몇 년 지나서 잊었다… **macOS에는 별도의 문제 세트가 있었다. 결국 macOS에서는 buildx와 Colima로 갔다. (우리는 Docker Desktop을 쓰지 않는다.)**") — https://news.ycombinator.com/item?id=48766439

**Podman의 남은 마찰 — compose 호환 (`psadauskas`, 2026-07-02):**
> "This is my biggest gripe. If you're using docker-compose.yml on a team that mostly uses docker, you can't use use that same docker-compose.yml with rootless podman. Any volume mounts that need to be writable (like the app, or databases) need to have `:X` or `:x` as a suffix, or podman won't set the SELinux label correctly to make it writable. But if you add those, docker blows up because it doesn't understand them."
(번역: "이게 내 가장 큰 불만이다. 팀 대부분이 도커를 쓰는데 docker-compose.yml을 쓴다면, 같은 파일을 rootless podman으로는 못 쓴다. 쓰기 가능해야 하는 볼륨 마운트(앱이나 DB 같은)에는 `:X`나 `:x` 접미사가 필요한데, 안 붙이면 podman이 SELinux 라벨을 제대로 못 붙여서 쓰기가 안 된다. 그런데 붙이면 도커가 그걸 이해 못 해서 터진다.") — https://news.ycombinator.com/item?id=48767287
- ⚠️ 이 SELinux 마찰은 **리눅스 이야기**다. 맥 독자에게 직결되진 않는다. **"한 팀에 두 런타임이 섞이면 설정 파일이 갈라진다"**는 일반 패턴의 증거로만 쓸 것 (1차 H10과 연결).

### C-2. ⭐⭐ Apple Containers 등장 — 2026년 7월, 대안이 하나 더 늘었다

- **출처:** Hacker News — https://news.ycombinator.com/item?id=48821848 ("Show HN: Davit, a Apple Containers UI", 2026-07-07, **389 points**, 검색: 2026-07-25)
- **인용 등급:** 축자 인용 가능

**⭐ 아키텍처 차이 — 저자 본인 설명 (`xinit`, 2026-07-07):**
> "Docker Desktop/Obstack start a single VM that runs all your containers. This means that you'll have to scale it accordingly. Davit uses Apple Containers that runs a very thin VM for each container you spin up. Depending on your use case it's more, less or equivalently effcient."
(번역: "Docker Desktop/OrbStack은 **모든 컨테이너를 돌리는 VM 하나**를 띄운다. 그래서 그에 맞게 크기를 잡아야 한다. Davit은 Apple Containers를 쓰는데, 이건 **띄우는 컨테이너마다 아주 얇은 VM 하나씩**을 돌린다. 용례에 따라 더 효율적일 수도, 덜할 수도, 같을 수도 있다.") — https://news.ycombinator.com/item?id=48824924
- **쓸 곳:** ⭐⭐ §1-3/§1-4(맥에서 리눅스 VM이 끼는 구조) 챕터. **"VM 하나 vs 컨테이너당 VM"은 이 책의 중심축(아키텍처)에 정확히 꽂히는 2026년 신규 변수**다.

**메모리 관점의 반론 (`watermelon0`, 2026-07-08):**
> "Docker Desktop's memory saver shuts down VM when containers are not running. Additionally, Docker/Podman/Orbstack start a single VM, where memory is shared between containers. On the other hand, **Apple Containers create a separate VM for each container, which results in higher memory usage due to Linux kernel overhead**, as well as the fact that kernel will try to use most of the available memory for file caching."
(번역: "Docker Desktop의 메모리 세이버는 컨테이너가 안 돌 때 VM을 내린다. 게다가 Docker/Podman/OrbStack은 VM 하나를 띄우고 컨테이너들이 메모리를 공유한다. 반면 **Apple Containers는 컨테이너마다 별도 VM을 만들고, 리눅스 커널 오버헤드 때문에 메모리 사용량이 더 커진다.** 커널이 가용 메모리 대부분을 파일 캐싱에 쓰려 한다는 사실도 겹친다.") — https://news.ycombinator.com/item?id=48827674

**OrbStack의 단일 VM 이점 (`TimTheTinker`, 2026-07-08):**
> "OrbStack's claim to fame is that all containers run in a single Linux VM, with lots of optimizations on both sides of the VM boundary (including use of a sparse image file for disk storage, which saves a lot of space on the macOS side). **If you run more than 4-5 containers on macOS, the performance and resource usage savings of OrbStack really starts to add up quickly.**"
(번역: "OrbStack의 자랑은 모든 컨테이너가 단일 리눅스 VM에서 돌고, VM 경계 양쪽에 최적화가 많다는 것이다(디스크 저장에 sparse 이미지 파일을 써서 macOS 쪽 공간을 많이 아끼는 것 포함). **macOS에서 컨테이너를 4~5개 넘게 돌리면 OrbStack의 성능·자원 절약이 정말 빠르게 쌓이기 시작한다.**") — https://news.ycombinator.com/item?id=48833227

**⭐ Docker Desktop 자원 소모 — 2026년 7월의 짧은 증언 3건:**

| 발언자·시점 | 원문 | 번역 | 링크 |
|---|---|---|---|
| `david_p` 2026-07-07 | "Docker desktop on mac does not work well (uses lots of resources) and my current alternative is OrbStack (very slick, uses far less resources, but freemium)." | "맥의 도커 데스크톱은 잘 안 굴러간다(자원을 많이 쓴다). 내 현재 대안은 OrbStack이다(아주 매끈하고 자원을 훨씬 덜 쓰지만 프리미엄 모델)." | [48824625](https://news.ycombinator.com/item?id=48824625) |
| `ballislife30` 2026-07-07 | "Docker desktop is a memory hog. What's the memory usage of Davit?" | "도커 데스크톱은 메모리 먹깨비다. Davit의 메모리 사용량은?" | [48823605](https://news.ycombinator.com/item?id=48823605) |
| `samgranieri` 2026-07-08 | "I've worked with docker desktop and podman desktop for years on macOS. Those programs start up a virtual machine that **consistently eats ram regardless of whether or not you are running containers in it.** In the age of ridiculous ram costs, you gotta save resources." | "macOS에서 도커 데스크톱과 팟맨 데스크톱을 수년간 써왔다. 이 프로그램들은 **컨테이너를 돌리든 안 돌리든 일관되게 램을 먹는** 가상 머신을 띄운다. 램 값이 말도 안 되는 시대에는 자원을 아껴야 한다." | [48826637](https://news.ycombinator.com/item?id=48826637) |

- ⚠️ `samgranieri`의 "돌리든 안 돌리든"은 `watermelon0`의 "메모리 세이버가 VM을 내린다"와 **충돌**한다. 양쪽 다 2026-07-08. **어느 쪽도 단정하지 말고, Docker Desktop의 Resource Saver 동작은 1차 소스(공식 문서)로 확인할 것.**

### C-3. Colima 전환 후기 (2025-10)

- **출처:** Hacker News — https://news.ycombinator.com/item?id=45492438 ("From Docker Desktop (300% CPU) to Colima and Portainer (0.2%) on macOS", 2025-10-06, 11 points, 검색: 2026-07-25). 원문은 Medium
- **인용 등급:** 축자 인용 가능 (HN 본문 텍스트에 한함). ⚠️ Medium 원문 미열람
- **원문(`muthuishere`, 2025-10-06):**
  > "Docker Desktop on macOS often sits in a VM that constantly sucks CPU. For years I tolerated it—until today, when **running just two Node.js apps + one Python app pegged my system, froze the UI.**
  > I switched to Colima and pointed docker context use colima. Then added Portainer for UI…
  > With the same compose setup, **Colima usage dropped to ~0.2%**"

  (번역: "macOS의 Docker Desktop은 CPU를 계속 빨아먹는 VM 안에 앉아 있곤 한다. 수년간 참았다 — 오늘까지는. **Node.js 앱 두 개 + 파이썬 앱 하나를 돌린 것만으로 시스템이 못 박힌 듯 멈추고 UI가 얼어붙었다.** / Colima로 갈아타고 `docker context use colima`를 가리켰다. UI용으로 Portainer를 추가했다… / 같은 compose 설정으로 **Colima 사용률은 ~0.2%로 떨어졌다.**")

- ⚠️ **"300% → 0.2%"를 수치로 인용하지 말 것.** 측정 방법·구간·도구가 전부 불명이고 검증 없는 자기 보고다. **"이런 체감 후기가 있다"** 수준으로만.
- **쓸 곳:** 대안 런타임 챕터 — "왜 사람들이 옮기는가"의 최신 사례.

### C-4. ⭐⭐ Red Hat이 Podman Desktop 상용판을 낸 스레드 (2026-02) — 대안 지형의 결정판

- **출처:** Hacker News — https://news.ycombinator.com/item?id=47151163 ("Red Hat takes on Docker Desktop with its enterprise Podman Desktop build", 2026-02-25, 130 points, 검색: 2026-07-25). 원문은 thenewstack.io
- **인용 등급:** 축자 인용 가능 (HN 댓글에 한함). ⚠️ 기사 원문 미열람
- **왜 중요한가:** 이 스레드에는 **Podman Desktop 팀 멤버(`cdrage`)가 직접 등장해 답한다**(🟢 메인테이너급 근거). 그리고 자바 워크로드의 구체적 실측 대화가 오간다.

#### ⭐⭐⭐ C-4-a. 자바 독자 정조준 — "스프링 부트를 Podman에서 돌리니 24.96초"

- **원문(`p0w3n3d`, 2026-02-25, 최초 보고):**
  > "My Podman starts containers in arch x86-64-v3 with rosetta on for 27 seconds which Docker does it in 9s. I wonder what's wrong. I've already upgraded Mac to Tahoe (which has x86-64-v3 support included into rosetta)"
  (번역: "내 Podman은 rosetta를 켠 x86-64-v3 아키텍처 컨테이너를 **27초**에 시작하는데, Docker는 **9초**에 한다. 뭐가 잘못됐는지 모르겠다. 이미 맥을 Tahoe로 올렸는데(로제타에 x86-64-v3 지원이 들어간 버전).") — https://news.ycombinator.com/item?id=47151862

- **⭐ 후속(`p0w3n3d`, 2026-02-26) — 여기서 스프링 부트가 나온다:**
  > "I've checked and there is no difference between podman and docker on my machine.
  > However **when running a spring boot over eclipse-temurin:25-jdk-ubi10-minimal image there is this huge difference**
  > ```
  > podman run   0.02s user 0.01s system 0% cpu 24.960 total
  > ```
  > you can see the java app starting slowly. I've double checked that rosetta is enabled on podman."

  (번역: "확인해보니 내 머신에서 podman과 docker 사이에 차이가 없다. / 그런데 **`eclipse-temurin:25-jdk-ubi10-minimal` 이미지 위에서 스프링 부트를 돌리면 이 엄청난 차이가 난다.** / `podman run 0.02s user 0.01s system 0% cpu 24.960 total` / 자바 앱이 느리게 뜨는 걸 볼 수 있다. podman에 rosetta가 켜져 있는지 두 번 확인했다.") — https://news.ycombinator.com/item?id=47163089

- ⚠️ **인용 규율:** 이 수치(27초/9초/24.96초)는 **한 사용자의 자기 보고**다. 머신·이미지 태그·측정 반복 횟수가 불완전하고, 본인이 중간에 "차이가 없다"로 한 번 번복했다. **본문에서 벤치마크로 제시 금지.** "한 사용자가 스프링 부트 + amd64 + Rosetta 조합에서 20초대를 보고했다"까지만.
- **쓸 곳:** ⭐⭐ **자바 독자에게 이보다 정확히 꽂히는 최신 증언이 없다** — 스프링 부트 + Temurin + amd64 에뮬레이션 + Apple Silicon + 대안 런타임이 한 댓글에 다 있다. 1차의 A5(Rosetta 33,656초)와 **같은 축, 3년 뒤, 자바 워크로드**다. Rosetta 챕터 오프닝 또는 §2-2 보강.

#### ⭐ C-4-b. 메인테이너가 밝힌 기본값 차이 (Docker Desktop vs Podman Desktop)

- **원문(`cdrage`, Podman Desktop 팀, 2026-02-25):**
  > "Ahhh, one of the reasons could be that **Docker Desktop by default uses 50% of your RAM when they create their VM and the maximum amount of CPUs. Podman Desktop by default has a much lower RAM (4GB) + CPU usage (50% CPU).** That's something that could be improved... I've opened up an issue"
  (번역: "아, 이유 중 하나는 이것일 수 있다 — **Docker Desktop은 VM을 만들 때 기본적으로 램의 50%와 CPU 최대치를 쓴다. Podman Desktop은 기본값이 훨씬 낮다(램 4GB + CPU 50%).** 개선할 여지가 있는 부분이다… 이슈를 열었다.") — https://news.ycombinator.com/item?id=47152469
- **그런데 반증(`p0w3n3d`, 2026-02-25):**
  > "No I checked it against the amount of RAM. Podman with 8GB does not increase speed, Docker with 4GB is still 9s
  > ```
  > podman run   27->24
  > docker run   9.4->9.769 total
  > ```"
  (번역: "아니다, 램 양을 기준으로 확인해봤다. Podman에 8GB를 줘도 속도가 안 오르고, Docker는 4GB로도 여전히 9초다.") — https://news.ycombinator.com/item?id=47153204
- **쓸 곳:** ⭐ **"메모리를 늘리면 빨라진다"는 가장 흔한 처방이 여기서 반증된다.** 맥 리소스 튜닝 절의 "흔한 오해"에 배치. 그리고 **런타임마다 기본 할당량이 다르다**는 사실(🟢 메인테이너 발언)은 §2-3(클라이언트/데몬 분리)과 이어진다.

#### C-4-c. Rancher Desktop의 2026년 후기 (이 맥에 설치돼 있는 런타임)

- **원문(`bmurphy1976`, 2026-02-25):**
  > "I tried to use podman desktop for a bit but I ran into some screwy compatibility issues. It just wasn't as smooth as docker.
  > **I really really want an alternative to docker desktop. I don't like the path they're going down. I don't like the AI crap in the UI. The licensing is crazy. It just doesn't feel right.**
  > So I've been lately using rancher by SuSE. Surprisingly, it's been all right. So far it just works. I'm using this on Mac OS."

  (번역: "팟맨 데스크톱을 잠깐 써봤는데 이상한 호환성 문제를 만났다. 그냥 도커만큼 매끄럽지 않았다. / **나는 정말 정말로 도커 데스크톱의 대안을 원한다. 그들이 가는 길이 마음에 안 든다. UI에 들어간 AI 쓰레기가 싫다. 라이선스는 미쳤다. 그냥 옳게 느껴지지 않는다.** / 그래서 최근엔 SuSE의 rancher를 쓰고 있다. 놀랍게도 괜찮았다. 지금까지는 그냥 잘 된다. macOS에서 쓰는 중이다.") — https://news.ycombinator.com/item?id=47152238

- **디스크 관점(`zitterbewegung`, 2026-02-25):**
  > "I love rancher too and I have less issues of docker using all of my local disk."
  (번역: "나도 rancher를 좋아한다. 도커가 내 로컬 디스크를 다 잡아먹는 문제가 덜하다.") — https://news.ycombinator.com/item?id=47152911
- **쓸 곳:** §7-3 #11의 짝. 그리고 이 책의 실측 환경(Rancher Desktop 설치됨)과 직접 연결된다.

#### C-4-d. OrbStack 옹호 — 2026-02의 집중 증언

- 전부 축자 인용 가능, 전부 2026-02-25, 같은 스레드

| 발언자 | 원문 | 번역 | 링크 |
|---|---|---|---|
| `chuckadams` | "OrbStack is a very compelling alternative on macOS. **The GUI launches instantly due to being a Swift app and not Electron.** Container filesystems are visible in Finder. You can spin up full-blown VMs with it (only Linux ones though). **Storage is managed dynamically, so you don't have to reserve or resize the virtual disk.** Free for personal use, with zero nags or upsells." | "OrbStack은 macOS에서 아주 설득력 있는 대안이다. **Electron이 아니라 Swift 앱이라 GUI가 즉시 뜬다.** 컨테이너 파일시스템이 파인더에서 보인다. 본격적인 VM도 띄울 수 있다(리눅스만). **스토리지가 동적으로 관리돼서 가상 디스크를 예약하거나 리사이즈할 필요가 없다.** 개인 사용은 무료고, 성가신 알림이나 업셀이 전혀 없다." | [47152648](https://news.ycombinator.com/item?id=47152648) |
| `moltar` | "Orb is definitely the winner. It's fast. It does the job well. **Never had an issue with it in two years.**" | "Orb이 확실한 승자다. 빠르다. 일을 잘한다. **2년 동안 한 번도 문제가 없었다.**" | [47152703](https://news.ycombinator.com/item?id=47152703) |
| `blakesterz` | "I'll just add another vote for OrbStack. **I found it way faster on M1 and M5** and never found any compatibility issues." | "OrbStack에 한 표 더 보탠다. **M1과 M5에서 훨씬 빨랐고** 호환성 문제를 하나도 못 찾았다." | [47153173](https://news.ycombinator.com/item?id=47153173) |
| `nsbk` | "Some devs in my team are running it as a more performant alternative to Docker Desktop for Mac and they are very happy so far." | "우리 팀 개발자 몇몇이 맥용 Docker Desktop의 더 성능 좋은 대안으로 쓰고 있는데 지금까지 아주 만족한다." | [47152602](https://news.ycombinator.com/item?id=47152602) |

- **⚠️ 반대편 — 유지보수 우려(`Shebanator`, 2026-02-25):**
  > "Does anyone know if the company is still active. Haven't seen any updates for a while now. I like the product a lot, but products like this need security updates at the very least."
  (번역: "이 회사가 아직 활동 중인지 아는 사람? 한동안 업데이트를 못 봤다. 제품은 아주 좋아하는데, 이런 제품은 최소한 보안 업데이트는 필요하다.") — https://news.ycombinator.com/item?id=47155715
- **답(`chuckadams`, 2026-02-25):**
  > "Last release was November 2025 which isn't that terribly long ago. … They do look to have stopped blogging on orbstack.dev for more than a year now."
  (번역: "마지막 릴리스는 2025년 11월이라 그렇게 오래되진 않았다. … 다만 orbstack.dev 블로그는 1년 넘게 멈춘 것으로 보인다.") — https://news.ycombinator.com/item?id=47159776
- ⚠️ **이 릴리스 시점 주장은 커뮤니티 발언이다.** 본문에 쓰려면 §2-4의 공개 릴리스 라인으로 **반드시 1차 확인**할 것.
- **쓸 곳:** ⭐ §4-7("OrbStack 유료가 합당한가")의 **반대편 리스크 항목**. "빠르다"에만 몰린 후기 속에서 **유일하게 다른 축(지속성·보안 업데이트)을 짚는 발언**이다. 대안 런타임 이주 결정표에 "벤더 리스크" 행을 넣을 근거.

#### C-4-e. Podman이 맥에서 아직 못 넘은 것들 (2026-02)

| 발언자 | 원문 | 번역 | 링크 |
|---|---|---|---|
| `p0w3n3d` | "**I got into problems with test containers on podman and I have no idea how to solve them.** Have you fought with that by any chance?" | "**podman에서 테스트컨테이너 문제에 빠졌는데 어떻게 푸는지 전혀 모르겠다.** 혹시 이걸로 싸워본 적 있나?" | [47153288](https://news.ycombinator.com/item?id=47153288) |
| `enlightens` | "The most common one I run into is with volumes, when the full path doesn't already exist. Docker will just make the path, Podman throws an error. … **Podman is technically correct here but functionally broken in a way that keeps pushing me away because I don't have time to deal with that** :(" | "가장 자주 만나는 건 볼륨이다. 전체 경로가 아직 없을 때 도커는 그냥 경로를 만들어주는데, 팟맨은 에러를 던진다. … **팟맨이 기술적으로는 옳지만, 나를 계속 밀어내는 방식으로 기능적으로 망가져 있다. 그걸 붙들고 있을 시간이 없기 때문이다** :(" | [47152400](https://news.ycombinator.com/item?id=47152400) |
| `jph` | "I'm switching my teams from Docker to Podman on macOS. I'm hitting blockers for multi-user setups i.e. each developer has a non-admin account on the machine, whereas brew runs in its own account with admin permissions." | "macOS에서 팀을 Docker에서 Podman으로 옮기는 중인데, 멀티유저 셋업에서 막혔다. 개발자마다 머신에 비관리자 계정을 쓰는데, brew는 관리자 권한을 가진 자기 계정에서 돈다." | [47155635](https://news.ycombinator.com/item?id=47155635) |

- **쓸 곳:** ⭐ `enlightens`의 "technically correct but functionally broken" — **이 책 전체에서 쓸 만한 문장**이다. "표준을 지키는 것"과 "사람들이 쓰는 것"의 간극. 대안 런타임 챕터 마무리 후보. `p0w3n3d`의 Testcontainers 언급은 C-1의 `tsfenwick`과 함께 **"Podman + Testcontainers"가 2026년에도 살아 있는 마찰**임을 보여준다(2건, 서로 다른 스레드).

---

# 🔴 2순위 — "완전히 0건"이던 일화들

## D. 맥 메모리·디스크 할당 튜닝 실패담 — ✅ **확보 (대량)**

> §7-3 #5: "맥 메모리 할당 튜닝 실패담 — 이슈 제목 + 체감 2건뿐." → **해소.** 아래는 본문·댓글을 전부 열어 읽은 것이다.

### D-1. ⭐⭐⭐ "6GB를 주랬더니 11.5GB를 쓴다" — `com.docker.krun` 메모리 이슈

- **출처:** GitHub — https://github.com/docker/for-mac/issues/7749 ("com.docker.krun using insane amount of memory", 등록 2025-08-21, 댓글 22, 조회 2026-07-25 시점 **OPEN**)
- **인용 등급:** 축자 인용 가능 (`gh issue view --comments`로 본문·댓글 전문 열람)

**증상 보고 (`bastibense`, Docker Desktop 4.44.3 / Docker VMM):**
> "Same here, set Docker Desktop to use 6 GB of RAM, instead it uses 11,5 GB. Using Docker VMM."
(번역: "여기도 같다. **Docker Desktop에 램 6GB를 쓰라고 설정했는데, 대신 11.5GB를 쓴다.** Docker VMM 사용 중.")

**규모가 커진다 (`YoannD42`, Docker Desktop 4.45.0 / Docker VMM):**
> "Same issue here, **it went up to 40GB on our macs with colleagues.** Easily reproducible, just need to let even A container run, for a few hours, and the memory use goes up. **Only releases memory, when restarting docker desktop.**"
(번역: "여기도 같은 문제다. **동료들과 우리 맥에서 40GB까지 올라갔다.** 재현하기 쉽다. 컨테이너 **하나**만 몇 시간 돌게 놔두면 메모리 사용량이 올라간다. **도커 데스크톱을 재시작해야만 메모리를 반환한다.**")

**⭐⭐ 극단값 (`bastibense`):**
> "Can confirm this, **today I had 122 GB RAM usage for a container that usually took up like 200 MB.**"
(번역: "확인한다. **오늘 평소 200MB쯤 쓰던 컨테이너 하나에 램 사용량 122GB가 찍혔다.**")

**⭐ 발열·팬 증언 (`Fail-Safe`) — §7-3 #4의 인접 자료:**
> "I'm seeing this behavior as well, though I became aware of something amiss based on CPU usage. While I also see the ever-increasing memory usage, **I notice my MacBook M3 machine getting noticeably warm, which is rare. CPU usage stays constant at ~200%**"
(번역: "나도 이 동작을 본다. 다만 내가 뭔가 잘못됐다는 걸 알아차린 건 CPU 사용률 때문이었다. 메모리가 계속 늘어나는 것도 보이지만, **내 MacBook M3가 눈에 띄게 뜨거워지는 게 느껴진다. 드문 일이다. CPU 사용률은 ~200%로 계속 고정돼 있다.**")

**(`VikiAnn`) — 컨테이너를 안 돌리는데도:**
> "My macbook rebooted overnight and Docker is not running now (`docker ps` in the terminal gives me the "is the docker daemon running?" message) but **I have a `com.docker.krun` process in Activity Monitor that's using almost 140 GB memory and like 668% CPU (it's running loudly, too.)**"
(번역: "맥북이 밤새 재부팅됐고 지금 도커는 안 돌고 있다(터미널에서 `docker ps`를 치면 '도커 데몬이 돌고 있냐'는 메시지가 나온다). 그런데 **활성 상태 보기에 `com.docker.krun` 프로세스가 메모리 140GB 가까이와 CPU 668%쯤을 쓰고 있다(팬도 시끄럽게 돌고 있다).**")

**⭐⭐ 🟢 Docker 컨트리뷰터의 진단 (`djs55`, association: contributor):**
> "Thanks for the report. **The current theory is that the memory is being miscounted by the "footprint" metric** (the one labelled "Memory" in Activity Monitor), leading to the process appear to leak over time. In practice the VM is signalling free memory to the host and macOS is informed with `madvise` … that it can drop the contents, but the footprint metric doesn't currently reflect that reliably. We're investigating various options.
> Perhaps try adding other memory columns in Activity Monitor (View Menu -> Columns -> ...) and see how they compare to the footprint metric."

(번역: "보고 감사하다. **현재 가설은 '풋프린트' 지표**(활성 상태 보기에서 '메모리'라고 붙은 것)**가 메모리를 잘못 세고 있다는 것**이다. 그래서 프로세스가 시간이 갈수록 새는 것처럼 보인다. 실제로는 VM이 호스트에 여유 메모리를 신호로 보내고 macOS는 `madvise`로 내용을 버려도 된다고 통보받는데, 풋프린트 지표가 아직 그걸 안정적으로 반영하지 못한다. 여러 선택지를 조사 중이다. / 활성 상태 보기에 다른 메모리 열을 추가해서(보기 메뉴 → 열 → …) 풋프린트 지표와 비교해보면 어떨까.")

**⭐⭐⭐ 그리고 그 진단이 반박된다 (`YoannD42`):**
> "@djs55 Thank you, for me shows 45GB (well well...) of memory, 7.2 of real memory; Container memory usage shows, 5.3GB at the same time. **Nonetheless, the mac displays memory pressure in red, things get in swap, seems like it's not only a display thing, or at least the OS is actively acting upon it, by sabotaging the rest.**"
(번역: "@djs55 감사하다. 나는 메모리 45GB(허허…), 실제 메모리 7.2GB로 나온다. 같은 시각 컨테이너 메모리 사용량은 5.3GB로 표시된다. **그런데도 맥은 메모리 압력을 빨간색으로 표시하고, 스왑으로 넘어간다. 단순히 표시 문제만은 아닌 것 같다. 적어도 OS가 그걸 근거로 실제로 행동해서 나머지를 방해하고 있다.**")

- **🟢 컨트리뷰터의 재답변:** "This is a definite possibility. We're looking at other APIs to inform macOS that the memory is free."
  (번역: "충분히 가능한 이야기다. macOS에 메모리가 비었다고 알릴 다른 API들을 보고 있다.")

**그리고 사람들이 떠난다:**
- `pavlealeksic`: "a fix seems to be to change from docker VMM to Apple Virtualization Framework and enabling rosetta in the general settings" (번역: "해결책은 Docker VMM에서 Apple Virtualization Framework로 바꾸고 일반 설정에서 rosetta를 켜는 것 같다.")
- `iammikeb`: "**Got tired of waiting and made the jump to OrbStack.** It was painless with automatic DD migration and far more efficient on MacOS. I don't see myself going back at this point."
  (번역: "**기다리다 지쳐서 OrbStack으로 건너뛰었다.** 자동 DD 마이그레이션이 있어서 고통 없었고 macOS에서 훨씬 효율적이다. 이 시점에 돌아갈 일은 없어 보인다.")

- **⭐ 왜 이게 이 책에 중요한가:**
  1. **"화면에 뜬 숫자가 진짜인가"라는 질문이 실제 논쟁**이 됐다. 이 책의 §2-3(클라이언트/데몬 분리)·§1-3(맥에 VM이 낀다)이 만드는 인지 왜곡의 살아 있는 사례다.
  2. **사용자가 설정한 한도(6GB)와 실제 관측치(11.5GB)가 어긋난다** — "메모리 슬라이더를 조절하면 된다"는 흔한 처방을 정면으로 흔든다.
  3. **`Fail-Safe`의 발열 증언과 `VikiAnn`의 "팬이 시끄럽다"**는 §7-3 #4(배터리·발열)에 **가장 근접한** 실제 증언이다 — 다만 **로컬 K8s가 아니라 Docker Desktop 자체**에 대한 것이다. 혼동해서 쓰지 말 것.
- **쓸 곳:** ⭐⭐⭐ **맥 리소스 챕터의 오프닝으로 가장 강한 후보.** "6GB를 주랬더니 11.5GB를 쓴다" 또는 "200MB짜리 컨테이너에 122GB가 찍혔다"로 열 수 있다. 오프닝 기법은 **충격적 수치** 또는 **실패 장면**.
- **📌 fact-checker 주의:** 이 이슈는 **2026-07-25 조회 시점 OPEN**이며 원인 규명이 진행 중이다. 본문에서 **"이건 버그다"로 단정하지 말 것.** 🟢 컨트리뷰터의 가설(풋프린트 지표 오계수)과 🟡 사용자들의 반박(스왑이 실제로 발생)을 **양쪽 다 적을 것.**

### D-2. 📒 디스크 관련 이슈 (제목·상태·날짜만 — 본문 미열람)

⛔ **아래는 §3 A18과 동일한 제한이 걸린다. 인용·해석 금지, 분포 근거로만.**

| 이슈 | 제목 | 등록일 | 2026-07-25 상태 |
|---|---|---|---|
| docker/for-mac#7576 | Docker not respecting disk usage limit | 2025-02-02 | OPEN (댓글 0) |
| docker/for-mac#7530 | Unable to increase disk size above 2 TB | 2025-01-09 | OPEN (댓글 0) |
| docker/for-mac#7834 | Docker Desktop crashes on startup with disk.extend panic after update | 2026-01-23 | OPEN (댓글 1) |
| docker/for-mac#7766 | The disk image couldn't be opened: Failed to mount filesystems | 2025-09-24 | CLOSED |

- **✅ 한 건은 본문을 열었다** — docker/for-mac#7517 "Simple Way to Shrink Docker.raw Disk"(2025-01-02, CLOSED). 유일한 댓글은 Docker 컨트리뷰터 `bsousaa`의 **"closing as duplicate of https://github.com/docker/roadmap/issues/771"** 한 줄이다. 즉 **"Docker.raw를 줄여달라"는 요청이 로드맵 이슈로 넘어가 있는 상태**라는 사실만 확인됐다. 그 로드맵 이슈는 열지 않았다.
- **쓸 곳:** "디스크가 안 줄어든다"가 **개별 버그가 아니라 로드맵 항목**이라는 사실. 1차의 A15(Rancher Desktop 디스크 100%)와 짝. **인용문은 위 한 줄뿐이다.**

---

## E. 취약점 스캔 알림 피로 — ✅ **확보 (단, 컨테이너 이미지가 아니라 의존성 스캐너)**

> §7-3 #3: "취약점 스캔 도입 후의 알림 피로 — 자료 없음." → **부분 해소.**
> ⚠️ **중요한 단서:** 확보한 자료는 **Dependabot/Snyk/Trivy 의존성 스캔** 이야기다. **`docker scout`·Trivy로 컨테이너 이미지를 스캔한 뒤의 알림 피로 증언은 이번에도 0건**이다. 본문에서 "컨테이너 이미지 스캔"의 근거로 곧장 옮기면 과잉 일반화다.

### E-1. ⭐⭐⭐ "Dependabot을 꺼라" — 2026년 2월, 647 points

- **출처:** Hacker News — https://news.ycombinator.com/item?id=47094192 ("Turn Dependabot off", 제출 2026-02-20, **647 points**, 검색: 2026-07-25). 원문은 Filippo Valsorda의 words.filippo.io
- **인용 등급:** 축자 인용 가능 (HN 댓글). ⚠️ 블로그 원문 미열람 — **글쓴이의 주장은 인용 금지**, 댓글만

**⭐⭐⭐ 알림 피로의 정의에 가장 가까운 문장 (`indiekitai`, 2026-02-21):**
> "The core problem is that Dependabot treats dependency graphs as flat lists. It knows you depend on package X, and X has a CVE, so it alerts you. **But it has no idea whether you actually call the vulnerable code path.** …
> **The irony is that Dependabot's noise makes teams less secure, not more. When every PR has 12 security alerts, people stop reading them. Alert fatigue is a real attack surface.**"

(번역: "핵심 문제는 Dependabot이 의존성 그래프를 **평평한 목록**으로 다룬다는 것이다. 당신이 패키지 X에 의존하고 X에 CVE가 있다는 것만 알고, 그래서 알린다. **그런데 당신이 취약한 코드 경로를 실제로 호출하는지는 전혀 모른다.** … / **아이러니는, Dependabot의 소음이 팀을 더 안전하게가 아니라 덜 안전하게 만든다는 것이다. 모든 PR에 보안 경고가 12개씩 붙으면 사람들은 그걸 읽기를 멈춘다. 알림 피로는 실재하는 공격 표면이다.**")

**⭐ 구체적 사례 (`nfm`, 2026-02-20):**
> "**The number of ReDoS vulnerabilities we see in Dependabot alerts for NPM packages we're only using in client code is absurd.** I'd love a fix for this that was aware of whether the package is running on our backend or not. Client side ReDoS is not relevant to us at all."
(번역: "**클라이언트 코드에서만 쓰는 NPM 패키지에 대해 Dependabot 경고로 뜨는 ReDoS 취약점 개수가 터무니없다.** 그 패키지가 우리 백엔드에서 도는지 아닌지를 아는 수정이 있으면 좋겠다. 클라이언트 사이드 ReDoS는 우리와 전혀 무관하다.") — https://news.ycombinator.com/item?id=47094795

**(`adverbly`, 2026-02-20):** "We also suffer from this. Although in some cases it's due to a Dev dependency. **It's crazy how much noise it adds specifically from ReDoS...**"
(번역: "우리도 이걸로 고생한다. 어떤 경우엔 개발 의존성 때문이기도 하다. **특히 ReDoS에서 붙는 소음의 양이 미친 수준이다…**") — https://news.ycombinator.com/item?id=47095051

**(`monkpit`, 2026-02-21):** "ReDoS cves in your dev dependencies like playwright that could literally never be exploited, so annoying."
(번역: "playwright 같은 개발 의존성에 뜨는, 말 그대로 절대 익스플로잇될 수 없는 ReDoS CVE들. 정말 짜증난다.") — https://news.ycombinator.com/item?id=47097224

**⭐ 자바 독자 정조준 — 스레드 안에서 JVM 도구를 묻는 대목:**
- `bpavuk` (2026-02-20): "is there a `govulncheck`-like tool for the JVM ecosystem? I heard Gradle has something like that in its ecosystem. search revealed Sonatype Scan Gradle plugin. how is it?"
  (번역: "JVM 생태계에 `govulncheck` 같은 도구가 있나? Gradle 생태계에 비슷한 게 있다고 들었다. 검색해보니 Sonatype Scan Gradle 플러그인이 나오는데, 어떤가?") — https://news.ycombinator.com/item?id=47094599
- `wpollock` (2026-02-21): "It's been a few years, but for Java I used OWASP: https://owasp.org/www-project-dependency-check/, which downloads the NVD (so first run was slow) and scans all dependicies against that. I ran it from maven as part of the build."
  (번역: "몇 년 됐지만 자바에서는 OWASP dependency-check를 썼다. NVD를 내려받아(그래서 첫 실행이 느렸다) 모든 의존성을 대조 스캔한다. 메이븐에서 빌드의 일부로 돌렸다.") — https://news.ycombinator.com/item?id=47096512
- ⚠️ **`bpavuk`의 질문에 실질적 답이 하나(그것도 "몇 년 전 경험")뿐**이라는 것 자체가 관측이다. 본문에서 "자바 생태계엔 도달 가능성 기반 도구가 없다"로 **단정하지 말 것** — HN 한 스레드의 표본이다.

**⭐ 실무 처방 — "쿨다운"이 2025~2026의 답으로 등장한다:**
- `seg_lol` (2026-02-20): "Be wary of upgrading dependencies too quickly. This is how supply chain incursions are able to spread too quickly. **Time is a good firwall.**"
  (번역: "의존성을 너무 빨리 올리는 걸 경계하라. 공급망 침투가 너무 빨리 퍼지는 게 이 경로다. **시간은 좋은 방화벽이다.**" — 원문 오타 `firwall` 그대로) — https://news.ycombinator.com/item?id=47094562
- 🟢 **Renovate 메인테이너 `jamietanna` (2026-02-20):** "Yep, and we've had it for a while in Renovate too … (I'm a Renovate maintainer) (I agree with Filippo's post and it can also be applied to Renovate's security updates for Go modules - **we don't have a way, right now, of ingesting better data sources like `govulncheck` when raising security PRs**)"
  (번역: "그렇다. Renovate에도 한동안 있었다 … (나는 Renovate 메인테이너다) (필리포의 글에 동의한다. Renovate의 Go 모듈 보안 업데이트에도 적용될 수 있다 — **지금은 보안 PR을 올릴 때 `govulncheck` 같은 더 나은 데이터 소스를 흡수할 방법이 없다**)") — https://news.ycombinator.com/item?id=47094652
- `esafak` (2026-02-20): "**I automate updates with a cooldown, security scanning, and the usual tests. If it passes all that I don't worry about merging it.** When something breaks, it is usually because the tests were not good enough, so I fix them. … Better that than accrue tech debt."
  (번역: "**나는 쿨다운·보안 스캔·평소 테스트를 붙여 업데이트를 자동화한다. 그걸 다 통과하면 머지를 걱정하지 않는다.** 뭔가 깨지면 대개 테스트가 충분히 좋지 않아서라서, 테스트를 고친다. … 기술 부채를 쌓는 것보다 낫다.") — https://news.ycombinator.com/item?id=47094661

- **쓸 곳:** ⭐⭐ **취약점 스캔 챕터의 오프닝은 "CVE가 몇 개 떴다"가 아니라 `indiekitai`의 "알림 피로는 실재하는 공격 표면이다"로 뒤집어 열 수 있다** (오프닝 기법: **정의 뒤집기**). 그리고 §5/§8-4(`docker scout`)의 실무 절에는 **"쿨다운(최소 릴리스 경과 시간)"**이라는 2026년의 커뮤니티 처방을 넣을 것.
- **📌 §7-3 #3 판정:** **부분 확보.** "의존성 스캐너의 알림 피로"는 풍부하게 확보됐고, **"컨테이너 이미지 스캔의 알림 피로"는 여전히 0건**이다.

### E-2. 요약 경유(인용 불가) — 컨테이너 이미지 CVE 쪽 실마리

아래는 **HN 검색 결과 목록에서 제목·URL·점수만 확인**했고 **스레드를 열지 않았다.** ⛔ **인용 금지, 존재 근거로만.**

| 스토리 | 제목 | 시점 | 점수 |
|---|---|---|---|
| [45491911](https://news.ycombinator.com/item?id=45491911) | Vulnerability-Free Raspberry Pi Image on Chainguard OS | 2025-10-06 | 30 |
| [46978301](https://news.ycombinator.com/item?id=46978301) | The hunt for zero-CVE container images | 2026-02-11 | 3 |
| [43986405](https://news.ycombinator.com/item?id=43986405) | Wiz hardened, near-zero-CVE base images | 2025-05-14 | 6 |

- **관측:** **"제로 CVE 베이스 이미지"가 2025~2026년의 상품 카테고리로 등장했다**는 사실 자체는 확인된다(Chainguard·Wiz 양쪽). 이는 §8-3(베이스 이미지 선택)에 새 선택지 축이 생겼다는 뜻이다. 다만 **본문에 쓰려면 1차 소스(각 벤더 문서)로 다시 확인**해야 한다.

---

## F. 베이스 이미지 업데이트를 실제로 어떻게 굴리는가 — ⚠️ **부분 확보(간접)**

> §7-3 #2: "베이스 이미지 업데이트를 실제로 어떻게 굴리는가(자동화 vs 수동, 주기) — 커뮤니티 자료 없음."
> **판정: 여전히 "컨테이너 베이스 이미지" 직접 자료는 0건.** 확보한 것은 **의존성 업데이트 운영 방식**이며, E-1과 같은 스레드다.

**확보된 것 (전부 E-1 스레드, 축자 인용 가능):**
1. **자동 머지 + 쿨다운 파** — `esafak`(위 인용). 자동화하되 쿨다운·스캔·테스트를 앞에 세운다.
2. **자동 머지 반대파** — `robszumski`: "Totally hear you on the noise…but **we should want to auto-merge vs ignore, no?** Given the right tooling of course." / `dotancohen`의 답은 한 단어: "**No**" / `UqWBcuFx6NV4r`: "We could just skip some steps and I could send you a zip file of malware for you to install on your infra directly if you'd like."
   (번역: — "소음 얘기는 완전히 공감한다… 그런데 **무시하는 것보다는 자동 머지를 원해야 하지 않나?** 물론 제대로 된 도구가 있다면." / — "**아니.**" / — "몇 단계를 그냥 건너뛰고, 원한다면 내가 당신 인프라에 직접 설치할 멀웨어 zip 파일을 보내줄 수도 있다.")
   — https://news.ycombinator.com/item?id=47095246 / https://news.ycombinator.com/item?id=47095701 / https://news.ycombinator.com/item?id=47095735
3. **🟢 Renovate 메인테이너의 도구 상태 고백** — `jamietanna`(위 인용): 지금은 도달 가능성 데이터를 흡수할 방법이 없다.

- **📌 판정:** **§7-3 #2는 "여전히 0건"으로 유지한다.** "몇 주에 한 번 베이스 이미지를 올린다"류의 컨테이너 운영 주기 증언은 이번 검색에서도 나오지 않았다. **본문에서 주기·빈도를 쓰지 말 것.**
- **다만 쓸 수 있는 것:** "자동화하느냐"라는 질문에 대해 커뮤니티가 **합의하지 않았다**는 사실 자체(자동 머지 찬반이 같은 스레드에서 정면 충돌). 이건 비교 대조형 챕터의 재료가 된다.

---

## G. `latest` 태그 사고담 — ✅ **확보 (한국어, 스프링 부트)**

> §7-3 #1: "`latest` 태그 때문에 터진 구체적 사고담 — HN 전수 검색에도 일화라 부를 스레드가 없었다."
> **HN 재검색(3회)에서도 0건.** 그러나 **한국어 velog에서 스프링 부트 사례를 찾았다.**

### G-1. ⭐⭐⭐ "코드를 고쳐서 다시 빌드했는데 계속 null이 들어간다"

- **출처:** velog — https://velog.io/@vector13/springbootdocker-push한-도커-이미지가-적용이-안된다면 (게시: **2022-11-20**, 검색: 2026-07-25)
- **인용 등급:** **축자 인용 가능** (velog Apollo 상태에서 본문 원문 직접 추출)
- **원문(제목):** "[springboot&docker] push한 도커 이미지가 적용이 안된다면?"
- **⭐ 원문(발단):**
  > "그런데 실행을 시킨 후에 여러가지 코드를 고칠 것이 필요해서 코드를 고쳐서 **"같은 이름으로" 여러번 Image build, push pull을 했는데 변경 내용이 적용이 안된 문제**를 만났다."
- **⭐⭐ 원문(증상 — 구체적이라 오프닝에 쓸 수 있다):**
  > "**문제** : spring 처음에 띄운 것 대로 nickname이 null로 들어가고, "kakao", "apple"처럼 fix 된 string을 넣도록 코드를 고쳐서 다시 docker image 빌드를 했으나 **계속해서 nickname이 null로 들어가는 문제 발생**"
- **⭐⭐ 원문(원인 추정 — 본인이 확신하지 못한다는 게 중요하다):**
  > "**문제 예상 원인** : docker Image의 버전관리를 안하고 **"같은 이름"으로, "같은 태그"인 latest 로 계속 배포했던 것 때문에** 변경된 코드가 적용이 안됐을 것이라고 예상. **Ec2에서 docker가 어떤 생태 흐름으로 흘러가는지는 모르나,** docker image를 다운받아 저장하는 repository가 따로 있을 것이고, 여기서 docker image의
  > - 1 이름이 같거나 특정 어떤것이 같다면 이전의 이미지를 run 시키거나
  > - 2 저장된 이미지 이름은 여러개 (pull여러번 받아서) `sudo docker run` 자체가 image 이름으로 run 시키므로, **가장 앞의(다운 받은지 오래된) 이미지를 run 시킬 가능성이 있다.**"
- **⭐ 원문(무지의 자백 — 인용 가치가 높다):**
  > "이제까지 무지성으로 사용했던 `$ docker image build -t javatest:latest` 의 -t 명령어가 이름과 태그를 붙이는 옵션이었다. **태그명은 생략 가능한데, 생략하면 기본적으로 `latest`가 붙는다**"
- **원문(관측 — EC2에 같은 이름 이미지가 3개):**
  > "문제가 발생한 ec2에서 docker 이미지를 확인해보면 **같은 이름으로 3개가 있다.**"
- **원문(해결):** 태그를 `v1`으로 붙여 빌드·push → EC2에서 기존 컨테이너 stop·rm → `:v1`으로 pull·run.

- **맥락:** 스프링 부트 애플리케이션(`ae_SpringServer-0.0.1-SNAPSHOT.jar`)을 EC2에 배포하던 개발자. **버그를 고쳤는데 고쳐지지 않았고, 원인이 코드가 아니라 태그였다.**
- **⚠️ 정직한 한계:**
  - **2022년 글**이다(3년 반 전). 본문에서 "최근"이라고 쓰지 말 것.
  - **운영 장애가 아니라 개발/실습 성격**의 배포다. "프로덕션 사고"로 격상하지 말 것.
  - **본인도 원인을 확정하지 못했다** — "예상 원인"이라고 스스로 적었다. **"latest 때문이었다"로 단정하지 말고, "본인이 latest를 원인으로 지목했고 태그를 붙여 해결했다"로 쓸 것.**
  - 저자가 추정한 메커니즘("가장 앞의 오래된 이미지를 run") 자체는 **기술적으로 부정확할 수 있다.** ⛔ **이 추정을 사실로 옮기지 말 것.** §7-3 #1이 권한 대로 **정확한 메커니즘은 kind 문서의 pull policy 규칙(`:latest`면 기본 `Always`) 등 1차 소스로 설명**하고, 이 글은 **"사람이 겪는 증상"의 증거로만** 쓸 것.
- **쓸 곳:** ⭐⭐⭐ **이미지 태그 챕터의 오프닝.** 오프닝 기법 **실패 장면**. 자바·스프링·한국어·구체적 증상이 한 글에 다 있다 — 이 책의 독자가 자기 얼굴을 볼 수 있는 몇 안 되는 자료다.

### G-2. 📌 확정 — 영어권 `latest` 사고담은 **재검색에도 0건**

- 시도: HN Algolia 코멘트 검색 3회 — `latest tag docker deployed wrong` / `docker latest tag production incident` / `pinning image tags rollback`, 전부 2024-01-01 이후 필터. **결과 0건.**
- 1차 리서치의 "HN 전수 검색에도 없다"를 **재확인**한다. **부재는 확정적이다**(HN 범위 안에서).

---

## H. 로컬 K8s의 맥북 배터리·발열 — ❌ **여전히 0건 (재확인)**

> §7-3 #4: "로컬 K8s(kind/minikube/k3s/Docker Desktop 내장)의 맥북 배터리·메모리 소모 비교 — 수치 자료 없음. 체감 증언 1건뿐."

- **시도:** HN 코멘트 검색 3회(`minikube kind laptop battery` / `local kubernetes laptop fan` / `kind vs minikube local development`, 2024 이후). **직결 결과 0건**(구인 광고·무관 스레드만 반환).
- **판정: 여전히 0건.** 배터리·발열을 **로컬 K8s에 귀속**시키는 증언은 이번에도 못 찾았다.

**⚠️ 인접 자료는 있으나 K8s가 아니다 — 혼동 금지:**
- D-1의 `Fail-Safe`("MacBook M3가 눈에 띄게 뜨거워진다, CPU ~200%")와 `VikiAnn`("팬도 시끄럽게 돌고 있다")은 **Docker Desktop의 `com.docker.krun` 메모리 이슈**에 대한 것이다. **로컬 K8s를 켜서 그런 게 아니다.**
- 📒 **제목·상태만 확인:** docker/for-mac#7648 "Resource Saver does not kick in with Kubernetes enabled"(2025-04-07 등록, 2026-07-25 조회 시점 OPEN). **본문·유일한 댓글을 열었으나**, 유일한 댓글(`segevfiner`)은 트레이 아이콘 표시에 관한 것이고 **배터리·발열·전력을 언급하지 않는다.**
  > "Hmmm it could also be that the Docker icon in the task tray no longer shows the leaf icon when resource saver is kicking in... Cause when I manually pause, the icon doesn't change either..."
  (번역: "음, 리소스 세이버가 작동할 때 작업 트레이의 도커 아이콘이 잎사귀 아이콘을 더 이상 안 보여주는 것일 수도 있다… 수동으로 일시정지해도 아이콘이 안 바뀌니까…")
  - ⚠️ 이건 **"K8s를 켜면 절전이 안 든다"는 메커니즘 가설의 존재**를 보여줄 뿐, **배터리 소모 증언이 아니다.** 본문에서 "K8s를 켜두면 배터리가 빨리 닳는다"고 쓰려면 **이 이슈를 근거로 삼을 수 없다.**
- **📌 저술 지침:** 이 주제는 **범위에서 빼거나**, 쓰더라도 "커뮤니티에 비교 자료가 없다"는 **검증된 부재**로 다룰 것. §5-7(성능에 대해 정직하게 말하기)과 같은 처리.

---

# 🟡 3순위 — 자바·스프링 독자 정조준

## I. Testcontainers 실사용 고통 (2025~2026 신규)

### I-1. ⭐⭐⭐ "Rancher Desktop을 못 알아본다" — 2.0.1은 되고 2.0.2는 안 된다

- **출처:** GitHub — https://github.com/testcontainers/testcontainers-java/issues/11254 ("[Bug]: Can't overwrite Docker socket path with 2.0.2 / Podman stopped working", 등록 2025-12-01, 댓글 8, 조회 2026-07-25 시점 **OPEN**)
- **인용 등급:** 축자 인용 가능 (본문·댓글 전문 열람)

**⭐⭐ 🟢 메인테이너의 한마디 (`eddumelendez`, association: **member**):**
> "I would like to know when we broke this. Version 2.x doesn't have changes related to this, it has been more related to dependencies and JUnit 4 drop support."
(번역: "**우리가 언제 이걸 망가뜨렸는지 알고 싶다.** 2.x 버전에는 이와 관련된 변경이 없다. 의존성과 JUnit 4 지원 중단 쪽이었다.")

**⭐⭐⭐ 컨트리뷰터의 이등분 탐색 (`linghengqian`, association: contributor, 2025-12-17 로그 포함):**
> "Although … 2.0.3 has been released, my tests show that Maven modules, including `org.testcontainers:testcontainers-postgresql:2.0.3`, **still cannot detect Docker Engine 28.3.3 provided by Rancher Desktop 1.20.1. Of course, the testcontainers' GitHub actions file does not test either Rancher Desktop or Docker Desktop.**"

(번역: "… 2.0.3이 릴리스됐지만, 내 테스트로는 `org.testcontainers:testcontainers-postgresql:2.0.3`을 포함한 메이븐 모듈들이 **Rancher Desktop 1.20.1이 제공하는 Docker Engine 28.3.3을 여전히 감지하지 못한다. 물론 테스트컨테이너의 GitHub Actions 파일은 Rancher Desktop도 Docker Desktop도 테스트하지 않는다.**")

- **⭐ 첨부된 실제 오류 로그(축자):**
  > `[ERROR] 2025-12-17 10:38:58.557 [main] o.t.d.DockerClientProviderStrategy - Could not find a valid Docker environment. Please check configuration. Attempted configurations were: NpipeSocketClientProviderStrategy: failed with exception RuntimeException (…MalformedChunkCodingException: Bad chunk header: )…`
  > `java.lang.IllegalStateException: Could not find a valid Docker environment. Please see logs and check configuration`
  > `at org.testcontainers.DockerClientFactory.getOrInitializeStrategy(DockerClientFactory.java:154)`
  > `at com.zaxxer.hikari.pool.HikariPool …`

- **⭐⭐ 이등분 결과(축자):**
  > "I did an even more interesting test: even `org.testcontainers:testcontainers-postgresql:2.0.1`, it still correctly detected Docker Engine 28.3.3 in Rancher Desktop 1.20.1. **Only `org.testcontainers:testcontainers-postgresql:2.0.2` and `org.testcontainers:testcontainers-postgresql:2.0.3` failed** to detect Docker Engine 28.3.3 in Rancher Desktop 1.20.1.
  > To be honest, **I don't see any disruptive changes in the changelog.**"

  (번역: "더 흥미로운 테스트를 했다. `2.0.1`은 Rancher Desktop 1.20.1의 Docker Engine 28.3.3을 여전히 제대로 감지했다. **`2.0.2`와 `2.0.3`만 감지에 실패했다.** 솔직히 **체인지로그에서 파괴적 변경을 하나도 못 찾겠다.**")

- **⭐ 사용자 쪽 가설 (`mpolonio`):**
  > "I do not know but I think in our case the situation arised because **we have automatic updates enabled on Docker Desktop** and they should have updated the Docker server version to one in which included some change in the way to request for the docker Unix socket path.... or at least that is what some people were commenting"
  (번역: "모르겠지만 우리 경우엔 **Docker Desktop 자동 업데이트를 켜놨기 때문에** 상황이 생긴 것 같다. 도커 서버 버전이 도커 유닉스 소켓 경로를 요청하는 방식에 변경이 들어간 버전으로 올라갔을 것이다… 적어도 몇몇 사람들이 그렇게 얘기하고 있었다.")
  - 그리고 그는 **Docker Desktop을 쓰는데도 같은 증상**을 겪었다: "I think it is happening also for me on MacOS with Docker Desktop"

- **⭐⭐⭐ 왜 이게 이 책에 중요한가:**
  1. **"라이브러리 마이너 버전 하나(2.0.1→2.0.2)가 런타임 감지를 깨뜨렸다"** — 자바 개발자가 통제하지 못하는 층에서 문제가 난다. 1차 A13(Ryuk이 소켓을 못 찾음)과 **같은 계열, 3년 뒤, 다른 원인.**
  2. **"테스트컨테이너의 CI는 Rancher Desktop도 Docker Desktop도 테스트하지 않는다"** — 이 한 문장이 **맥 개발자가 왜 계속 얻어맞는지에 대한 구조적 설명**이다. 🟢 컨트리뷰터 발언.
  3. **자동 업데이트가 범인 후보다** — 1차의 A6(Docker Desktop 4.26.1→4.27.1 업데이트 후 JVM 세그폴트)과 같은 패턴.
- **쓸 곳:** ⭐⭐⭐ Testcontainers 챕터 오프닝 또는 §5-6 보강. 오프닝 기법 **실패 장면** 또는 **정의 뒤집기**("내 코드도, 내 도커도 안 바뀌었는데 테스트가 죽었다").
- **📌 fact-checker 주의:** 이 이슈는 **2026-07-25 조회 시점 OPEN**이고 원인이 확정되지 않았다. `linghengqian`의 이등분은 **본인 환경 1개**의 결과다. "2.0.2에서 회귀가 있었다"로 단정 금지, "한 컨트리뷰터가 그렇게 이등분해 보고했고 메인테이너도 원인을 모른다고 말했다"까지.

### I-2. ⭐⭐ Ryuk 비활성화 — 2026년 1월, 요청은 올라왔고 **메인테이너가 기각했다**

> 1차가 잡은 논쟁: `TESTCONTAINERS_RYUK_DISABLED=true` 복붙 확산 vs 메인테이너의 반박(§4-3).
> **최신 상태(2026-02-03): `testcontainers.properties`로 끄게 해달라는 요청과 PR이 올라왔으나, 메인테이너가 "빌드 도구 설정으로 같은 목적을 달성할 수 있다"며 PR을 닫았다. 병합되지 않았다.**
> **검증:** `gh pr view 11414 --json state,mergedAt,mergedBy,mergeCommit` → `state: CLOSED`, **`mergedAt: null`, `mergedBy: null`, `mergeCommit: null`** (2026-07-25 조회). ⛔ **"Testcontainers가 `ryuk.disabled` 프로퍼티를 지원한다"는 서술은 틀린다.**

- **출처:** GitHub — https://github.com/testcontainers/testcontainers-java/issues/11413 ("[Feature]: Allow setting TESTCONTAINERS_RYUK_DISABLED via testcontainers.properties", 등록 2026-01-05, CLOSED) / 대응 PR https://github.com/testcontainers/testcontainers-java/pull/11414 ("Add property ryuk.disabled", 2026-01-05 등록, **2026-02-03 미병합 CLOSED**)
- **인용 등급:** 축자 인용 가능 (이슈·PR 코멘트 열람)
- **⭐ PR 리뷰에서 잡힌 것 (`VolkovIO`, 2026-01):**
  > "One small thing I noticed: previously **Ryuk was enabled by default and only disabled when `TESTCONTAINERS_RYUK_DISABLED=true` was set.**
  > With your PR code: `Boolean.parseBoolean(getEnvVarOrProperty("ryuk.disabled", "true"))`
  > **if neither the env var nor the property is present, Ryuk ends up being disabled by default. This changes old behavior.** It should probably use `"false"` as the default value"

  (번역: "작은 것 하나를 발견했다. 이전엔 **Ryuk이 기본으로 켜져 있고 `TESTCONTAINERS_RYUK_DISABLED=true`가 설정될 때만 꺼졌다.** / 당신 PR 코드로는: `Boolean.parseBoolean(getEnvVarOrProperty("ryuk.disabled", "true"))` / **환경변수도 프로퍼티도 없으면 Ryuk이 기본으로 꺼져버린다. 이건 기존 동작을 바꾼다.** 기본값으로 `"false"`를 써야 할 것 같다.")
- **PR 작성자의 답 (`joca-bt`):** "I missed that, thanks! I'm unable to run the tests, but I'd imagine they would catch that."
  (번역: "놓쳤다, 고맙다! 테스트를 못 돌리는 상황인데, 테스트가 잡아줬으리라 생각한다.")

- **⭐⭐ 그리고 PR은 이렇게 닫혔다 — 🟢 메인테이너 `eddumelendez`(member), 2026-02-03:**
  > "Hi, you can achieve the same goal configuring your build tool
  > **Maven**
  > ```xml
  > <plugin>
  >     <groupId>org.apache.maven.plugins</groupId>
  >     <artifactId>maven-surefire-plugin</artifactId>
  >     <configuration>
  >         <environmentVariables>
  >             <TESTCONTAINERS_RYUK_DISABLED>true</TESTCONTAINERS_RYUK_DISABLED>
  >         </environmentVariables>
  >     </configuration>
  > </plugin>
  > ```
  > **Gradle**
  > ```groovy
  > tasks.named("test", Test) {
  >   environment "TESTCONTAINERS_RYUK_DISABLED", "true"
  > }
  > ```"

  (번역: "안녕하세요, **빌드 도구를 설정해서 같은 목적을 달성할 수 있습니다.**" + Maven surefire / Gradle test 태스크의 환경변수 설정 예제)
  — https://github.com/testcontainers/testcontainers-java/pull/11414#issuecomment-3843490159 (이 코멘트 시각이 PR의 `closedAt`과 정확히 일치한다: `2026-02-03T20:28:14Z`)

- **⭐⭐⭐ 이 일화의 값어치 — 두 겹이다:**
  1. **"Ryuk을 끄는 기능을 추가하는 PR에서, 실수로 Ryuk이 기본으로 꺼질 뻔했다."** 정리 컨테이너를 끄는 우회가 얼마나 깊이 일상화됐는지, 그리고 **기본값 하나가 뒤집히는 게 얼마나 쉬운지**를 동시에 보여준다.
  2. **그런데 그 PR은 병합되지 않았다.** 메인테이너의 답은 "환영한다"가 아니라 **"이미 빌드 도구로 할 수 있다"**였다. 즉 §4-3의 메인테이너 입장은 **2026년에도 유지된다** — Ryuk 비활성화를 **라이브러리 1급 설정으로 승격시키지는 않겠다**는 것.
- **쓸 곳:** ⭐ §4-3(Ryuk 우회 논쟁) 보강. 논쟁의 결말을 **"공식 경로가 생겼다"로 쓰면 틀린다.** 정확히는 **"요청은 반복되고, 메인테이너는 매번 우회 방법을 알려주며 반려한다"**다. 오프닝 기법 **정의 뒤집기**.
- **✅ 검증 완료 항목:** PR 미병합(`mergedAt: null`), 반려 사유(위 인용), 반려 시각(2026-02-03) 전부 확인.
- **📌 fact-checker 주의:** 위에 인용한 Maven/Gradle 설정 스니펫은 **메인테이너가 코멘트에 적은 것**이다. 본문에 실행 가능한 예제로 옮기려면 각 플러그인 문서로 1차 확인할 것.

### I-3. Podman + Testcontainers 마찰 — 2026년에도 2건 (위에서 인용)

- `tsfenwick`, 2026-07-02 — https://news.ycombinator.com/item?id=48766152 (C-1 참조)
- `p0w3n3d`, 2026-02-25 — https://news.ycombinator.com/item?id=47153288 (C-4-e 참조)
- **관측:** 두 건 다 **원인 규명 없이 "모르겠다" 또는 "도커로 돌아갔다"로 끝난다.** 1차의 A13(2022, Colima)과 합치면 **"대안 런타임 + Testcontainers = 미해결 마찰"이 4년째 반복되는 패턴**이라고 말할 수 있다.
- **⚠️ 단, 표본은 3건이다.** "항상 깨진다"로 일반화 금지.

### I-4. 📒 Testcontainers 관련 최신 이슈 (제목·상태·날짜만 — 본문 미열람)

⛔ **인용·해석 금지. 분포 근거로만.**

| 이슈 | 제목 | 등록일 | 상태(2026-07-25) |
|---|---|---|---|
| tc-java#11860 | [Bug]: PostgreSQL container intermittently fails to start with "Wait strategy failed. Container is removed" (TimeoutException) in CI environment | 2026-06-30 | OPEN |
| tc-java#11724 | [Bug]: SIGSEGV (Segmentation Fault) during Docker environment detection on OpenJDK 25 / Ubuntu 24.04 | 2026-04-25 | CLOSED |
| tc-java#11713 | [Bug]: macOS docker-credential-desktop - "IntelliJ IDEA.app" would like to access data from other apps. | 2026-04-16 | CLOSED |
| tc-java#9140 | Improve support for alternative container runtimes | 2024-08-22 | OPEN |
| tc-java#8869 | Support docker socket overrides to be set in `~/.testcontainers.properties` | 2024-07-10 | OPEN |
| tc-java#10528 | [Bug]: LocalStack fails on macOS/colima with socket creation error | 2025-07-24 | CLOSED |
| tc-java#11342 | [Bug]: LocalStackContainer - Lambda function doesn't work in MacOS Colima environment | 2025-12-11 | CLOSED |
| docker/for-mac#7787 | Docker Desktop on macOS no longer reports HostIp/HostPort bindings (empty in docker inspect) causing broken HTTP behavior in Keycloak and Testcontainers | 2025-10-16 | OPEN |

- **⭐ 분포만으로 말할 수 있는 것:** **`#9140`("대안 컨테이너 런타임 지원 개선")이 2024-08 등록 이후 2026-07-25까지 OPEN**이고, 소켓 오버라이드 관련 요청(`#8869`, 2024-07)도 **2년째 OPEN**이다. 이건 §7-3 A18과 같은 "존속 기간" 근거로 쓸 수 있다.

---

## J. `bootBuildImage` / Paketo — 2025년 신규 사례

### J-1. ⭐⭐⭐ containerd 이미지 스토어가 `imagePlatform`을 깨뜨리는 정확한 메커니즘

- **출처:** GitHub — https://github.com/spring-projects/spring-boot/issues/46674 ("Image building may fail when specifying a platform if an image has already been built with a different platform", 등록 2025-08-05, 댓글 6, **CLOSED** — PR #47292로 대체)
- **인용 등급:** 축자 인용 가능
- **⭐⭐ 컨트리뷰터의 근본 원인 분석 (`hojooo`, association: contributor):**
  > "While testing this issue with Docker Desktop's **"Use containerd for pulling and storing images"** enabled, I observed that current Docker API usage supports multi-arch during pull/create, **but not during inspect/export.**
  > ### Environment
  > * Docker Engine API: **v1.51** … * Docker Desktop: M1 processor, **Use containerd for pulling and storing images = ON**
  > ```gradle
  > bootBuildImage {
  >   builder = "paketobuildpacks/builder-noble-java-tiny:latest"
  >   imageName = "demo:v1"
  >   imagePlatform = "linux/amd64"
  >   buildpacks = ["paketobuildpacks/java","paketobuildpacks/opentelemetry:2"]
  > }
  > ```
  > ### What's happening
  > * With the **containerd** image store, a tag like `builder-noble-java-tiny:latest` is kept as a **multi-platform index (manifest list)** locally.
  > * `DockerApi` still inspects images using **API v1.41**, where `GET /images/{name}/json` does **not** support selecting a platform. In this case the daemon resolves the index using the **host default platform** (on Apple Silicon -> `linux/arm64`).
  > * Meanwhile `bootBuildImage` is asking for `linux/amd64`. Result: **inspect sees arm64** but the build requires **amd64** → *platform mismatch*.
  > ### Workarounds for affected users (temporary)
  > * Set `DOCKER_DEFAULT_PLATFORM=linux/amd64` or
  > * Disable the containerd image store temporarily"

  (번역 요약: "Docker Desktop의 **'이미지 pull·저장에 containerd 사용'을 켠 상태로** 이 이슈를 테스트하다가, 현재 Docker API 사용 방식이 pull/create 때는 멀티아키를 지원하지만 **inspect/export 때는 지원하지 않는다**는 걸 관찰했다. / 환경: Docker Engine API v1.51, Docker Desktop, **M1 프로세서**, containerd 이미지 스토어 ON. / 무슨 일이 벌어지나: containerd 이미지 스토어에서는 `builder-noble-java-tiny:latest` 같은 태그가 로컬에 **멀티플랫폼 인덱스(매니페스트 리스트)**로 보관된다. `DockerApi`는 여전히 **API v1.41**로 이미지를 inspect하는데, 거기선 `GET /images/{name}/json`이 플랫폼 선택을 지원하지 않는다. 그래서 데몬이 **호스트 기본 플랫폼**으로 인덱스를 해석한다(Apple Silicon에서는 `linux/arm64`). 한편 `bootBuildImage`는 `linux/amd64`를 요구한다. 결과: **inspect는 arm64를 보는데 빌드는 amd64를 요구** → 플랫폼 불일치. / 임시 우회: `DOCKER_DEFAULT_PLATFORM=linux/amd64`를 설정하거나, containerd 이미지 스토어를 잠시 끈다.")

- **🟢 Spring 팀 멤버의 정리 (`philwebb`, association: member):** "Closing in favor of PR #47292. Thanks @hojooo!"
- **또 다른 보고 (`hiro345g`):** "My Docker API version is 1.52 (Min 1.44), and I see the exact same 400 Bad Request error when using **Spring Boot 3.5.7**."
  (번역: "내 Docker API 버전은 1.52(최소 1.44)인데, **스프링 부트 3.5.7**에서 정확히 같은 400 Bad Request 오류를 본다.")
- **기여자 지원 대화 (`bzsil8989` / `philwebb`):** "Is this issue still available for contribution?" / "It's not assigned to anyone, but **it might be a little tricky to fix given the complexity around that area of the codebase.**"
  (번역: "이 이슈 아직 기여 가능한가?" / "아무에게도 할당 안 됐다. 다만 **코드베이스의 그 영역이 복잡해서 고치기가 좀 까다로울 수 있다.**")

- **⭐⭐⭐ 이 자료의 값:** 1차 리서치의 **H4**("Docker Desktop의 'Use containerd for pulling and storing images' 토글은 빌드 결과를 바꾼다")는 **경험칙**이었다. 이 이슈는 그 경험칙의 **정확한 메커니즘**(멀티플랫폼 인덱스 + API v1.41 inspect의 플랫폼 미지원 + 호스트 기본 플랫폼 해석)을 🟢 컨트리뷰터의 분석으로 준다. **§8-6(`--load` 문서 충돌)과 §5-2(Spring Boot 이미지 빌드)를 잇는 다리.**
- **쓸 곳:** ⭐⭐⭐ `bootBuildImage` 절의 **핵심 설명**. 다만 **본문에 쓰기 전 fact-checker가 API 버전 번호(1.41 / 1.51 / 1.52)를 1차 소스로 대조**할 것 — 이 숫자들은 **이슈 보고자의 서술**이다.
- **📌 상태:** CLOSED(PR #47292로 대체). **PR #47292가 머지됐는지, 어느 릴리스에 들어갔는지는 확인하지 않았다.** "고쳐졌다"고 쓰지 말 것.

### J-2. 📒 관련 이슈 (제목·상태·날짜만)

| 이슈 | 제목 | 등록일 | 상태 |
|---|---|---|---|
| spring-boot#48127 | New arm64 macbooks fail to bootBuildImage due to incorrect platform image | 2025-11-13 | CLOSED (댓글 0) |
| spring-boot#48128 | New arm64 macbooks fail to bootBuildImage due to incorrect platform image | 2025-11-13 | CLOSED (댓글 0) |
| spring-boot#48050 | (hiro345g가 위에서 "상세 로그"로 지목) | 2025 | 미열람 |

- **⭐ 분포만으로 말할 수 있는 것:** **"New arm64 macbooks fail to bootBuildImage due to incorrect platform image"라는 똑같은 제목의 이슈가 2025-08(#46665, 1차 확보분), 2025-11(#48127, #48128) 세 번 등록됐다.** 같은 문제를 서로 다른 사람이 최소 3번 신고했다는 뜻이다. §7-2의 "반복 패턴" 근거로 사용 가능.
- ⛔ #48127/#48128은 **댓글 0, 본문 미열람**이다. 내용 인용 금지.

---

## K. 스프링 부트 컨테이너 메모리 튜닝 실패담 — ⚠️ **부분 (자바 직결은 0건)**

- **검색:** GitHub 이슈 전역 검색(`OOMKilled spring boot container memory`, 2024-06 이후) 11건 반환. **자바/스프링의 힙-컨테이너 한도 불일치를 다룬 일화형 이슈는 0건.** 대부분 무관하거나 자동 생성 성격의 리포지터리였다.
- **판정:** 스프링 부트 앱이 컨테이너 한도를 안 봐서 OOMKilled 됐다는 **구체적 일화는 이번에도 확보 못 했다.**
- **✅ 대신 확보한 것:** 한국어 컨테이너 OOMKilled 삽질기 1건 — **L-1 참조**(단, Redis다).
- **📌 저술 지침:** §5-4(JVM과 컨테이너)는 **일화 없이 1차 소스(JVM 플래그·`UseContainerSupport`·`MaxRAMPercentage`)와 실측으로 쓰는 것**이 정확하다. 없는 일화를 만들지 말 것.

---

# 🟡 한국어 커뮤니티 — 신규 확보분

> §7-3 #12: "한국어 소스 5건 중 축자 인용 가능한 건 1건." → **이번에 축자 인용 가능한 한국어 자료 3건을 추가 확보했다.**
> 확보 방법: velog 페이지를 직접 받아 `__APOLLO_STATE__`에서 **본문 마크다운 원문을 추출**했다. WebFetch 요약 경유가 아니다. **이 방법은 재현 가능하며, 향후 velog 자료 회수에 그대로 쓸 수 있다.**

## L-1. ⭐⭐⭐ "다른 팀원들은 잘 동작하지만, 나만 꺼지는 상황"

- **출처:** velog — https://velog.io/@js03210/Docker-컨테이너가-나만-죽는-이유와-해결방안 (게시: **2025-08-13**, 검색: 2026-07-25)
- **인용 등급:** **축자 인용 가능** (Apollo 상태에서 본문 원문 추출)
- **⭐⭐ 원문(상황 — 오프닝 그 자체다):**
  > "### 상황
  > - Docker로 여러 컨테이너를 띄워놨는데, Redis 컨테이너가 자주 꺼짐
  > - **다른 팀원들은 잘 동작하지만, 나만 꺼지는 상황**"
- **원문(진단):**
  > "docker inspect 결과: `OOMKilled=true (exit=137)` → 메모리 부족(OOM Kill) 이 원인."
- **⭐⭐ 원문(원인 — 이 책의 핵심 논지와 정확히 겹친다):**
  > "1. Docker Desktop 메모리 설정 차이
  > - 팀원: Docker Desktop → Settings → Resources → Memory 값이 4GB 이상.
  > - **나: 기본값(2GB)으로 설정** → Redis가 순간적으로 fork 시 메모리를 더 쓰면 바로 종료."
  > "2. 로컬 메모리 여유 부족
  > - 나만 다른 컨테이너, VSCode, Chrome, DB 등 메모리 많이 쓰는 프로그램을 동시에 실행.
  > - **Docker VM에서 사용 가능한 메모리가 적어서 Redis가 죽음**"
- **원문(결말):**
  > "나의 원인은 1번 (Docker Desktop 메모리 설정) 때문이었고, `Docker Desktop → Settings → Resources → Memory Limit` 값을 늘리자, Redis 컨테이너가 더 이상 종료되지 않았다."

- **⭐⭐⭐ 왜 강한가:**
  1. **"나만 죽는다"** — 이 책이 반복해서 다루는 "같은 Dockerfile, 다른 결과"의 **한국어 표현 그 자체**다. 1차 A9("다른 분 노트북으로 빌드했더니 그냥 됐다")와 **같은 감정, 다른 원인**(아키텍처 vs 메모리 한도).
  2. **"Docker VM에서 사용 가능한 메모리"**라고 저자가 스스로 적었다 — §1-3/§1-4(맥에는 VM이 낀다)를 독자가 스스로 도달한 사례.
  3. **2025-08**로 최신이다. §7-3 #12·#13의 "한국어 최신 자료 없음"을 부분적으로 채운다.
- **⚠️ 한계:** **자바가 아니라 Redis다.** 스프링 부트 OOMKilled 사례로 옮기지 말 것. `exit=137`과 `OOMKilled=true`라는 **신호는 언어 무관**이므로, 그 부분만 일반화 가능.
- **쓸 곳:** ⭐⭐⭐ **맥 리소스 챕터 오프닝(한국어 독자용 최우선 후보).** 오프닝 기법 **실패 장면**. D-1(영어, 122GB)과 짝지으면 "설정한 한도와 실제가 어긋난다"를 양쪽에서 조명할 수 있다.

## L-2. ⭐⭐ latest 태그 사고담 (스프링 부트) — G-1 참조

- velog @vector13, 2022-11-20, 축자 인용 가능. 상세는 **§G-1**.

## L-3. ⭐ "이틀간 삽질" — M1에서 빌드해 클라우드에 올렸다가 안 뜬 이야기

- **출처:** velog — https://velog.io/@atoye1/Docker-M1-맥으로-도커-이미지-빌드시-유의할-점 (게시: **2022-11-17**, 검색: 2026-07-25)
- **인용 등급:** **축자 인용 가능**
- **⭐ 원문(막힌 지점 — "로그를 어디서 보는지도 몰랐다"):**
  > "하면 깔끔하게 성공되어야 하는데 **도무지 도커 컨테이너가 실행 안되는거다. 당시에는 앱서비스 메뉴 중 어디에서 로그를 봐야하는지도 몰랐어서 무작정 1~3 과정을 반복하고, 좌절하고 스트레스만 쌓고 있었다.** 나중에 안 사실이지만 로그는 `로그스트림` 메뉴를 통해서 볼 수 있다."
- **원문(전환점 — 진단 방법을 바꿨다):**
  > "다음날 다시 시도해보기로 했다. 이번에는 VM에 직접 배포하는 방식으로 시도했다. **콘솔에 명령어를 직접 입력해서 직접 에러메시지를 확인할 수 있으니 이 편이 더 디버깅하기 쉽다고 생각했기 때문이다.**"
- **원문(범인):**
  > "docker run -p 80:80 snowdelver/node-web-app을 실행하고 발견한 메세지... 결국 M1와 서버의 플랫폼 차이 때문에 발생한 문제였다.
  > > The requested image's platform (linux/arm64/v8) does not match the detected host platform (linux/amd64)"
- **원문(교훈):**
  > "플랫폼을 지정해주지 않으면 arm64로 빌드하므로 서버에서 실행이 되지 않았다."
  > "**이틀간 삽질한 덕에** 로컬 노드앱의 도커라이징과 클라우드에 컨테이너로 배포하는 과정을 기초부터 학습할 수 있었다."

- **⭐ 값어치:** ⭐ **"관리형 서비스에서는 로그를 못 봤고, VM에 직접 올려 콘솔을 보고서야 원인을 찾았다"** — 이 책의 트러블슈팅 휴리스틱(§5-1 H1: "무엇이 실행되고 어디에 붙는가를 분리해서 물어라")과 정확히 맞물리는 **한국어 서사**다. **오류 문구가 보이기까지가 진짜 싸움이었다**는 구조.
- **⚠️ 한계:** **Node.js다, 자바가 아니다.** 그리고 **2022년**이다. 1차의 A9(velog @___pepper, 2022-01)와 **시기·성격이 비슷**하므로, 둘 중 하나만 오프닝에 쓰고 나머지는 본문 근거로 돌릴 것(같은 리듬 반복 방지).
- **쓸 곳:** 아키텍처 챕터의 보조 사례, 또는 §5-1 트러블슈팅 절의 도입.

## L-4. ⛔ 한국어 — 여전히 확보 못 한 것

- **OrbStack·Podman·Colima의 한국어 실사용 후기 중 축자 인용 가치가 있는 것: 0건.** 검색 결과에 velog 글 2건(@zzerym, @nchime)이 나와 **@zzerym은 실제로 열었으나**, 2023-11 게시에 내용이 "성능면에서도 도커보다 더 낫다고 한다"(전언), "설치하자마자 바로 로컬 쿠버네티스가 만들어져서 편하다" 수준의 **짧은 추천글**이었다. **1차 체감 서술이 없어 인용 가치가 낮다.**
- **OKKY·GeekNews(news.hada.io)·커리어리·브런치: 이번 세션에서 신규 확보 0건.** 검색 경로에서 직결 스레드가 잡히지 않았다. ⛔ **"국내에 없다"로 격상 금지** — §8-7의 경고가 그대로 적용된다.
- **국내 회사 엔지니어링 블로그(우아한형제들·카카오·토스·네이버 D2·LINE): 이번에도 0건.** §7-3 #13 유지.

---

# 📊 표 1 — §7-3의 "0건" 항목이 살아났나

| # | §7-3 항목 | 판정 | 근거 | 축자 인용 가능? |
|---|---|---|---|---|
| 1 | `latest` 태그 사고담 | ✅ **확보(한국어)** + ❌ **영어권은 재확인 0건** | G-1 (velog @vector13, 2022-11-20, 스프링 부트) / HN 재검색 3회 0건 | ✅ 예 |
| 2 | 베이스 이미지 업데이트를 어떻게 굴리는가 | ⚠️ **간접만** — 컨테이너 베이스 이미지 직접 자료는 **여전히 0건** | F (Dependabot/Renovate 운영론, 자동 머지 찬반 충돌) | ✅ 예(단, 의존성 스캐너 이야기) |
| 3 | 취약점 스캔 알림 피로 | ⚠️ **부분 확보** — 의존성 스캐너는 대량, **컨테이너 이미지 스캔은 0건** | E-1 (HN 47094192, 2026-02, 647pts) | ✅ 예 |
| 4 | 로컬 K8s의 맥북 배터리·발열 | ❌ **여전히 0건 (재확인)** | H — HN 검색 3회 노이즈만. #7648은 배터리를 언급하지 않음 | — |
| 5 | 맥 메모리 할당 튜닝 실패담 | ✅ **확보(대량)** | D-1 (for-mac#7749, 22댓글, OPEN) + L-1 (velog, 한국어) | ✅ 예 |
| 6 | 맥 Testcontainers "느리다" 성능 증언 | ⚠️ **인접만** — "느리다"가 아니라 **"안 붙는다/제때 안 뜬다"** | I-1(감지 실패), I-3(시작 타임아웃) | ✅ 예 |
| 7 | Gradle/Maven 볼륨 마운트 성능 **수치** | ❌ **여전히 수치 0건** — 단일 체감 증언 1건만 확보 | C-1 (`spockz`, "maven 빌드 3~4배 저하 체감") | ✅ 예(단, **수치로 쓰면 안 됨**) |
| 8 | K8s 논쟁이 2020년 자료 | ✅ **뒤집힘 — 2025·2026 스레드 확보** | A-1~A-5 (HN 44976292 / 46576224) | ✅ 예 |
| 9 | Alpine 논쟁이 2023년 자료 | ✅ **뒤집힘 — 논거 자체가 교체됨** | B-1 (HN 45143347, 2025-09, musl 할당자) | ✅ 예 |
| 10 | Docker Desktop 라이선스 원 공지 HN 스레드 미열람 | ❌ **미해소** (그 스레드는 열지 않음) — 단, **5년 뒤 착지점**은 확보 | C-1 (`pjmlp`/`ifwinterco`, 2026-02) | ✅ 예(2026분만) |
| 11 | Podman 후기가 2021~22년뿐 | ✅ **뒤집힘 — 2026-07 / 2026-02 스레드 2건** | C-1 (48762098, 648pts) / C-4 (47151163, 130pts) | ✅ 예 |
| 12 | 한국어 5건 중 축자 인용 1건 | ✅ **개선 — 축자 인용 가능 3건 추가** | L-1, L-2(=G-1), L-3 | ✅ 예 |
| 13 | 국내 회사 엔지니어링 블로그 최신 사례 | ❌ **여전히 0건** — ⛔ 부재 단정 금지 | — | — |
| — | 스프링 부트 컨테이너 OOMKilled 일화 | ❌ **0건**(자바 직결) | K | — |

**요약:** 살아난 것 **6항목**(#1 부분·#5·#8·#9·#11·#12), 부분 해소 **3항목**(#2·#3·#6), **여전히 0건으로 확정 4항목**(#4·#7·#13, 그리고 스프링 OOMKilled).

---

# 📊 표 2 — 논쟁 최신화 결과 (1차 시점 → 지금)

| 논쟁 | 1차 리서치 시점 | **2026-07-25 확인된 것** | 본문 저술 지침 |
|---|---|---|---|
| **K8s 도입** | 2020-03 HN 22491170 중심(6년 전). "K8s는 과하다" vs "그래도 필요하다" | **논쟁의 전제가 바뀌었다.** ① **managed K8s**(EKS/GKE)가 논쟁의 새 중심 — 그런데 그마저 갈린다: `tnjm` "유지보수 사실상 0, managed가 내 기본 선택" vs `therealfiona` "EKS 7년 굴리고 ECS로 내려간다, 엔지니어 0.5명/년" (같은 스레드, 같은 날). ② **LLM이 YAML 작성 비용을 낮췄다**는 새 논거 등장(`herval`). ③ 무게중심이 "기술이 복잡하다"에서 **"한 사람의 지식에 조직이 인질 잡힌다"**로 이동(`elthor89`, 2026-01). ④ **"k8s를 피하라 ≠ 컨테이너를 피하라"**라는 정리가 등장(`dangus`) | 2020년 자료는 **"2020년 당시"**로 명시하고, **A-2/A-3의 충돌을 나란히** 놓을 것. "managed면 해결"이라고 쓰지 말 것 |
| **Alpine vs Debian slim** | 2023-03 HN 35056594. 핵심 논거는 **musl DNS-over-TCP 부재**(당시 이미 수정 중) | **논거가 교체됐다.** 2025-09 HN 45143347에서 중심 논거는 **musl 기본 할당자의 멀티스레드 성능**이다. 컨테이너 실무자 시점의 정리(`jauntywundrkind`): "엔지니어들이 나방처럼 Alpine에 끌린다… **컨테이너 크기는 굿하트의 법칙 문제**". 반대편(`flohofwoe`): "고빈도 할당은 일반적 경우가 아니라 나쁜 설계". 재반박(`masklinn`): "2025년에 멀티스레드를 곤두박질치게 안 하는 할당자는 특수화의 반대말" | **DNS 논거를 현재형으로 쓰지 말 것.** 2025년 논거는 할당자다. ⚠️ **그 스레드에 JVM 언급은 없다** — 자바로 확장 서술 금지. §8-3(1차 소스 기반 선택 기준)이 판정을 주고, B-1은 **논쟁의 존재**만 준다 |
| **대안 런타임 (Podman/Colima/Rancher/OrbStack)** | Podman 후기 2021~22년뿐. OrbStack은 2024-09 HN 41421846 | **판세가 다시 그려졌다.** ① **OrbStack이 맥에서 사실상의 추천 기본값**이 됐다(2026-02·2026-07 스레드에서 반복 등장, 반대 증언 거의 없음). ② **Podman은 맥에서 여전히 뒤처진다**는 평(`spockz`: "miles less refined"), 그런데 **Red Hat이 상용 Podman Desktop을 냈고 팀 멤버가 스레드에 직접 답한다**(2026-02). ③ **Apple Containers라는 새 축이 2026년에 등장** — "VM 하나 vs 컨테이너당 VM"이라는 새 트레이드오프. ④ **Rancher Desktop이 "놀랍게도 괜찮다"는 후기로 재등장**(2026-02). ⑤ **Docker Desktop 자체의 평판이 나빠졌다** — 메모리·AI UI·라이선스 3중 불만 | 2021~22년 후기를 현재형으로 쓰지 말 것. **OrbStack 쏠림에는 반대 축(C-4-d `Shebanator`의 유지보수 우려)을 반드시 병기**. Apple Containers는 **1차 소스 확인 후에만** 서술 |

---

# 🔬 이 리서치가 1차의 판단을 뒤집는 것 (저술 전 반드시 반영)

1. **§7-3 #8은 틀렸다.** "2024~2026 최신 K8s 스레드는 빈약했다"는 사실이 아니다. 2025-08(50댓글)·2026-01(17댓글) 스레드가 있고, **논쟁의 축이 이동했다.** 6년 전 논쟁을 현재형으로 쓰면 오보다.
2. **§7-3 #11은 틀렸다.** Podman 후기는 2021~22년이 전부가 아니다. **2026-07-02에 648 points 스레드**가 있고 거기에 **자바 워크로드 실측 대화와 메인테이너 답변**이 있다.
3. **§7-3 #9의 위험은 실재했고, 방향이 예상과 다르다.** DNS 논거는 죽지 않고 **다른 논거(할당자)로 대체**됐다. 즉 "Alpine 논쟁이 끝났다"고 써도 오보고, "DNS 때문에 논쟁이 있다"고 써도 오보다.
4. **§5-1 H4는 경험칙에서 메커니즘으로 승격 가능하다.** J-1(spring-boot#46674)이 containerd 이미지 스토어 → 멀티플랫폼 인덱스 → API v1.41 inspect의 플랫폼 미지원 → 호스트 기본 플랫폼 해석이라는 **경로 전체**를 🟢 컨트리뷰터 분석으로 준다.
5. **§4-3(Ryuk 논쟁)의 메인테이너 입장은 2026년에도 그대로다 — 오히려 재확인됐다.**
   ⚠️ **이 항목은 이 리서치 도중 한 번 뒤집혔다.** 처음에는 "2026-01에 `testcontainers.properties`로 끌 수 있게 열어줬다"고 판단했으나, **PR 병합 여부를 실제로 조회하자 반대였다.** `gh pr view 11414` 결과 `mergedAt: null` — **병합되지 않았고**, 메인테이너 `eddumelendez`가 **"빌드 도구 설정으로 같은 목적을 달성할 수 있다"**며 닫았다(2026-02-03).
   → **본문 서술:** "Ryuk 비활성화를 공식 설정으로 승격해달라는 요청이 2026년에도 올라왔고, **메인테이너는 매번 우회 방법을 알려주며 반려한다.**" ⛔ **"`ryuk.disabled` 프로퍼티를 지원한다"고 쓰면 오보다.**
   📌 **교훈(다른 항목에도 적용):** GitHub에서 **PR의 `CLOSED`는 병합과 반려 양쪽을 뜻한다.** 이 파일의 다른 CLOSED 항목(J-1의 PR #47292 등)도 같은 검증 없이 "고쳐졌다"로 읽으면 안 된다.
6. **⚠️ 반대로, 뒤집지 말아야 할 것:** §7-3 #7(Gradle/Maven 볼륨 마운트 성능 **수치**)은 **해소되지 않았다.** `spockz`의 "메이븐 빌드 3~4배 저하"는 **환경·방법 불명의 단일 체감**이다. 수치로 쓰면 이 책의 fact-check 게이트가 잡아야 한다.

---

# 🧾 신선도·수집 원장

| 항목 | 값 |
|---|---|
| 검색·조회 시점 | **2026-07-25** (모든 GitHub 이슈 상태, 모든 HN 스레드 포인트/댓글 수) |
| HN 수집 방법 | Algolia 공식 API — `search`(스토리·코멘트) + `items/{id}`(스레드 전문). **댓글 텍스트는 API 원문** |
| GitHub 수집 방법 | `gh api search/issues` + `gh issue view --comments` (본문·댓글 전문) |
| velog 수집 방법 | 페이지 직접 요청 후 `__APOLLO_STATE__`의 `body` 필드에서 **마크다운 원문 추출** (WebFetch 요약 경유 아님) |
| 접근 실패 | **Reddit** — 2회 시도, 둘 다 실패. ① `www.reddit.com/r/kubernetes/search.json` → 봇 차단 HTML(UA 위장 포함) ② `old.reddit.com/r/devops/search.json` → **HTTP 403**. r/kubernetes·r/devops·r/java **0건**. ⛔ **"레딧에서는 ~"이라고 쓰지 말 것 — 도구 실패지 부재가 아니다** |
| 미시도/미접근 | Lobsters(검색 품질 불량으로 조기 포기), Dev.to, Stack Overflow, X/Mastodon, Discord/Slack 로그, OKKY(신규 0), 커리어리, 브런치, 네이버 카페 |
| 원문 미열람(제목·링크만 확인) | Medium 기사 3건(A-5·C-3의 원 링크), nickb.dev 블로그(B-1), words.filippo.io(E-1), blog.podman.io(C-1), thenewstack.io(C-4). **⛔ 전부 본문 인용 금지** |

### 수집 산출물 계수 (세 종류를 섞어 세지 말 것)

| 종류 | 수량 | 내역 |
|---|---|---|
| **① 축자 인용 가능 항목** | **25건** | A-1~A-5(5) / B-1·B-2(2) / C-1·C-2·C-3·C-4-a~e(8) / D-1(1) / E-1(1) / F(1) / G-1(1) / I-1·I-2·I-3(3) / J-1(1) / L-1·L-3(2). **L-2는 G-1과 동일 자료이므로 중복 계수하지 않았다** |
| **② 📒 제목·상태만 확인(인용 금지)** | **4군 / 18행** | D-2(4행) · I-4(8행) · J-2(3행) · E-2(3행, 요약 경유) |
| **③ 부재 확정(재검색에도 0건)** | **6건** | G-2(영어권 latest 사고담) · H(로컬 K8s 배터리·발열) · K(스프링 부트 OOMKilled 일화) · L-4(한국어 대안 런타임 후기/OKKY·GeekNews 신규/국내 엔지니어링 블로그) · E 내부(컨테이너 이미지 스캔 알림 피로) · F 내부(베이스 이미지 업데이트 주기) |

| 신규 한국어 축자 인용 자료 | **3건** (L-1 2025-08 / L-2=G-1 2022-11 / L-3 2022-11) |

## ⛔ 저술가에게 보내는 마지막 경고 세 줄

1. **이 파일의 수치는 대부분 자기 보고다.** 122GB·40GB·11.5GB·27초·24.96초·3~4배·300%→0.2%·4배 — **전부 측정 방법이 불완전하다.** 벤치마크로 제시하면 안 된다. "한 사용자가 ~를 보고했다"까지.
2. **"제목만 확인" 표(D-2·I-4·J-2)에서 인용문을 만들지 마라.** 이슈 제목을 문장으로 늘려 쓰는 순간 창작이 된다.
3. **0건인 것은 0건이다.** 로컬 K8s 배터리(H), 스프링 OOMKilled 일화(K), 국내 엔지니어링 블로그(L-4), 컨테이너 이미지 스캔 알림 피로(E), 베이스 이미지 업데이트 주기(F) — **이 다섯은 재검색에도 나오지 않았다. 채우지 말고 비워라.**

