# 8장. `FROM` 뒤의 선택, 그리고 그 안의 자바

이미지를 작게 만들면 정말 빨라질까?

Dockerfile 첫 줄을 고칠 때 우리가 은근히 기대하는 것이 이것이다. 그런데 무엇이 빨라진다는 걸까? 빌드가? 배포가? 아니면 앱의 기동이? 셋은 완전히 다른 이야기인데, 우리는 대개 구분하지 않은 채 한 줄을 고치고 뿌듯해한다. 그리고 며칠 뒤에도 체감은 그대로라서 뒷맛이 조금 찜찜하다.

`FROM` 뒤에 무엇을 쓸지 정하고 나면 곧바로 두 번째 질문이 따라온다. 그 안에 앉은 자바는 지금 자기가 어디에 있다고 생각하고 있을까? 힙의 상한을 정할 때 무엇을 보고, 스레드 풀 크기를 계산할 때 코어를 몇 개로 셌을까? 두 질문은 사실 하나다. **이미지 안에 자바를 어떻게 앉힐 것인가.**

### 이미지 다이어트는 언제 효과가 있는가

논문 두 편을 나란히 놓으면 답이 꽤 선명해진다. 다만 둘은 반대되는 말을 하는 것처럼 보여서, 한 편만 읽으면 한쪽으로 치우친다. 먼저 오래된 쪽이다.

> "Our analysis shows that pulling packages accounts for 76% of container start time, but only 6.4% of that data is read."
> — Harter et al., FAST '16 Abstract (**2016년 측정**)

컨테이너가 뜨는 데 걸린 시간의 76%가 이미지를 내려받는 데 쓰였고, 그렇게 내려받은 데이터 중 실제로 읽힌 것은 6.4%뿐이었다는 것이다. 처음 보면 조금 아찔한 수치다. 우리가 이미지에 욱여넣은 것의 대부분은 한 번도 열리지 않은 채 네트워크만 왕복했다는 뜻이니까.

이제 최근 쪽이다. 같은 질문을 warm start, 즉 **이미 내려받아 놓은 상태에서의 재기동**으로 좁혀 잰 결과다. Premium SSD 환경에서 5MB짜리 alpine 이미지와 155MB짜리 `python:3.11-slim` 이미지의 기동 시간 차이는 554~568밀리초 구간, 비율로는 **2.5%**에 그쳤다(Khan, arXiv:2602.15214 Finding 1, **2026년, 프리프린트**). 이 편차를 지배하는 것은 이미지 크기가 아니라 런타임 오버헤드 — 네임스페이스 생성, cgroup 설정, 파일시스템 마운트 준비 — 라는 것이 저자의 설명이다. 2장에서 컨테이너를 만드는 재료로 봤던 이름들이 여기서는 비용 항목으로 다시 나온다.

두 결과는 충돌하지 않는다. **재는 구간이 다를 뿐이다.** 그래서 "이미지를 줄이면 빨라진다"는 명제는 조건부로만 참이다. 처음 내려받는 경로 — CI 러너가 캐시 없이 도는 순간, 새 노드에 파드가 처음 스케줄되는 순간 — 에서는 크기가 곧 시간이다. 반대로 이미 이미지를 갖고 있는 내 맥에서 컨테이너를 껐다 켜는 동안에는 베이스를 무엇으로 바꾸든 체감이 거의 없다.

그러니 잠시 멈추고 물어보자. 지금 내가 줄이려는 그 100MB는 **누가 몇 번 내려받는 100MB인가?** 다이어트에 쓸 시간이 있다면, 그 답이 나오는 쪽에 쓰는 편이 낫다.

계보로 보면 첫 점은 더 앞에 있다. 구글의 Borg를 다룬 논문은 작업 기동 지연의 중앙값이 대략 25초였고 그중 **패키지 설치가 약 80%**를 차지한다고 적었다(Verma et al., EuroSys '15 §3.4, 2015년 기준). 다만 **Borg는 Kubernetes가 아니다** — 같은 계보의 선조일 뿐이므로 이 수치를 쿠버네티스의 숫자처럼 옮기면 안 된다. 10년 넘게 같은 자리에서 같은 병목이 관측됐다는 사실, 딱 거기까지가 우리 몫이다.

### 후보 다섯과 그 근거

그렇다면 `FROM` 뒤에 실제로 무엇을 쓸 수 있을까. 자바 이미지를 만들 때 현실적으로 손에 잡히는 후보는 다섯 정도다(전부 2026년 7월 25일 조회 기준).

| 후보 | 특징 | 근거 |
|------|------|------|
| `eclipse-temurin:{ver}-jre-{noble\|jammy}` | Ubuntu 기반, glibc, 무난한 기본값 | Docker Official Images의 Temurin README |
| `eclipse-temurin:{ver}-jdk-alpine-{ver}` | ~5MB 베이스, **musl libc 주의** | 같은 README의 caveat |
| `debian:{suite}-slim` | man page·문서 제거, 런타임은 그대로 | Docker Official Images의 debian README |
| `gcr.io/distroless/java{17\|21\|25}-debian13` | 셸·패키지 매니저 없음, `nonroot`/`debug` 변형 | GoogleContainerTools/distroless README |
| `bellsoft/liberica-openjre-debian:25-cds` | Spring Boot 공식 문서의 Dockerfile 예제가 쓰는 이미지 | Spring Boot 문서(표기 4.1.0) |

이 표에서 가장 자주 헷갈리는 두 칸부터 갈라놓자. **`-slim`과 Alpine은 같은 종류의 절약이 아니다.** Debian의 `-slim` 태그에 대한 공식 설명은 이렇다.

> "an experiment in providing a slimmer base (removing some extra files that are normally not necessary within containers, such as man pages and documentation)"

컨테이너 안에서 굳이 필요 없는 파일 — man page와 문서 같은 것 — 을 걷어낸 것이다. 리눅스 배포판도 그대로고 C 라이브러리도 그대로다. 반면 Alpine은 애초에 **musl libc와 busybox 위에 지어진** 배포판이라고 공식 소개가 밝힌다. 다시 말해 `-slim`은 짐을 덜어낸 같은 집이고, Alpine은 다른 집이다. 이 차이가 자바에서 갈리는 지점이다.

distroless는 이름이 주는 인상보다 이해하기 쉽다. 공식 README가 스스로 정의를 준다 — "Distroless" 이미지는 **애플리케이션과 그 런타임 의존성만** 담고 있고, "package managers, shells or any other programs you would expect to find in a standard Linux distribution"을 포함하지 않는다. 가장 빠른 설명은 3단 논리다. **셸이 없다 → `docker exec ... sh`로 들어갈 수가 없다 → 그래서 `debug` 태그가 따로 존재한다.** 디버그 이미지는 들어갈 수 있는 busybox 셸을 제공한다고 README가 명시한다. 공격 표면이 줄어드는 대신, 장애 났을 때 컨테이너에 들어가 뒤져보던 습관은 못 쓰게 된다. 어느 쪽이 비싼지는 팀마다 다르다. 자바 이미지는 arm64를 지원하니 맥에서 그대로 실습할 수 있다.

Temurin은 권고를 하나 남겨뒀는데, 의외로 "JRE 이미지를 쓰라"가 아니다.

> "JRE images are available for all versions of Eclipse Temurin but it is recommended that you produce a custom JRE-like runtime using `jlink`."

모든 버전에 JRE 이미지가 있긴 하지만, `jlink`로 필요한 모듈만 담은 런타임을 직접 만들어 쓰는 편을 권한다는 것이다. 앞 소절의 계산을 대보면 이 권고의 값어치가 보인다 — cold path가 잦을수록 돈이 되고, 로컬에서만 도는 앱이면 손댈 이유가 약하다. 마지막 후보 BellSoft Liberica는 Spring Boot 공식 문서의 Dockerfile 예제가 빌더와 런타임 양쪽에서 쓰는 이미지다(그 예제는 7장에서 펼쳤다). 다만 태그 라인업은 이 책이 확인하지 못했으니, 쓰기로 했다면 벤더 문서를 열어보고 고르자.

### Alpine 논쟁은 무엇에 대한 논쟁인가

Alpine 이야기가 나오면 자바 진영에서 반사적으로 따라 나오는 문장이 하나 있다. 2023년 3월 Hacker News에서 `huksley`라는 사용자가 이렇게 적었다.

> "those java/jdk-*-alpine images... actually support only subset of a (gigantic) APIs available in Java."

Alpine용 JDK 이미지는 자바가 제공하는 거대한 API의 **부분집합만** 지원한다는 것이다. 이 말이 널리 퍼진 이유는 짐작이 간다. 무섭고, 외우기 쉽고, 결론까지 한 번에 나오니까.

그런데 이 주장은 근거를 대기가 어렵다. 이 책이 확인한 범위에서는 뒷받침하는 공식 서술이 없었고, 오히려 반증이 우세하다. 첫째, **Eclipse Temurin이 `eclipse-temurin:25-jdk-alpine-3.23`을 JDK로 배포하고 있다.** 표준 API가 잘려 있는 런타임이라면 `jdk` 태그를 달 수 없다. 둘째, **Alpine 변형에 대한 공식 caveat이 가리키는 곳은 Java API가 아니라 libc다.**

> "Alpine Linux is much smaller than most distribution base images (~5MB), and thus leads to much slimmer images in general... the main caveat to note is that it does use musl libc instead of glibc and friends, so software will often run into issues depending on the depth of their libc requirements/assumptions."

glibc 대신 musl libc를 쓰기 때문에, libc에 대한 요구나 가정이 깊은 소프트웨어일수록 문제를 만난다는 이야기다. 자바로 옮기면 이렇게 읽는 편이 정확하다 — **위험한 것은 자바 표준 API가 아니라, 네이티브 라이브러리를 끼고 도는 의존성이다.** 이미지 처리나 암호화, 일부 DB 드라이버처럼 JNI로 네이티브 코드를 부르는 쪽이 먼저 삐끗한다. 덧붙이면 원 발언자 본인도 자기 말에 불확실 표시를 달아두었다. 커뮤니티의 말이 몇 다리를 건너며 단정문으로 굳는 과정을 보여주는 표본에 가깝다.

더 흥미로운 건 이 논쟁의 **논거 자체가 교체됐다**는 사실이다. 몇 년 전 대표 근거는 musl의 DNS 처리였는데, 논쟁이 오가던 당시 이미 수정이 진행 중이라는 지적이 같은 스레드에 달렸다. 2025년 9월 Hacker News에서 다시 불붙었을 때 중심에 있던 것은 DNS가 아니라 **musl 기본 할당자의 멀티스레드 성능**이었다.

> "Because engineers seem drawn like moths to the flame to Alpine container images. Yes they are small, but the ramifications of Alpine & using musl are significant."
> "Container size has always struck me as such a Goodhart's Law issue"
> — `jauntywundrkind`, 2025-09-08

엔지니어들이 불에 뛰어드는 나방처럼 Alpine 이미지에 끌리지만 musl을 쓰는 대가는 만만치 않다는 것, 그리고 **컨테이너 크기는 늘 굿하트의 법칙 문제로 보였다**는 것이다 — 측정치가 목표가 되는 순간 좋은 측정치이기를 멈춘다는 그 법칙. 반대편도 만만치 않다. 같은 날 `flohofwoe`는 "경합에 걸릴 만큼 높은 빈도로 할당할 때에만 문제가 된다. 지나치게 높은 접근 빈도는 '일반적 경우'가 아니라 그냥 잘못 설계된 멀티스레드 코드"라고 받았고, `masklinn`은 "2025년에, 멀티스레드 프로그램을 곤두박질치게 만들지 않는 할당자는 '특수화'의 반대말"이라고 재반박했다.

여기서 아주 조심할 것이 있다. **저 스레드는 JVM 이야기가 아니다.** 맥락은 Rust와 C 쪽이고, 대화 어디에도 자바나 JVM 언급이 없다. "그래서 Alpine 위의 스프링 부트가 느리다"로 이어 붙이면, 근거가 하지 않은 말을 우리가 대신 해주는 셈이다. 가져갈 수 있는 것은 여기까지다. **2025년 Alpine 논쟁의 논거는 할당자 성능으로 옮겨갔고, 그 논거가 성립하는 조건은 고빈도 할당과 멀티스레드다.** 그 조건이 내 워크로드에 해당하는지는 남의 스레드가 아니라 내 애플리케이션으로 확인할 문제다.

한편 2025~2026년 사이에는 "CVE 0건"을 내세운 베이스 이미지가 하나의 상품 범주로 등장했다는 관측도 있다. 이 책은 그 제품군의 1차 자료를 열어보지 못했으니 존재를 언급하는 선에서 멈춘다 (사실 확인 필요) — 각 벤더 공식 문서로 대조할 것.

### JVM이 cgroup을 읽는다

2장에서 다리 하나를 놓고 건너지 않았다. JVM이 컨테이너 안에서 힙 크기를 정할 때 읽는 값이 바로 그 cgroup이라고만 말하고 넘어갔다. 이제 건널 차례다.

JDK 21의 `java` 문서는 컨테이너 인식 기능을 이렇게 설명한다.

> "**Linux only:** The VM now provides automatic container detection support, which allows the VM to determine the amount of memory and number of processors that are available to a Java process running in docker containers... **The default for this flag is `true`**, and container support is enabled by default."

읽자마자 걸리는 대목이 있을 것이다. "Linux only"라니, 나는 맥에서 개발하는데? 2장의 계층도를 떠올려보자. 컨테이너 안의 자바는 macOS 위가 아니라 **리눅스 VM의 커널 위에서** 돈다. 맥이라서 비켜가는 게 아니라, 한 겹 더 멀리 있을 뿐이다. 그리고 문서가 말하는 그 "사용 가능한 메모리와 프로세서 수"는 어디에 적혀 있을까. 2장에서 본 cgroups의 memory·cpu 컨트롤러, 우리가 `--memory`와 `--cpus`로 값을 적어 넣은 바로 그 자리다.

기능 이름은 `UseContainerSupport`이고 기본값은 `true`다. 켜져 있는 상태를 명시하려면 `-XX:+UseContainerSupport`, 굳이 끄려면 `-XX:-UseContainerSupport`를 쓴다. JVM이 컨테이너를 어떻게 인식했는지 확인하고 싶다면 문서가 진단 방법도 알려준다 — "Use `-Xlog:os+container=trace` for maximum logging of container information." 이상하다 싶을 때 추측으로 시작하지 말고 이 로그부터 켜보는 편이 낫다.

그런데 "메모리를 인식한다"와 "그만큼 힙으로 쓴다"는 다른 이야기다. 이 책을 쓴 맥에서 JDK 21.0.10으로 기본값들을 뽑아보면 이렇게 나온다(2026년 7월 25일, 호스트에서 실행).

```
$ java -XX:+PrintFlagsFinal -version | grep -Ei "RAMPercentage|ActiveProcessorCount|MaxRAM "
   int  ActiveProcessorCount   = -1            {product} {default}
double  InitialRAMPercentage   = 1.562500      {product} {default}
uint64_t MaxRAM               = 137438953472   {pd product} {default}
double  MaxRAMPercentage       = 25.000000     {product} {default}
double  MinRAMPercentage       = 50.000000     {product} {default}
```

눈여겨볼 값은 `MaxRAMPercentage = 25.0`이다. 이 JDK 빌드는 인식한 메모리의 25%를 최대 힙의 기본 상한으로 잡는다는 뜻이다. 산수를 해보자. 컨테이너에 2GB를 줬다면 힙 상한은 500MB 근처다. 넉넉히 줬다고 생각한 메모리의 4분의 3이 힙 바깥에 남는 셈이다.

여기서 선을 하나 긋자. **위 값은 이 책을 쓴 맥의 그 JDK 빌드에서 관측된 것이지, 모든 JVM의 기본값이라는 근거가 아니다.** `MaxRAMPercentage`에 대한 공식 문서 기재는 이 책이 확보하지 못했다. 그러니 숫자를 외우는 대신 재는 법을 익히자. 위 명령을 **여러분이 쓸 베이스 이미지로, 메모리 한도를 걸어놓은 컨테이너 안에서** 돌려보는 것이다. 위 출력은 컨테이너 밖 호스트에서 잰 것이니, 두 결과를 나란히 놓으면 간격이 보인다.

CPU 쪽도 같은 구조인데 맥에서는 사정이 한 겹 더 복잡하다. 4장에서 `--cpus`로 건 제한이 맥에서는 그대로 지켜지지 않는다는 관측을 보고, `-XX:ActiveProcessorCount`는 여기서 다시 만나자고 미뤄뒀다. 그 나머지 절반이 이것이다. 문서는 이 옵션이 "Overrides the number of CPUs that the VM will use to calculate the size of thread pools"라고 설명하고, 이어서 결정적인 한 줄을 붙인다 — "**This flag is honored even if `UseContainerSupport` is not enabled.**" 컨테이너 지원이 켜져 있지 않아도 이 값은 존중된다는 것이다. JVM이 코어 수를 스스로 추측하게 두면, 그 추측의 재료가 되는 층이 맥에서는 흔들린다. 스레드 풀 크기가 성능에 직결되는 서비스라면 **코어 수를 명시하는 편이 낫다.** 손으로 박아두면 적어도 어제와 오늘이 같아진다.

### 빌드팩은 메모리를 어떻게 계산하는가

`FROM`을 직접 쓰지 않는 길을 골랐다면 — 즉 빌드팩에 맡겼다면 — 위 계산을 누가 대신 하고 있을까? Paketo 자바 빌드팩에는 Memory Calculator라는 컴포넌트가 있고, 공식 문서가 공식을 그대로 공개한다.

```
Heap = Total Container Memory - Non-Heap - Headroom
```

컨테이너에 주어진 전체 메모리에서 힙이 아닌 몫과 여유분을 뺀 나머지가 힙이다. 중요한 건 **뺄셈의 대상들이 문서에 숫자로 적혀 있다**는 점이다. `-XX:MaxDirectMemorySize`는 10MB, `-XX:ReservedCodeCacheSize`는 240MB, `-XX:MaxMetaspaceSize`는 자동 계산, `-Xss`는 1MB에 스레드 250개를 곱한 값, 그리고 남은 것이 `-Xmx`다. 이 값들은 이미지에 굳어 있는 게 아니라 **런타임에 `JAVA_TOOL_OPTIONS`로 붙는다.** 컨테이너를 띄우고 그 환경변수를 찍어보면 JVM이 무엇을 받아 들었는지 그대로 보인다.

앞 소절과 견줘보면 성격 차이가 분명하다. 직접 만든 이미지에서는 우리가 비율을 정하거나 방치하고, 빌드팩 경로에서는 계산기가 항목별로 빼준다. 게다가 Spring Boot 전용 컴포넌트는 "can apply domain-specific knowledge to optimize the performance of Spring Boot applications"라고 되어 있고, 예로 리액티브 웹 앱의 스레드 수를 50으로 줄이는 경우를 든다. 편한 대신 결정권이 넘어간 것이니, 왜 그런 값이 나왔는지 읽을 줄 아는 것이 더 중요해진다.

기동을 더 당기고 싶다면 최근 JDK가 주는 장치도 있다. Spring Boot 공식 문서(표기 4.1.0 기준)는 클래스 데이터 공유(CDS)와 AOT 캐시 두 갈래를 예시로 보여주고, **Java 25 이상에서는 CDS보다 AOT 캐시를 권한다.**

| 기법 | 요구 버전 | 훈련 실행 | 실행 |
|------|-----------|----------|------|
| AOT 캐시 | Java 25+ | `RUN java -XX:AOTCacheOutput=app.aot -Dspring.context.exit=onRefresh -jar application.jar` | `ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "application.jar"]` |
| CDS | Java 24+ | `RUN java -XX:ArchiveClassesAtExit=application.jsa -Dspring.context.exit=onRefresh -jar application.jar` | `ENTRYPOINT ["java", "-XX:SharedArchiveFile=application.jsa", "-jar", "application.jar"]` |

여기서 버전 전제를 확인하자. 참고로 이 책이 실측에 쓴 맥의 자바는 **21.0.10**이라 둘 다 그대로는 쓸 수 없다. 여러분의 JDK부터 확인하고, 조건이 맞지 않으면 이 표는 다음 업그레이드 때의 메모로 남겨두자.

---

이 장을 지나며 질문이 두 번 바뀌었다. 처음에는 "무엇을 담을 것인가"였고, 끝에서는 "그 안의 자바는 무엇을 보고 있는가"가 됐다. 둘 다 남에게 물어서는 끝나지 않는 질문이다. 베이스 선택은 내 의존성이 네이티브를 얼마나 쓰는지에 달렸고, 힙 상한은 내 컨테이너가 무엇을 인식했는지에 달렸다.

그래서 이 장의 숙제는 읽는 것이 아니라 재는 것이다. 지금 만들고 있는 이미지에 메모리 한도를 걸어 컨테이너로 띄우고, 그 안에서 `java -XX:+PrintFlagsFinal -version`을 돌려 세 값을 확인해보자. **`MaxRAMPercentage`**, **`MaxRAM`**, 그리고 **`ActiveProcessorCount`**. 예상한 값과 같다면 다행이고, 다르다면 그 간격이 이 장에서 이야기한 전부다.
