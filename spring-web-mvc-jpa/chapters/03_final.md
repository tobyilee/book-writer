# 3장. 첫 엔드포인트 — 빌드 도구부터 동작하는 서버까지

새 프로젝트 폴더를 하나 만들었다고 해보자. 그런데 그 안에는 아직 아무것도 없다. `package.json`도, `node_modules`도, 익숙한 `npm run dev`도 없다. 대신 `build.gradle`이라는 처음 보는 파일과 `gradlew`라는 정체불명의 실행 파일이 놓여 있다. 터미널에 무엇을 쳐야 서버가 뜨는지조차 모르겠다. 이 순간, 자바를 문법까지는 떼었어도 빌드 한 번 돌려본 적 없는 프런트 개발자라면 누구나 살짝 막막해진다.

앞의 두 장에서 우리는 머릿속 모델을 다듬었다. `fetch`의 반대편을 들여다봤고, AI를 동반자로 쓰되 맹신하지 않는 태도를 약속했다. 그런데 머리로만 아는 것과 손으로 띄워보는 것 사이에는 생각보다 큰 강이 있다. 이번 장에서 그 강을 건넌다. 이론은 잠시 접어두자. 우리의 목표는 단 하나다 — **가장 빨리, 응답하는 서버 하나를 손으로 띄우는 것.** 현장의 백엔드 선배들이 입을 모아 하는 조언도 똑같다. "이론부터 시작하면 막힌다. 동작하는 엔드포인트를 먼저 띄우고, 이론은 그 뒤에." 프런트에서 우리가 "일단 화면부터 렌더해보자"며 배웠던 그 경로와 정확히 같다.

그러니 이번 장에서 우리가 키워나갈 연속 프로젝트의 첫 삽을 뜨자. 이 책 전체를 함께 자라날 프로젝트의 이름은 **TaskBoard** — 할 일을 관리하는 작은 API다. 오늘은 그 빈 땅에 첫 말뚝을 박는다.

## npm 세계에서 온 당신을 위한 빌드 지도

코드를 짜기 전에 먼저 길부터 익히자. 자바 빌드를 한 번도 안 해본 사람이 가장 먼저 좌절하는 지점이 바로 여기다. "코드는 한 줄도 안 썼는데 빌드 도구에서 막혔다"는 경험은 정말 맥이 빠진다. 다행히 우리에겐 이미 든든한 무기가 하나 있다. 바로 `npm`에 대한 감각이다. 자바의 빌드 세계도 결국 같은 문제를 푸는 도구라서, npm에 빗대면 의외로 빠르게 손에 잡힌다.

자바 진영에는 빌드 도구가 둘 있다. **Gradle**과 **Maven**이다. 둘 다 의존성을 받아오고 프로젝트를 빌드하고 실행하는 일을 한다는 점에서는 같다. 우리는 이 책 내내 **Gradle**을 쓴다. 이유는 단순하다. Gradle은 설정을 Groovy나 Kotlin 같은 코드로 쓸 수 있어 표현력이 좋고, 한 번 빌드한 결과를 영리하게 재활용하는 증분 빌드 덕분에 빠르다. Maven도 여전히 현장에서 많이 쓰이지만, 우리는 존재만 알아두고 지나가자. 둘 중 하나만 익혀도 다른 하나는 어렵지 않게 따라온다.

Gradle을 npm에 빗대면 이렇게 정리된다.

| npm 세계 | Gradle 세계 | 하는 일 |
|---|---|---|
| `package.json`의 `dependencies` | `build.gradle`의 `dependencies` | 외부 라이브러리 선언 |
| `npm install` | (Gradle이 빌드/실행 시 자동으로) | 의존성 내려받기 |
| `npm run dev` | `./gradlew bootRun` | 개발 서버 띄우기 |
| `npm run build` | `./gradlew build` | 배포용 산출물 만들기 |
| `node_modules/` | `~/.gradle` 캐시 | 받아온 라이브러리 보관 |

표를 보면 한결 마음이 놓이지 않는가? 새로운 도구를 처음부터 배우는 게 아니라, 이미 아는 개념에 새 이름표를 붙이는 일에 가깝다.

조금 더 들여다보자. 프런트에서 새 라이브러리를 쓰고 싶을 때 우리는 `package.json`의 `dependencies`에 한 줄을 추가했다. 자바에서도 똑같다. 라이브러리가 필요하면 `build.gradle`의 `dependencies` 블록에 한 줄을 더한다. 이 파일이 곧 우리 프로젝트의 `package.json`이라고 생각하면 된다.

그렇다면 `gradlew`, 즉 `./gradlew`로 시작하는 명령은 뭘까? 이건 **Gradle Wrapper**라는 것으로, "이 프로젝트에 딱 맞는 버전의 Gradle을 알아서 받아 실행해주는 작은 스크립트"다. 내 컴퓨터에 Gradle이 깔려 있든 없든, 버전이 다르든 상관없이 프로젝트가 정한 버전으로 돌려준다. npm으로 치면 `npx`로 특정 버전 도구를 고정해 실행하는 감각과 비슷하다. 그러니 우리는 그냥 프로젝트 폴더 안에서 `./gradlew bootRun`이라고 치기만 하면 된다.

서버를 띄웠다가 코드를 고쳐 다시 띄우고 싶을 때는 실행 중인 터미널에서 `Ctrl+C`로 멈춘 뒤 `./gradlew bootRun`을 다시 치면 된다. 프런트의 핫 리로드에 익숙한 우리에게 이 "멈췄다 다시 켜는" 과정이 처음엔 번거롭게 느껴질 수 있다. (자동 재시작이 답답하다면 나중에 Spring Boot DevTools 같은 도구를 의존성에 더할 수 있지만, 지금은 일단 한 번 제대로 띄워 응답을 받는 데 집중하자.)

그리고 `./gradlew build`는 서버를 띄우는 게 아니라 배포할 수 있는 산출물(`.jar` 파일)을 만드는 명령이다. `npm run build`가 배포용 번들을 뽑아내던 것과 똑같은 자리에 있다. 개발 중에는 거의 쓸 일이 없으니 "배포할 때 쓰는 것" 정도로만 기억해두면 충분하다. 디버깅이 필요할 때는 IntelliJ의 디버그(벌레 모양) 버튼으로 실행을 멈춰 세우고 변수를 들여다볼 수 있다 — 막막할 때를 위한 안전장치 정도로만 알아두자.

## start.spring.io에서 프로젝트를 빚어내자

길을 익혔으니 이제 진짜 프로젝트를 만들 차례다. 빈 폴더에 `build.gradle`을 손으로 쓰는 일은, 다행히 우리가 직접 하지 않아도 된다. 프런트에 `create-next-app`이 있다면, Spring에는 **Spring Initializr**가 있다. 브라우저에서 [`start.spring.io`](https://start.spring.io)에 접속하면, 몇 가지를 고르는 것만으로 빌드 파일과 폴더 구조가 갖춰진 프로젝트 한 벌을 압축 파일로 내려받을 수 있다.

화면에서 우리가 정해야 할 것들을 하나씩 살펴보자.

- **Project:** Gradle - Groovy(또는 Gradle - Kotlin)를 고르자. 앞서 정한 대로 Gradle을 쓴다.
- **Language:** Java.
- **Spring Boot:** **3.x** 버전을 고르자. 여기서 잠깐 멈추고 생각해볼 게 있다. (바로 아래에서 다룬다.)
- **Project Metadata:** Group은 `com.example`, Artifact는 `taskboard` 정도로 두자. 이건 프로젝트 식별자일 뿐이라 부담 없이 정해도 된다.
- **Packaging:** Jar.
- **Java:** **17** 또는 **21**을 고르자. 둘 다 장기 지원(LTS) 버전이라 안심하고 써도 된다. Spring Boot 3.x는 Java 17 이상을 요구한다.
- **Dependencies:** 오른쪽 "ADD DEPENDENCIES" 버튼을 눌러 **Spring Web**을 추가하자. 이게 HTTP 요청을 받아 처리하는 데 필요한 핵심이다. (다음 장들에서 Validation, JPA 같은 것들을 하나씩 더 붙여나갈 텐데, 지금은 Spring Web 하나면 충분하다.)

> Spring Initializr의 화면 구성과 버전 선택지는 시점에 따라 조금씩 달라질 수 있다. 화면에 보이는 명칭이 책과 다르더라도 당황하지 말고, 큰 흐름(Gradle·Java·Spring Boot 3.x·Spring Web)만 맞추면 된다.

여기서 잠깐, 왜 굳이 Spring Boot **3.x**일까? 이 책을 쓰는 2026년 5월 시점에 이미 더 높은 버전이 stable로 나와 있는데 말이다. 답은 이렇다. 3.x가 여전히 수많은 실무 현장에서 굴러가는 주류 버전이라, 지금 배워두면 당장 마주칠 코드와 가장 잘 맞는다. 다만 한 가지는 솔직히 짚어두자. 버전 경계는 빠르게 움직이는 영역이라, 새 그린필드 프로젝트를 시작한다면 더 높은 버전도 고려할 가치가 있다. 이 책에서 다지는 토대(특히 `jakarta` 네임스페이스 같은 것)는 그대로 다음 버전으로 이어지니 걱정하지 말자. "왜 3.x로 시작했는가"라는 이야기는 책의 마지막 장에서 다시 매듭짓는다.

`GENERATE` 버튼을 누르면 zip 파일이 떨어진다. 압축을 풀고 IntelliJ로 그 폴더를 열어보자. 프런트에서 `create-next-app`이 만들어준 프로젝트를 처음 열었을 때처럼, 낯설지만 정돈된 구조가 우리를 맞이한다.

## 폴더를 한 바퀴 둘러보자

프로젝트를 열면 폴더가 제법 많아 당황스러울 수 있다. 하지만 우리가 당장 신경 쓸 곳은 몇 군데뿐이다. 천천히 둘러보자.

```
taskboard/
├── build.gradle               ← package.json에 해당. 의존성·빌드 설정
├── gradlew, gradlew.bat       ← Gradle Wrapper 실행 스크립트
├── settings.gradle            ← 프로젝트 이름 등 최상위 설정
└── src/
    └── main/
        ├── java/com/example/taskboard/
        │   └── TaskboardApplication.java   ← 시작점 (main 함수)
        └── resources/
            └── application.properties      ← 환경 설정 (.env 비슷한 자리)
```

`build.gradle`은 이미 익숙하다. 우리의 `package.json`이다. 한번 열어보면 `dependencies` 블록 안에 `spring-boot-starter-web`이 들어 있을 것이다. 우리가 Initializr에서 고른 "Spring Web"이 바로 이 한 줄로 들어온 것이다.

그리고 `TaskboardApplication.java`. 이 파일이 우리 서버의 시작점이다. 프런트로 치면 앱이 처음 부팅되는 진입 파일과 같다. 열어보면 이렇게 생겼다.

```java
package com.example.taskboard;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TaskboardApplication {

    public static void main(String[] args) {
        SpringApplication.run(TaskboardApplication.class, args);
    }
}
```

코드를 보면 의문이 하나 생긴다. 고작 이 몇 줄로 어떻게 웹 서버가 뜬다는 걸까? `main` 함수 안에서 하는 일이라고는 `SpringApplication.run(...)` 한 줄 호출이 전부인데 말이다. 비밀은 클래스 위에 붙은 `@SpringBootApplication`이라는 표식, 그리고 Spring Boot의 **자동 설정(auto-configuration)**에 있다. 우리가 `spring-boot-starter-web`을 의존성에 넣었다는 사실만으로, Spring Boot는 "아, 이 사람은 웹 서버를 원하는구나" 하고 알아서 톰캣이라는 웹 서버를 띄울 준비를 마친다. 우리가 일일이 "서버를 켜라, 포트를 열어라, 요청을 받아라"라고 명령하지 않았는데도 말이다.

솔직히 말하면, 이쯤에서 조금 찜찜할 수 있다. "보이지 않는 곳에서 누가 뭘 알아서 해준다"는 건 편하면서도 어딘가 미덥지 않다. 직접 `new`로 객체를 만들어 연결한 기억이 없는데 모든 게 굴러가니, 마치 마법 같다. 그 찜찜함, 아주 건강한 감각이다. **하지만 지금은 그 마법을 그냥 누리자.** 마법의 정체를 걷어내고 "누가, 무엇을, 어떻게" 연결했는지 손으로 헤집어보는 일은 바로 다음 장에서 한다. 오늘은 "일단 동작한다"는 사실만 즐기면 된다.

## 첫 엔드포인트를 띄우고, 눈으로 확인하자

드디어 코드를 쓴다. 우리의 목표는 `/api/tasks`로 GET 요청이 들어오면 할 일 목록을 JSON으로 돌려주는 것이다. 프런트에서 우리가 수없이 `fetch('/api/tasks')`로 때렸던 바로 그 반대편을, 이번엔 우리가 만든다.

`TaskboardApplication.java`가 있는 폴더에 `TaskController.java`라는 새 파일을 하나 만들자.

```java
package com.example.taskboard;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class TaskController {

    @GetMapping("/api/tasks")
    public List<String> getTasks() {
        return List.of("Spring 첫 엔드포인트 띄우기", "커피 마시기");
    }
}
```

이게 전부다. Next.js의 API route를 떠올려보자. 특정 경로로 요청이 오면 핸들러 함수가 실행되고, 그 함수가 반환한 값이 응답이 됐다. 여기서도 똑같다. `@GetMapping("/api/tasks")`는 "이 경로로 GET 요청이 오면 이 메서드를 실행하라"는 뜻이고, `getTasks()`가 반환한 리스트가 그대로 응답 바디가 된다.

코드를 한 줄씩 짚어보자. 클래스 위의 `@RestController`는 "이 클래스는 HTTP 요청을 받아 처리하고, 반환값을 JSON으로 바꿔 돌려주는 역할이다"라고 Spring에게 알리는 표식이다. 프런트에서 우리가 `fetch().then(res => res.json())`으로 손수 파싱하던 그 직렬화/역직렬화를, 서버 쪽에서는 Spring이 알아서 해준다. 우리가 `List<String>`을 반환하면, Spring은 그걸 `["...", "..."]` 형태의 JSON 배열로 변환해 응답에 실어 보낸다. 손으로 `JSON.stringify`를 부를 필요가 없다. 편하지 않은가?

프런트 경험과 나란히 놓고 보면 더 또렷해진다. Next.js의 App Router에서라면 우리는 이런 식으로 같은 엔드포인트를 만들었을 것이다.

```javascript
// app/api/tasks/route.js (Next.js)
export async function GET() {
  return Response.json(["Spring 첫 엔드포인트 띄우기", "커피 마시기"]);
}
```

`route.js`라는 파일을 특정 경로에 두면 그 경로가 곧 라우팅이 됐고, `GET`이라는 이름의 함수가 GET 요청을 받았다. Spring에서는 그 "파일 위치로 정해지던 경로"가 `@GetMapping("/api/tasks")`라는 어노테이션으로, "함수 이름으로 정해지던 메서드"가 `@GetMapping`이라는 표식으로 옮겨왔을 뿐이다. 본질은 똑같다 — 어떤 경로로 어떤 메서드의 요청이 오면, 어떤 함수가 실행되어 응답을 만든다. 자리만 바뀌었지, 우리가 이미 아는 그 구조 그대로다. 이렇게 익숙한 것 위에 새 이름표를 얹으면, 낯선 어노테이션도 한결 만만해진다.

이제 서버를 띄울 차례다. 터미널을 프로젝트 폴더로 옮긴 뒤(또는 IntelliJ의 내장 터미널에서) 이렇게 친다.

```bash
./gradlew bootRun
```

처음 실행하면 의존성을 내려받느라 잠깐 시간이 걸린다. `npm install`이 처음 한 번 오래 걸리던 것과 같다. 로그가 주르륵 흐르다가 "Started TaskboardApplication"이라는 줄이 보이면 성공이다. 기본적으로 서버는 8080 포트에서 우리의 요청을 기다린다.

이제 정말로 응답하는지 두 눈으로 확인하자. 브라우저를 열고 주소창에 이렇게 입력해보자.

```
http://localhost:8080/api/tasks
```

화면에 이런 JSON이 떠야 한다.

```json
["Spring 첫 엔드포인트 띄우기","커피 마시기"]
```

터미널을 더 좋아한다면 `curl`로 같은 걸 확인할 수도 있다.

```bash
curl http://localhost:8080/api/tasks
```

이 한 줄의 JSON이 화면에 떴다면, 축하한다. 방금 당신은 손으로 첫 Spring 서버를 띄우고, 그 서버가 응답하는 모습을 직접 봤다. 며칠 전까지만 해도 `fetch`가 때리는 블랙박스였던 그 반대편을, 이제 당신이 만들어 통제하고 있다. 이 작은 성취감을 충분히 누리자. "할 수 있다"는 이 감각이 앞으로의 여정을 끌고 가는 연료가 된다.

> **TaskBoard 진행 현황** — 지금 우리의 할 일 목록은 코드 안에 박힌 문자열 두 개에 불과하다. 서버를 끄면 사라지고, 새로 추가할 수도 없다. 괜찮다. 5장에서 메모리에 사는 제대로 된 목록으로, 6장에서는 데이터베이스에 눌러 담는 목록으로 한 걸음씩 키워나간다. 오늘은 첫 말뚝을 박았다는 것으로 충분하다.

## AI에게 스캐폴드를 맡길 때 — 첫 번째 함정

::: tip AI 페어코딩 학습 포인트
이 작은 프로젝트를 손으로 만들어봤으니, 이제 같은 일을 AI에게 시켜보면 어떨까? 실무에서는 이런 보일러플레이트성 작업이야말로 AI가 가장 잘하는 영역이다. 다만 — 여기서 우리가 2장에서 약속한 태도가 처음으로 시험대에 오른다.
:::

상상해보자. 당신이 Cursor나 Claude Code에게 이렇게 부탁한다. "Spring Boot로 할 일 목록을 반환하는 REST 컨트롤러를 만들어줘." AI는 척척 코드를 뱉어낸다. 그럴듯해 보인다. 그런데 정말 그대로 믿어도 될까?

문제는 이렇다. AI가 학습한 방대한 코드 중에는 **오래된 버전**으로 짜인 것이 아주 많다. 그래서 별다른 단서를 주지 않으면, AI는 종종 자신만만하게 구버전 코드를 내놓는다. 가장 흔한 함정이 바로 **`javax`와 `jakarta`** 사이의 혼동이다.

무슨 이야기인지 짚어보자. 자바 진영은 한때 `javax.*`라는 네임스페이스를 썼다. 그런데 오라클에서 이클립스 재단으로 기술이 넘어가면서 상표 문제가 생겼고, 그 결과 `javax.*`가 `jakarta.*`로 통째로 이름이 바뀌었다. 그리고 **Spring Boot 3.0이 바로 이 `jakarta.*`를 채택한 첫 버전이다.** 즉, 우리가 쓰는 3.x에서는 `import jakarta.persistence.Entity` 같은 식으로 써야 하는데, AI가 옛 기억을 더듬어 `import javax.persistence.Entity`를 주면 — 컴파일조차 되지 않거나, 되더라도 엉뚱하게 동작한다. 처음 겪으면 정말 난감하다. 분명 AI가 시키는 대로 했는데 빨간 줄이 가득하니 말이다.

그렇다면 어떻게 막을까? 답은 의외로 단순하다. **프롬프트에 버전을 명시하는 것**이다. 이렇게 부탁해보자.

> "Spring Boot 3.x 기준으로, jakarta 네임스페이스를 써서 할 일 목록을 반환하는 REST 컨트롤러를 만들어줘."

버전과 네임스페이스를 못 박아주는 것만으로 AI가 구버전 코드를 줄 확률이 크게 줄어든다. 하지만 여기서 멈추면 안 된다. 더 중요한 두 번째 습관이 있다. **AI가 준 코드를 직접 읽고 검수하는 것**이다. 생성된 `build.gradle`을 열어 Spring Boot 버전이 3.x로 적혀 있는지, import 문에 `javax.*`가 슬쩍 섞여 있지 않은지 두 눈으로 확인하자. 의존성에 엉뚱한 게 끼어들지는 않았는지도 살펴보자.

이게 바로 우리가 2장에서 이야기한 신선도 함정의 첫 실전이다. AI는 스캐폴드를 빠르게 만들어주는 훌륭한 동반자다. 하지만 그 결과물이 우리가 쓰는 버전과 맞는지 가려내는 일은, 끝까지 사람의 몫이다. 기억해두자. **AI는 코드를 주고, 검증은 우리가 한다.**

## 마무리

이번 장에서 우리는 머릿속에만 있던 모델을 처음으로 손끝으로 끌어냈다. 낯설던 Gradle을 `package.json`에 빗대 길들였고, `@RestController`와 `@GetMapping` 단 몇 줄로 첫 엔드포인트를 띄워 브라우저로 응답까지 확인했다. AI에게 스캐폴드를 맡길 때 버전을 명시하고 결과물을 직접 검수하는 첫 실전도 치렀다.

그런데 우리는 어디서도 컨트롤러를 `new`로 만들지 않았는데, Spring은 그 컨트롤러를 알아서 만들어 요청에 연결했다. "보이지 않는 손이 객체를 만들어 끼워 넣는" 이 마법, 편하긴 한데 정체를 모르고 쓰는 건 어딘가 찜찜하다. 다음 장에서 그 마법을 정면으로 걷어낸다. 의존성 주입(DI)과 제어의 역전(IoC)이 실제로 무슨 일을 하는지, 오늘 띄운 이 코드를 첫 표본 삼아 손으로 헤집어보자.
