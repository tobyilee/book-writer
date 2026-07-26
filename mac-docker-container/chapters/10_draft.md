# 10장. 만든 뒤가 진짜다 — 갱신·스캔·승격

Docker 이미지 안의 소프트웨어가 취약점 패치를 받기까지, 평균 **422일**이 걸렸다.

> "Vulnerability patching of software in Docker images is significantly delayed by 422 days on average."
> (도커 이미지 안 소프트웨어의 취약점 패치는 평균 422일만큼 유의하게 지연된다.)
> — Liu et al., ESORICS 2020 §1 (**2019년경 수집**, 약 220만 개 이미지 조사)

422일이면 1년 2개월이다. 그동안 그 이미지는 아무 일 없다는 듯 잘 돌았을 것이다. 같은 조사에서 커뮤니티 이미지의 **64% 초과**가 고위험 또는 치명 등급 취약점을 갖고 있었다. 논문이 지목한 원인도 담담하다 — 이미지 안의 프로그램들은 본류에서 떨어져 나와 있어서, 개발자가 그것을 갱신할 동기가 약하다는 것이다.

그런데 이 숫자를 지금 이 순간의 사실로 읽으면 곤란하다. 수집 시점이 **2019년경**이고, 그 뒤 Docker Hub는 Docker Scout, 자동 스캔, Verified Publisher 같은 장치를 차례로 들였다. 그러니 "요즘도 422일"이라고 말할 근거는 우리에게 없다. 재측정값 역시 확보하지 못했다. 남는 것은 수치가 아니라 **구조**다. 이미지를 만든 사람은 대개 다시 오지 않고, 그 안의 패키지들은 스스로 손을 들지 않는다.

9장까지가 "만들 때"의 이야기였다면, 여기서부터는 **만든 뒤**다. 그리고 만든 뒤에 반복해야 하는 일은 생각보다 또렷한 순서를 갖는다. 베이스가 바뀐 걸 알아채고, 다시 빌드하고, 태그를 파생시키고, 검증을 통과한 것을 승격하고, 그 전부를 사람 손에서 도구로 넘긴다. 하나씩 짚어보자.

### 베이스가 바뀌었다는 걸 어떻게 아는가

먼저 반가운 소식 하나. 맥에서 Docker Desktop을 쓰고 있다면 도구는 이미 손에 있다.

> "The Docker Scout CLI plugin comes pre-installed with Docker Desktop."
> (Docker Scout CLI 플러그인은 Docker Desktop에 사전 설치되어 나온다.)

Docker Desktop 없이 Docker Engine만 쓰는 환경이라면 별도 바이너리로 설치해야 한다고 같은 문서가 덧붙인다. 우리는 앞의 경우이니, 설치 절차 없이 바로 쳐볼 수 있다. `docker scout`의 하위 명령은 **19개**다(2026년 7월 25일 조회 기준). 그중 지금 우리 질문에 직접 답하는 것은 넷이다.

| 명령 | 문서의 한 줄 규정 |
|------|------------------|
| `docker scout quickview` | "Quick overview of an image" |
| `docker scout cves` | "Display CVEs identified in a software artifact" |
| `docker scout recommendations` | "**Display available base image updates and remediation recommendations**" |
| `docker scout sbom` | "Generate or display SBOM of an image" |

순서대로 읽으면 쓰임이 보인다. `quickview`로 이미지를 한눈에 훑고, 궁금한 데가 있으면 `cves`로 어떤 취약점이 잡혔는지 들여다본다. 그런데 이 장의 첫 질문 — "베이스가 바뀐 걸 어떻게 아는가" — 에 정확히 대응하는 것은 세 번째다. `recommendations`는 취약점 목록이 아니라 **지금 쓸 수 있는 베이스 이미지 업데이트와 개선 권고**를 보여준다고 문서가 스스로 규정한다. 매일 `docker pull`을 쳐보며 다이제스트가 바뀌었나 눈으로 비교하는 대신, 도구에게 물어보면 되는 것이다.

한 가지 주의. 같은 문서에서 `compare`·`policy`·`environment`·`stream`에는 **`(experimental)`** 표시가 붙어 있다. 실험 단계라는 뜻이니, 팀의 파이프라인에 못 박아 넣기 전에 그 표시부터 확인하는 편이 낫다.

여기까지 오면 다음 질문이 자연스럽게 따라붙는다. 도구가 "올릴 게 있다"고 알려준다면, **그걸 누가 언제 올리는가?**

### 갱신을 도구에 맡기기

사람이 기억해서 하는 일은 결국 잊힌다. 그래서 Dockerfile의 `FROM` 줄을 **의존성으로 취급하는** 도구들이 있다. GitHub의 Dependabot과 Renovate 둘 다 이 일을 한다.

Dependabot 쪽 최소 설정은 놀랄 만큼 짧다.

```yaml
- package-ecosystem: "docker"
  directory: "/"
  schedule:
    interval: "weekly"
```

공식 문서가 이 예시에 붙여둔 주석이 그대로 설명이다 — "Look for a `Dockerfile` in the `root` directory"(루트 디렉터리에서 `Dockerfile`을 찾는다), "Check for updates once a week."(일주일에 한 번 업데이트를 확인한다). 생태계 값이 `"docker"`라는 것, 그리고 별도로 `"docker-compose"` 값도 있다는 것만 기억해두자.

Renovate는 접근이 조금 다르다. 문서는 "Renovate supports updating Dockerfile dependencies."라고 말한 뒤, 어떤 파일을 대상으로 삼는지를 정규식으로 공개한다.

```
/(^|/|\.)([Dd]ocker|[Cc]ontainer)file$/
/(^|/)([Dd]ocker|[Cc]ontainer)file[^/]*$/
```

파일 이름이 `Dockerfile.prod`처럼 변형돼 있어도 잡힌다는 뜻이다.

여기서 선을 하나 분명히 긋자. **두 문서 모두, 서술 범위는 "PR을 여는 것"까지다.** "Dependabot이 재빌드를 트리거한다"고 읽으면 틀린다. 재빌드는 그 PR에 붙은 CI가 하는 일이고, 그 연결을 명시한 1차 문장은 확보하지 못했다. 도구가 해주는 것은 **`FROM` 줄을 고친 변경 제안을 올려놓는 것**이고, 그 뒤는 우리 파이프라인의 몫이다.

그리고 9장을 떠올려보자. 베이스를 digest로 못 박아 뒀다면 `--pull`은 아무것도 바꾸지 못한다. 고정을 풀어 올리려면 **누군가 그 줄을 직접 고쳐야 한다.** 그 "누군가"를 사람에서 도구로 옮기는 것이 이 소절의 전부다.

### 자동 갱신 PR을 어떻게 굴릴 것인가 — 쿨다운과 자동 머지 논쟁

자동 PR이 열리기 시작하면, 남는 질문은 하나뿐이다. **머지는 누가, 언제 하는가?**

2026년 2월 20일 해커뉴스에 "Turn Dependabot off"라는 제목의 글이 올라와 647점을 받았다. 원문 블로그는 이 책이 열어보지 않았으므로 글쓴이의 주장은 옮기지 않는다. 대신 그 아래 달린 댓글들이 우리에게 재료다. 2025~2026년의 처방으로 반복해서 등장하는 단어가 하나 있는데, **쿨다운**이다.

> `esafak` (2026-02-20): "I automate updates with a cooldown, security scanning, and the usual tests. If it passes all that I don't worry about merging it."
> (나는 쿨다운·보안 스캔·평소 테스트를 붙여 업데이트를 자동화한다. 그걸 다 통과하면 머지를 걱정하지 않는다.)

> `seg_lol` (2026-02-20): "Be wary of upgrading dependencies too quickly. This is how supply chain incursions are able to spread too quickly. **Time is a good firwall.**"
> (의존성을 너무 빨리 올리는 걸 경계하라. 공급망 침투가 빠르게 퍼지는 경로가 이것이다. **시간은 좋은 방화벽이다.** — 원문의 `firwall` 오타 그대로)

자동화를 끄자는 말이 아니라, 자동화 **앞에** 시간과 검사를 세우자는 말이다. 갓 나온 릴리스를 그날 바로 밀어 넣지 않는 것만으로도 공급망 사고의 확산 경로 하나가 좁아진다.

물론 반대편도 만만치 않다. 같은 스레드에서 `robszumski`는 "우리는 무시하는 것보다 자동 머지를 원해야 하지 않나?"라고 물었고, `dotancohen`의 답은 한 단어였다 — "No". 또 다른 참여자는 "몇 단계를 건너뛰고 내가 당신 인프라에 설치할 멀웨어 zip을 직접 보내줄 수도 있다"고 비꼬았다. 정리하자면, **자동 머지에 대해 커뮤니티는 합의하지 않았다.** 이 책이 어느 쪽 손을 들어주기보다, 합의가 없다는 사실 자체를 판단 재료로 건네는 편이 정직하다.

도구를 만드는 쪽의 고백도 같은 스레드에 있다. Renovate 메인테이너 `jamietanna`(2026-02-20)는, 보안 PR을 올릴 때 `govulncheck` 같은 더 나은 데이터 소스를 흡수할 방법이 지금은 없다고 적었다. 도구가 무엇을 모르는지를 도구 쪽이 먼저 말한 셈이다.

무엇을 모르길래 문제가 되는가. 같은 스레드의 `indiekitai`(2026-02-21)가 남긴 문장은 **의존성 스캐너를 두고 나온 말이지만**, 그 답을 가장 날카롭게 담고 있다.

> "It knows you depend on package X, and X has a CVE, so it alerts you. **But it has no idea whether you actually call the vulnerable code path.** … The irony is that Dependabot's noise makes teams less secure, not more. When every PR has 12 security alerts, people stop reading them. **Alert fatigue is a real attack surface.**"
> (당신이 패키지 X에 의존하고 X에 CVE가 있다는 것만 알고 알린다. **그런데 당신이 그 취약한 코드 경로를 실제로 호출하는지는 전혀 모른다.** … 아이러니는 Dependabot의 소음이 팀을 더 안전하게가 아니라 덜 안전하게 만든다는 것이다. 모든 PR에 보안 경고가 12개씩 붙으면 사람들은 그걸 읽기를 멈춘다. **알림 피로는 실재하는 공격 표면이다.**)

자바 쪽 도구를 묻는 대목도 있었다. `wpollock`(2026-02-21)이 OWASP dependency-check를 메이븐 빌드에 붙여 썼다고 답한 정도인데, 이건 한 스레드의 표본 하나다. "자바 생태계엔 도달 가능성을 아는 도구가 없다"로 단정할 근거는 되지 못한다.

마지막으로 이 소절의 경계를 정직하게 밝혀두자. **여기 인용한 증언은 전부 의존성 스캐너 이야기다.** `docker scout`이나 그에 준하는 도구로 **컨테이너 이미지를 스캔한 뒤**의 알림 피로에 대해서는, 2026년 7월 25일 재검색에서도 인용할 만한 증언을 찾지 못했다. 위 문장들을 이미지 스캔 쪽으로 옮겨 읽지 말자.

### 태그 하나에서 여러 태그를 파생시키기

이제 갱신된 베이스로 다시 빌드했다고 하자. 그 결과물에 어떤 태그를 붙일 것인가?

`v1.2.3`이라는 git 태그 하나에서 여러 개의 도커 태그를 파생시키는 규칙을, GitHub Actions 공식 액션 `docker/metadata-action`(**v6**, 2026년 기준)이 표로 명문화해 두었다.

| Git tag | Pattern | Output |
|---|---|---|
| `v1.2.3` | `{{raw}}` | `v1.2.3` |
| `v1.2.3` | `{{version}}` | `1.2.3` |
| `v1.2.3` | `{{major}}.{{minor}}` | `1.2` |
| `v1.2.3` | `v{{major}}` | `v1` |
| `v2.0.8-beta.67` | `{{version}}` | `2.0.8-beta.67` |
| `v2.0.8-beta.67` | `{{major}}` | `2.0.8-beta.67` |
| `v2.0.8-beta.67` | `{{major}}.{{minor}}` | `2.0.8-beta.67` |

앞의 네 줄은 예상대로다. 릴리스 하나에서 정확한 버전(`1.2.3`), 마이너 라인(`1.2`), 메이저 라인(`v1`)이 한꺼번에 나온다. 뒤의 세 줄이 백미다. **프리릴리스 태그에 `{{major}}` 패턴을 걸어도 `2`가 나오지 않는다.** 원본이 그대로 나온다. 무슨 뜻일까? 베타를 하나 찍었다고 해서 `v1`이나 `1.2` 같은 **이동 태그가 베타를 가리키게 되는 일이 없다**는 뜻이다.

이 예외 하나가, 태깅을 직접 짠 셸 스크립트에 맡기지 않을 이유로 충분하다. 직접 짜면 대개 문자열을 점으로 잘라 앞 조각을 쓰는데, 그러면 `2.0.8-beta.67`은 조용히 `2`가 되어 운영 태그를 오염시킨다. 커밋 단위로 찍고 싶다면 `type=sha`가 "Output Git short commit (or long if specified) as Docker tag like `sha-860c190`."라고 규정돼 있고, `latest`는 별도 옵션이 아니라 `flavor` 입력으로 다뤄져 기본 `auto` 모드에서 생성된다.

⚠️ 한 가지는 분명히 해두자. 이 표의 출처는 **그 액션 자신의 README**다. 널리 쓰이는 구현이 채택한 규칙이라고는 말할 수 있어도, "semver 태깅의 업계 표준"이라고 부를 근거는 아니다.

### 재빌드 없이 태그만 옮기기 — 승격

스테이징에서 검증을 통과한 이미지를 운영으로 올린다고 해보자. 흔히 하는 실수는 **운영 태그를 붙여 다시 빌드하는 것**이다. 그런데 잠시 생각해보자. 다시 빌드한 그 이미지는, 방금 검증한 이미지와 정말 같은 이미지인가? 9장에서 봤듯 같은 Dockerfile이 어제와 오늘 다른 결과를 낸다. 검증한 것과 배포하는 것이 어긋나는 순간, 검증은 의미를 잃는다.

그래서 승격은 **다시 만드는 일이 아니라 이름을 하나 더 붙이는 일**이어야 한다. 이 일을 가장 명확하게 규정한 도구는 `crane`이다.

> `crane tag`: "**Tag remote image without downloading it.**"
> (원격 이미지를 내려받지 않고 태그한다.)

```
crane tag ubuntu v1
```

문서는 `copy`와의 차이도 설명한다. 매니페스트가 이미 존재한다는 것을 알기 때문에 레이어 존재 확인을 건너뛸 수 있고, 그래서 `tag`가 `copy`보다 조금 더 빠르다는 것이다.

도커 툴체인만으로 하고 싶다면 `docker buildx imagetools create`가 대안이다. 다만 소개하는 방식에 주의가 필요하다. 이 명령의 자기 규정은 여전히 "Create a new manifest list based on source manifests."이고, "태그만 붙이는 명령"이 아니다. 승격에 쓸 수 있는 근거는 도입부의 두 문장이다.

> "The source manifests … **must already exist in the registry** where the new manifest is created."
> (소스 매니페스트는 새 매니페스트가 만들어지는 레지스트리에 **이미 존재해야 한다**.)

> "If only one source is specified and that source is a manifest list or image index, create performs a **carbon copy**."
> (소스가 하나뿐이고 그것이 매니페스트 리스트나 이미지 인덱스라면, `create`는 **그대로 복사**한다.)

소스가 레지스트리에 이미 있어야 한다는 것은, 로컬 재빌드가 이 과정에 끼어들지 않는다는 뜻이다. 그리고 함정이 하나 있다. 소스가 **리스트나 인덱스가 아닌 단일 매니페스트**이면 출력은 매니페스트 리스트가 되고, 그 동작은 `--prefer-index=false`로만 끌 수 있다. 단일 아키텍처 이미지를 승격했더니 형식이 바뀌어 있을 수 있다는 이야기다. 알고 쓰면 문제가 아니지만, 모르고 만나면 꽤 난감하다.

### 같은 태그를 두 번 밀 수 없게 만들기

승격까지 왔는데도 뒷맛이 찜찜한 구석이 하나 남는다. 누군가 `v1.2.3`이라는 태그를 **다시** 밀어버리면 어떻게 되는가?

기억해둘 것은, 태그 불변성이 OCI 스펙의 성질이 아니라 **레지스트리가 켜고 끄는 기능**이라는 점이다. AWS ECR은 리포지터리 단위 설정으로 이것을 제공한다.

> "You can prevent image tags from being overwritten by turning on tag immutability in a repository. After tag immutability is turned on, the `ImageTagAlreadyExistsException` error is returned if you push an image with a tag that is already in the repository."
> (리포지터리에서 태그 불변성을 켜면 이미지 태그가 덮어써지는 것을 막을 수 있다. 켠 뒤에 이미 있는 태그로 push하면 `ImageTagAlreadyExistsException` 에러가 반환된다.)

푸시가 실패하는 것이 아니라 **거부되는** 것이다. 문서에는 예외 필터를 두는 옵션(`IMMUTABLE_WITH_EXCLUSION`)도 함께 실려 있다. 다만 같은 페이지에 "모든 태그에 적용되며 일부만 불변으로 만들 수는 없다"는 옛 문장도 남아 있어서 **페이지 안이 서로 어긋난다**(2026년 7월 25일 조회). 그러니 "ECR은 전부 아니면 전무"라고 외우지 말고, 쓰기 직전에 콘솔에서 직접 확인하는 편이 낫다.

다른 레지스트리는 어떨까. GitHub Container Registry(GHCR)에 대해서는 조심스럽게 말해야 한다. **이 책이 확인한 컨테이너 레지스트리 문서 페이지에는 태그 불변성·덮어쓰기 방지에 대한 언급이 없었다.** 이것은 "GHCR에 그런 기능이 없다"는 뜻이 아니라, 확인한 문서에 나오지 않았다는 뜻이다. 다른 페이지에 있을 수 있으니 필요하면 직접 찾아보자. Docker Hub는 이번 리서치에서 조회하지 않았다.

마지막으로, 이미지가 무엇으로 이루어졌고 어떻게 만들어졌는지를 **함께 실어 보내는** 장치도 있다. 여기서 계속 나오는 SBOM이라는 말부터 풀어두자. 이미지 안에 어떤 소프트웨어 부품이 들어 있는지를 적은 **자재 명세서**다. Docker Scout이 하는 일도 결국 이것을 만든 뒤 "계속 갱신되는 취약점 데이터베이스에 대조"하는 것이라고 문서가 설명한다. 부품 목록이 있어야 대조가 되고, 대조가 돼야 "이 이미지의 어느 부품이 문제인가"를 말할 수 있는 셈이다.

그 명세서를 조회만 하는 것이 아니라 이미지에 붙여 보낼 수도 있다. `docker buildx build --sbom=true`는 이미지에 담긴 소프트웨어 목록(SBOM)을, `--provenance=mode=max`는 빌드 경위를 첨부물로 붙인다. 문서는 `mode=min` 수준의 프로비넌스가 기본으로 붙는다고 말하는데, 빌더와 출력 종류에 따라 조건이 붙는지는 확인하지 못했으니 무조건적인 기본값으로 여기지는 말자. 앞서 본 `docker scout sbom`과 헷갈리기 쉬운데, **이쪽은 만들어 붙이는 일이고 저쪽은 이미 있는 것을 조회하는 일**이다. 층위가 다르다. 서명이 필요하다면 `cosign sign $IMAGE` 형태로 시작하면 되고, 검증 쪽 명령은 이 책이 1차 소스로 확인하지 못했으니 sigstore 문서를 직접 확인하자.

---

이 장에서 한 일을 한 줄로 이으면 이렇게 된다. **베이스가 바뀐 것을 `docker scout`으로 알아채고, 그 변경을 Dependabot이나 Renovate가 PR로 올리고, 쿨다운과 테스트를 통과한 것만 머지해 다시 빌드하고, `metadata-action`의 규칙으로 태그를 파생시키고, 검증을 통과한 그 이미지를 재빌드 없이 승격한다.** 그리고 승격의 종착지인 태그를 아무도 덮어쓰지 못하게 잠근다.

이 다섯 걸음이 한 바퀴다. 한 번 만들어놓고 잊는 것과, 도구가 대신 돌려주는 이 바퀴를 갖는 것 사이에 얼마만큼의 거리가 있는지 — 그것을 2019년경의 이미지들에서 재본 숫자가 이 장의 첫머리에 있던 422일이었다. 오늘의 거리는 각자 자기 레지스트리에서 재볼 일이다.
