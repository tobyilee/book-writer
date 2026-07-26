# 9장. 코드를 고쳤는데 왜 그대로일까 — 태그·캐시·재현성

`nickname`이 계속 `null`로 들어간다.

스프링 부트 앱을 EC2에 올려둔 개발자가 남긴 기록이다. 처음 띄웠을 때 값이 비어 들어오길래 코드를 고쳤다. 고정된 문자열이 들어가도록 바꾸고, 다시 빌드해서 다시 밀었다. 그런데 결과는 그대로였다.

> "**문제** : spring 처음에 띄운 것 대로 nickname이 null로 들어가고, "kakao", "apple"처럼 fix 된 string을 넣도록 코드를 고쳐서 다시 docker image 빌드를 했으나 **계속해서 nickname이 null로 들어가는 문제 발생**"
> — velog, 「[springboot&docker] push한 도커 이미지가 적용이 안된다면?」 (2022-11-20 게시, 2026-07-25 검색)

고쳤는데 안 고쳐진다. 이 한 줄에 등이 서늘해지는 이유는, 우리가 아는 디버깅 절차가 전부 헛돌기 때문이다. 로컬에서 돌리면 멀쩡하고, 코드를 다시 열어봐도 고친 그대로다. 의심할 곳이 코드에 없을 때 우리는 어디를 봐야 할까?

### 태그는 고정된 이미지를 가리키지 않는다

먼저 이 글에서 무엇을 가져올 수 있고 무엇은 가져올 수 없는지 갈라두자. 남의 기록을 읽는 일에는 이 작업이 늘 먼저다.

가져올 수 있는 건 **증상**이다. 코드를 고쳐 다시 빌드하고 다시 밀었는데 바뀐 내용이 반영되지 않았다 — 이건 이 개발자가 실제로 관측한 것이고, 남의 해석이 끼어들 자리가 없다. 반면 **원인**은 그렇지 않다. 글쓴이 본인이 그 대목을 "문제 예상 원인"이라고 적었고, "Ec2에서 docker가 어떤 생태 흐름으로 흘러가는지는 모르나"라고 스스로 단서를 달았다. 그러니 그가 추정한 메커니즘은 이 책이 사실로 옮기지 않는다. 시점도 붙여두자. **2022년 11월 글**이고, 운영 장애가 아니라 개발 성격의 배포다. "프로덕션이 죽었다"는 이야기로 부풀리지 말자.

그럼 확인된 사실만으로 어디까지 갈 수 있을까. 뜻밖에도 꽤 멀리 간다. 출발점은 도커 공식 문서의 이 한 문장이다(2026년 7월 검색 기준).

> "If you specify `FROM alpine:3.21` in your Dockerfile, `3.21` resolves to the **latest patch version** for `3.21`."
> (Dockerfile에 `FROM alpine:3.21`이라고 적으면, `3.21`은 `3.21`의 최신 패치 버전으로 해석된다.)

읽고 넘기기 쉬운 문장인데, 담긴 뜻은 제법 무겁다. **`3.21`이라는 글자는 특정 이미지의 이름이 아니라 "지금 그 자리에 놓인 것"을 가리키는 화살표다.** 어제의 `3.21`과 오늘의 `3.21`이 다른 내용일 수 있다. 즉 **같은 Dockerfile이 어제와 오늘 다른 이미지를 만든다.** 6장에서 태그가 인덱스를 거쳐 여러 매니페스트로 갈라지는 걸 봤는데, 그때 심어둔 성질이 여기서 정체를 드러낸다. 태그는 내용에 붙는 이름이 아니라 **내용을 갈아 끼울 수 있는 꼬리표**다.

그 성질이 배포에도 그대로 작동한다. 같은 이름으로 다시 밀면 태그 글자는 그대로인 채 뒤에 놓인 내용만 바뀐다. 그러면 어느 시점의 내용이 지금 쓰이고 있는지, **태그만 봐서는 알 수 없다.** 위 글이 겪은 상황이 정확히 이 모양이었다 — 이름이 같은 이미지가 그 EC2에 세 개 있었다고 적혀 있다.

여기서 정직하게 멈추자. **"그래서 그 서버가 왜 옛날 것을 돌렸는가"까지는 이 책이 말하지 않는다.** 그 대목의 근거는 글쓴이의 추정뿐이고, 추정을 사실로 승격하는 순간 이 책은 자기가 하지 말자고 약속한 일을 하게 된다. 대신 확인된 것만으로도 실무에서 쓸 결론이 하나 남는다. **같은 태그를 여러 번 밀어놓고 나면, 지금 돌아가는 것이 어느 빌드인지 태그로는 증명할 수 없다.** 증명할 수 없다는 것 자체가 이미 문제다. 원인을 좁히려 해도 좁힐 근거가 없으니, 남는 건 재시작해보고 지워보는 식의 주먹구구뿐이다.

한 가지 더. 그 개발자는 사고를 정리하면서 이렇게 적었다. "이제까지 무지성으로 사용했던 `-t`가 이름과 태그를 붙이는 옵션이었다. 태그명은 생략 가능한데, 생략하면 기본적으로 `latest`가 붙는다." **7장에서 우리가 표로 미리 본 그 기본값이다.** 생략은 선택을 안 한 게 아니라 남에게 맡긴 것이라고 그때 말했는데, 맡긴 결과를 이 개발자는 사고를 겪고 나서 알았다. 그렇다면 태그가 못 하는 그 일 — 내용을 못 박는 일 — 은 무엇이 해줄까?

### digest가 보장하는 것

답은 2장에서 이미 지나쳤다. 이미지가 태그에서 시작해 매니페스트를 거쳐 레이어까지 이어지는 사슬이라고 했을 때, 그 조각들을 서로 붙들고 있던 것 — digest다. OCI 이미지 스펙의 규정은 이렇다.

> "The digest property of a Descriptor acts as a **content identifier**, enabling content addressability. It **uniquely identifies content by taking a collision-resistant hash of the bytes.**"
> (Descriptor의 digest 속성은 콘텐츠 식별자로 동작하며 콘텐츠 주소 지정을 가능하게 한다. 바이트들의 충돌 저항 해시를 취해 콘텐츠를 고유하게 식별한다.)

핵심은 **내용에서 계산된다**는 점이다. 이름을 붙이는 게 아니라 바이트를 세어 지문을 뜬다. 그러니 내용이 한 바이트라도 달라지면 다른 digest가 나오고, 반대로 digest가 같으면 같은 내용이다. 태그가 갈아 끼울 수 있는 꼬리표였다면, digest는 갈아 끼울 수 없는 지문이다.

Dockerfile에는 이렇게 박는다.

```dockerfile
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

이 한 줄이 무엇을 보장하는지도 문서가 직접 말해준다.

> "By pinning your images to a digest, you're **guaranteed to always use the same image version**, even if a publisher replaces the tag with a new image."
> (이미지를 digest로 고정하면, 배포자가 그 태그를 새 이미지로 교체하더라도 항상 같은 이미지 버전을 쓰는 것이 보장된다.)

"even if a publisher replaces the tag" — 교체가 일어난다는 것을 전제에 깔고 쓴 문장이다. 실제로 태그 덮어쓰기를 막는 기능은 레지스트리가 **옵션으로 켜고 끄는 상품**이다. 즉 기본이 불변이 아니라는 뜻인데, 그 이야기는 운영 쪽 재료라 10장에서 다룬다.

작은 주의 하나. 위 예시가 `sha256:`으로 시작한다고 해서 digest가 곧 SHA-256인 것은 아니다. 스펙의 문법은 `algorithm ":" encoded`라는 일반형이고, `sha256`은 실무에서 흔히 보게 되는 형태일 뿐이다. 그리고 예고 한 줄 — **쿠버네티스에서는 태그로 두느냐 digest로 박느냐가 이미지를 내려받는 동작까지 바꾼다.** 그건 12장의 몫이다.

### `--pull`과 `--no-cache`는 다른 일을 한다

여기서 많은 사람이 두 플래그를 같은 것으로 뭉뚱그린다. "안 바뀌면 이거 붙여봐" 정도로 배우기 때문이다. 문서의 정의를 나란히 놓아보자.

> `--pull`: "forces Docker to check for and download a **newer version of the base image**, even if you have a version cached locally."
> (로컬에 캐시된 버전이 있더라도, 베이스 이미지의 새 버전을 확인하고 내려받도록 강제한다.)
>
> `--no-cache`: "**disables the build cache**, forcing Docker to rebuild all layers from scratch."
> (빌드 캐시를 비활성화하여, 모든 레이어를 처음부터 다시 만들도록 강제한다.)

```console
$ docker build --pull -t my-image:my-tag .
$ docker build --no-cache -t my-image:my-tag .
$ docker build --pull --no-cache -t my-image:my-tag .
```

건드리는 대상이 다르다. 앞은 **바깥에서 가져오는 재료**를 새로 확인하고, 뒤는 **내가 만들어둔 중간 결과**를 버린다. 이 정의 둘을 앞 소절과 겹쳐 놓으면 세 갈래가 저절로 갈린다.

**digest로 고정했다면 `--pull`은 아무것도 바꾸지 못한다.** 지문을 지정해뒀으니 확인하러 가도 같은 것이 돌아온다. **태그로 뒀다면 `--pull`이 베이스의 패치를 끌어온다.** 태그 뒤의 내용이 바뀌어 있을 수 있으니 확인이 의미를 갖는다. **그리고 내 코드가 반영되지 않는 문제는 이 둘 어느 쪽도 아니다** — 그건 캐시의 영역이다. 세 갈래를 구분하지 못하면 증상마다 아무 플래그나 붙여보게 되고, 운 좋게 고쳐진 날에도 왜 고쳐졌는지 모른 채 넘어간다. 뒷맛이 찜찜한 성공이다.

### 캐시는 언제 재사용되는가

그럼 캐시는 어떤 규칙으로 움직일까. 문서의 규정은 짧다.

> "a layer is reused from the build cache if **the instruction and the files it depends on hasn't changed** since it was previously built."
> (명령과 그 명령이 의존하는 파일이 이전 빌드 이후로 바뀌지 않았다면, 레이어는 빌드 캐시에서 재사용된다.)
>
> "a change causes a **rebuild for steps that follow**."
> (변경이 생기면 그 뒤에 오는 단계들이 다시 만들어진다.)

두 문장을 붙여 읽으면 Dockerfile의 줄 순서가 왜 성능을 좌우하는지가 보인다. 위쪽에서 한 번 깨지면 아래는 전부 따라 깨진다. 그래서 자주 바뀌는 것을 아래에 두는 것이고, 7장에서 본 layered jar의 `COPY` 네 줄이 바로 그 원리의 자바판이었다.

그런데 "그 명령이 의존하는 파일"은 어디까지를 말하는 걸까. 여기서 **빌드 컨텍스트**라는 말을 짚고 가자. 빌드를 시작할 때 우리가 마지막에 찍는 그 점(`docker build ... .`)이 컨텍스트다. 그 자리에 적은 디렉터리가 통째로 빌더에게 건네지고, `COPY`가 가져올 수 있는 범위도 거기까지다. 다시 말해 **내 프로젝트 폴더 안에 있는 것들이 빌드의 입력이 된다.** 그래서 무엇을 빼둘지가 캐시의 운명을 가른다. 빼는 데 쓰는 것이 `.dockerignore`이고, 그 규칙이 걸리는 범위는 이렇다.

> "Ignore-rules specified in the `.dockerignore` file apply to the **entire build context, including subdirectories**."
> (`.dockerignore` 파일에 지정한 무시 규칙은 하위 디렉터리를 포함한 빌드 컨텍스트 전체에 적용된다.)

하위 디렉터리까지 포함한다는 말은 뒤집으면 이렇게 읽힌다. **거기서 빠뜨린 파일 하나가 바뀔 때마다 캐시가 깨진다.** 자바 프로젝트라면 `build/`나 `target/` 같은 산출물 디렉터리가 후보다. 빌드할 때마다 값이 달라지는 것들이 컨텍스트에 들어 있으면, 매번 새로 만드는 셈이 된다.

반대로 캐시가 **너무 잘 들어서** 문제가 되는 고전 함정도 있다. 문서의 권고는 단호하다 — "Always combine `RUN apt-get update` with `apt-get install` in the same `RUN` statement." 두 줄로 나눠두면 `update` 줄이 캐시에 굳어버려서, 몇 달 뒤 빌드해도 낡은 패키지 목록으로 설치하게 된다. 아찔한 종류의 성공이다.

한편, 매번 다시 받는 게 아까운 것들은 따로 붙잡아둘 수 있다. BuildKit의 캐시 마운트다.

```dockerfile
RUN --mount=type=cache,target=/root/.npm npm install
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked apt update && apt-get install -y gcc
```

문서에 실린 예시 그대로다. 방금 본 레이어 캐시와는 성격이 다르다는 점을 눈여겨보자. 레이어 캐시가 **단계를 통째로 건너뛰는** 장치라면, 캐시 마운트는 **그 단계가 다시 돌아야 할 때 빈손으로 시작하지 않게** 해주는 쪽에 가깝다. 위 예시로 말하면, `package.json`이 바뀌어 그 줄의 캐시가 깨지면 `npm install`은 다시 돌아간다. 다만 이미 받아둔 것을 또 받지는 않는다.

자바 독자라면 여기서 `~/.gradle`이나 `~/.m2`를 떠올렸을 것이다. 의존성을 매번 새로 내려받는 빌드만큼 지치는 것도 없으니까. 그런데 **그 예시는 문서에 없다.** 원리상 같은 방식이 적용될 것 같지만, 이 책은 확인하지 못한 것을 확인한 척 쓰지 않기로 했다. 원리를 자기 프로젝트에 옮겨 적용해보고, 실제로 캐시가 살아나는지는 직접 재보자.

여러 사람이 캐시를 나눠 쓰고 싶다면 캐시를 레지스트리에 얹는 길도 있다(`docker buildx build --cache-from type=registry,ref=user/app:buildcache .`). CI에서 매번 빈 손으로 시작하는 것을 줄이는 용도다.

### 빌드 시크릿 — `ARG`는 이미지에 남는다

빌드 중에 비밀값이 필요할 때가 있다. 사설 저장소 자격증명이나 토큰 같은 것들이다. 손에 잡히는 대로 `ARG`나 `ENV`로 넘기기 쉬운데, 문서가 그 방식을 정면으로 막는다.

> "Build arguments and environment variables are **inappropriate for passing secrets to your build, because they persist in the final image.**"
> (빌드 인자와 환경변수는 빌드에 비밀값을 넘기는 데 부적절하다. 최종 이미지에 남기 때문이다.)

"persist in the final image" — 빌드가 끝나면 사라질 것 같지만 남는다. 빌드할 때만 쓴 값이라는 감각과 실제가 어긋나는 지점이라, 모르고 지나가기 딱 좋다. 그리고 이 어긋남이 특히 끔찍한 이유는 **회수가 안 되기 때문**이다. 이미지는 만들어서 끝나는 게 아니라 레지스트리에 올려 남들이 내려받는 물건이다. 그러니 이미지에 남았다는 건 그 이미지를 받아본 사람 모두에게 남았다는 뜻이고, 그걸 뒤늦게 알아차렸을 때 할 수 있는 일은 이미지를 지우는 게 아니라 **비밀값 자체를 폐기하고 새로 발급받는 것**뿐이다. 대신 쓰라고 문서가 안내하는 것이 시크릿 마운트다.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

```console
$ docker build --secret id=aws,src=$HOME/.aws/credentials .
$ docker build --secret id=kube,env=KUBECONFIG .
$ docker build --secret id=API_TOKEN .
```

파일에서, 환경변수에서, 혹은 이름만 주고 넘기는 세 형태다. 컨테이너 안에서 값이 놓이는 기본 경로도 정해져 있다 — "The default file path of the secret, inside the build container, is `/run/secrets/<id>`." 그러니까 `id=aws`로 넘겼으면 빌드 중에는 `/run/secrets/aws`에서 읽는다. 문서가 이 방식을 `ARG`·`ENV`의 대안으로 내세우는 이유는 앞 문장에 이미 나왔다 — 그쪽은 최종 이미지에 남고, 이쪽은 빌드에 비밀값을 "securely" 노출하는 방법으로 소개된다. 손이 한 번 더 가는 대신, 값을 이미지에 굳히지 않는다.

### 레이어를 뜯어보기

여기까지 오면 자연스럽게 드는 궁금증이 있다. 내 이미지는 어떤 층으로 쌓여 있고, 그중 무엇이 자리를 차지하고 있을까? 눈으로 확인할 방법이 둘 있다.

하나는 도커에 들어 있다. `docker image history`, 한 줄 규정은 "Show the history of an image"다(옵션과 컬럼은 2026년 7월 검색 기준). 출력 컬럼은 `IMAGE`, `CREATED`, `CREATED BY`, `SIZE`, `COMMENT` 다섯이고, `CREATED BY`가 그 레이어를 만든 명령이라 Dockerfile을 거꾸로 읽는 느낌으로 볼 수 있다. 값은 여기 옮기지 않는다 — 문서의 예제 출력이 오래된 형식이라, 여러분이 직접 친 결과가 훨씬 정확하다.

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--format` | | Format output using a custom template: 'table', 'json', or Go template |
| `-H`, `--human` | `true` | Print sizes and dates in human readable format |
| `--no-trunc` | | Don't truncate output |
| `--platform` | | Show history for the given platform (e.g., `linux/amd64`) |
| `-q`, `--quiet` | | Only show image IDs |

이 표에서 이 책에 특히 반가운 건 `--platform`이다. 6장에서 만든 멀티플랫폼 이미지를 **아키텍처별로 나눠서** 들여다볼 수 있다는 뜻이니까. 다만 문서는 이 옵션이 있다는 것까지만 말한다. 그 이상의 활용법은 확인된 바 없으니 직접 쳐 보고 판단하자.

다른 하나는 별도 도구다. `dive`는 스스로를 이렇게 소개한다 — "A tool for exploring a Docker image, layer contents, and discovering ways to shrink the size of your Docker/OCI image." 맥에서는 `brew install dive`로 깔고 `dive <your-image-tag>`로 연다. 재미있는 건 CI 모드다. 환경변수 `CI=true`를 주고 실행하면 이미지 효율과 낭비 공간을 기준으로 **통과/실패 결과**를 돌려준다. 파이프라인에 문지기를 세울 수 있다는 뜻이다. 물론 이건 이 도구가 자기 자신에 대해 하는 말이고, 이 책이 다른 도구와 견줘본 것은 아니다. 마음에 들면 쓰고, 아니면 `docker image history`만으로도 충분하다.

마지막으로 7장에서 본 멀티스테이지 Dockerfile을 이 눈으로 다시 보자. 앞 단계에서 jar를 풀어헤치고, 뒤 단계는 그중 필요한 디렉터리만 `COPY --from=builder`로 건네받았다. 그러니 레이어 목록에는 **건네받은 것만** 보인다. 추출하느라 만들었던 중간 산출물도, 그 작업에 쓴 도구도 최종 이미지의 이력에는 없다. 멀티스테이지가 이미지를 줄이는 원리를 한 줄로 줄이면 이것이다 — **남기지 않은 것은 뜯어봐도 없다.** 크기를 줄이려고 이것저것 지우는 대신, 애초에 옮기지 않는 쪽을 택한 설계다.

---

같은 명령이 다른 결과를 낼 때, 의심할 곳은 셋이다. **태그**(가리키는 대상이 바뀌었나), **캐시**(내가 고친 것이 반영되지 않았나), **컨텍스트**(빌드에 들어간 파일이 내 생각과 같은가). 이 셋을 나눠서 묻기 시작하면 "어제는 됐는데"라는 말이 수사에서 질문으로 바뀐다.

방금 digest로 못 박아둔 그 베이스 이미지 말이다. 고정해뒀으니 안심이라고 적었는데, 고정했다는 건 **바뀌어도 모른다**는 뜻이기도 하다. 마지막으로 갱신한 게 언제였더라?
