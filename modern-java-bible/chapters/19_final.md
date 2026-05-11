# 19장. AOT · Leyden · Compact Object Headers — 시작 시간과 메모리의 새 풍경

새벽 두 시, AWS Lambda 알람이 울린다. p99 콜드 스타트가 8초를 찍고 SLA를 깼다는 통보다. PayBridge의 결제 검증 Lambda는 평소 200ms에 처리되던 일이라, 8초는 그냥 *사고*다. 우리는 익숙한 절차로 들어간다. 메모리를 1.5GB에서 3GB로 올려보고, Provisioned Concurrency를 켜고, JVM 옵션을 만지작거린다. 그러다 누군가 회의에서 한 마디 꺼낸다. "이쯤 되면 GraalVM 네이티브 이미지로 가야 하는 거 아닙니까?" 모두 잠시 말이 없다. 네이티브 이미지로 가면 Reflection 메타데이터를 한참 정리해야 하고, Hibernate proxy도 손봐야 하고, 그 검증을 누가 4주 안에 끝낼지 아무도 자신하지 못한다.

콜드 스타트, 정말 GraalVM만 답일까?

이 장은 그 질문에서 출발한다. *GraalVM 없이도 빠른 자바가 가능한가*. 결론부터 말하면, 가능해지는 중이다. AppCDS에서 Dynamic CDS로, 다시 JEP 483 AOT Class Loading & Linking으로, 그리고 Project Leyden의 더 큰 그림으로 — OpenJDK는 콜드 스타트 문제를 자기 영역 안에서 풀어내려 한다. 거기에 Java 25에서 도착한 Compact Object Headers가 메모리 풍경까지 바꾼다. JVM을 *떠나지 않고도* 시작 시간과 메모리를 동시에 개선할 수 있게 됐다는 뜻이다. 한 단계씩 따라가 보자.

## CDS의 십 년: AppCDS에서 Dynamic CDS로

먼저 잘못된 통념부터 정리하자. *Java의 콜드 스타트는 JIT 컴파일 때문에 느리다*는 말은 절반만 맞다. 실제로 JVM이 시작될 때 가장 오래 걸리는 일 중 하나는 *클래스 로딩*이다. `java.base`만 해도 수천 개의 클래스가 있고, Spring Boot 앱은 거기에 다시 수만 개의 클래스를 더 얹는다. 클래스 파일을 디스크에서 읽고, 파싱하고, 검증하고, 메타데이터를 메타스페이스에 올리는 그 과정이 매 실행마다 반복된다. 같은 클래스를 매번 다시 읽고 매번 다시 파싱하는 일 — 곰곰이 따져보면 *번거롭다*.

Class-Data Sharing(CDS)은 이 번거로움에 처음 손을 댄 도구다. 시작은 오래됐다. Java 5에서 부트클래스로더의 일부 클래스를 미리 메모리에 매핑해두던 기능이 그 뿌리다. 그러나 그건 JDK 내부에 박힌 클래스 한정의 좁은 기능이었다. 우리 애플리케이션 클래스에는 도움이 되지 않았다.

판도를 바꾼 것은 Java 10의 **JEP 310: Application Class-Data Sharing**, 흔히 AppCDS라 부르는 기능이다. 핵심 발상은 단순하다. 처음 한 번은 애플리케이션을 평소처럼 실행해 *어떤 클래스가 로드되는지* 목록을 뽑는다. 그 목록을 입력으로 다시 한 번 실행해 *클래스 메타데이터를 통째로 직렬화한 아카이브*를 만든다. 그다음부터는 JVM이 시작할 때 그 아카이브를 메모리에 mmap으로 매핑한다. 클래스 파일을 읽고 파싱하는 단계가 통째로 사라지는 것이다.

AppCDS는 효과가 분명했다. 그러나 *세 단계*로 나눠 실행해야 했다 — 클래스 목록 뽑기, 아카이브 만들기, 그리고 실제 실행. 운영팀 입장에서는 도입 비용이 만만치 않았다. CI에 단계 두 개를 끼워야 했고, 클래스 목록과 실제 실행이 어긋나면 효과가 사라졌다. 도입하는 회사보다 알면서도 미루는 회사가 더 많았던 이유다.

Java 13의 **JEP 350: Dynamic CDS Archives**가 그 마찰을 한 번에 줄였다. 한 줄로 바뀐다. `-XX:ArchiveClassesAtExit=app.jsa` 옵션을 붙여 한 번만 평소처럼 실행하면, JVM이 종료될 때 알아서 아카이브를 떨궈준다. 다음 실행부터는 `-XX:SharedArchiveFile=app.jsa`로 그 아카이브를 매핑해 띄운다. 세 단계가 두 단계로 — 그것도 자연스러운 *training run* 한 번으로 — 줄어든 것이다. Spring Boot 3.3부터 이 패턴을 공식적으로 지원한다. 컨테이너 빌드 단계에서 한 번 띄웠다 죽이는 *워밍업 실행*을 한 번 끼우는 것만으로 충분하다.

여기까지가 *클래스 메타데이터*의 캐시다. 그런데 메타데이터를 캐시했다고 해서, 클래스를 *초기화*하고 *링크*하는 비용까지 사라지는 것은 아니다. `<clinit>` 블록을 실행하고, 상수 풀을 해석하고, 메서드 디스패치 테이블을 준비하는 일은 여전히 매 실행마다 반복된다. 그 다음 카드가 필요한 자리다.

## JEP 483: AOT Class Loading & Linking — Leyden의 첫 카드

Project Leyden은 2020년 즈음부터 OpenJDK 내부에서 회자되던 *시작 시간 프로젝트*의 우산 이름이다. Mark Reinhold가 처음 제안할 때의 야망은 컸다 — *static image*, 즉 GraalVM 네이티브 이미지에 준하는 일체형 바이너리를 OpenJDK 안에서 만들겠다는 그림이었다. 그러나 OpenJDK의 일하는 방식은 야망을 한 번에 풀지 않는다. Leyden은 자신의 *premain branch*에서 콘덴서(condenser)라는 개념을 다듬으면서, *점진적으로* JEP를 끊어 본류에 흘려보내는 길을 골랐다. 그 첫 결실이 Java 24에 도착한 **JEP 483: Ahead-of-Time Class Loading & Linking**이다.

발상의 진전은 한 줄로 표현된다. *클래스 메타데이터만 캐시할 게 아니라, 로딩과 링킹까지 끝낸 상태를 캐시하자*. Dynamic CDS가 클래스의 *형태*를 저장했다면, JEP 483은 *이미 해석된 클래스*를 저장한다. 결과는 인상적이다. 비슷한 training run 한 번으로 만들어진 캐시를 매핑해 띄우면, JVM이 클래스 로딩과 링킹 단계 대부분을 건너뛴다. Spring Boot 표준 데모로 자주 인용되는 Petclinic에서 시작 시간이 36~42%까지 짧아진다는 측정이 공개돼 있다. (구체 수치는 측정 환경과 Spring Boot 버전에 따라 흔들린다.)

Java 25는 거기에 두 장을 더 얹는다. **JEP 514: Ahead-of-Time Command-Line Ergonomics**는 사용성 정리다. `-XX:AOTMode=record`로 training run을 돌리고, `-XX:AOTCacheOutput=app.aot`로 캐시를 떨구고, `-XX:AOTCache=app.aot`로 실제 실행에서 그 캐시를 쓴다는 일관된 옵션 체계를 깔았다. **JEP 515: Ahead-of-Time Method Profiling**은 한 발 더 들어간다. JIT 컴파일러가 평소 *런타임에 모으는* 메서드 호출 빈도·분기 확률 같은 프로파일 정보를 training run에서 미리 모아두면, 실제 실행에서 JIT가 그 정보를 *재사용*해 더 빠르게 핫 메서드를 최적화한다. 클래스 로딩의 차원을 넘어, *컴파일러 워밍업*의 일부까지 캐시로 이전하기 시작한 것이다.

여기까지 와도 캐시는 *코드 자체*는 담지 않는다. 컴파일된 네이티브 코드를 캐시에 박는 일 — *AOT 코드 캐시* — 은 Leyden의 premain branch에서 여전히 실험 중이고, 표준 본류에 흘러들 시점은 정해지지 않았다. 그래도 흐름은 분명하다. AppCDS가 *메타데이터*를, JEP 483이 *로딩·링킹*을, JEP 515가 *프로파일*을 캐시한다. 그 다음 단계로 *코드*와 *프록시 생성*까지 캐시되면, OpenJDK의 콜드 스타트는 GraalVM 네이티브 이미지와의 격차를 의미 있게 줄이게 될 것이다. *그날은 멀지 않다*고 Leyden 팀이 이야기한다.

## 그래서, GraalVM은 어디로 가는가

여기서 한 발 멈춰 서서 GraalVM 네이티브 이미지의 정체를 정확히 짚어두자. 막연히 "더 빠른 자바"라고 알고 도입했다가 *난감해진* 팀을 본 적이 있을 것이다.

GraalVM Native Image의 핵심 가정은 **closed-world hypothesis**다. 빌드 시점에 *모든 도달 가능한 코드*를 정적으로 알 수 있다고 가정하고, 그 정적 분석 결과를 토대로 통째로 네이티브 바이너리를 만든다. 결과물은 JVM 없이 OS 위에서 바로 도는 단일 실행 파일이다. 시작은 밀리초 단위, 메모리 풋프린트는 JVM의 일부 — 서버리스 워크로드에는 매력적이다.

그러나 closed-world의 *닫혀 있다*는 가정이 자바 생태계와 마찰을 일으킨다. 자바는 30년간 *open-world*에서 살아왔다. Reflection으로 임의의 클래스를 들춰보고, dynamic proxy로 인터페이스 구현체를 런타임에 찍어내고, ServiceLoader로 어떤 구현이 올라올지 실행 시점에야 결정한다. Spring·Hibernate·Jackson 같은 프레임워크는 이 동적 능력 위에 세워졌다. closed-world에 가두려면 *어떤 클래스가 reflection으로 접근될지, 어떤 인터페이스가 proxy 대상인지, 어떤 리소스가 로드될지*를 빌드 시점에 GraalVM에게 알려줘야 한다. 그 메타데이터를 **reachability metadata**라고 부른다. 다행히 Spring Boot 3가 빌드 타임에 이 메타데이터를 알아서 뽑아주지만, 마이너한 라이브러리를 쓰는 자리에선 우리가 직접 손으로 채워줘야 한다. 한두 번 해보면 *번거로운* 정도가 아니라 마음이 *찜찜해진다*.

게다가 동적 클래스 로딩, 임의의 바이트코드 생성, JVM 에이전트는 닫혀 있는 세계에선 원천적으로 못 쓴다. 모니터링 에이전트를 붙이려다 *어, 안 되네* 한 번 겪으면 그 기억이 오래 간다.

이쯤에서 JDK AOT(Leyden)와 GraalVM의 차이를 한 표로 정리하자.

| 축 | GraalVM Native Image | JDK AOT (Leyden) |
|---|---|---|
| 산출물 | 네이티브 실행 파일 (JVM 불필요) | JVM + AOT 캐시 (`.aot` 또는 `.jsa`) |
| 세계관 | closed-world (정적 분석) | open-world (기존 JVM과 동일) |
| Reflection·proxy | reachability metadata 필요 | 그대로 동작 |
| 빌드 시간 | 수 분 단위 (정적 분석이 무겁다) | 짧음 (training run 한 번) |
| 시작 시간 | 수십 ms 수준 | 수백 ms ~ 1초대 |
| 메모리 풋프린트 | 매우 낮음 | JVM 기본보다 약간 낮음 |
| 호환성 | 라이브러리 따라 위험 | 기존 코드 그대로 |
| 운영 도구 | JFR·JMC 일부 제한 | 그대로 사용 |

표만 봐도 어떻게 갈라야 할지 윤곽이 잡힌다. *극단의 콜드 스타트와 메모리가 최우선*이고, *라이브러리 호환성을 통제할 수 있는* 상황이면 GraalVM이 답이다. *기존 코드 그대로 두고 시작 시간을 합리적으로 줄이고 싶다*면 JDK AOT가 자연스러운 첫 카드다. 두 길은 경쟁이라기보다, *연속적인 선택지*에 가깝다. 우리는 둘 다 가질 권리가 있다.

## Spring Boot 3.3+의 CDS 통합 — training run으로 충분하다

말로만 효과를 이야기하면 와닿지 않으니, Spring Boot에서 실제로 어떻게 쓰는지 보자. Spring Boot 3.3은 *Class-Data Sharing*을 *Maven/Gradle 플러그인 한 줄*로 지원한다. 컨테이너 이미지를 빌드할 때 *워밍업 단계*가 한 번 들어간다는 차이뿐이다.

```bash
# 1) training run — 앱을 한 번 띄웠다 곧장 종료한다
java -Dspring.context.exit=onRefresh \
     -XX:ArchiveClassesAtExit=application.jsa \
     -jar app.jar

# 2) 실제 실행 — 만들어진 아카이브를 매핑해 띄운다
java -XX:SharedArchiveFile=application.jsa -jar app.jar
```

`spring.context.exit=onRefresh`는 Spring 6.1에 들어간 옵션이다. ApplicationContext가 `refresh()`까지 끝낸 순간 곧장 종료한다 — *컨트롤러는 한 번도 호출하지 않고*. 그 사이에 Spring은 BeanDefinition을 모두 로드하고 AutoConfiguration을 다 돌렸으니, 컨테이너에 자주 들어오는 클래스 목록은 이미 다 메타스페이스에 올라가 있다. JVM은 종료 직전에 그 상태를 통째로 아카이브로 떨군다. *컨테이너 이미지를 빌드하는 그 자리에서* 한 번이면 충분하다.

여기에 Spring Framework 6.1의 *Spring AOT*까지 얹으면 그림이 더 흥미로워진다. Spring AOT는 *빌드 타임에* BeanFactory의 초기화 코드를 미리 계산해 자바 코드로 생성해 둔다. 런타임의 BeanFactoryPostProcessor 단계 상당 부분이 *컴파일된 코드*로 치환된다는 의미다. Spring AOT + JDK AOT 캐시를 둘 다 켠 Petclinic 측정에서, *기본 실행 대비 startup이 4배 정도* 짧아진다는 보고가 Spring 블로그와 Piotr Minkowski의 글에 올라와 있다. (정확한 배수는 머신·버전·heap 크기에 따라 흔들리니, 우리 환경에서 직접 측정하는 편이 낫다.)

PayBridge의 Lambda로 돌아가 보자. 평소 cold start가 3.2초였다고 하면, Spring Boot 3.3의 CDS만으로 2초 안쪽으로 떨어진다. JDK 24의 JEP 483 AOT 캐시를 더하면 1.5초대. JDK 25의 JEP 515 method profiling이 합쳐지면 1초 안쪽이 시야에 들어온다. *GraalVM으로 가지 않고도* SLA를 다시 맞출 가능성이 생기는 것이다. 운영팀 입장에서는 *기존 코드 그대로* 라는 한 마디가 묵직하다.

## JEP 519: Compact Object Headers — 64비트로 줄어든 객체 머리

이번엔 시작 시간과 결이 다른 이야기다. 메모리.

자바의 모든 객체는 *헤더*를 가진다. 64비트 JVM 기준으로 평소 96~128비트, 즉 12~16바이트가 매 객체마다 붙어 다닌다. 이 헤더는 두 부분으로 나뉜다. **mark word**는 객체의 락 상태, identity hash code, GC 마크 비트 같은 메타데이터를 담는 64비트짜리 슬롯이다. **klass pointer**는 이 객체가 어떤 클래스의 인스턴스인지 가리키는 포인터로, compressed class pointer가 켜져 있으면 32비트, 아니면 64비트다.

작은 객체일수록 헤더 비율이 *부담스럽다*. `Integer` 박싱 객체 하나가 실제로 담는 데이터는 `int` 4바이트인데, 그 위에 헤더가 12~16바이트 붙는다. 캐시에 `Long`을 수십만 개 쌓아두는 워크로드, JSON 파서가 임시 객체를 양산하는 워크로드, ORM이 엔티티 그래프를 메모리에 펼치는 워크로드 — 이런 자리에선 헤더가 차지하는 비율이 만만치 않다.

Java 25의 **JEP 519: Compact Object Headers**는 이 헤더를 *64비트로 압축*한다. mark word의 자주 안 쓰는 필드를 줄이고, klass pointer를 mark word 안에 작은 인덱스로 끼워 넣는 설계다. 효과는 측정에 따라 다양하게 보고된다.

- 작은 객체가 많은 워크로드(캐시, JSON 파싱, 컬렉션 무거운 코드)에서 *힙 사용량 10~22% 감소*.
- 캐시 라인 효율이 좋아지면서 GC 압력이 줄어든다 — 같은 힙 안에 더 많은 객체가 들어가니까.
- 일부 측정에서 CPU 사용량이 *30%까지* 절감됐다는 보고가 있다. (Compact Headers 자체보다는, GC 사이클이 줄어든 부수 효과가 큰 것으로 보인다.)

켜는 방법은 단순하다.

```bash
java -XX:+UnlockExperimentalVMOptions \
     -XX:+UseCompactObjectHeaders \
     -jar app.jar
```

Java 25에서는 experimental 플래그 단계지만, Java 26~27에 기본 동작으로 승격될 가능성이 높다. 그렇다면 *지금 그냥 켜도 되는가*?

조심해야 할 자리가 있다. `Unsafe`로 객체 헤더 오프셋을 *손으로 계산*하는 라이브러리가 있다면 마음 *졸일 일*이다. 16바이트를 가정하고 코드 안에 상수가 박혀 있다면 헤더가 8바이트로 줄어든 순간 깨진다. Lucene이나 일부 고성능 직렬화 라이브러리가 이런 코드를 가졌다는 보고가 있었고, 대부분 빠르게 패치됐지만 *우리 의존성 트리에 어떤 게 있는지 한 번은 훑고 가는 편이 낫다*. JOL(Java Object Layout) 같은 도구로 실제 객체 레이아웃을 한 번 떠보면 마음이 편해진다.

또 하나, 작은 객체 비중이 낮은 워크로드 — *큰 byte 배열을 중심으로 도는* 동영상 처리나 머신러닝 추론 같은 자리 — 에서는 효과가 미미하다. 모든 워크로드를 다 살리는 마법은 아니다. *어디서 켜고 어디서 끌지*는 측정으로 결정하는 편이 낫다.

## 한 단계씩 쌓아보자 — Baseline에서 Compact Headers까지

도구가 늘어났으니 한 자리에 모아 보자. PayBridge의 결제 검증 서비스 — Spring Boot 3.3, Java 25, 평소 startup 3.2초, heap 사용량 380MB — 를 가정하고 단계별 효과를 누적해 보자. (수치는 환경에 따라 흔들리니, *비율의 감*만 잡자.)

| 단계 | 명령/옵션 | startup | heap | 비고 |
|---|---|---|---|---|
| Baseline | 평소 실행 | 3.2s | 380MB | 비교 기준 |
| + CDS | `-XX:ArchiveClassesAtExit=app.jsa` | ~2.1s | 360MB | training run 1회 |
| + JDK AOT (JEP 483) | `-XX:AOTCache=app.aot` | ~1.5s | 350MB | Java 24+ |
| + Method Profiling (JEP 515) | `-XX:AOTMode=record/use` | ~1.1s | 350MB | Java 25+ |
| + Spring AOT | `spring-aot` 플러그인 | ~0.8s | 340MB | 빌드 시간은 늘어남 |
| + Compact Headers | `-XX:+UseCompactObjectHeaders` | ~0.8s | 290MB | startup보다 heap 효과 |

표를 들여다보면 두 가지가 보인다. *startup에 가장 큰 영향을 주는 것은 CDS와 JDK AOT*다. Spring AOT를 더하면 한 번 더 떨어지지만, 빌드 시간이 길어진다는 트레이드오프가 따라온다. *heap에 가장 큰 영향을 주는 것은 Compact Headers*다. 둘은 *겹치지 않고 서로 다른 자리를 친다*. 그래서 함께 쓰는 의미가 있다.

PayBridge 팀의 결론은 이렇게 정해진다. Lambda·Cloud Run의 단명 워크로드에는 CDS + JDK AOT + Compact Headers를 *기본 세트*로 켠다. 매니페스트와 Dockerfile에 한 번 박아두면 그 다음부터는 잊고 살아도 된다. 더 극단적인 콜드 스타트가 필요한 *몇몇 핫스팟*만 GraalVM 네이티브 이미지를 검토한다. 운영팀이 길게 한숨을 돌리는 풍경이 그려진다.

## 마무리: GraalVM이 답이 아닐 자유

11년 전 자바는 *시작이 느린 언어*였다. JIT 워밍업과 무거운 클래스 로딩이 *어쩔 수 없는 자바의 운명*처럼 여겨졌다. 그 운명을 옆에서 깬 것이 GraalVM 네이티브 이미지였고, *자바는 못 한다*는 통념을 한 번 뒤집은 공로가 컸다. 그러나 모든 팀이 closed-world의 비용을 치르고 거기까지 갈 필요는 없다. OpenJDK는 자기 영역 안에서 그 비용을 점진적으로 깎아내고 있다 — AppCDS, Dynamic CDS, JEP 483, JEP 515, 그리고 Leyden이 가져올 그 다음 카드들로. 거기에 Compact Object Headers가 메모리 풍경까지 한 번 더 깎는다.

이번 장에서 기억해둘 것은 셋이다. *첫째, CDS와 JDK AOT는 한 번의 training run으로 켜진다.* 도입 비용이 GraalVM과 비교가 안 된다. *둘째, GraalVM과 JDK AOT는 경쟁이 아니라 연속적인 선택지다.* 우리의 코드와 운영 사정에 맞춰 어느 자리에 어떤 카드를 쓸지 결정하면 된다. *셋째, Compact Object Headers는 작은 객체 많은 워크로드에서 마음 편히 켤 만하다.* `Unsafe`로 헤더를 들춰보는 라이브러리만 한 번 점검해두자.

다음 장에서는 결이 다른 이야기로 넘어간다. 11년 사이 우리 손에 쥐어진 *도구들* — JShell부터 jpackage, jlink, jwebserver, jextract, JFR/JMC, 그리고 빌드 도구의 자바 호환까지 — 을 한 자리에 모아 본다. *우리 손에 있는 도구를 우리는 어디까지 알고 있는가*. 그 점검의 시간이다.
