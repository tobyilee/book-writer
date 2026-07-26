<!-- 검색 시점: 2026-07-25 기준 -->
<!-- 2차 표적 보강 리서치 (gap-fill 2) — §7-2 "소스 0건" 목록 되살리기 -->

# 웹 리서치 2차 보강: 맥에서의 Docker/컨테이너 — §7-2 0건 항목 표적 확보

> **이 문서의 목적.** `01_reference.md` §7-2에는 "Phase 2가 계획에 넣으면 안 되는 소절(소스 0건)" 8행이 있다. 그중 상당수가 **사용자가 명시적으로 요청한 내용**(요구 3번 "업데이트하는 방법", 요구 4번 "맥에서 써보려면")이라 뺄 수 없다. 이 문서는 그 항목들에 **1차 소스를 붙여 되살린 결과**다.
>
> **소스 규율.** 여기 실린 인용은 **전부 WebFetch로 원문 페이지를 열어 확인한 것**이다. WebSearch 결과 요약문은 소스로 쓰지 않았다(1건 예외는 §A-4에 명시). 개인 블로그·Medium·Stack Overflow는 버전·플래그·기본값의 근거로 채택하지 않았다 — 1차 리서치 방침 승계.
>
> **⛔ 이 문서가 발견한 가장 중요한 것.** §D에 정리한 **"책을 틀리게 만들 뻔한 사실" 3건**을 Phase 2·Phase 4가 먼저 읽어야 한다. 특히 **ingress-nginx는 2026년 3월 은퇴했고**, **Kubernetes Ingress API는 frozen이며**, **k8s의 `imagePullPolicy` 기본값 규칙은 4갈래**다 — 기존 레퍼런스의 2갈래 서술은 불완전하다.

---

## A. 🔴 1순위 — 이미지 태깅·업데이트 워크플로 (사용자 요구 3번)

### A-1. 태그 vs digest의 본질 (OCI 스펙)

- **상태:** ✅ 확보
- **핵심 사실:** digest는 **내용의 해시**이며 콘텐츠 주소(content addressability)를 만든다. 형식은 `algorithm ":" encoded`이고 실무에서 쓰는 형태가 `sha256:...`이다. 레지스트리에서 매니페스트를 가리키는 `<reference>`는 **태그이거나 digest**, 둘 중 하나다.
- **1차 소스:**
  - OCI Image Spec — Content Descriptors — https://github.com/opencontainers/image-spec/blob/main/descriptor.md (문서버전: `main` 브랜치, 발행일 미확인 — 스펙 문서는 본문에 날짜 미노출. 검색: 2026-07-25)
  - OCI Distribution Spec — https://github.com/opencontainers/distribution-spec/blob/main/spec.md (동일 조건)
- **인용 가능한 원문:**
  > "The digest property of a Descriptor acts as a content identifier, enabling content addressability. It uniquely identifies content by taking a collision-resistant hash of the bytes." — OCI Image Spec, descriptor.md

  > "If the digest can be communicated in a secure manner, one can verify content from an insecure source by recalculating the digest independently, ensuring the content has not been modified." — 동일

  digest 문법(축자):
  ```
  digest                ::= algorithm ":" encoded
  algorithm             ::= algorithm-component (algorithm-separator algorithm-component)*
  algorithm-component   ::= [a-z0-9]+
  algorithm-separator   ::= [+._-]
  encoded               ::= [a-zA-Z0-9=_-]+
  ```
  예시(문서 게재): `sha256:6c3c624b58dbbcd3c0dd82b4c53f04194d1247c6eebdaab7c610cf7d66709b3b`

  > "`<tag-or-digest>` MUST be either (a) the digest of the manifest or (b) a tag." — OCI Distribution Spec

  유효 태그 정규식(축자): `[a-zA-Z0-9_][a-zA-Z0-9._-]{0,127}`
- **주의:**
  - ⛔ **"태그는 가변(mutable)이다"라는 문장을 OCI 스펙 인용으로 달지 마라.** distribution-spec에서 **태그의 가변성을 명시적으로 서술한 문장은 찾지 못했다(NOT_PRESENT)**. 가변성 논거는 (a) 레지스트리가 immutability를 **옵션 기능**으로 판다는 사실(§A-2), (b) 기존 레퍼런스가 이미 확보한 Docker best-practices의 `FROM alpine:3.21` → "resolves to the latest patch version" 문장으로 대야 한다.
  - digest 알고리즘은 스펙상 `sha256` 고정이 아니다(문법이 일반형이고 `blake3:` 예시도 함께 실려 있다). "digest = sha256"으로 단정하지 마라.

### A-2. 태그 불변성(immutable tags) — 레지스트리별

- **상태:** ⚠️ 부분 (AWS ECR ✅ 확보 / GHCR ❌ 부재확정 / Docker Hub 🕒 미확인)
- **핵심 사실:** 태그 불변성은 **OCI 스펙의 성질이 아니라 레지스트리가 켜고 끄는 기능**이다. AWS ECR은 리포지터리 단위 설정으로 제공하며, 켜면 같은 태그 push가 **에러로 거부**된다.
- **1차 소스:** "Preventing image tags from being overwritten in Amazon ECR" — https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html (발행일 미확인 — AWS 문서는 본문에 날짜 미노출. 검색: 2026-07-25)
- **인용 가능한 원문:**
  > "You can prevent image tags from being overwritten by turning on tag immutability in a repository. After tag immutability is turned on, the `ImageTagAlreadyExistsException` error is returned if you push an image with a tag that is already in the repository."

  설정값(축자, 콘솔 기준): **Mutable** — "Choose this option if you want image tags to be overwritten." / **Immutable** — "Choose this option if you want to prevent image tags from being overwritten... Amazon ECR returns an `ImageTagAlreadyExistsException` if you attempt to push an image with an existing tag."

  CLI(축자): `aws ecr create-repository --repository-name {{name}} --image-tag-mutability {{IMMUTABLE}} --region {{us-east-2}}` / 기존 리포 변경은 `aws ecr put-image-tag-mutability`
- **⛔ 주의 — 이 문서에서 갱신된 사실:** ECR은 이제 **전부-아니면-전무가 아니다.** 문서에 `IMMUTABLE_WITH_EXCLUSION`(및 `--image-tag-mutability-exclusion-filters filterType=WILDCARD,filter=...`)이 함께 실려 있다. 그런데 **같은 페이지에 옛 문장도 남아 있다**: "Tag immutability affects all tags. You cannot make some tags immutable while others aren't." → **페이지 내부가 자기모순**이다. 책에 "ECR은 전체 태그에만 적용된다"고 단정하지 마라. 안전한 서술: "리포지터리 단위로 켜며, 예외 필터를 두는 옵션도 문서에 있다(2026-07-25 조회)."
- **GHCR:** ❌ **부재확정(확인한 페이지 기준)** — https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry 를 열어 확인했으나 **태그 불변성·태그 보호·덮어쓰기 방지 언급이 전혀 없다.** ⛔ 표기는 "확인한 페이지에 없음"으로만. "GHCR에는 그 기능이 없다"로 격상 금지 — 다른 문서 페이지에 있을 수 있다.
- **Docker Hub:** 🕒 **미확인** — 이번 회차에서 조회하지 않았다. 책에 Docker Hub 태그 불변성 언급이 필요하면 저술 시점에 별도 확보.

### A-3. semver 기반 태깅 — `docker/metadata-action` (사실상 표준 구현)

- **상태:** ✅ 확보 (이 항목이 "semver 태깅 워크플로" 소절을 되살린 핵심)
- **핵심 사실:** GitHub Actions 공식 액션 `docker/metadata-action`(**v6**/2026 기준)이 git 태그 하나에서 여러 Docker 태그를 파생시키는 규칙을 표로 명문화하고 있다. `{{version}}`·`{{major}}.{{minor}}`·`{{major}}`가 문서의 실제 표기다.
- **1차 소스:** docker/metadata-action README — https://github.com/docker/metadata-action (문서버전: `master` 브랜치 README, 액션 버전 **v6**. 발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문:**
  사용 선언(축자): `uses: docker/metadata-action@v6`

  설정 예시(축자):
  ```yaml
  tags: |
    # minimal
    type=semver,pattern={{version}}
    # use custom value instead of git tag
    type=semver,pattern={{version}},value=v1.0.0
    # use custom value and match part of it
    type=semver,pattern={{version}},value=p1/v1.0.0,match=v(\d.\d.\d)$
  ```

  ⭐ **파생 규칙 표 (축자 — 이 표가 소절의 뼈대다):**

  | Git tag | Pattern | Match | Output |
  |---|---|---|---|
  | `v1.2.3` | `{{raw}}` | | `v1.2.3` |
  | `v1.2.3` | `{{version}}` | | `1.2.3` |
  | `v1.2.3` | `{{major}}.{{minor}}` | | `1.2` |
  | `v1.2.3` | `v{{major}}` | | `v1` |
  | `v1.2.3` | `{{minor}}` | | `2` |
  | `v1.2.3` | `{{patch}}` | | `3` |
  | `p1/v1.2.3` | `{{version}}` | `v(\d.\d.\d)$` | `1.2.3` |
  | `v2.0.8-beta.67` | `{{raw}}` | | `v2.0.8-beta.67` |
  | `v2.0.8-beta.67` | `{{version}}` | | `2.0.8-beta.67` |
  | `v2.0.8-beta.67` | `{{major}}` | | `2.0.8-beta.67`* |
  | `v2.0.8-beta.67` | `{{major}}.{{minor}}` | | `2.0.8-beta.67`* |

  ⭐ **프리릴리스 예외(마지막 두 행의 `*`)가 이 표의 백미다.** `v2.0.8-beta.67`에 `{{major}}` 패턴을 걸어도 `2`가 나오지 않고 원본이 그대로 나온다 — 즉 **베타 태그가 `2`라는 이동 태그를 오염시키지 않는다.** 자바 독자에게 "왜 이 액션을 직접 만든 스크립트보다 쓰는가"를 설명할 구체 논거.

  `type=sha`(축자): "Output Git short commit (or long if specified) as Docker tag like `sha-860c190`."

  `latest` 처리(축자): "`latest` tag is handled through the `flavor` input. It will be generated by default (`auto` mode) for: type=ref,event=tag / type=semver,pattern=... / type=pep440,pattern= / type=match,pattern=..."
- **⛔ 주의 (fact-checker 대비):** 이 README는 **자기 자신(이 액션)에 대한 1차 소스일 뿐, "업계 표준 semver 태깅 규약"의 1차 소스가 아니다.** 책에 "이것이 semver 태깅의 표준이다"라고 쓰면 ❌ 판정 대상이다. 안전한 문장: "GitHub Actions 공식 액션이 채택한 규칙" / "사실상 가장 널리 쓰이는 구현". 규범적 단정 금지.

### A-4. 태그 승격(promotion) — 재빌드 없이 태그 붙이기

- **상태:** ✅ 확보 (crane) / ⚠️ 부분 (buildx imagetools — 재태깅 전용 예제는 부재)
- **핵심 사실:** **재빌드·재업로드 없이 태그만 추가하는 것은 `crane tag`가 가장 명시적**이다. 문서가 "다운로드하지 않고 태그한다"고 직접 말한다. `docker buildx imagetools create -t`도 소스 매니페스트로부터 새 참조를 만들지만, **문서의 자기 규정은 "매니페스트 리스트 생성"**이지 "재태깅"이 아니다.
- **1차 소스:**
  - `crane tag` — https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_tag.md (문서버전: `main`, 발행일 미확인. 검색: 2026-07-25)
  - `crane copy` — https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_copy.md (동일)
  - `docker buildx imagetools create` — https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/ (발행일·버전 마커 **미확인** — 페이지에 없음. 검색: 2026-07-25)
- **인용 가능한 원문:**
  ⭐ `crane tag` 한 줄 규정(축자): **"Tag remote image without downloading it."**

  > "This differs slightly from the 'copy' command in a couple subtle ways: 1. You don't have to specify the entire repository for the tag you're adding... 2. We can skip layer existence checks because we know the manifest already exists. This makes 'tag' slightly faster than 'copy'."

  예제(축자): `crane tag ubuntu v1`

  `crane copy`(축자): **"Efficiently copy a remote image from src to dst while retaining the digest value"** / 옵션 `-n, --no-clobber   (Optional) if true, avoid overwriting existing tags in DST`

  `imagetools create`(축자): 한 줄 규정 **"Create a new manifest list based on source manifests."** / `-t`: **"Use the -t or --tag flag to set the name of the image to be created."** / `--append`: "Use the `--append` flag to append the new sources to an existing manifest list in the destination." / `--dry-run`: "Use the `--dry-run` flag to not push the image, just show it."

  `imagetools create` 예제(축자):
  ```console
  $ docker buildx imagetools create --dry-run alpine@sha256:5c40b3c27b9f13c873fefb2139765c56ce97fd50230f1f2d5c91e55dec171907 sha256:c4ba6347b0e4258ce6a6de2401619316f982b7bcc529f73d2a410d0097730204
  $ docker buildx imagetools create -t tonistiigi/myapp -f image1 -f image2
  ```
  ⭐ **`imagetools create` 도입부 설명 (축자 — 재확인으로 확보. 이게 승격의 근거다):**
  > "The source manifests can be manifest lists or single platform distribution manifests and must already exist in the registry where the new manifest is created."

  > "If only one source is specified and that source is a manifest list or image index, create performs a carbon copy."

  > "If one source is specified and that source is *not* a list or index, the output will be a manifest list, however you can disable this behavior with `--prefer-index=false` which attempts to preserve the source manifest format in the output."
- **⛔ 주의 — 정밀하게 쓸 것:**
  - **1차 조회에서는 "재태깅 전용 예제 없음"으로 판정했으나, 도입부를 재확인해 근거를 확보했다.** 핵심 두 문장: 소스가 **"must already exist in the registry"**(= 로컬 재빌드가 개입하지 않는다)이고, 단일 소스가 리스트/인덱스면 **"carbon copy"**다. → **`docker buildx imagetools create -t new:tag existing:tag`가 승격에 쓸 수 있는 공식 근거는 있다.**
  - 다만 문서의 **자기 규정은 여전히 "Create a new manifest list based on source manifests"**다. "태그만 붙이는 명령"이라고 소개하지 말고, **"레지스트리에 이미 있는 매니페스트로부터 새 참조를 만든다"**로 서술하라. 그게 문서에 정확히 대응한다.
  - **승격 소절의 주인공은 `crane tag`로 잡는 편이 안전하다** — 근거 문장이 "Tag remote image without downloading it." 한 줄로 명확하다. `imagetools create`는 "도커 툴체인만으로 하려면" 대안으로 병기.
  - ⛔ `--prefer-index=false`의 존재는 **단일 매니페스트를 복사하면 기본적으로 매니페스트 리스트로 바뀐다**는 뜻이다. 단일 아키텍처 이미지를 승격할 때 **출력 형식이 바뀔 수 있다** — 이 함정을 빼먹지 말 것.
  - `crane copy`도 "로컬로 안 받는다"는 문장은 **없다**. 확인된 것은 "efficiently"와 "retaining the digest value"뿐. 과장 금지.
  - `crane`의 현재 버전: 🕒 **미확인** (릴리스 페이지 미조회. GitHub Releases 날짜는 §4-8 방침대로 채택하지 않음).

### A-5. Kubernetes 쪽 귀결 — `imagePullPolicy` 기본값 (⭐ 기존 서술 교정)

- **상태:** ✅ 확보 — **그리고 기존 레퍼런스를 교정한다**
- **핵심 사실:** 기본값 규칙은 **2갈래가 아니라 4갈래**다. 기존 레퍼런스(§L-1638, kind 문서 경유)는 "`IfNotPresent`, 단 태그가 `:latest`면 `Always`"만 담고 있어 **두 경우가 빠져 있다** — (a) **digest를 지정하면 `IfNotPresent`**, (b) **태그를 아예 생략하면 `Always`**.
- **1차 소스:** Kubernetes 공식 문서 "Images" — https://kubernetes.io/docs/concepts/containers/images/ (발행일 미확인 — kubernetes.io/docs는 본문에 날짜 미노출. 검색: 2026-07-25)
- **인용 가능한 원문 (축자, 4갈래 전문):**
  > "when you (or a controller) submit a new Pod to the API server, your cluster sets the imagePullPolicy field when specific conditions are met: if you omit the imagePullPolicy field, and you specify the digest for the container image, the imagePullPolicy is automatically set to IfNotPresent. if you omit the imagePullPolicy field, and the tag for the container image is :latest, imagePullPolicy is automatically set to Always. if you omit the imagePullPolicy field, and you don't specify the tag for the container image, imagePullPolicy is automatically set to Always. if you omit the imagePullPolicy field, and you specify a tag for the container image that isn't :latest, the imagePullPolicy is automatically set to IfNotPresent."

  ⭐ `latest` 경고(축자 — 요구 3번 소절의 정확한 근거):
  > "You should avoid using the :latest tag when deploying containers in production as it is harder to track which version of the image is running and more difficult to roll back properly."

  digest 고정 문법(축자):
  > "To make sure the Pod always uses the same version of a container image, you can specify the image's digest; replace `<image-name>:<tag>` with `<image-name>@<digest>` (for example, `image@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`)."
- **⛔ 주의:** 이 4갈래는 **`imagePullPolicy`를 생략했을 때만** 적용되는 자동 설정이다. 명시하면 명시값이 이긴다. 책에서 "쿠버네티스의 기본 pull 정책은 X다"라고 조건 없이 쓰면 부정확하다 — **"필드를 생략하면"**을 반드시 붙여라.
- **Phase 2 활용:** §A-1(digest)·§A-5(digest면 `IfNotPresent`)·§A-3(이동 태그의 위험)이 **한 줄로 이어진다.** "왜 digest로 고정하는가"의 논증 사슬이 전부 1차 소스로 깔렸다.

### A-6. 베이스 이미지 갱신 자동화 — Dependabot / Renovate

- **상태:** ✅ 확보 (도구 존재·설정 문법) / ❌ 여전히 부재 (운영 실태·일화)
- **핵심 사실:** 두 도구 모두 Dockerfile의 베이스 이미지를 **의존성으로 취급해 자동 갱신 PR을 연다.** Dependabot의 생태계 값은 `"docker"`(별도로 `"docker-compose"`도 존재). Renovate는 Dockerfile 매니저를 정규식 파일 매칭으로 굴린다.
- **1차 소스:**
  - GitHub Docs — "Dependabot options reference" — https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference (발행일 미확인. 검색: 2026-07-25)
  - Renovate Docs — "dockerfile" manager — https://docs.renovatebot.com/modules/manager/dockerfile/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문:**
  Dependabot 최소 설정(축자):
  ```yaml
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
  ```
  문서 주석(축자): "Look for a `Dockerfile` in the `root` directory" / "Check for updates once a week."

  Renovate(축자): "Renovate supports updating Dockerfile dependencies."
  > "By default, Renovate will check any files matching any of the following regular expressions: `/(^|/|\.)([Dd]ocker|[Cc]ontainer)file$/ /(^|/)([Dd]ocker|[Cc]ontainer)file[^/]*$/`"
- **주의:**
  - ⛔ **"재빌드 트리거 방법"은 확인하지 못했다(🕒 미확인).** 두 문서 모두 **PR을 여는 것까지**가 서술 범위다. "Dependabot이 재빌드를 트리거한다"고 쓰지 마라 — 재빌드는 그 PR에 붙은 CI가 하는 것이고, 그 연결을 서술한 1차 문장은 확보하지 못했다.
  - ⛔ Renovate의 `pinDigests`(digest 고정) 서술은 **이 페이지에 없다(NOT_PRESENT).** digest 자동 고정을 책에 쓰려면 별도 페이지 확보 필요.
  - ❌ **"실무에서 실제로 어떤 주기로 굴리는가"(§7-3 공백 2번)는 여전히 0건이다.** 이 절로 채워지는 것은 **도구의 존재와 설정 문법**뿐이다. 운영 실태·일화는 커뮤니티 리서치 영역이고 이번 회차 범위 밖.

### A-7. `docker history` / `dive` — 레이어 뜯어보기

- **상태:** ✅ 확보 (둘 다)
- **1차 소스:**
  - `docker image history` CLI 레퍼런스 — https://docs.docker.com/reference/cli/docker/image/history/ (발행일·버전 마커 미확인. 검색: 2026-07-25)
  - dive README — https://github.com/wagoodman/dive (문서버전: `main` 브랜치 README. 검색: 2026-07-25)
- **인용 가능한 원문:**
  `docker history` 한 줄 규정(축자): **"Show the history of an image"**

  옵션 표(축자):

  | Option | Default | Description |
  |---|---|---|
  | `--format` | | Format output using a custom template: 'table', 'json', or Go template |
  | `-H`, `--human` | `true` | Print sizes and dates in human readable format |
  | `--no-trunc` | | Don't truncate output |
  | `--platform` | | Show history for the given platform (e.g., `linux/amd64`) |
  | `-q`, `--quiet` | | Only show image IDs |

  출력 컬럼(축자, 문서 예제 헤더): `IMAGE   CREATED   CREATED BY   SIZE   COMMENT`

  ⭐ `--platform` 옵션의 존재가 이 책에 특히 유용하다 — 멀티아키 이미지의 레이어를 아키텍처별로 뜯어볼 수 있다는 뜻. (단, 문서는 옵션 존재만 말한다. 멀티아키 활용법 서술은 없음 — 확대 해석 금지.)

  dive(축자): **"A tool for exploring a Docker image, layer contents, and discovering ways to shrink the size of your Docker/OCI image."**
  - 사용(축자): `dive <your-image-tag>` / `dive build -t <some-tag> .`
  - 맥 설치(축자): `brew install dive`
  - CI 모드(축자): "Analyze an image and get a pass/fail result based on the image efficiency and wasted space. Simply set CI=true in the environment when invoking any valid dive command."
- **주의:**
  - dive **현재 버전: 🕒 미확인** — README 설치 안내에 버전 번호가 인쇄돼 있지 않다(NOT_PRESENT). §4-8 방침대로 GitHub Releases에서 날짜/버전을 끌어오지 않았다. 책에 dive 버전 숫자를 쓰지 마라.
  - dive README는 **자기 도구에 대한 1차 소스**다. "레이어 분석의 표준 도구"류의 규범적 표현 금지(§A-3과 같은 이유).
  - `docker history` 문서의 예제 출력은 **오래된 형식**(9 months ago / `511136ea3c5a` 등 옛 이미지 ID)이다. 그대로 옮기면 낡아 보인다 — 컬럼 이름만 인용하고 값은 독자가 직접 실행한 결과로 대체할 것을 권장.

---

## B. 🔴 2순위 — 맥에서 로컬 K8s 실습 (사용자 요구 4번)

### B-0. ⛔⛔ 이 절을 쓰기 전에 반드시 읽을 것 — Ingress 지형이 바뀌었다

**세 가지가 동시에 일어났고, 셋 다 이 책의 발행 시점(2026-07) 이전이다.**

1. **ingress-nginx 은퇴** — 2026년 3월. 보안 패치도 끊겼다.
2. **Kubernetes Ingress API 자체가 frozen** — 공식 문서가 Gateway API를 권한다.
3. **kind의 Ingress 가이드가 통째로 바뀌었다** — 예전의 `extraPortMappings` + `node-labels` + ingress-nginx 매니페스트 레시피가 **더 이상 문서에 없다.** 지금은 `cloud-provider-kind`가 네이티브로 처리한다.

→ **옛 튜토리얼(그리고 LLM의 기억)을 그대로 옮기면 이 책은 발행 즉시 틀린 책이 된다.** 상세는 §B-1~B-3.

### B-1. ⭐⭐ ingress-nginx 은퇴 — 2026년 3월

- **상태:** ✅ 확보 (공식 블로그 2건 + 저장소 README)
- **핵심 사실:** Kubernetes 프로젝트가 ingress-nginx를 **2026년 3월에 은퇴**시켰다. 이후 릴리스·버그픽스·**보안 패치 없음**. 공식 권고는 Gateway API 또는 다른 서드파티 Ingress 컨트롤러로의 이주다.
- **1차 소스:**
  - "Ingress NGINX Retirement: What You Need to Know" — https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/ (**발행일: 2025-11-11**, 저자: Tabitha Sable (Kubernetes SRC). 검색: 2026-07-25)
  - "Ingress NGINX: Statement from the Kubernetes Steering and Security Response Committees" — https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/ (**발행일: 2026-01-29**, 저자: Kat Cosgrove (Steering Committee). 검색: 2026-07-25)
  - kubernetes/ingress-nginx README — https://github.com/kubernetes/ingress-nginx (검색: 2026-07-25)
- **인용 가능한 원문:**
  > "Best-effort maintenance will continue until March 2026. Afterward, there will be no further releases, no bugfixes, and no updates to resolve any security vulnerabilities that may be discovered." — 블로그(2025-11-11) 및 README

  ⭐ 가장 강한 문장(축자, 2026-01-29 성명):
  > "To be abundantly clear: choosing to remain with Ingress NGINX after its retirement leaves you and your users vulnerable to attack."

  > "Existing deployments will continue to work, so unless you proactively check, you may not know you are affected until you are compromised." — 동일

  > "With the technical debt that has piled up, and fundamental design decisions that exacerbate security flaws, it is no longer reasonable or even possible to continue maintaining the tool even if resources did materialize." — 동일

  README의 지침(축자):
  > "If you are not already using ingress-nginx, you should not be deploying it as it is not being developed. Instead you should identify a Gateway API implementation and use it."

  이주 권고(축자, 2025-11-11):
  > "We recommend migrating to one of the many alternatives. Consider migrating to Gateway API, the modern replacement for Ingress. If you must continue using Ingress, many alternative Ingress controllers are listed in the Kubernetes documentation."
- **주의:**
  - **정확한 은퇴일:** 공식 문서 3곳이 일관되게 말하는 것은 **"March 2026"**이다. WebSearch 요약문에는 "retired on March 24, 2026"이라는 **일(日) 단위 날짜**가 나왔으나 **내가 연 페이지 어디에서도 그 날짜를 축자로 확인하지 못했다.** ⛔ **책에 "3월 24일"을 쓰지 마라. "2026년 3월"까지만 쓸 것.**
  - 마찬가지로 WebSearch 요약문의 **"약 50% (Datadog 조사)"** 수치도 축자 확인 실패다. 내가 연 2025-11-11 블로그는 수치 없이 **"Ingress NGINX has continued to be one of the most popular, deployed as part of many hosted Kubernetes platforms and within innumerable independent users' clusters."**라고만 말한다. ⛔ **50% 수치 인용 금지.**
  - 참고: 이 은퇴의 배경에는 기존 레퍼런스에 없는 CVE 사건도 있다 — https://kubernetes.io/blog/2025/03/24/ingress-nginx-cve-2025-1974/ (**제목·URL만 확인, 본문 미열람 — 인용하려면 별도 확보**).

### B-2. ⭐ Ingress API는 frozen이다 — Gateway API가 후계

- **상태:** ✅ 확보
- **핵심 사실:** Kubernetes 공식 Ingress 문서 스스로가 **Gateway를 쓰라고 권하고, Ingress API가 frozen이라고 명시**한다. 단 **제거 계획은 없다**(GA 안정성 보장 유지).
- **1차 소스:** Kubernetes — "Ingress" — https://kubernetes.io/docs/concepts/services-networking/ingress/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  > "The Kubernetes project recommends using Gateway instead of Ingress. The Ingress API has been frozen."

  > "The Ingress API is generally available, and is subject to the stability guarantees for generally available APIs. The Kubernetes project has no plans to remove Ingress from Kubernetes."

  > "The Ingress API is no longer being developed, and will have no further changes or updates made to it."

  정의(축자): "Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. Traffic routing is controlled by rules defined on the Ingress resource."

  ⭐ 컨트롤러 필요성(축자 — 실습 함정의 근거):
  > "Only creating an Ingress resource has no effect. You must have an Ingress controller to satisfy an Ingress."

  ⭐ **최소 Ingress 리소스 (축자, `networking.k8s.io/v1`):**
  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: minimal-ingress
  spec:
    ingressClassName: nginx-example
    rules:
    - http:
        paths:
        - path: /testpath
          pathType: Prefix
          backend:
            service:
              name: test
              port:
                number: 80
  ```
- **주의:** "frozen"과 "deprecated"는 다르다. **Ingress는 deprecated가 아니고 제거 예정도 없다.** 책에서 "Ingress는 곧 없어진다"고 쓰면 ❌ — 공식 문서가 정반대를 말한다. 정확한 서술: "더 이상 발전하지 않는다(frozen). 새로 짓는다면 Gateway API를 권한다. 다만 기존 Ingress가 사라지지는 않는다."
- **이주 도구:** "Announcing Ingress2Gateway 1.0" — https://kubernetes.io/blog/2026/03/20/ingress2gateway-1-0-release/ (**발행일: 2026-03-20**. 검색: 2026-07-25). 축자: ingress2gateway는 "translates Ingress resources/manifests along with implementation-specific annotations to Gateway API while warning you about untranslatable configuration and offering suggestions." (⚠️ 변환 **명령어 예제는 페이지 절단으로 확보 실패 — 🕒 미확인.** 명령을 쓰려면 별도 확보)

### B-3. ⭐ kind의 Ingress 가이드가 바뀌었다 — `extraPortMappings` 레시피는 문서에 없다

- **상태:** ⚠️ 부분 확보 + ❌ 옛 레시피 부재확정
- **핵심 사실:** kind 공식 Ingress 문서는 이제 **`cloud-provider-kind` v0.9.0+ 기준**으로 다시 쓰였다. **third-party ingress controller가 기본적으로 필요 없다**고 말하며, 널리 퍼진 `extraPortMappings` + `node-labels` + ingress-nginx 매니페스트 레시피는 **현재 페이지에 없다.**
- **1차 소스:** kind — "Ingress" — https://kind.sigs.k8s.io/docs/user/ingress/ (렌더링 페이지 + 저장소 소스 https://github.com/kubernetes-sigs/kind/blob/main/site/content/docs/user/ingress.md 양쪽 조회. 발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  > "Since cloud-provider-kind v0.9.0, it natively supports Ingress. No third-party ingress controllers are required by default."

  > "This guide applies to cloud-provider-kind v0.9.0+. For older versions, refer to historical docs."

  > "Gateway API is also natively supported (along with Ingress)."

  경고(축자): "If you are using a rootless container runtime, ensure your host is properly configured before creating the KIND cluster."

  확인 흐름(축자):
  ```bash
  kubectl get ingress
  INGRESS_IP=$(kubectl get ingress example-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  curl ${INGRESS_IP}/foo
  curl ${INGRESS_IP}/bar
  ```
  예제 적용: `kubectl apply -f` + kind 사이트의 `examples/ingress/usage.yaml`
- **⛔ 주의 (매우 중요):**
  - **`extraPortMappings`/`node-labels` 클러스터 config YAML은 현재 이 페이지에 없다(❌ 확인한 페이지 기준 부재).** "kind에서 Ingress 쓰려면 `extraPortMappings`를 열어야 한다"는 널리 퍼진 서술을 **kind 공식 문서 근거로 달지 마라.** 문서가 "historical docs"를 따로 가리키고 있다 = 그 레시피는 구버전용으로 격하됐다.
  - `usage.yaml`의 실제 내용은 미확보(사이트 템플릿 변수로만 노출). 예제 YAML을 본문에 실으려면 §B-2의 공식 최소 Ingress를 쓰는 편이 안전하다.

### B-3b. ⭐⭐⭐ `cloud-provider-kind` — 맥에서는 kind 문서대로 하면 안 된다

> **이번 회차 최대 수확 중 하나.** §B-3의 kind 문서가 보여주는 확인 흐름(`INGRESS_IP=$(kubectl get ingress ... )` → `curl ${INGRESS_IP}/foo`)은 **맥에서 그대로 되지 않는다.** 그 이유를 후속 컴포넌트의 README가 직접 말한다. 이 책의 존재 이유("맥에서는 왜 다른가")에 정확히 꽂히는 재료다.

- **상태:** ✅ 확보
- **1차 소스:** cloud-provider-kind README — https://github.com/kubernetes-sigs/cloud-provider-kind (문서버전: `main` 브랜치 README. 발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  존재 이유:
  > "KIND has demonstrated to be a very versatile, efficient, cheap and very useful tool for Kubernetes testing. However, KIND doesn't offer capabilities for testing all the features that depend on cloud-providers, specifically the Load Balancers, causing a gap on testing and a bad user experience, since is not easy to connect to the applications running on the cluster."

  ⭐⭐ **맥의 벽 (이 책의 핵심 문장 후보):**
  > "Mac and Windows run the containers inside a VM and, on the contrary to Linux, the KIND nodes are not reachable from the host, so the LoadBalancer assigned IP is not working for users."

  우회:
  > "cloud-provider-kind, leverages the existing docker portmap capabilities to expose the Loadbalancer IP and Ports on the host."

  > `--enable-lb-port-mapping` — "This configures the Envoy container with an ephemeral host port that maps to the port the `LoadBalancer`'s external IP is listening on." → "Use this ephemeral port to connect to the service" (`curl localhost:[port]`)

  ⭐ 권한:
  > "On macOS and WSL2 you must run cloud-provider-kind using `sudo`"

  설치(축자):
  ```sh
  brew install cloud-provider-kind
  ```
  ```sh
  go install sigs.k8s.io/cloud-provider-kind@latest
  sudo install ~/go/bin/cloud-provider-kind /usr/local/bin
  ```
  실행(축자): `bin/cloud-provider-kind`

  제약(축자):
  > "Mutation of Services, adding or removing ports to an existing Services, is not supported"

  > "Overlapping IP between the containers and the host can break connectivity."
- **⭐ Phase 2 활용 (강력):** 이건 **기존 레퍼런스 §1-3("왜 맥에서는 리눅스 VM이 끼는가")의 귀결이 실습 층위에서 그대로 재현되는 사례**다. 같은 원인(맥의 컨테이너는 VM 안에 있다)이 파일 공유·네트워크·그리고 이제 **LoadBalancer IP 도달 불가**까지 낳는다. 챕터를 관통하는 반복 모티프로 쓸 수 있다.
- **주의:** cloud-provider-kind 버전: 🕒 미확인. `sudo`가 필요하다는 사실은 맥 독자에게 **마찰 지점**으로 정직하게 알릴 것.

### B-4. 최소 시스템 요구사항 — 도구별 (⭐ "수치 0건" 항목이 절반 살아났다)

- **상태:** ✅ 확보 (minikube, k3s, Colima) / ❌ 부재확정 (kind)

| 도구 | 최소 사양 (공식) | 소스 | 비고 |
|---|---|---|---|
| **minikube** | **2 CPUs or more / 2GB of free memory / 20GB of free disk space** + 인터넷 + 컨테이너·VM 매니저 | minikube "Get Started!" | 축자 확보 |
| **k3s** | **Server: 2 cores / 2 GB RAM**, **Agent: 1 core / 512 MB RAM** | k3s Requirements | ⛔ 리눅스 기준 |
| **Colima** | (최소값 아님) **기본 VM = 2 CPUs / 2GiB memory / 100GiB storage** | Colima README | 최소가 아니라 **기본값** |
| **kind** | ❌ **확인한 페이지에 명시 없음** | kind quick-start | 부재확정 |

- **1차 소스:**
  - minikube — https://minikube.sigs.k8s.io/docs/start/ (발행일 미확인. 검색: 2026-07-25)
  - k3s — https://docs.k3s.io/installation/requirements (발행일 미확인. 검색: 2026-07-25)
  - Colima README — https://github.com/abiosoft/colima (검색: 2026-07-25)
  - kind — https://kind.sigs.k8s.io/docs/user/quick-start/ (검색: 2026-07-25) → **최소 CPU/메모리/디스크 수치 없음**
- **인용 가능한 원문:**
  minikube "What you'll need"(축자 전문): "2 CPUs or more" / "2GB of free memory" / "20GB of free disk space" / "Internet connection" / "Container or virtual machine manager, such as: Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation"

  k3s 하드웨어 요구사항(축자 표):

  | Node | CPU | RAM |
  |---|---|---|
  | Server | 2 cores | 2 GB |
  | Agent | 1 core | 512 MB |

  k3s 아키텍처(축자): x86_64 / armhf / **arm64/aarch64** 제공. **macOS 지원 언급 없음.** OS: "K3s is expected to work on most modern Linux systems."

  Colima(축자): **"The default VM created by Colima has 2 CPUs, 2GiB memory and 100GiB storage."**
- **⛔ 주의 (이 표를 쓸 때 반드시 병기):**
  - **성질이 다른 세 수치를 한 표에 나란히 놓지 마라.** minikube는 *최소 요구사항*, k3s는 *리눅스 노드 하드웨어 요구사항*, Colima는 *기본 할당값*이다. 열 제목을 "최소 사양"으로 통일하면 부정확하다.
  - **k3s 수치는 리눅스 노드 기준이고, 맥에서는 그 위에 VM 오버헤드가 얹힌다.** k3s 문서는 macOS를 지원 OS로 언급조차 하지 않는다. "맥에서 k3s가 2코어 2GB면 된다"로 옮기면 ❌.
  - **kind는 부재확정이다** — 표기는 "확인한 페이지(quick-start)에 명시 없음"으로. "kind는 요구사항이 없다/가볍다"로 격상 금지.
  - ❌ **실제 소모량(배터리·메모리) 측정 비교는 여전히 0건이다.** 이 표는 *공표된 요구사항* 비교이지 *실측 비교*가 아니다. §7-3 공백 4번은 살아나지 않았다.

### B-5. kind — 현재 버전과 기본 명령

- **상태:** ✅ 확보
- **1차 소스:** kind "Quick Start" — https://kind.sigs.k8s.io/docs/user/quick-start/ (발행일 미확인. 검색: 2026-07-25)
- **핵심 사실:** **kind v0.32.0 / 2026 기준** (설치 섹션에 인쇄된 값).
- **인용 가능한 원문 (축자):**
  ```bash
  kind create cluster
  kind create cluster --name kind-2
  kind delete cluster
  kind load docker-image my-app:latest
  kind load docker-image my-app:latest my-db:latest my-cache:latest
  kind load docker-image my-app:latest --name test-cluster
  ```
  멀티노드 config(축자):
  ```yaml
  # three node (two workers) cluster config
  kind: Cluster
  apiVersion: kind.x-k8s.io/v1alpha4
  nodes:
  - role: control-plane
  - role: worker
  - role: worker
  ```
- **주의:** 노드 이미지 버전은 **버전 고정값이 없다** — 문서는 "prebuilt images are hosted at `kindest/node`"라며 "check the release notes for your given kind version"으로 넘긴다. **책에 특정 k8s 노드 이미지 태그를 박지 마라.** (기존 레퍼런스의 `kind load` 명령과 일치 — 중복이지만 v0.32.0이라는 **버전 확정**이 새로 추가된 값이다.)

### B-6. minikube — 맥에서의 노출 경로 (`service` / `tunnel`)

- **상태:** ✅ 확보
- **1차 소스:** minikube — "Accessing apps" — https://minikube.sigs.k8s.io/docs/handbook/accessing/ (발행일 미확인. 검색: 2026-07-25) / 설치는 https://minikube.sigs.k8s.io/docs/start/
- **인용 가능한 원문 (축자):**
  > "Services of type `NodePort` can be exposed via the `minikube service <service-name> --url` command."

  ⭐ LoadBalancer 함정(축자 — 로컬 실습의 가장 흔한 막힘):
  > "Note that without minikube tunnel, Kubernetes will show the external IP as 'pending'."

  > "`minikube tunnel` runs as a process, creating a network route on the host to the service CIDR of the cluster using the cluster's IP address as a gateway."

  > "It must be run in a separate terminal window to keep the `LoadBalancer` running." / "It will ask for a password"

  맥 arm64 설치(축자):
  ```
  brew install minikube
  ```
  ```
  curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-darwin-arm64
  sudo install minikube-darwin-arm64 /usr/local/bin/minikube
  ```
- **주의:**
  - minikube **현재 버전: 🕒 미확인** — 설치 문서에 버전 번호가 인쇄돼 있지 않다(`latest/download` URL만). 실측값 `v1.35.0`(env_probe §3)은 **이 맥의 관측값**이지 최신 버전이 아니다. 병기 규칙 준수.
  - ⛔⛔ **`minikube addons enable ingress`는 은퇴한 ingress-nginx를 설치한다 — 확인 완료.** minikube 공식 튜토리얼 축자:
    > "The minikube ingress addon enables developers to route traffic from their host (Laptop, Desktop, etc) to a Kubernetes service running inside their minikube cluster. **The ingress addon uses the ingress nginx controller** which by default is only configured to listen on ports 80 and 443."

    — https://minikube.sigs.k8s.io/docs/tutorials/nginx_tcp_udp_ingress/ (발행일 미확인. 검색: 2026-07-25)

    → **§B-1(2026년 3월 은퇴)과 정면으로 만난다.** 이 책이 `minikube addons enable ingress`를 아무 말 없이 실습으로 실으면, 독자에게 **보안 패치가 끊긴 컨트롤러를 깔라고 시키는 것**이 된다. **반드시 그 사실을 병기하거나, 실습 경로를 kind + cloud-provider-kind(§B-3b)로 잡아라.** 이것이 이번 리서치가 막아낸 가장 실질적인 사고다.
    - ⚠️ 단, minikube 문서가 addon을 **철회했거나 대체 컨트롤러로 갈아탔는지는 확인하지 않았다(🕒)**. "minikube가 은퇴한 걸 아직도 깐다"고 단정하기 전에 저술 시점에 addons 목록을 재확인할 것. 확인된 것은 위 튜토리얼 페이지의 문장뿐이다.
  - 드라이버 옵션(docker/qemu/vfkit 등)의 맥 관련 상세: 🕒 **미확인** — start 문서의 "Container or virtual machine manager" 목록(위 §B-4 축자)까지만 확보. `vfkit`은 그 목록에 **없다**. "맥에서 vfkit 드라이버를 쓴다"고 쓰지 마라.

### B-7. Colima — `--kubernetes` 경로

- **상태:** ⚠️ 부분 (플래그 ✅ / **k3s라는 근거 ❌**)
- **1차 소스:** Colima README — https://github.com/abiosoft/colima (검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  > "To enable Kubernetes, start Colima with `--kubernetes` flag."

  > "The default VM created by Colima has 2 CPUs, 2GiB memory and 100GiB storage."

  > "The VM can be customized either by passing additional flags to `colima start`. e.g. `--cpu`, `--memory`, `--disk`, `--runtime`. Or by editing the config file with `colima start --edit`."

  Rosetta(축자): "create VM with Rosetta 2 emulation. Requires v0.5.3 and macOS >= 13 (Ventura) on Apple Silicon."

  플랫폼(축자): "Support for Intel and Apple Silicon macOS, and Linux"
- **⛔ 주의 — 지목받은 가설이 확인되지 않았다:**
  - **"Colima의 쿠버네티스는 k3s 기반"이라는 서술을 README에서 확인하지 못했다.** 문서는 어떤 배포판을 쓰는지 **명시하지 않는다(NOT_PRESENT).** → **"Colima는 k3s를 쓴다"고 책에 쓰지 마라.** 안전한 서술: "`colima start --kubernetes`로 쿠버네티스를 켤 수 있다(어떤 배포판인지는 README에 명시돼 있지 않다)."
  - `--arch` 플래그는 README에서 확인되지 않았다(NOT_PRESENT). Rosetta 관련 서술만 존재.
  - 기존 레퍼런스 §2-4의 경고 승계: **Colima 최신 릴리스가 2025-06-04로 1년 이상 정체**돼 있다. "활발히 개발 중" 금지.
  - → **결론: "k3s(Colima)로 로컬 K8s 돌리기" 소절은 *Colima 경로*로는 쓸 수 있으나 *k3s 경로*로는 쓸 수 없다.** 소절 제목에서 "k3s"를 빼라.

### B-8. Service 타입과 로컬 노출 — `port-forward`

- **상태:** ⚠️ 부분 (`port-forward` ✅ / NodePort·LoadBalancer 정의 🕒 미확인)
- **1차 소스:** `kubectl port-forward` — https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  Synopsis: `kubectl port-forward TYPE/NAME [options] [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N]`

  > "Forward one or more local ports to a pod."

  ⭐ 실습 함정(축자):
  > "If there are multiple pods matching the criteria, a pod will be selected automatically. The forwarding session ends when the selected pod terminates, and a rerun of the command is needed to resume forwarding."

  예제(축자, 발췌):
  ```bash
  kubectl port-forward pod/mypod 5000 6000
  kubectl port-forward deployment/mydeployment 5000 6000
  kubectl port-forward service/myservice 8443:https
  kubectl port-forward pod/mypod 8888:5000
  kubectl port-forward --address 0.0.0.0 pod/mypod 8888:5000
  kubectl port-forward pod/mypod :5000
  ```
- **⛔ 주의 — 확보 실패 항목:**
  - **NodePort의 기본 포트 범위(30000–32767)와 LoadBalancer의 "클라우드 없으면 pending" 공식 서술은 확보하지 못했다.** Service 개념 페이지가 **길어서 WebFetch가 해당 섹션 전에 절단**됐고(TRUNCATED), 대체로 시도한 두 페이지(`connect-applications-service`, `virtual-ips`)에서도 NOT_PRESENT였다. → **🕒 미확인. 30000–32767이라는 숫자를 책에 쓰지 마라** (널리 알려진 값이지만 이번에 축자 확인 실패).
  - **다만 "LoadBalancer가 로컬에서 pending에 머문다"는 사실 자체는 §B-6의 minikube 문서 축자로 커버된다.** 그쪽 근거를 쓰면 된다 — 그게 오히려 "맥에서 실습" 맥락에 더 정확하다.
  - 프로토콜(TCP/UDP) 서술: NOT_PRESENT.

---

## C. 🟡 3순위

### C-1. BuildKit 빌드 시크릿 — `RUN --mount=type=secret`

- **상태:** ✅ 확보 (§7-2의 "예시 0건" 해소)
- **1차 소스:** Docker Docs — "Build secrets" — https://docs.docker.com/build/building/secrets/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  ⭐ 존재 이유(축자 — 소절 오프닝용):
  > "Build arguments and environment variables are inappropriate for passing secrets to your build, because they persist in the final image."

  > 대신 "secret mounts or SSH mounts, which expose secrets to your builds securely."

  Dockerfile(축자):
  ```dockerfile
  RUN --mount=type=secret,id=aws \
      AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
      aws s3 cp ...
  ```
  빌드 명령(축자):
  ```console
  $ docker build --secret id=aws,src=$HOME/.aws/credentials .
  $ docker build --secret id=kube,env=KUBECONFIG .
  $ docker build --secret id=API_TOKEN .
  ```
  기본 경로(축자): **"The default file path of the secret, inside the build container, is `/run/secrets/<id>`."**
- **주의:** 자바 독자 맥락에서 유용한 대비 — `ARG`/`ENV`로 넘긴 값은 `docker history`(§A-7)로 그대로 보인다는 점과 짝지으면 두 절이 서로를 보강한다. (단, **"`docker history`로 `ARG` 값이 보인다"는 축자 문장은 확보하지 않았다** — 위 "persist in the final image" 문장까지만 근거로 쓸 것.)

### C-2. SBOM·프로비넌스 생성 (BuildKit attestations)

- **상태:** ✅ 확보 (§7-2의 "SBOM **생성** 실습 공식 문서 0건" 해소)
- **1차 소스:** Docker Docs — "Build attestations" — https://docs.docker.com/build/metadata/attestations/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  > "Build attestations describe how an image was built, and what it contains."

  두 종류(축자): "Software Bill of Material (SBOM): list of software artifacts that an image contains, or that were used to build the image" / "Provenance: how an image was built."

  ```bash
  docker buildx build --sbom=true .
  docker buildx build --provenance=mode=max .
  docker buildx build --provenance=false .
  ```
  ⭐ 기본 동작(축자): **"Provenance attestations with the `mode=min` level are added to images by default."** — 끄려면 `BUILDX_NO_DEFAULT_ATTESTATIONS` 환경변수.
- **주의:** "기본으로 붙는다"는 서술에 **빌더·출력 종류별 조건이 붙는지는 확인하지 못했다(🕒 미확인).** 무조건적 기본값으로 단정하지 마라. `docker scout sbom`(§8-4)과는 **다른 층위**다 — 이쪽은 *생성/첨부*, 저쪽은 *조회*. 혼동해 쓰지 말 것.

### C-3. 이미지 서명 — cosign

- **상태:** ⚠️ 부분 (sign ✅ / verify ❌ 미확보)
- **1차 소스:** Sigstore Docs — "Signing with containers" — https://docs.sigstore.dev/cosign/signing/signing_with_containers/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  ```
  $ cosign sign $IMAGE
  $ cosign sign --key cosign.key $IMAGE
  $ cosign sign -a foo=bar -a baz=bat $IMAGE
  ```
- **⛔ 주의:**
  - **`cosign verify` 예제와 `--certificate-identity`/`--certificate-oidc-issuer` 플래그는 이 페이지에 없다(NOT_PRESENT).** 검증 명령을 책에 쓰려면 `/cosign/verifying/verify/` 페이지를 저술 시점에 별도 확보. **지금 상태로 검증 명령을 쓰면 ❌.**
  - "서명은 태그가 아니라 digest를 가리켜야 한다"는 서술도 **이 페이지에 없다(NOT_PRESENT).** §A-1·§A-5의 digest 논거로 저자가 잇는 것은 가능하지만, **cosign 문서의 권고로 인용하지 마라.**
  - cosign 버전: 🕒 미확인.

### C-4. rootless 모드

- **상태:** ⚠️ 부분 — **맥에서 쓸 근거가 약하다**
- **1차 소스:** Docker Docs — "Rootless mode" — https://docs.docker.com/engine/security/rootless/ (발행일 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  > "Rootless mode lets you run the Docker daemon and containers as a non-root user to mitigate potential vulnerabilities in the daemon and the container runtime."
- **⛔ 주의 — 판단 근거:**
  - **"Known limitations" 목록을 확보하지 못했다(문서 내 해당 섹션 미획득).** 제약사항을 책에 나열하지 마라.
  - **macOS는 이 페이지에서 전혀 언급되지 않는다.** 맥 독자에게 rootless를 실습으로 권할 1차 근거가 없다.
  - → **판정: 이 책에서 rootless는 소절로 세우지 말 것.** 쓰더라도 "리눅스 데몬 이야기이고, 맥은 이미 VM 안에서 돌기 때문에 맥락이 다르다"는 **한두 문장 각주**로 제한하라. (단, "맥은 VM이라 rootless가 불필요하다"는 **주장 자체의 1차 근거는 없다** — 저자 해석임을 명시할 것.)
  - 부수 확보: kind 문서가 rootless 런타임 사용자에게 별도 경고를 단다(§B-3 축자) — 맥 독자보다는 리눅스 독자용이지만, "rootless는 실습에 마찰을 준다"는 방증으로 쓸 수 있다.

### C-5. overlayfs — 컨테이너 레이어의 실체

- **상태:** ✅ 확보 (§7-1 G영역 "overlayfs 전용 문서 미열람" 해소)
- **1차 소스:** Linux Kernel Documentation — "Overlay Filesystem" — https://docs.kernel.org/filesystems/overlayfs.html (커널 공식 문서. 발행일/커널 버전 마커 미확인. 검색: 2026-07-25)
- **인용 가능한 원문 (축자):**
  > "An overlay-filesystem tries to present a filesystem which is the result of overlaying one filesystem on top of the other."

  > "At mount time, the two directories given as mount options 'lowerdir' and 'upperdir' are combined into a merged directory" — workdir은 "needs to be an empty directory on the same filesystem as upperdir."

  ```
  mount -t overlay overlay -olowerdir=/lower,upperdir=/upper,workdir=/work /merged
  ```
  ⭐ copy-up(축자 — 레이어 이해의 핵심):
  > "When a file in the lower filesystem is accessed in a way that requires write-access, such as opening for write access, changing some metadata etc., the file is first copied from the lower filesystem to the upper filesystem (copy_up)."
- **주의:** 이 문서는 **리눅스 커널의 overlayfs**를 설명한다. **"Docker의 이미지 레이어가 정확히 이 overlayfs로 구현된다"는 연결은 이 문서가 하지 않는다** — Docker의 스토리지 드라이버(`overlay2`)와의 대응은 별도 근거가 필요하다(🕒 미확인). 개념적 대응("레이어를 겹쳐 하나로 보이게 하는 커널 기능이 이것이다")까지만 쓰고, 구현 동일시는 피하라.
  - ⭐ **이 절은 기존 레퍼런스 §5-7의 논문 수치(OverlayFS vs 볼륨 쓰기, macOS 1.06×)와 짝을 이룬다.** copy_up 개념이 "왜 쓰기가 비싼가"를 설명해 준다 — 다만 **논문 수치와 이 커널 문서를 인과로 잇는 것은 저자 해석**이다. 명시할 것.

---

## D. ⛔⛔ 책을 틀리게 만들 뻔한 사실 — Phase 2·Phase 4 필독

| # | 위험 | 실제 (1차 소스 확인) | 영향 |
|---|---|---|---|
| **1** | "맥 로컬 K8s에서 Ingress 실습 = ingress-nginx 설치" (거의 모든 기존 튜토리얼·LLM 기본 응답) | **ingress-nginx는 2026년 3월 은퇴.** 보안 패치 없음. 공식 성명: "choosing to remain with Ingress NGINX after its retirement leaves you and your users vulnerable to attack" | 이 책 발행(2026-07) 시점에 **이미 4개월 지난 사실.** 실습 절을 ingress-nginx로 쓰면 독자에게 취약한 구성을 가르치는 셈 |
| **2** | "Ingress는 쿠버네티스 외부 노출의 표준" | **Ingress API는 frozen.** 공식 문서가 "The Kubernetes project recommends using Gateway instead of Ingress"라고 직접 말함. 단 **제거 계획은 없음** | 표현을 "지금도 유효하지만 더 이상 발전하지 않는 API"로 정확히. 반대로 "곧 없어진다"도 ❌ |
| **3** | "K8s pull 정책 기본값 = `IfNotPresent`, 단 `:latest`면 `Always`" (기존 §L-1638, kind 문서 경유) | **4갈래다.** digest 지정 → `IfNotPresent` / `:latest` → `Always` / **태그 생략 → `Always`** / `:latest` 아닌 태그 → `IfNotPresent`. 그리고 **`imagePullPolicy`를 생략했을 때만** 적용 | 2갈래로 쓰면 불완전. 특히 "태그 생략 시 `Always`"가 빠져 있었다 |
| **4** | `minikube addons enable ingress`를 맥 실습으로 그대로 싣기 | minikube 공식 문서 축자: **"The ingress addon uses the ingress nginx controller"** — 즉 **#1에서 은퇴한 그 컨트롤러**다(§B-6) | 아무 말 없이 실으면 **독자에게 보안 패치가 끊긴 컴포넌트를 설치시키는 것**. 이번 리서치가 막아낸 가장 실질적인 사고 |
| **5** | kind 공식 Ingress 가이드의 `curl ${INGRESS_IP}/foo`를 맥 실습으로 그대로 싣기 | **맥에서는 그 IP에 도달할 수 없다.** cloud-provider-kind README 축자: "Mac and Windows run the containers inside a VM and, on the contrary to Linux, **the KIND nodes are not reachable from the host, so the LoadBalancer assigned IP is not working for users.**" 맥은 `sudo` + `--enable-lb-port-mapping` + `curl localhost:[port]`(§B-3b) | 리눅스 기준 문서를 그대로 옮기면 **독자가 실습에서 막힌다.** 동시에 이 책의 중심 논제("맥은 VM이 껴서 다르다")를 실습 층위에서 증명하는 **최고의 재료** |

**부수 위험 3건 (같은 성격, 등급 낮음):**
- **kind의 `extraPortMappings` Ingress 레시피는 현재 kind 문서에 없다.** `cloud-provider-kind` 기반으로 다시 쓰였다. 옛 레시피를 kind 공식 근거로 달면 ❌.
- **Colima가 k3s를 쓴다는 근거가 README에 없다.** 널리 통용되는 서술이지만 1차 확인 실패 — 소절 제목에서 "k3s"를 빼라.
- **ECR 태그 불변성 문서가 자기모순이다** ("affects all tags" vs `IMMUTABLE_WITH_EXCLUSION`). 단정 금지.

**WebSearch 요약문에만 있고 축자 확인에 실패해 폐기한 값 2건 (⛔ 인용 금지):**
- ingress-nginx 은퇴일 **"3월 24일"** → 확인된 것은 "March 2026"까지
- ingress-nginx 사용률 **"약 50% (Datadog)"** → 내가 연 페이지에 수치 없음

---

## E. ⭐ §7-2 "소스 0건" 목록 — 무엇이 살아났나 (Phase 2 planner용 판정표)

| # | §7-2 소절 후보 | 판정 | 쓸 수 있는 소절 (한 줄) |
|---|---|---|---|
| 1 | semver 태깅 전략 / 태그 승격 워크플로 | ✅ **계획 가능** | `metadata-action`의 파생 규칙 표(§A-3)로 "태그 하나에서 `1.2.3`·`1.2`·`1`을 만드는 법", 승격은 **`crane tag`** 주(主) + `imagetools create`("carbon copy", 레지스트리에 이미 있는 매니페스트) 부(副) — §A-4 |
| 2 | `dive`/`docker history`로 레이어 뜯어보기 | ✅ **계획 가능** | 옵션 표·컬럼·`--platform`(§A-7) + dive `brew install dive`·CI 모드. ⛔ dive 버전 숫자 금지 |
| 3 | `--mount=type=secret` 실습 | ✅ **계획 가능** | 문법·`--secret` 3형태·`/run/secrets/<id>` 기본 경로 전부 축자(§C-1). "ARG는 이미지에 남는다"가 오프닝 |
| 4 | Ingress로 외부 노출하기 | ✅✅ **계획 가능 — 프레임을 바꾸면 오히려 이 책 최고의 소절** | ingress-nginx 실습 ❌ → **"Ingress는 frozen, ingress-nginx는 은퇴, kind는 이제 네이티브, 그런데 맥에서는 그 IP에 못 닿는다"**(§B-1~B-3b). 최소 Ingress YAML·맥 우회(`sudo` + `--enable-lb-port-mapping`) 전부 축자 확보 |
| 5 | k3s(Colima)로 로컬 K8s 돌리기 | ⚠️ **부분 가능 — 제목 수정 필수** | **"Colima로 로컬 K8s"**로 쓸 것. `--kubernetes` 플래그·기본 2CPU/2GiB/100GiB 확보(§B-7). ⛔ **"k3s 기반"이라는 근거 없음** |
| 6 | 로컬 K8s 리소스 소모 비교 (kind vs minikube vs Desktop) | ⚠️ **부분 가능 — 성격 변경** | **"공표된 최소 요구사항 비교"**는 가능(§B-4: minikube 2C/2GB/20GB, k3s 2core/2GB, Colima 기본 2C/2GiB/100GiB, **kind 부재확정**). ❌ **실측 소모량 비교는 여전히 0건**. ⛔ **kind의 "수치 부재"를 "가볍다"로 읽지 말 것** — §B-3b대로 맥에서 kind로 노출 실습을 하려면 cloud-provider-kind + `sudo` + 포트 매핑이 붙어 **설치 비용은 오히려 크다.** 비교 축을 "요구 사양"과 "셋업 비용" 둘로 나눠 쓸 것 |
| 7 | rootless / cosign 서명 / SBOM **생성** | ⚠️ **쪼개서 판정** | **SBOM/프로비넌스 생성 ✅ 계획 가능**(`--sbom=true`·`--provenance`, §C-2) / **cosign ⚠️ 서명만**(verify 미확보, §C-3) / **rootless ❌ 소절 금지 — 각주로만**(맥 언급조차 없음, §C-4) |
| 8 | `latest` 사고담 · 베이스 갱신 운영 실태 · 스캔 알림 피로 | ❌ **여전히 불가 (일화)** / ⚠️ **도구 층위는 가능** | 일화·실태는 **커뮤니티 리서치 영역이고 이번 회차 범위 밖 — 0건 유지**. 다만 **"베이스 갱신을 자동화하는 도구"**는 Dependabot/Renovate 1차 소스로 계획 가능(§A-6). ⛔ 재빌드 트리거 서술 금지 |

**보너스 — §7-1 등급을 올릴 수 있는 것:**
- **D영역(이미지 만들기·업데이트):** 0건 3항목(semver 태깅·`dive`/`history`·`type=secret`)이 **전부 해소.** 루브릭상 **보통 → 충분** 상향 가능.
- **G영역(원리):** **overlayfs 전용 문서 확보**(§C-5) + SBOM 생성 문서 확보로 결손 2개 해소. rootless·컨테이너 vs VM 보안 경계는 여전히 결손 → **보통 유지**.
- **F영역(Kubernetes):** 0건 3항목 중 **1개 완전 해소(Ingress)·2개 부분 해소.** 그리고 §D-1·D-2로 **신선도가 극적으로 개선**됐다. **보통 → 충분에 근접**(실측 소모량 비교만 미해결).

---

## F. 수집 한계 (정직한 목록)

**🕒 이번 회차에서 확인하지 못한 것 (추측으로 채우지 않음):**
1. **NodePort 기본 포트 범위(30000–32767)** — **4개 페이지에서 시도 실패**(Service 개념 페이지 TRUNCATED, `connect-applications-service`·`virtual-ips`·`source-ip` 전부 NOT_PRESENT). ⛔ **널리 알려진 숫자지만 축자 확인에 실패했으므로 책에 쓰지 마라.** LoadBalancer "pending"은 minikube 문서 축자로 대체 가능(§B-6)
2. ~~`cloud-provider-kind` 설치·실행 명령~~ → **✅ 해소됨 (§B-3b)**
3. ~~`minikube addons enable ingress`가 무엇을 설치하는지~~ → **✅ 해소됨 — ingress-nginx다 (§B-6, §D-4)**. 다만 minikube가 이후 대체 컨트롤러로 갈아탔는지는 미확인
4. minikube 드라이버 옵션의 맥 상세 (vfkit은 확인된 목록에 **없음**)
5. `cosign verify` 명령·플래그
6. Docker rootless "Known limitations" 목록
7. Docker Hub 태그 불변성 정책 (미조회)
8. Renovate `pinDigests` (해당 페이지에 NOT_PRESENT)
9. `crane`·`dive`·`minikube`·`cosign`의 현재 버전 숫자 (릴리스 페이지 미조회 — §4-8 방침 승계로 GitHub Releases 날짜·버전 채택 안 함)
10. ingress2gateway 변환 명령 예제 (페이지 절단)
11. Docker `overlay2` 스토리지 드라이버와 커널 overlayfs의 대응 관계
12. `--sbom`/`--provenance` 기본 동작의 빌더·출력별 조건

**❌ 부재확정 (확인한 페이지에 없음 — "존재하지 않음"이 아니다):**
- GHCR 태그 불변성 — working-with-the-container-registry 페이지에 언급 전무
- kind 최소 시스템 요구사항 — quick-start 페이지에 수치 없음
- OCI distribution-spec의 "태그는 가변" 명시 문장
- kind Ingress 문서의 `extraPortMappings`/`node-labels` 레시피
- Colima README의 "k3s" 언급
- cosign 문서의 "digest로 서명하라" 권고
- `imagetools create`의 **재태깅 전용 *예제*** (Examples 섹션에 없음). ⚠️ **단, 재태깅의 *근거 문장*은 도입부에서 확보했다** — "must already exist in the registry" + "carbon copy". §A-4가 최종 판정이며, 이 줄은 "예제가 없다"는 뜻일 뿐 "근거가 없다"는 뜻이 아니다

**방침 준수 기록:**
- 이 문서의 모든 인용은 **WebFetch로 원문을 열어 얻은 축자**다. WebSearch는 URL 발견 1회(ingress-nginx 블로그)에만 썼고, **그 요약문에서 나온 수치 2건은 축자 확인 실패로 폐기**했다(§D 하단).
- 개인 블로그·Medium·Stack Overflow **0건 채택**.
- 기존 `research/*.md`·`01_reference.md` **수정·삭제 없음.** 이 파일은 신규 산출물이다.
