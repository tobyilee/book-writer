# 5장. 제대로 된 REST API — DTO·검증·전역 예외·CORS·첫 테스트

당신이 지금까지 만든 TaskBoard에 대고, 이런 요청을 한번 던져본다고 해보자.

```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": ""}'
```

제목이 텅 비어 있다. 누가 봐도 잘못된 요청이다. 그런데 서버는 어떻게 반응할까? 운이 나쁘면 빈 제목짜리 할 일이 아무렇지 않게 목록에 들어앉는다. 운이 더 나쁘면 어딘가에서 `NullPointerException`이 터지고, 클라이언트에는 500 에러와 함께 자바 스택 트레이스가 주르륵 쏟아진다. 우리 React 앱에서 이 응답을 받았다고 상상해보자. 사용자에게 뭐라고 보여줄 것인가? "서버에서 `java.lang.NullPointerException`이 발생했습니다"라고? 생각만 해도 아찔하다.

지금까지 우리가 만든 API는 분명 **동작은 한다**. 정상적인 요청을 주면 정상적인 응답을 돌려준다. 하지만 딱 거기까지다. 잘못된 요청을 어떻게 거를지, 에러가 났을 때 클라이언트에게 무슨 말을 돌려줄지, 그리고 정작 내 React 앱에서 이 API를 부르면 왜 빨간 CORS 에러가 뜨는지 — 이 셋을 우리는 아직 손도 대지 않았다. 동작하지만 엉성한 API다. 이번 장에서 그 엉성함을 걷어내고, 험한 요청이 와도 품위를 잃지 않는 **견고한 API**로 키워보자. 그리고 마지막엔, 그 견고함을 두 눈이 아니라 코드로 증명하는 첫 테스트까지 손에 쥔다.

## 엔티티를 그대로 내보내면 안 될까? — DTO라는 칸막이

먼저 작은 질문 하나. 우리가 4장에서 만든 `Task`라는 객체를 요청 받을 때도 쓰고 응답 돌려줄 때도 쓰면 안 될까? 어차피 같은 할 일인데, 굳이 따로 만들 이유가 있을까?

이 의문은 자연스럽다. 처음엔 그렇게 해도 잘 돌아간다. 문제는 프로젝트가 자랄수록 고개를 든다. 지금은 `Task`가 `id`와 `title` 정도지만, 6장에서 DB를 붙이면 여기엔 생성 시각, 내부용 상태 플래그, 나중엔 비밀번호 해시 같은 민감한 필드까지 들러붙는다. 이 객체를 그대로 응답에 실어 보내면 클라이언트가 알 필요도 없는 내부 사정이 JSON에 통째로 노출된다. 반대로 요청을 받을 때 그대로 쓰면, 클라이언트가 `id`나 생성 시각을 멋대로 채워 보낼 수도 있다. 서버가 정해야 할 값을 클라이언트가 쥐고 흔드는 셈이다. 뒷맛이 영 찜찜하지 않은가?

그래서 우리는 **칸막이**를 하나 세운다. 데이터를 담아 계층 사이를 오가는 전용 객체, 바로 **DTO(Data Transfer Object)**다. 안에서 데이터를 다루는 객체(엔티티)와, 바깥으로 주고받는 객체(DTO)를 갈라놓는 것이다. 요청을 받는 DTO 하나, 응답을 돌려주는 DTO 하나, 이렇게 따로 둔다.

자바 17부터 들어온 **레코드(record)**를 쓰면 이런 DTO를 아주 간결하게 쓸 수 있다. 먼저 요청용 DTO다.

```java
package com.example.taskboard.dto;

public record TaskCreateRequest(String title, String description) {
}
```

이게 전부다. `record`는 "값을 담는 것이 전부인 불변 객체"를 한 줄로 선언하게 해준다. 프런트에서 요청 바디의 모양을 타입스크립트 `interface`로 정의하던 그 감각과 비슷하다. "이 엔드포인트는 `title`과 `description`을 받는다"는 계약을 코드로 못 박는 것이다.

응답용 DTO도 만들자.

```java
package com.example.taskboard.dto;

public record TaskResponse(Long id, String title, String description, boolean done) {
}
```

요청용엔 `id`가 없고 응답용엔 있다는 점에 주목하자. `id`는 서버가 정하는 값이지 클라이언트가 보내는 값이 아니기 때문이다. 들어오는 모양과 나가는 모양을 따로 설계할 수 있다는 것, 이게 DTO를 나누는 가장 큰 실익이다. **기억해두자. 검증과 노출의 경계는 엔티티가 아니라 DTO에서 그어야 한다.**

## `@Valid` — 검증을 프레임워크에 맡기자

칸막이를 세웠으니, 이제 그 칸막이에서 험한 요청을 걸러내자. 처음의 빈 제목 문제로 돌아가 보자. `title`이 비어 있으면 거절해야 한다. 가장 손쉽게 떠오르는 방법은 컨트롤러 안에서 직접 `if`로 검사하는 것이다.

```java
if (request.title() == null || request.title().isBlank()) {
    // 에러 처리...
}
```

이렇게 해도 동작은 한다. 하지만 검증 규칙이 한둘이 아니라면? 제목은 1자 이상 100자 이하, 설명은 500자 이하, 게다가 엔드포인트마다 비슷한 검사가 반복된다면? 컨트롤러는 금세 `if` 덩어리로 뒤덮이고, 정작 중요한 비즈니스 로직은 그 틈바구니에 파묻힌다. 번거롭고, 빠뜨리기 쉽고, 무엇보다 지저분하다.

그렇다면 어떻게 해야 할까? 이 반복을 프레임워크에 맡기는 방법이 있다. **Jakarta Bean Validation**(구현체는 Hibernate Validator)이다. DTO의 각 필드에 "이 필드는 이런 조건을 만족해야 한다"는 표식만 붙여두면, 검증은 Spring이 알아서 해준다. 앞서 만든 요청 DTO에 규칙을 붙여보자.

```java
package com.example.taskboard.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record TaskCreateRequest(

    @NotBlank(message = "제목은 비어 있을 수 없습니다.")
    @Size(max = 100, message = "제목은 100자를 넘을 수 없습니다.")
    String title,

    @Size(max = 500, message = "설명은 500자를 넘을 수 없습니다.")
    String description
) {
}
```

import 문을 잠깐 눈여겨보자. `jakarta.validation.constraints`다. `javax`가 아니다. 3장에서 약속한 그 신선도 감각, 여기서도 살아 있어야 한다. (이 어노테이션을 쓰려면 `build.gradle`에 `spring-boot-starter-validation` 의존성이 필요하다. 3장에서 Spring Web만 넣었다면 여기서 한 줄 더 보태자.)

이제 컨트롤러에서 이 검증을 발동시키자. 받는 파라미터 앞에 `@Valid`를 붙이기만 하면 된다.

```java
package com.example.taskboard.controller;

import com.example.taskboard.dto.TaskCreateRequest;
import com.example.taskboard.dto.TaskResponse;
import com.example.taskboard.service.TaskService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @PostMapping
    public ResponseEntity<TaskResponse> create(@Valid @RequestBody TaskCreateRequest request) {
        TaskResponse created = taskService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

생성자 주입으로 `TaskService`를 받는 모양은 4장에서 익힌 그대로다. 새로 등장한 건 `@Valid @RequestBody`다. `@RequestBody`는 "요청 바디의 JSON을 이 객체로 바꿔달라"는 뜻이고(이 변환은 Jackson이 맡는다. 프런트에서 `await res.json()`으로 손수 파싱하던 일을 서버에선 자동으로 해준다), `@Valid`는 "그렇게 만든 객체가 DTO에 적힌 규칙을 지키는지 검사해달라"는 뜻이다.

그래서 빈 제목을 보내면? `@NotBlank` 규칙이 깨지고, Spring은 `MethodArgumentNotValidException`이라는 예외를 던진다. 우리가 `if` 한 줄 쓰지 않았는데도 말이다. 검증을 프레임워크에 위임한다는 게 바로 이런 것이다. 그런데 한 가지 의문이 남는다. 예외가 던져진 건 좋은데, 그래서 클라이언트는 대체 뭘 받게 될까?

## `ResponseEntity`와 상태코드 — 응답을 내가 설계한다

여기서 1장의 이야기를 다시 꺼내자. 우리는 그때 "상태코드는 받는 것이 아니라 내가 결정하는 책임"이라고 했다. 그 책임을 이제 실제로 행사할 때가 왔다.

방금 컨트롤러 코드를 다시 보자. 반환 타입이 그냥 `TaskResponse`가 아니라 `ResponseEntity<TaskResponse>`다. 이 `ResponseEntity`가 바로 "응답 전체를 내 손으로 빚는" 도구다. 바디뿐 아니라 **상태코드와 헤더까지** 내가 직접 정해 실어 보낼 수 있다.

새 할 일을 만들었을 때 우리가 돌려준 상태코드를 보자. `HttpStatus.CREATED`, 즉 **201**이다. 그냥 200이 아니다. 왜 굳이 구별할까? 프런트 입장에서 생각해보자. 응답 바디를 일일이 까보지 않아도 상태코드 201만 보고 "아, 새로 만들어졌구나" 하고 알 수 있다면 얼마나 깔끔한가. 상태코드는 그 자체로 하나의 약속이고 언어다.

1장에서 본 상태코드 표(200·201·400·404 등)를 이제 `ResponseEntity`로 직접 실어 보내는 셈이다. 생성엔 201, 조회·수정엔 200, 검증 실패엔 400, 없는 자원엔 404. 여기에 하나만 새로 더하자. **409 Conflict** — 요청은 멀쩡하지만 현재 상태와 충돌할 때(이미 있는 걸 또 만들려 할 때 같은 경우) 쓴다. 이걸 "받는 코드"가 아니라 "내가 의도적으로 고르는 코드"로 보기 시작하면, API 설계의 결이 완전히 달라진다. 프런트에서 `res.status`를 읽어 분기하던 우리가, 이제는 그 `status`를 **결정하는 쪽**에 선 것이다.

## 전역 예외 처리 — 에러도 일관된 모양으로

자, 가장 찜찜했던 지점으로 돌아가자. 검증에 실패하면 `MethodArgumentNotValidException`이 던져진다고 했다. 그런데 우리가 이걸 아무 데서도 받아주지 않으면, 이 예외는 Spring의 기본 에러 처리로 흘러가 두서없는 응답이 된다. 어떨 땐 장황한 자바 메시지가, 어떨 땐 빈 응답이 클라이언트에 전달된다. 엔드포인트마다 에러 모양이 제각각이라면, 우리 React 앱의 에러 처리 코드는 어디에 장단을 맞춰야 할지 난감해진다.

그렇다면 어떻게 해야 할까? 에러 응답의 모양을 한 군데에서 통일하면 된다. 컨트롤러마다 `try-catch`를 흩뿌리는 게 아니라, **모든 컨트롤러의 예외를 한곳에서 가로채는** 장치를 두는 것이다. 그게 바로 `@RestControllerAdvice`다.

먼저 클라이언트에게 돌려줄 에러 응답의 모양부터 DTO로 정하자.

```java
package com.example.taskboard.dto;

import java.time.LocalDateTime;
import java.util.Map;

public record ErrorResponse(
    LocalDateTime timestamp,
    int status,
    String message,
    Map<String, String> fieldErrors
) {
}
```

타임스탬프, 상태코드, 사람이 읽을 메시지, 그리고 필드별로 무엇이 잘못됐는지 알려주는 지도. 프런트는 이제 어떤 에러가 와도 이 네 가지를 기대하면 된다. 약속이 고정되면 클라이언트 쪽 에러 처리가 훨씬 단순해진다.

이제 이 모양으로 예외를 받아 빚어내는 핸들러를 만들자.

```java
package com.example.taskboard.exception;

import com.example.taskboard.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> fieldErrors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            fieldErrors.put(error.getField(), error.getDefaultMessage())
        );

        ErrorResponse body = new ErrorResponse(
            LocalDateTime.now(),
            HttpStatus.BAD_REQUEST.value(),
            "입력값 검증에 실패했습니다.",
            fieldErrors
        );
        return ResponseEntity.badRequest().body(body);
    }
}
```

코드가 조금 길어 보여도 하는 일은 단순하다. `@RestControllerAdvice`는 "이 클래스는 모든 컨트롤러를 지켜보다가 예외를 가로채는 곳이다"라는 표식이고, `@ExceptionHandler(MethodArgumentNotValidException.class)`는 "그중에서도 검증 실패 예외가 던져지면 이 메서드가 처리한다"는 뜻이다. 메서드 안에서는 깨진 규칙들을 모아 필드별 메시지로 정리하고, 400 상태코드와 함께 일관된 모양으로 돌려준다.

이제 다시 빈 제목으로 요청을 던지면, 클라이언트는 이런 깔끔한 응답을 받는다.

```json
{
  "timestamp": "2026-05-25T14:30:00",
  "status": 400,
  "message": "입력값 검증에 실패했습니다.",
  "fieldErrors": {
    "title": "제목은 비어 있을 수 없습니다."
  }
}
```

처음의 그 끔찍한 스택 트레이스와 비교하면 천지 차이다. 프런트는 `fieldErrors.title`을 그대로 입력 칸 아래 에러 메시지로 띄우면 된다. 검증 실패 말고도 404·409 같은 예외를 `@ExceptionHandler`로 하나씩 더 얹으면 된다. 핵심은 하나 — **에러의 모양을 한곳에서 다스리자.** 그래야 클라이언트가 신뢰할 수 있는 약속이 된다.

## 왜 브라우저만 막고 curl은 통과할까 — CORS는 서버의 책임

이제 1장에서 심어둔 씨앗을 거둘 차례다. 그때 우리는 프런트 개발자라면 누구나 한 번쯤 본 그 빨간 콘솔 에러 — `blocked by CORS policy` — 를 "증상"으로만 꺼내두고, "이걸 막는 것도 푸는 것도 결국 서버의 책임"이라는 말과 함께 5장으로 미뤄두었다. 약속한 자리에 도착했다.

상황을 그려보자. 당신의 React 개발 서버는 `localhost:3000`에서 돌고, 방금 만든 Spring 서버는 `localhost:8080`에서 돈다. React 앱에서 `fetch('http://localhost:8080/api/tasks')`를 부르면 콘솔에 그 익숙한 빨간 줄이 뜬다. 요청이 막힌 것이다. 그런데 묘한 일이 하나 있다. 똑같은 주소를 `curl`이나 Postman으로 때리면 멀쩡히 응답이 온다. 같은 서버, 같은 엔드포인트인데 브라우저에서만 막힌다. 왜 그럴까?

비밀은 **브라우저**에 있다. CORS를 막는 주체는 서버가 아니라 브라우저다. 브라우저에는 "동일 출처 정책(Same-Origin Policy)"이라는 보안 규칙이 있어서, 자바스크립트가 자기가 떠 있는 출처(`localhost:3000`)와 다른 출처(`localhost:8080`)로 요청을 보내면, 응답을 받아도 그 결과를 읽지 못하게 막아버린다. 악의적인 교차 출처 요청으로부터 사용자를 보호하기 위한 장치다. 반면 `curl`이나 Postman은 브라우저가 아니라서 이 정책의 적용을 받지 않는다. 그래서 멀쩡히 통과한다.

그렇다면 이 빗장을 어떻게 풀까? 빗장을 거는 건 브라우저지만, **"이 출처는 믿어도 된다"고 허락해주는 건 서버**다. 서버가 응답에 "나는 `localhost:3000`에서 오는 요청을 허용한다"는 헤더를 실어 보내면, 브라우저는 그제야 빗장을 풀고 자바스크립트가 응답을 읽도록 허락한다. 1장에서 심은 씨앗 — "막는 것도 푸는 것도 서버의 책임" — 이 바로 이 뜻이었다.

Spring에서 이 허락을 선언하는 방법은 둘이다. 특정 컨트롤러나 메서드 위에 `@CrossOrigin`을 붙이거나, `CorsConfigurationSource`라는 빈을 하나 두어 **전역으로** 한 번에 정하는 것이다. 좁은 범위만 잠깐 열 때는 `@CrossOrigin`이 편하지만, 우리는 전역 설정을 권하는 편이 낫다. CORS 정책은 한곳에서 일관되게 다스려야 빠뜨리거나 어긋나는 일이 없기 때문이다.

```java
package com.example.taskboard.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
public class CorsConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("http://localhost:3000"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
```

`setAllowedOrigins`로 "이 출처에서 오는 요청은 허용한다"고 못 박는다. 여기선 React 개발 서버인 `localhost:3000`을 적었다. `setAllowedMethods`로는 허용할 HTTP 메서드를 정하는데, 여기 **`OPTIONS`**가 끼어 있는 걸 눈여겨보자. 브라우저는 본 요청(예: `DELETE`)을 보내기 전에 "이런 요청을 보내도 되겠니?" 하고 슬쩍 물어보는 **예비 요청(preflight)**을 `OPTIONS`로 던지고, 서버가 "괜찮아"라고 답해야 진짜 요청을 보낸다. 그래서 허용 메서드에 `OPTIONS`를 빠뜨리면 이 예비 단계에서 막혀버린다. "분명 CORS 설정을 했는데 왜 또 막히지?" 싶으면 십중팔구 이 preflight 언저리를 의심해볼 만하다.

지금 일부러 비워둔 설정이 하나 있다. 쿠키 같은 인증 정보를 실어도 되는지 정하는 **`allowCredentials`**다. 아직 인증이 없으니 건드리지 않았다. 다만 와일드카드(`"*"`)와 함께 켜면 브라우저가 거부하는 함정이 있는데, 이건 11장에서 세션·쿠키 인증과 함께 다시 만난다.

마지막으로 한 가지 주의. AI에게 CORS 설정을 부탁하면, 종종 `allowedOrigins("*")`에 인증까지 허용하는 식으로 모든 걸 활짝 열어버린 위험한 코드를 준다. 편하지만 보안 구멍이다. AI는 설정의 뼈대를 잡아주는 동반자이되, **무엇을 얼마나 열지는 끝까지 우리가 정한다.** 3장부터 이어온 그 원칙, 여기서도 그대로다.

## 첫 테스트 — MockMvc는 supertest다

여기까지 왔으면 우리 API는 제법 견고해졌다. 검증도 하고, 에러도 일관되게 돌려주고, CORS도 풀었다. 그런데 이걸 매번 어떻게 확인하고 있었나? 서버를 띄우고, 브라우저나 `curl`로 요청을 던져보고, 눈으로 응답을 확인했다. 손으로 말이다.

여기서 잠시 멈추고 생각해보자. 코드를 고칠 때마다 이 손 검사를 전부 다시 해야 한다면? 엔드포인트가 다섯, 열 개로 늘어나면? 검증 규칙이 제대로 도는지, 201이 잘 나오는지, 400 에러 모양이 맞는지를 매번 손으로 확인하는 건 금세 번거로워지고, 결국 "귀찮으니 대충 넘기자"가 된다. 그 순간 버그가 슬며시 끼어든다.

그래서 우리는 이 확인을 **코드로** 자동화한다. 바로 테스트다. "테스트"라는 말에 지레 겁먹을 필요 없다. 프런트에서 이미 해본 일이기 때문이다. Node 백엔드를 만져봤다면 **supertest**를 떠올려보자. 가짜로 서버를 띄워 요청을 던지고, 돌아온 상태코드와 바디를 단언(assert)하던 그 도구다.

```javascript
// supertest (Node) — 이미 익숙한 모양
await request(app)
  .post('/api/tasks')
  .send({ title: '' })
  .expect(400);
```

Spring에도 정확히 이 모양을 하는 도구가 있다. **MockMvc**다. 진짜 서버를 8080 포트에 띄우지 않고도, 컨트롤러에 가짜 요청을 던지고 응답을 단언할 수 있다. supertest와 판박이다.

```java
package com.example.taskboard.controller;

import com.example.taskboard.service.TaskService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TaskController.class)
class TaskControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void 제목이_비어있으면_400을_돌려준다() throws Exception {
        String body = """
            { "title": "", "description": "설명" }
            """;

        mockMvc.perform(post("/api/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(body))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.fieldErrors.title").exists());
    }
}
```

supertest 예제와 나란히 두고 보면 구조가 똑같다. `perform(post(...))`로 요청을 던지고(supertest의 `.post().send()`), `andExpect(status().isBadRequest())`로 상태코드를 단언하고(`.expect(400)`), `jsonPath`로 응답 바디 안을 들여다본다. 모양만 자바일 뿐, 우리가 하는 생각은 완전히 같다 — **"이런 요청을 던지면, 이런 응답이 와야 한다."**

클래스 위의 `@WebMvcTest(TaskController.class)`는 "이 테스트는 컨트롤러 한 겹(슬라이스)만 띄워서 검사한다"는 뜻이다. DB나 다른 무거운 부품은 부르지 않고 웹 계층만 가볍게 올리니, 테스트가 빠르고 가볍다. 성공 경로(정상 요청에 201)도 같은 방식으로 단언할 수 있는데, 이 경우엔 컨트롤러가 부르는 `TaskService`를 가짜(mock)로 채워줘야 한다(`@WebMvcTest`는 웹 계층만 띄우므로). 그 구체적인 방법은 손이 조금 더 가니 여기서는 "같은 방식으로 단언할 수 있다"는 것만 확인하고 넘어가자.

지금 테스트 하나가 별것 아닌 것처럼 보일 수 있다. 하지만 이 작은 습관이 13장에서 큰 무기가 된다. 그때 우리는 AI와 함께 기능 하나를 스펙부터 구현까지 완주하는데, 마지막 단계가 바로 "테스트로 검증하기"다. **기억해두자. 견고함은 두 눈이 아니라 코드로 증명할 때 비로소 무너지지 않는다.**

## 마무리

이번 장에서 우리는 "동작은 하지만 엉성한" API를 "험한 요청에도 품위를 잃지 않는" API로 키웠다. 엔티티를 그대로 노출하지 않도록 DTO라는 칸막이를 세웠고, `@Valid`로 검증을 프레임워크에 위임했고, `ResponseEntity`로 상태코드를 의도적으로 골랐고, `@RestControllerAdvice`로 에러의 모양을 한곳에서 다스렸고, 1장에서 심어둔 CORS의 씨앗을 거뒀고, MockMvc로 첫 테스트를 작성했다.

이 모든 걸 관통하는 감각은 하나다 — **API의 모든 출력(상태코드·에러·허용 출처)은 내가 의도적으로 설계하는 것이지, 우연히 그렇게 되는 것이 아니다.** 1장에서 "내가 결정하는 책임"이라 불렀던 말이, 이번 장에서 비로소 코드로 실현된 셈이다.

다만 한 가지, 우리의 할 일들은 **아직 메모리에 산다**. 서버를 끄면 깨끗이 사라진다. 다음 장에서는 그 마지막 찜찜함을 끝낸다. JPA를 붙여 메모리에 살던 TaskBoard를 데이터베이스로 옮겨 심되, 흥미롭게도 **API 계약은 단 한 줄도 바꾸지 않은 채** 그 아래 저장소만 갈아 끼운다. 오늘 우리가 DTO로 안과 밖을 갈라둔 덕분에 가능한 일이다. 오늘의 칸막이가 내일의 갈아 끼우기를 떠받친다. 그럼, 메모리에서 데이터베이스로 건너가 보자.
