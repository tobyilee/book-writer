# 6장. 디버깅 — JVM 도구 체인을 Node 도구 체인으로 옮기기

> 부제: jstack·jmap·VisualVM 대신 `--inspect`·clinic.js·heap snapshot

한 회고를 들여다보자. Netflix 엔지니어가 production node.js 인스턴스 앞에 앉아 있다. 응답 시간이 들쭉날쭉하고, 어떤 시간대에는 CPU가 까닭 없이 80%까지 치솟는다. 코드를 아무리 들여다봐도 의심 가는 구간이 안 잡힌다. 로그도 멀쩡하다. APM 그래프도 큰 그림은 보여주지만 "어느 함수가 핫스팟인가"를 정확히 짚어주진 않는다. 답답한 일이다. JVM이었다면 jstack 한 번, jmap 한 번, 그래도 모자라면 VisualVM이나 JFR을 붙여 메소드 단위까지 파고들어갔을 텐데, Node 앞에서는 그 손이 갈 곳을 찾지 못한다.

엔지니어는 결국 V8의 내부 프로파일러를 깎아 flame graph를 만들었다. 그래프를 그려보니 한 줄짜리 정규식이 그래프 전체를 짙은 색으로 칠하고 있었다. 정규식 한 줄이 production 트래픽 절반의 CPU를 먹어 치우고 있던 것이다. 코드 리뷰로는 영영 못 잡았을 종류의 버그였다. Netflix 팀은 이 일을 회고하면서 이렇게 적었다. "도구가 없으면 이런 버그는 영영 못 찾는다." Netflix가 직접 이 도구를 키워서 OSS로 풀어낸 글이 그 유명한 "Node.js in Flames"다.

이 일화를 처음 읽었을 때의 느낌을 솔직히 적어두자. 자바 개발자라면 jstack과 jmap이 손에 박혀 있다. JVM 위에서 production을 운영해본 사람이라면, "이런 버그를 도구 없이 잡는다"는 말 자체가 비현실적으로 들린다. 도구는 늘 있었다. 그래서 Netflix의 "도구를 만들어서 풀었다"는 한 줄이 묘하게 낯설다. 우리가 당연히 갖고 있다고 생각했던 도구의 자리에, Node 진영은 한동안 그 도구가 없었다는 뜻이기도 하다. 그 자리를 채워온 게 지난 10년의 clinic.js와 0x와 Chrome DevTools다.

이 일화에서 우리가 가져갈 교훈은 두 개다. 첫째, Node.js에도 JVM의 도구들에 대응하는 도구들이 있다. 도구 이름이 다 바뀌었을 뿐, 사고 방식은 같다. 둘째, 어떤 종류의 버그는 도구로만 잡힌다. 코드 리뷰로 안 잡히고, 단위 테스트로 안 잡히고, 모니터링 그래프의 큰 그림으로도 안 잡힌다. 이벤트 루프를 막는 정규식 한 줄, 끊어지지 않은 클로저, 무한히 자라는 캐시 — 이런 것들은 production이 무릎을 꿇기 전까지 모습을 드러내지 않는다.

그래서 6장에서 우리가 던질 질문은 두 가지다. 운영 중인 Spring Boot 앱에서 jstack과 jmap을 떴던 그 손이, Node.js 앞에서는 어떤 명령을 치게 되는가? 그리고 어디서 두 런타임 도구의 사상이 갈라지는가? 답을 미리 한 줄로 압축해두자. **사고 방식은 그대로다. 명령어와 도구의 모양만 바뀐다.** 우리는 여전히 백엔드 개발자다. 도구가 바뀌었다고 해서 production을 디버깅하는 본능까지 새로 익혀야 하는 건 아니다.

## JVM ↔ Node 도구 매핑 — 한 장의 표로 잡는 좌표

자바 개발자가 production에서 흔히 쓰던 도구를 떠올려보자. CPU가 튀면 jstack을 떠 스레드 덤프를 본다. 메모리가 부풀면 jmap으로 heap dump를 받아 MAT(Eclipse Memory Analyzer)에 던진다. 더 정밀한 프로파일이 필요하면 VisualVM이나 JFR(Java Flight Recorder)을 붙인다. flame graph를 그릴 일이 있으면 async-profiler를 동원한다. 이 도구들이 머리에 박혀 있는 손은, Node 앞에 앉아도 같은 작업을 하고 싶어 한다. 메모리가 부풀면 heap dump를 받고 싶고, CPU가 튀면 어느 함수가 hot한지 보고 싶다. 이벤트 루프가 막히면 어디서 막혔는지 추적하고 싶다.

다행히 이 작업들에는 모두 Node 쪽 대응 도구가 있다. 한 장으로 정리해보자.

| JVM 도구 | Node.js 대응 | 하는 일 |
|---|---|---|
| jstack | `process.on('SIGUSR2', ...)` + V8 inspector report (`process.report.writeReport()`) | 스택 덤프 |
| jmap / heap dump | `--heapsnapshot-signal=SIGUSR2`, `v8.writeHeapSnapshot()` | heap snapshot |
| VisualVM | Chrome DevTools (`--inspect`), VS Code 디버거 | GUI 프로파일러 |
| JFR(Java Flight Recorder) | clinic.js (doctor / flame / bubbleprof) | CPU·이벤트 루프 분석 |
| async-profiler flame graph | 0x, clinic flame, Linux perf + `--perf-basic-prof` | flame graph |
| MAT(Eclipse Memory Analyzer) | Chrome DevTools Memory 탭 + heapdump | retainer chain 분석 |
| Spring Boot Actuator 메트릭 | `perf_hooks`, Terminus, Prometheus 클라이언트 | 운영 메트릭 |

표를 한참 보면 한 가지가 눈에 들어온다. JVM 쪽은 도구가 일을 분담한다. 스택 덤프는 jstack이, heap dump는 jmap이, GUI 프로파일러는 VisualVM이, flame graph는 async-profiler가 따로따로 한다. 반면 Node 쪽은 한 도구가 여러 일을 한다. Chrome DevTools 하나가 VisualVM과 MAT의 자리를 같이 차지하고, V8의 inspector 프로토콜이 jstack과 heap dump의 발판을 동시에 깔아준다. 도구 수는 적은데 한 도구가 무는 영역이 넓다.

이 차이가 우연은 아니다. JVM은 운영 도구의 표준화가 자바 1.5 시절부터 누적되어 있다. JMX, JVMTI, JDI 같은 표준 인터페이스 위에 도구들이 따로따로 자라났다. Node는 그 자리에 V8의 inspector 프로토콜 하나를 두고, Chrome 브라우저의 디버깅 UI를 그대로 가져다 붙였다. 즉 우리가 평소에 프론트엔드 개발자가 쓰는 그 Chrome DevTools를, 서버사이드 디버깅에도 똑같이 쓴다. 처음엔 어색하다. "프로파일러가 브라우저 개발자 도구라고?" 싶은 생각이 든다. 하지만 한 번 손에 익으면, 그 통합감이 묘하게 편하다.

표 안에 든 도구 하나하나를 본문에서 풀어가자. 사고 방식은 같으니, 그 매핑을 손에 익히는 게 이번 챕터의 목표다.

## `--inspect`와 Chrome DevTools — VisualVM의 자리

VisualVM은 자바 개발자라면 누구나 한 번쯤 띄워봤을 도구다. 로컬 JVM 프로세스를 자동으로 잡아서 GUI에 띄우고, CPU 샘플링, heap 분석, 스레드 덤프, JMX 모니터링까지 한자리에서 다 한다. Node에서 그 자리를 차지하는 게 Chrome DevTools다. 도구의 모양은 다르지만, 손에 잡히는 무게감은 닮아 있다.

쓰는 방식은 단순하다. Node 프로세스를 띄울 때 `--inspect` 플래그를 붙이면, V8이 9229 포트에 inspector 프로토콜 서버를 연다.

```bash
node --inspect app.js
# 출력 예:
# Debugger listening on ws://127.0.0.1:9229/abc-uuid
# For help, see: https://nodejs.org/en/docs/inspector
```

이 상태에서 Chrome 브라우저를 열고 주소창에 `chrome://inspect`를 친다. "Remote Target" 목록에 방금 띄운 Node 프로세스가 잡힌다. 옆의 "inspect" 링크를 누르면 익숙한 DevTools 창이 뜨는데, 거기서 우리가 평소에 프론트엔드 코드를 디버깅하던 그 인터페이스로 서버사이드 코드를 디버깅한다. 브레이크포인트, 변수 watch, 콜 스택, CPU 프로파일, heap snapshot — 모두 메뉴 한두 번 클릭이면 된다.

처음 Spring Boot 개발자가 이걸 보면 기분이 묘하다. IntelliJ의 디버거에 익숙한 손이, 갑자기 브라우저에서 서버 코드를 디버깅하고 있다. 어색할 수 있다. 그런데 며칠 쓰다 보면 이 통합감이 의외로 편하다는 걸 알게 된다. 프론트엔드 디버깅과 백엔드 디버깅의 도구 사용법이 같으니까, 풀스택을 오갈 때 머리를 다시 세팅할 필요가 없다.

VS Code도 같은 inspector 프로토콜에 붙는다. `.vscode/launch.json`에 다음과 같이 적어두면 IDE 안에서 바로 디버깅이 된다.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug NestJS",
      "runtimeArgs": ["--nolazy", "-r", "ts-node/register"],
      "args": ["${workspaceFolder}/src/main.ts"],
      "cwd": "${workspaceFolder}",
      "env": { "NODE_ENV": "development" },
      "console": "integratedTerminal"
    }
  ]
}
```

IntelliJ에서 Spring Boot main 클래스를 우클릭해 "Debug"를 누르던 그 손동작이, VS Code에서 이 launch.json을 만들고 F5를 누르는 손동작으로 바뀐 것뿐이다. 도구 이름이 다 바뀌지만 사고 방식은 같다 — 이번 장의 통주제를 처음으로 손으로 확인하는 순간이다.

### 원격 컨테이너의 Node를 디버깅하기

로컬은 쉬운데 원격 컨테이너의 Node를 들여다보는 일은 어떨까? Spring Boot에서는 `-agentlib:jdwp=...`로 JVM에 디버깅 포트를 열고, IntelliJ에서 Remote JVM Debug 컨피그를 만들어 붙였다. Node에서도 본질은 같다. inspector 포트를 열고, 그걸 로컬로 끌어와 DevTools에 붙인다.

먼저 Node 프로세스를 컨테이너 안에서 띄울 때 인터페이스를 명시해야 한다. `--inspect`는 기본이 127.0.0.1이라 컨테이너 외부에서 접근이 안 된다. `0.0.0.0:9229`로 풀어줘야 한다.

```bash
# 컨테이너 안에서:
node --inspect=0.0.0.0:9229 dist/main.js
```

물론 production 컨테이너의 9229 포트를 인터넷에 그대로 공개하는 건 끔찍한 일이다. inspector 프로토콜에는 인증이 없다. 포트만 알면 누구나 임의 코드 실행이 가능하다. 그러니 인터넷으로 직접 노출하면 안 된다. 이때 우리가 늘 쓰던 SSH 포트포워딩이 그대로 답이다.

```bash
# 로컬에서:
ssh -L 9229:localhost:9229 user@bastion-host \
  kubectl port-forward -n production pod/api-7f8b9 9229:9229
```

이 한 줄이 하는 일을 풀어보자. SSH로 bastion에 붙고, 거기서 `kubectl port-forward`를 실행해 K8s 파드의 9229를 bastion의 9229로 가져온다. 그 9229를 다시 로컬 9229로 SSH 터널링한다. 그러고 나서 로컬 Chrome에서 `chrome://inspect`를 열고 "Configure" 버튼으로 `localhost:9229`를 등록하면, 마치 로컬 프로세스인 것처럼 production 컨테이너의 Node가 잡힌다. 브레이크포인트도 걸리고, heap snapshot도 받힌다. 신기하지만, 위험하기도 하다.

production에서 inspector를 붙일 때는 반드시 트래픽이 빠진 인스턴스에서만 한다. 이유는 둘이다. 첫째, 브레이크포인트가 걸리면 그 worker는 멈춘다. 진행 중이던 요청도 같이 멈춘다. 둘째, 프로파일링도 GC도 모두 비용이다. 살아 있는 트래픽 위에 도구를 붙이는 건 환자에게 마취 없이 수술을 하는 것과 비슷하다. K8s를 쓰는 환경이라면 라벨로 트래픽을 끊을 수 있다 — 서비스의 selector에서 그 파드만 빼고, drain 시간을 조금 두고, 그 다음에 inspect를 붙인다. 끝나면 다시 라벨을 붙여서 트래픽을 받는다. 이 흐름을 운영 SOP로 정리해두는 편이 낫다. 왜 그런 SOP가 필요한지는 7장에서 다시 만난다.

## heap snapshot — jmap의 자리

자바에서 OOM이 나면 손이 가장 먼저 가는 곳은 jmap이다. `jmap -dump:format=b,file=heap.hprof <pid>`로 hprof를 떠서 MAT에 던지고, dominator tree를 펼쳐 누가 메모리를 잡고 있는지 본다. 이 흐름이 손에 박혀 있다면, Node에서도 그 흐름을 거의 그대로 옮길 수 있다. 도구 이름만 바뀐다.

Node에서 heap snapshot을 받는 길은 세 가지가 있다. 첫째는 코드 안에서 명시적으로 호출하는 길이다.

```ts
import * as v8 from 'node:v8';
import * as path from 'node:path';

function dumpHeap(): string {
  const filename = path.join('/tmp', `heap-${Date.now()}.heapsnapshot`);
  v8.writeHeapSnapshot(filename);
  return filename;
}
```

이 코드는 동기다. 이 함수가 도는 동안 이벤트 루프는 멈춘다. heap이 1GB라면 약 1~3초는 멈춘다고 봐야 한다. 그 사이에 들어오는 요청은 줄 서서 기다린다. 위험하다. 그래서 운영에서 호출하려면 관리자 전용 엔드포인트로 분리하고, 호출 전에 트래픽을 끊는 게 안전하다.

둘째는 시그널이다. `--heapsnapshot-signal=SIGUSR2`를 붙여 프로세스를 띄우면, 외부에서 시그널을 보낼 때마다 자동으로 스냅샷이 저장된다.

```bash
# 띄울 때:
node --heapsnapshot-signal=SIGUSR2 dist/main.js

# 받을 때:
kill -USR2 <pid>
# 작업 디렉터리에 Heap.<timestamp>.<pid>.<seq>.heapsnapshot 파일이 떨어진다
```

`SIGUSR1`은 V8이 inspector를 붙이는 데 이미 쓰고 있으므로 `SIGUSR2`를 쓴다. Spring Boot에서 `kill -3 <pid>`로 thread dump를 stderr에 받던 그 손동작에 가장 가까운 방식이다.

셋째는 Chrome DevTools에서 직접 받는 길이다. inspector를 붙인 상태에서 "Memory" 탭으로 가서 "Take heap snapshot"을 누른다. 1~3초 기다리면 GUI에 분석 가능한 상태로 뜬다. 이 방식이 가장 편한데, 이유는 다음 단락에서 풀자.

### 운영 주의사항 — 힙의 2배 메모리, 그리고 멈추는 이벤트 루프

heap snapshot에는 가벼운 작업이라는 인상이 없다. 사실 꽤 무거운 작업이다. Node 공식 문서가 명시하는 두 가지 비용을 잊지 말자.

첫째, 메모리 비용이다. 스냅샷을 만드는 동안 V8은 힙의 약 2배에 해당하는 메모리를 잠시 더 쓴다. 1.5GB 힙이라면 그 순간 약 3GB가 필요하다. 컨테이너의 메모리 limit가 빡빡하면 OOM-Kill이 날 수 있다. 안 그래도 메모리가 의심스러워서 스냅샷을 받는 건데, 그 행위 자체로 OOM을 내고 컨테이너가 재시작되면 아무것도 못 건진다. 끔찍한 일이다. 그러니 컨테이너 limit에 1.5~2배 헤드룸이 없다면, 임시로 limit를 올려두고 받거나 별도 인스턴스에서 받자.

둘째, 시간 비용이다. 스냅샷을 만드는 동안 이벤트 루프는 멈춘다. 1GB 힙이면 1~3초 정도, 5GB 힙이면 5~15초 정도다. 라이브 트래픽이 흐르는 인스턴스에서 이걸 하면, 그 시간 동안 들어온 요청 전부가 timeout이 나거나 줄 서서 기다리게 된다. 운영 그래프에 갑자기 5초 응답 시간 spike가 찍힌다. 위험하다.

답은 단순하다. 트래픽이 빠진 인스턴스에서만 받자. K8s라면 그 파드만 service selector에서 빼고, drain 시간을 두고, 그 후에 스냅샷을 받는다. 받기가 끝나면 다시 트래픽을 받게 한다. 이 흐름은 7장에서 다룰 graceful shutdown SOP와 자연스럽게 만난다. 잊지 말자 — production heap snapshot은 가볍게 누를 버튼이 아니다.

### Chrome DevTools에서 retainer chain 읽기

스냅샷 파일이 손에 들어왔으면 이제 분석이다. Chrome 브라우저를 열고, DevTools를 띄우고, "Memory" 탭에서 우측 상단의 "Load profile..."을 누르면 스냅샷을 끌어다 놓을 수 있다. 한 번 로드되면 객체 카테고리별 사이즈, retainer chain, comparison view를 볼 수 있다.

자바의 MAT를 써본 손이라면 첫 화면이 익숙할 것이다. 객체 종류별로 누적 사이즈가 정렬되어 나오고, 객체 하나를 클릭하면 retainer가 나무처럼 펼쳐진다. retainer는 그 객체를 잡고 있어서 GC가 못 가져가게 만드는 존재다. 누수의 범인을 찾는 길은 retainer chain을 거슬러 올라가는 것 — MAT의 dominator tree를 읽던 그 본능이 그대로 통한다.

Node 쪽에서 가장 흔한 retainer 패턴은 다음 셋이다.

1. **모듈-레벨 캐시.** 리퀘스트마다 키를 추가만 하고 비우지 않는 `Map` 또는 `Object`. 시간이 갈수록 무한히 자란다. Spring 빈에서 `static Map`을 캐시로 쓰는 패턴과 동일한 함정이다.
2. **클로저로 잡힌 큰 객체.** Promise 체인 안에서 큰 buffer를 캡처해두고 그 Promise가 어딘가의 배열에 매달려 있는 경우. 자바스크립트의 클로저는 묘하게 길게 살 때가 있다.
3. **이벤트 리스너.** `EventEmitter.on()`만 부르고 `off`를 안 부르는 경우. 자바의 이벤트 리스너 누수와 같은 형태다.

이 셋을 머리에 심어두자. 누수가 의심스러우면 가장 먼저 의심할 후보다.

## clinic.js — JFR과 async-profiler의 자리

자바 진영에서 JFR이 자리잡은 다음, 운영 프로파일링은 한결 매끄러워졌다. JFR을 켜두면 적은 오버헤드로 CPU 샘플, 락, GC 이벤트, 메모리 할당이 한꺼번에 기록된다. JMC(Java Mission Control)에 던져보면 시간축으로 다 펼쳐진다. Node에 그 자리를 차지하는 도구가 clinic.js다. NearForm이 만들어 OSS로 풀었다.

clinic.js는 세 명령으로 갈라진다. 셋을 한 번씩 머리에 새겨두자.

- **`clinic doctor`**: 이벤트 루프 lag, GC, CPU, active handle 수를 한 그래프에 그려주고 "당신의 병이 무엇인지" 진단해준다.
- **`clinic flame`**: flame graph를 그린다. async-profiler와 같은 자리다.
- **`clinic bubbleprof`**: async 작업의 병목을 시각화한다. Promise 체인이 어디서 줄 서고 있는지를 풍선 그림으로 보여준다.

대표적인 시작점은 `clinic doctor`다. 한 줄이면 된다.

```bash
# 부하 생성기와 함께 돌린다 (autocannon이 흔하다):
clinic doctor --on-port 'autocannon -d 30 http://localhost:3000/' \
  -- node dist/main.js

# 끝나면 자동으로 브라우저에 보고서가 열린다:
# http://localhost:.../doctor.html
```

이 도구가 사랑받는 이유는 진단 결과가 친절하다는 점에 있다. 그래프 위에 빨간 박스로 "이건 I/O 병목 같다", "이건 이벤트 루프 블로킹이다", "GC pressure가 있다" 같은 말이 떠 있다. 마치 의사가 진료 차트를 펼쳐 손가락으로 짚어주는 느낌이다. 자바에서 JFR 분석이 처음에는 어디서부터 봐야 할지 막막했던 기억을 떠올려보자. clinic은 그 막막함을 한 단계 앞에서 줄여준다.

flame graph가 필요한 상황이면 `clinic flame` 또는 0x를 쓴다. async-profiler가 hot한 자바 메소드를 색깔로 보여주듯, clinic flame은 hot한 자바스크립트 함수를 색깔로 보여준다.

```bash
clinic flame --on-port 'autocannon -d 30 http://localhost:3000/api/users' \
  -- node dist/main.js
```

flame graph의 너비는 누적 시간이고, 위로 갈수록 콜 스택의 안쪽이다. 큰 평면이 길게 깔려 있는 함수가 핫스팟이다. Netflix가 정규식 한 줄을 잡은 그 그림이 이 모양이었다. 도입 일화의 그림을 머리에 심어두면 flame graph 읽기가 쉬워진다.

`bubbleprof`는 약간 다른 결의 도구다. async 작업의 병목을 보여주는데, 풍선이 클수록 거기 매달린 작업이 길었다는 뜻이다. Promise 체인이 깊거나 await가 줄을 서 있는 코드의 병목을 시각으로 보여준다. NestJS 같은 서버에서 파이프라인 어디가 엉기는지 찾을 때 도움이 된다.

clinic 시리즈의 대안 도구도 알아두자. 0x는 flame graph만 깎아주는 단일 목적 도구로, clinic flame보다 빠르고 가볍다. Linux perf를 직접 쓰는 길도 있는데, `node --perf-basic-prof` 플래그로 V8이 perf-map을 쏟게 하고, perf로 stack trace를 뜨고, FlameGraph.pl로 그림을 그리는 흐름이다. 자바의 async-profiler가 이 길과 가깝다. clinic이 먼저 익숙해지고 그 다음에 0x나 perf로 내려가도 늦지 않다.

## 이벤트 루프 블로킹 탐지 — Node에만 있는 항목

여기서 잠깐, 자바와 Node의 사고 방식이 갈라지는 지점을 짚자. 자바에는 "이벤트 루프 lag"라는 개념이 없다. 요청 하나당 스레드 하나가 붙기 때문에, 한 요청이 길게 끌어도 다른 요청이 막히지 않는다. 막히면 풀이 마르거나 큐가 길어질 뿐이다. Node는 다르다. 단일 스레드의 이벤트 루프가 모든 요청을 돌리니까, 한 콜백이 100ms를 먹으면 그 100ms 동안 모든 요청이 줄을 선다. 1장에서 본 Walmart의 convoy effect — 앞 작업이 뒷 작업을 줄세운다는 그 효과 — 가 바로 이 자리다.

그래서 Node에는 자바에 없는 모니터링 항목이 하나 더 있다. **이벤트 루프 lag.** 이걸 측정하지 않으면 그 어떤 도구도 "지금 이벤트 루프가 막혔다"를 못 잡는다.

Node 11.10 이후로는 표준 라이브러리 안에 `perf_hooks.monitorEventLoopDelay()`가 들어왔다. 한 번 셋업하면 백그라운드에서 lag 분포를 누적해 준다.

```ts
import { monitorEventLoopDelay } from 'node:perf_hooks';

const histogram = monitorEventLoopDelay({ resolution: 20 });
histogram.enable();

setInterval(() => {
  const stats = {
    p50: histogram.percentile(50) / 1e6, // ms
    p99: histogram.percentile(99) / 1e6,
    max: histogram.max / 1e6,
  };

  if (stats.p99 > 50) {
    console.warn('event loop lag p99 > 50ms', stats);
  }

  // Prometheus 등 메트릭 시스템에 푸시
  histogram.reset();
}, 10_000);
```

이 코드가 하는 일을 풀어보자. `monitorEventLoopDelay`는 V8 내부에서 일정 간격으로 self-check 타이머를 거는데, 그 타이머가 예상보다 늦게 호출된 만큼이 lag다. resolution 20ms로 잡으면 20ms 간격으로 측정한다. 실 운영에서 보는 임계는 보통 p99 lag 50ms 정도다. 그 이상이 5분 이상 지속되면 경보를 보내는 편이 낫다. p99가 200ms를 넘는다면 사용자가 체감할 만큼 느리다는 뜻이다.

표준 라이브러리 외에 가벼운 패키지도 있다. `loopbench`, `event-loop-lag` 같은 이름이다. 코드 한 줄 차이일 뿐 본질은 같다. 어떤 걸 쓰든, **운영 메트릭에 이벤트 루프 lag를 한 줄 더 넣는 일**은 Node로 운영하는 첫날에 끝내두자. Spring Boot Actuator에서 `/actuator/metrics`로 GC 시간을 보던 그 자리에, Node에서는 이벤트 루프 lag가 들어가야 한다.

이 메트릭이 있으면 트래블슈팅의 출발점이 달라진다. "응답 시간이 느려졌다"는 신고가 들어왔을 때, lag 그래프를 먼저 본다. lag가 정상이면 다운스트림(DB, 외부 API)의 문제일 확률이 높다. lag가 튀고 있으면 우리 코드 안에서 누가 이벤트 루프를 막고 있다는 신호다. 이때 `clinic doctor`나 `clinic flame`을 띄울 때다. 도구의 사상이 갈라지는 자리에는 새 메트릭이 자란다는 사실 — 이것을 잊지 말자.

## 메모리 누수 사냥 — Anvil과 dev.to의 회고

heap snapshot 도구를 손에 쥐었다고 해서 누수를 잡는 본능까지 따라오는 건 아니다. 두 개의 회고를 들여다보자. 둘 다 운영 환경에서 메모리 누수를 손으로 잡아낸 이야기다. 두 회고를 한 번씩 읽어보면, retainer chain을 어떻게 거슬러 올라가는지에 대한 직관이 생긴다.

첫 번째는 Anvil 엔지니어링 팀의 회고다. 그들의 production Node 서비스가 시간이 지나면서 메모리를 천천히 갉아먹었다. 처음엔 1GB, 며칠 후엔 1.5GB, 결국 OOM. Kubernetes가 친절하게 재시작해주니 사용자에겐 안 보였지만, 재시작 빈도가 점점 잦아지면서 알람이 울렸다. 팀은 트래픽 빠진 인스턴스에 inspector를 붙이고 한 시간 간격으로 heap snapshot 두 장을 받았다. DevTools의 "Comparison" 뷰로 두 장을 비교했더니, `Object` 카테고리에 정확히 N개의 새 객체가 보였다. retainer를 거슬러 올라가니 한 모듈-레벨 변수에 매달린 `Map`이 나왔다. 키는 요청 ID였고 값은 응답 객체였다. 누군가가 디버깅용 캐시를 만들어 두고 정리 코드를 까먹은 것이었다. 한 줄을 지웠더니 메모리 곡선이 평평해졌다.

두 번째는 dev.to의 어느 엔지니어가 적은 "2GB 누수 사냥" 회고다. 하루에 2GB씩 메모리가 부풀어 OOM이 나는 서비스가 있었다. heap snapshot을 까보니 `Buffer` 객체가 어마어마하게 잡혀 있었다. retainer chain을 따라가니 한 EventEmitter에 매달린 리스너 배열이 끝없이 자라고 있었다. 코드를 보니 매 요청마다 `socket.on('data', ...)`을 등록만 하고 `off`를 안 부르고 있었다. 고친 후 메모리는 평평해졌다.

두 회고에서 공통으로 도드라지는 손동작이 있다. **두 시점의 heap snapshot을 받아 비교한다**는 점이다. 한 장만 봐선 모른다. 사이즈가 큰 객체가 진짜 누수인지, 그냥 정상 크기인지 구별이 안 된다. 두 장을 비교해야 "시간이 지나도 안 줄어드는 객체"가 눈에 들어온다. DevTools의 "Comparison" 뷰 또는 "All objects between snapshots"가 그 일을 한다. MAT의 leak suspect 분석과 같은 사상이다.

손에 익히기 위해 작은 누수 시나리오를 일부러 만들고 잡아보자. 다음 코드는 의도적으로 메모리를 새는 Express 서버다.

```ts
import express from 'express';

const app = express();
const cache = new Map<string, Buffer>();

app.get('/leak', (req, res) => {
  // 의도된 누수: 키만 추가, 정리 없음
  const key = `req-${Date.now()}-${Math.random()}`;
  cache.set(key, Buffer.alloc(1024 * 100)); // 100KB
  res.json({ size: cache.size });
});

app.get('/heap', (_req, res) => {
  const v8 = require('node:v8');
  const file = `/tmp/heap-${Date.now()}.heapsnapshot`;
  v8.writeHeapSnapshot(file);
  res.json({ file });
});

app.listen(3000);
```

이 서버를 띄우고 `autocannon -d 30 http://localhost:3000/leak`로 30초 부하를 준 다음, `curl http://localhost:3000/heap`을 두 번 — 한 번은 부하 시작 직전, 한 번은 부하 끝난 직후 — 호출한다. 두 스냅샷 파일을 Chrome DevTools에 차례로 로드해서 두 번째 스냅샷에서 "Comparison" 뷰로 첫 번째와 비교한다. `Buffer`, `Map entry` 카테고리가 폭발적으로 늘어 있는 게 보인다. 객체 하나를 클릭해 retainer를 펼치면 `cache` 변수가 보인다. 한 번 손으로 해두면 진짜 누수가 났을 때 손이 빨라진다. 운영에서 처음 누수를 만나기 전에, 평화로운 시간에 한 번 연습해두는 편이 낫다.

## Netflix flame graph — 회수

도입에서 "정규식 한 줄이 production CPU의 절반을 먹었다"는 일화로 시작했다. 이제 우리에게 도구가 있으니 그 일이 어떻게 잡혔는지를 자세히 풀자.

상황은 이랬다. Netflix UI 서버는 BFF 레이어 — Java 모놀리스 위에 얇게 얹은 Node.js 게이트웨이 — 였다. 응답 시간 측정값이 어떤 시간대엔 평소의 두세 배로 튀어 올랐다. CPU 그래프도 같이 튀었다. 평소 30%를 쓰던 인스턴스가 80%를 친다. 그런데 코드를 봐도 의심 갈 곳이 안 보이고, 들어오는 트래픽 패턴도 평소와 같다. 답답한 일이다.

Netflix 팀은 production 인스턴스 한 대에 V8 프로파일러를 붙이기로 한다. 트래픽을 빼고, `--prof` 플래그로 V8 내부의 sampling profiler를 켜고, perf 출력과 V8 출력을 합쳐 flame graph를 그렸다. 그 시절엔 0x도 clinic도 없어서 도구를 직접 깎아야 했다. 그림을 처음 봤을 때 그들은 한 줄짜리 정규식이 그래프의 짙은 부분을 차지하고 있는 걸 발견했다. 그 정규식은 어떤 작은 헤더 검증에 쓰이고 있었는데, 입력 패턴 일부에서 catastrophic backtracking이 일어나고 있었다. 한 번 호출에 ms 단위로 끝나야 할 정규식이, 어떤 입력에서는 100ms 이상 걸렸다. 이벤트 루프가 그 100ms 동안 막혔고, 그 동안 들어온 모든 요청이 줄을 섰다. 정확히 Walmart의 convoy effect다.

수정은 한 줄이었다. backtracking이 안 일어나도록 정규식을 바꿨다. 응답 시간 곡선이 평평해졌고 CPU도 정상으로 돌아왔다. Netflix 팀은 이 경험을 "Node.js in Flames"라는 글로 풀었고, 거기서 깎은 도구는 OSS로 풀려 후일 0x와 clinic flame의 토양이 됐다.

이 일화에서 두 가지를 짚어두자. 첫째, **flame graph는 이런 종류의 버그를 거의 유일하게 잡는 도구다.** 정규식 한 줄, sync 압축 한 줄, 동기 crypto 한 줄 — 코드 라인 단위에서 보면 평범한데, 누적되면 production을 무릎 꿇리는 버그들이 있다. 코드 리뷰로는 안 잡힌다. APM 그래프로는 큰 그림은 보지만 어느 줄이 범인인지는 안 짚어준다. flame graph만이 라인 단위로 짚어준다. 그래서 Node 운영을 시작한 첫 분기에 flame graph 한 번은 그어보자. 정상 상태가 어떻게 생겼는지 알아두는 일이 의외로 중요하다.

둘째, **도구로 못 찾는 종류와 도구로만 찾는 종류가 따로 있다.** 비즈니스 로직의 버그는 도구로는 안 잡힌다. 통합 테스트가 잡는다. 반대로 catastrophic backtracking 같은 종류는 단위 테스트로는 안 잡힌다. flame graph가 잡는다. 두 종류를 머리에 함께 두고, 어떤 신호가 뜨면 어떤 도구를 든다는 작은 매핑을 익혀두자.

| 신호 | 첫 도구 |
|---|---|
| 응답 시간이 느려졌는데 다운스트림은 정상 | 이벤트 루프 lag 메트릭 |
| 이벤트 루프 lag p99이 50ms를 넘는다 | `clinic doctor` |
| CPU가 한 시점에 튄다, 평균이 아니라 spike | `clinic flame` 또는 0x |
| 메모리가 시간이 지날수록 자란다 | heap snapshot 비교 |
| async 작업이 줄 서서 늦어진다 | `clinic bubbleprof` |
| 운영 중에 스택 한 장이 필요하다 | `process.report.writeReport()` |

이 표가 머리에 박혀 있으면 production 알람이 울렸을 때 손이 멈칫하지 않는다. jstack 손이 inspector report 손으로, jmap 손이 `v8.writeHeapSnapshot()` 손으로 자연스럽게 옮겨간다.

## 운영 헬스 체크와 디버깅의 통합

여기까지 이야기한 도구들은 대부분 사후 분석 도구다. 문제가 일어난 다음에 들고 가서 들여다보는 도구다. 그런데 운영의 진짜 문제는 "그 도구를 들기 직전까지의 시간"에 있다. 알람이 울리고, 트래픽을 빼고, inspector를 붙이고, 데이터를 받는 — 이 일련의 흐름을 SOP로 미리 정리해두지 않으면, 정작 위기에 손이 빨리 안 움직인다. Netflix처럼 도구를 직접 깎아야 했던 시절은 지났지만, "언제 어떤 도구를 드는가"의 SOP는 각자 팀이 만들어야 한다.

Spring Boot 운영자라면 Actuator의 `/actuator/health`, `/actuator/metrics`, `/actuator/threaddump`, `/actuator/heapdump`가 손에 익었을 것이다. Node에는 이만큼 통합된 표준이 없다. 대신 작은 라이브러리들을 끼워 만든다. NestJS라면 `@nestjs/terminus`가 health 체크를 깎아주고, Prometheus 메트릭은 `prom-client`로 노출한다. heap snapshot은 위에서 본 것처럼 시그널 또는 관리자 엔드포인트로 받는다.

핵심은 다음 셋이다.

1. **`/health/live`와 `/health/ready` 둘로 나눈다.** liveness는 "프로세스가 살아 있는가", readiness는 "트래픽을 받을 준비가 되어 있는가"다. heap snapshot을 받기 전 트래픽을 빼는 작업은 readiness를 false로 돌려 service selector에서 빠지게 하는 식으로 구현한다.

```ts
import express from 'express';

const app = express();
let isReady = true;

app.get('/health/live', (_req, res) => res.json({ status: 'up' }));

app.get('/health/ready', (_req, res) => {
  res.status(isReady ? 200 : 503).json({ ready: isReady });
});

// 관리자 전용 - 보호 필수
app.post('/admin/drain', (_req, res) => {
  isReady = false;
  res.json({ draining: true });
});

app.post('/admin/heap-snapshot', async (_req, res) => {
  if (isReady) {
    return res.status(409).json({
      error: 'drain first via /admin/drain',
    });
  }
  const v8 = require('node:v8');
  const file = `/tmp/heap-${Date.now()}.heapsnapshot`;
  v8.writeHeapSnapshot(file);
  res.json({ file });
});

app.listen(3000);
```

2. **이벤트 루프 lag, GC 시간, heap 사이즈 메트릭을 처음부터 노출한다.** Spring Boot Actuator의 `/actuator/metrics`가 자동으로 깔아주던 메트릭들을 Node에서는 손으로 한 번 깐다. 한 번 깔아두면 두고두고 쓴다.

3. **heap snapshot은 트래픽 빠진 인스턴스에서만, 관리자 인증 뒤에서만 받는다.** 인터넷에 노출되는 일은 없어야 한다. inspector 포트도 같다. 두 번 강조하자 — inspector 프로토콜은 인증이 없다.

이 세 줄을 운영 SOP의 첫 페이지에 적어두는 편이 낫다. 7장에서 우리는 이 SOP를 더 본격적으로 풀 것이다. PM2와 Docker, Kubernetes에서의 graceful shutdown, Pino 로깅, OpenTelemetry trace 연결까지 — 이 챕터에서 배운 도구들이 운영 자리에서 어떤 모습으로 자리 잡는지를 그려보게 된다.

## 한 가지 더 — `process.report`로 한 줄 진단 받기

이 챕터의 마지막에 작은 보너스를 하나 두자. Node 11.8 이후 표준 라이브러리에 들어온 `process.report` 기능이다. jstack과 jmap을 동시에 합친 것 같은 진단 보고서를 한 번에 받게 해준다.

```ts
import * as process from 'node:process';

// 시그널로 받기:
process.on('SIGUSR2', () => {
  const file = process.report.writeReport();
  console.log(`diagnostic report written to ${file}`);
});

// 또는 코드 안에서 직접:
const file = process.report.writeReport();
```

이 함수가 만들어주는 JSON은 자바의 jstack(스레드 스택), jmap(heap 통계), 그리고 시스템 정보(libuv handle, env, resource usage)를 한 파일로 묶어준다. heap snapshot처럼 무겁지 않고, 1초 안에 떨어진다. 운영 중 알람이 떴을 때 가장 먼저 받기 좋은 가벼운 진단이다. 자바에서 `kill -3 <pid>`로 thread dump를 받던 그 첫 손동작과 가장 닮았다.

본격 분석 도구로 가기 전 단계로 두자. 이 보고서로 큰 그림을 잡고 — heap이 정상 사이즈인지, libuv handle이 폭발했는지, GC가 돌고 있는지 — 그 다음에 inspector나 clinic을 붙인다. 가벼운 게 먼저, 무거운 게 다음이다.

## 마무리 — 도구가 바뀌었을 뿐, 우리는 같은 일을 한다

이 챕터에서 우리가 한 일은 단순했다. 자바 개발자가 production에서 jstack·jmap·VisualVM·JFR·async-profiler·MAT를 들었던 손동작을, Node에서 `--inspect`·`v8.writeHeapSnapshot()`·Chrome DevTools·clinic.js·0x·heap snapshot diff로 다시 익힌 것이다. 도구 이름은 다 바뀌었다. 하지만 사고 방식은 같다. CPU가 튀면 hot path를 본다. 메모리가 부풀면 retainer를 거슬러 올라간다. 응답 시간이 느려지면 lag를 먼저 보고, lag가 정상이면 다운스트림을 본다. 이 본능은 런타임이 바뀌어도 그대로다.

도구의 사상이 갈라지는 자리도 짚었다. 자바의 도구 체인은 분담 — 도구 하나가 한 가지 일을 한다. Node는 통합 — Chrome DevTools 하나가 여러 자리를 차지하고, V8 inspector 하나가 그 발판이다. 자바에 없는 항목 한 가지가 Node에는 더 있다. 이벤트 루프 lag. 단일 스레드 모델의 대가다. 이 한 줄짜리 메트릭을 처음부터 손에 쥐고 가는 것이 6장의 핵심 챙길거리다.

도구로 못 찾는 종류와 도구로만 찾는 종류가 따로 있다는 것도 잊지 말자. catastrophic backtracking, 새는 EventEmitter, 자라는 모듈-레벨 캐시 — 이런 종류는 코드 리뷰로 안 잡힌다. heap snapshot diff와 flame graph가 잡는다. Netflix가 정규식 한 줄을 잡았듯이, 우리에게도 도구로만 잡히는 어떤 줄이 어딘가에 누워 있다. 그러니 평화로운 시간에 손에 한 번씩 익혀두자. 운영이 무릎을 꿇기 전에.

이제 손에 도구가 들렸다. 다음 장에서는 이 도구들을 어떻게 운영 환경 안에 자리 잡게 하는지를 본다. PM2와 Docker와 Kubernetes 위에서 Node 프로세스를 어떻게 띄우고, Pino와 OpenTelemetry로 로그와 trace를 어떻게 흐르게 하고, graceful shutdown을 어떻게 SOP로 만드는지. 그리고 보안 운영과 CI/CD 파이프라인까지. 6장에서 본 도구들이 7장의 운영 매뉴얼 안에서 어떤 자리에 박히는지 — 그 그림을 같이 그려보자.
