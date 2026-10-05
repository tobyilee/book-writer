# 웹 리서치 갭필 — vinext 1.0 / Spring·Access JWT / JVM on Containers / Hyperdrive·Stripe·R2(Java)

<!-- 갭필: 2026-10-03 web-researcher. 대상: Ch5(vinext), Ch7/10(Spring Security + Access JWT), Ch7(JVM on Containers), Ch8(Hyperdrive Supabase·RDS, Stripe 웹훅, R2 Java SDK). research/web.md·01_reference.md는 수정하지 않음 -->

- 장르: tech-book / 슬러그: cloudflare-developer-cloud
- 검색 시점: **2026-10-03** (모든 항목 공통)
- 표기 규칙: 각 사실에 `{제품} {날짜} 기준` + URL. 날짜는 문서의 "Last updated"/`dateModified`, GitHub 커밋·릴리스 시각(UTC) 중 실제로 확인한 것. 인용(> 블록)은 원문 그대로.
- 1차 소스 우선: developers.cloudflare.com(`/index.md` 원문), GitHub 소스·README·릴리스(`gh api`), docs.spring.io, docs.stripe.com, docs.aws.amazon.com.

---

## 1. (Ch5, 최우선) vinext 1.0 on Cloudflare Workers

### 1-1. 버전·날짜 (GitHub Releases, `gh api` 원값)

| 패키지 | 버전 | 게시 시각(UTC) |
|---|---|---|
| `vinext` | 1.0.0 | 2026-09-28T13:00:38Z |
| `create-vinext-app` | 1.0.0 | 2026-09-28T13:00:41Z |
| `@vinext/cloudflare` | 1.0.0 | 2026-09-28T13:00:44Z |
| `vinext` / `@vinext/cloudflare` | 1.0.1 | 2026-10-01T14:16:32Z / 14:16:38Z |
| 직전 프리릴리스 | `vinext@1.0.0-beta.13` | 2026-09-27T01:10:23Z |

출처: https://github.com/cloudflare/vinext/releases (vinext 2026-10-01 기준, 검색 시점 2026-10-03)
⚠ WebFetch 요약이 1.0.0 릴리스 날짜를 "September 28, 2024"로 돌려줬으나 오류. API 원값(2026-09-28)만 쓸 것.

### 1-2. 핵심 답: init/create는 무엇을 만드나 → **기본은 `cf` + `cloudflare.config.ts`. `wrangler.jsonc`는 레거시 플래그로만**

- vinext README (vinext 2026-09-28 기준 — README 마지막 변경 커밋 `1fe853e`, 2026-09-28T12:50:04Z; main HEAD `e5ada16` 2026-10-01) https://github.com/cloudflare/vinext :
  > "Cloudflare init uses `cf` and `cloudflare.config.ts` by default. Both `vinext init` and `create-vinext-app` accept `--legacy-wrangler-cloudflare-init` to retain the legacy Wrangler setup. Existing Wrangler configs are not automatically migrated."

  > "Before running `npx @vinext/cloudflare deploy` for the first time, run `vinext init --platform=cloudflare` to install `cf` and Cloudflare Vite plugin v2, create or update `vite.config.*`, and generate `cloudflare.config.ts`."
- 이 기본값을 바꾼 PR #3504 "feat(init): default Cloudflare projects to cf" (merged 2026-09-27T23:00:03Z) https://github.com/cloudflare/vinext/pull/3504 :
  > "Default both vinext init and create-vinext-app to cf, Cloudflare Vite plugin v2, cloudflare.config.ts, and Cloudflare Build Output."
  > "Keep Wrangler initialization behind --legacy-wrangler-cloudflare-init, using Vite plugin v1. Existing Wrangler configs remain protected from implicit migration."
  > "Build Output is no longer described as experimental"
- `create-vinext-app` CHANGELOG 1.0.0 (2026-09-28 기준): "**Init:** default Cloudflare projects to cf (#3504)" https://github.com/cloudflare/vinext/blob/main/packages/create-vinext-app/CHANGELOG.md
- **기존 `wrangler.*`가 있으면 init이 멈춘다** — `packages/vinext/src/init-cloudflare.ts` (main, 2026-10-03 조회) https://github.com/cloudflare/vinext/blob/main/packages/vinext/src/init-cloudflare.ts :
  > "Cloudflare init cannot replace an existing Wrangler config (${existingWrangler}). Migrate its bindings to cloudflare.config.ts first, or use --legacy-wrangler-cloudflare-init to keep the Wrangler setup."

  (레거시 경로에서도) > "wrangler.toml is not supported by vinext init. Convert it to wrangler.jsonc and rerun."
- 생성되는 `cloudflare.config.ts` 골격 (같은 파일의 템플릿 문자열에서 재구성한 골격 — **원문 아님**, `<…>`·한국어 주석은 리서처 표기. 캐시·이미지 옵션 없을 때):
  ```ts
  import { bindings, defineConfig, defineWorker } from "cf/config";

  export default defineConfig({
    worker: defineWorker({
      name: "<project-name>",
      entrypoint: "vinext/server/fetch-handler",   // worker/index.ts가 있으면 그 경로
      compatibilityDate: "<init 실행일>",
      compatibilityFlags: ["nodejs_compat"],
      assets: { notFoundHandling: "none" },
      env: {
        ASSETS: bindings.assets(),
        // 옵션: IMAGES: bindings.images(), VINEXT_KV_CACHE: bindings.kv()
      },
    }),
  });
  ```
  계정 지정: README > "Set `accountId` at the top level of `defineConfig` in `cloudflare.config.ts`, outside `worker`."
- 바인딩 추가 (README):
  ```ts
  import { bindings } from "cf/config";
  env: {
    DB: bindings.d1({ name: "my-db" }),
    CACHE: bindings.kv(),
  },
  ```
  > "Binding and runtime types are generated in `.cloudflare/types` during dev and build. Include that directory in `tsconfig.json`; run `cf workers types` before standalone type-checks."
- 인증 (vinext docs `docs/deploying/cloudflare.mdx`, main 2026-10-03 조회) https://github.com/cloudflare/vinext/blob/main/docs/deploying/cloudflare.mdx : `npx cf auth login`(로컬), CI는 `CLOUDFLARE_API_TOKEN`. README: "create a token … using the **Edit Cloudflare Workers** template."
- 바인딩 접근 코드: `import { env } from "cloudflare:workers";` — README > "`cloudflare:workers` is the recommended way to access bindings in vinext." (`getPlatformProxy()`·커스텀 엔트리 불필요)

### 1-3. 정확한 명령어 (vinext 1.0 기준)

| 목적 | 명령 | 근거 |
|---|---|---|
| 새 앱 | `pnpm create vinext-app@latest my-app` (Node 타깃은 `--platform=node`) | README "Quick start". > "It creates a TypeScript App Router project with Tailwind CSS and then runs the same vinext init setup used for existing apps" / "The generated project is Cloudflare Workers-ready by default." |
| 호환성 사전 점검 | `npx vinext check` | README, CF 가이드 |
| 기존 Next.js 이전 | `npx vinext init` (프롬프트 없이: `--platform=cloudflare`) | README. 기타 옵션 `--port <port>`(기본 3001), `--skip-check`, `--force` |
| 레거시(Wrangler) 유지 | `npx vinext init --legacy-wrangler-cloudflare-init` | README |
| 로컬 개발(이전한 앱) | `npm run dev:vinext` (vinext dev 서버, 포트 3001). `npm run dev`는 계속 Next.js | README: "npm run dev           # Still runs Next.js as before" |
| 빌드(이전한 앱) | `npm run build:vinext` | README, CF 가이드 |
| 로컬 프로덕션 서버 | `npm run start:vinext` / `vinext start` | README |
| 배포 | `npx @vinext/cloudflare deploy` (옵션 `--preview`, `--env <name>`, `--name <name>`, `--skip-build`, `--dry-run`, `--warm-cache`, `--traffic-aware-warm-cache`) | README CLI reference |
| create-vinext-app 프로젝트 | 스크립트 이름이 `dev`/`build`/`deploy` | docs/deploying/cloudflare.mdx: "`create-vinext-app` uses `build` and `deploy` instead of `build:vinext` and `deploy:vinext`." |

`vinext init`이 하는 일 (README 원문 목록):
> 1. Run `vinext check` to scan for compatibility issues
> 2. Install vinext runtime packages as dependencies and Vite/plugin tooling as devDependencies
> 3. Rename CJS config files (e.g. `postcss.config.js` -> `.cjs`) to avoid ESM conflicts
> 4. Add `"type": "module"` to `package.json`
> 5. Add `dev:vinext`, `build:vinext`, and `start:vinext` scripts to `package.json`
> 6. Prompt for a deployment platform (Cloudflare by default, or Node)
> 7. Generate the matching `vite.config.ts`
> 8. For Cloudflare, generate `cloudflare.config.ts` for `cf` and Cloudflare Vite plugin v2

> "The migration is non-destructive -- your existing Next.js setup continues to work alongside vinext. It does not modify `next.config`, `tsconfig.json`, or any source files, and it does not remove Next.js dependencies."

배포 동작 (README): > "`@vinext/cloudflare deploy` validates the initialized setup, builds the application, and deploys its Cloudflare Build Output with `cf` without rewriting project configuration."
툴체인: > "vinext targets Vite 8, which defaults to Rolldown, Oxc, Lightning CSS, and a newer browser baseline."

### 1-4. Next.js 기능 지원표 (vinext README 2026-09-28 기준 + CF 가이드 2026-08-25 기준)

| 기능 | vinext README | Cloudflare 가이드(2026-08-25) |
|---|---|---|
| ISR | ✅ "Stale-while-revalidate, pluggable `CacheHandler`, background regeneration" | Supported ("stale-while-revalidate caching model") |
| `"use cache"` | 표에는 ✅ "File-level and function-level. `cacheLife()` profiles, `cacheTag()`, stale-while-revalidate" — 그러나 Known gaps에 > "`"use cache"` is partially implemented, but full `cacheComponents` behavior is still incomplete. Cache profiles, tags, partial shells, resume behavior, prefetching, and some dev/build cache semantics do not yet match Next.js in every case." | (표에 항목 없음) |
| Middleware / proxy | ✅ "`middleware.ts` and `proxy.ts` (Next.js 16). Matcher patterns …" | Supported |
| Server Actions | ✅ "Action execution, FormData, re-render after mutation, `redirect()` in actions" | Supported |
| 이미지 최적화 / `next/image` | 🟡 "Remote images via @unpic/react (28 CDNs). Local images via `<img>` + srcSet. No build-time optimization/resizing". Known gaps: > "images can be optimized at request time on Cloudflare, but vinext does not yet reproduce Next.js's complete build-time image pipeline." `images` config: 🟡 "Parsed but not used for optimization" | Partially supported ("available at request time") |
| `next/font` | 🟡 런타임 CDN 로딩·런타임 `@font-face` 주입 | — |
| PPR / Cache Components | Known gap (위 인용) | — |
| `preferredRegion` | 무시됨 | — |
| 의도적 비지원 | Vercel 전용 기능, AMP, Turbopack/webpack 설정, `next/jest`, `create-next-app` 스캐폴딩 | — |

캐시 어댑터 (README, `@vinext/cloudflare`): `kvDataAdapter()`("backs the `"use cache"` data cache with a Workers KV namespace"), `workersCacheCdnAdapter()`("serves page-level ISR from the Cloudflare Workers Cache (`ctx.cache`)"), `staticAssetsAdapter()`, `responseStoreAdapter()`. 기본은 > "The default `MemoryCacheHandler` works out of the box. Swap in your own backend for production." 1.0.0 릴리스 노트: `cdnAdapter` → `workersCacheCdnAdapter` 이름 변경, "replace deploy prerendering with cache warming".

프로젝트 상태 문구 (README 상단, 1.0 이후에도 유지):
> "**Under active development.** vinext supports substantial Next.js applications today, but it is not yet a drop-in replacement for every application or production workload. Expect compatibility gaps, especially in newer App Router features, and evaluate it against your own application before adopting it."

FAQ: > "You can, with caution. vinext has known compatibility gaps and has not yet been battle-tested across the full range of production Next.js workloads."

### 1-5. Cloudflare 공식 Next.js 가이드 — **아직 beta 표기 + Wrangler 기준 서술 (갱신 전)**

Workers Next.js 가이드 2026-08-25 기준 (`dateModified` 2026-08-25, 2026-10-03 재조회 시 동일) https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/ :
> "Cloudflare recommends vinext as the default way to run Next.js applications on Cloudflare Workers. vinext gives you two starting points: scaffold a new Workers-ready app with `create-vinext-app`, or add vinext to an existing Next.js 16 app with a single non-destructive `vinext init` (your existing `next dev` keeps working)."

> "vinext is in beta. Before adopting it for an existing production application, run the compatibility check from your project directory and review the vinext compatibility dashboard."

> "Define bindings in your Wrangler configuration, then generate types with `wrangler types`."  ← vinext 1.0 기본값(`cloudflare.config.ts`, `cf workers types`)과 **불일치**

C3 경로(같은 가이드): `npm create cloudflare@latest -- my-next-app --framework=next` → > "C3 creates a new Next.js project, configures vinext for Cloudflare Workers, installs the required dependencies, and offers to deploy the application." 이후 `npm run dev` / `npm run build` / `npm run deploy`.

### 1-6. C3(`--framework=next`)의 실제 산출물 — 미확정

`workers-sdk/packages/create-cloudflare/templates/next/c3.ts` (마지막 변경 2026-09-25T08:58:26Z, 즉 vinext 1.0 이전) https://github.com/cloudflare/workers-sdk/blob/main/packages/create-cloudflare/templates/next/c3.ts :
- 변형 선택지 `"vinext (recommended)"` / `"OpenNext adapter"`, `-y`면 vinext.
- vinext 경로는 `create-vinext-app`에 `--platform cloudflare --data-cache none --yes --skip-install --disable-git`를 넘김(레거시 플래그 없음 → 1.0 기본값이면 `cf` 산출로 추정).
- 그러나 같은 파일이 `"cf-typegen": "wrangler types --env-interface CloudflareEnv ./worker-configuration.d.ts"` 스크립트를 덧붙이고, 주석에 "`wrangler deploy`"를 언급 → **C3 2.73.2 결과물이 `cf` 기반인지 Wrangler 기반인지 1차로 확정 못 함** [리서치 공백, 실행 검증 필요].

### 1-7. OpenNext(`@opennextjs/cloudflare`) — 기존 앱 유지 경로

Cloudflare OpenNext 가이드 2026-08-25 기준 https://developers.cloudflare.com/workers/framework-guides/web-apps/opennext/ :
> "Cloudflare recommends vinext instead of OpenNext for new Next.js applications on Cloudflare Workers. Use this guide to maintain an existing OpenNext application. Migrate to vinext when compatibility allows."
> "Wrangler automatic configuration uses vinext for Next.js projects. To use OpenNext, configure the adapter manually."

수동 구성 순서(원문 요지, 코드는 원문 그대로):
1. `npm i @opennextjs/cloudflare@latest` / `npm i -D wrangler@latest`
2. `wrangler.jsonc`:
   ```jsonc
   {
     "$schema": "./node_modules/wrangler/config-schema.json",
     "name": "my-app",
     "main": ".open-next/worker.js",
     "compatibility_date": "2026-10-02",
     "compatibility_flags": ["nodejs_compat"],
     "assets": { "directory": ".open-next/assets", "binding": "ASSETS" },
     "observability": { "enabled": true }
   }
   ```
   > "You must turn on the `nodejs_compat` compatibility flag and set your compatibility date to `2024-09-23` or later."
3. `open-next.config.ts`:
   ```ts
   import { defineCloudflareConfig } from "@opennextjs/cloudflare";
   export default defineCloudflareConfig();
   ```
4. `package.json` scripts:
   ```json
   "preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",
   "deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy",
   "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
   ```
5. 로컬 개발은 `npm run dev`(= `next dev`), Workers 런타임 미리보기 `npm run preview`, 배포 `npm run deploy`.

지원표(같은 문서): ISR·Server Actions·Middleware Supported, Image optimization "Supported through Cloudflare Images", PPR·`"use cache"` Supported("experimental in Next.js"), **"Node.js in Middleware — Not yet supported"**.
OpenNext 사이트 get-started (조회 2026-10-03, 페이지 날짜 미표시) https://opennext.js.org/cloudflare/get-started : 자동 이전 `npx @opennextjs/cloudflare migrate`, 개발 중 바인딩 사용 `import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare"; initOpenNextCloudflareForDev();`(next.config.ts), > "The edge runtime is not supported yet with `@opennextjs/cloudflare`". 최신 버전 `@opennextjs/cloudflare` 1.20.8(01_reference §8과 동일).

### 1-8. 책 권장 표현 (Ch5)
- "vinext 1.0(2026-09-28)부터 `vinext init`과 `create-vinext-app`은 Wrangler 설정 대신 `cf` CLI와 타입 있는 `cloudflare.config.ts`를 만든다. Wrangler 설정이 필요하면 `--legacy-wrangler-cloudflare-init`."
- "단 Cloudflare 공식 Next.js 가이드(2026-08-25 갱신)는 아직 'vinext is in beta'라고 적고 바인딩을 Wrangler 설정에 정의하라고 안내한다(2026-10 기준, 갱신 전)."
- 이미 `wrangler.jsonc`가 있는 프로젝트에 `vinext init`을 돌리면 에러로 멈춘다는 점을 실습 함정으로 넣을 것.

---

## 2. (Ch7/10) Spring Boot·Spring Security 버전과 Access JWT 검증 설정

### 2-1. GA 버전 (GitHub Releases `prerelease=false`, 2026-10-03 조회)

| 프로젝트 | 최신 GA | 날짜 | 병행 GA | 다음(프리릴리스) |
|---|---|---|---|---|
| Spring Boot | **4.1.1** | 2026-08-20 | 4.0.8(2026-08-21), 3.5.16(2026-06-25) | 4.2.0-M2(2026-09-24) |
| Spring Security | **7.1.1** | 2026-08-20 | 7.0.7(2026-08-20), 6.5.11(2026-06-09) | 7.2.0-M2(2026-09-24) |
| Spring Framework | 7.0.9 | 2026-08-20 | 6.2.19(2026-06-08) | 7.1.0-M2(2026-09-24) |

출처: https://github.com/spring-projects/spring-boot/releases , https://github.com/spring-projects/spring-security/releases , https://github.com/spring-projects/spring-framework/releases (검색 시점 2026-10-03). spring.io 프로젝트 페이지도 4.1.1을 현재 버전으로 표시 https://spring.io/projects/spring-boot .
⚠ Maven Central `maven-metadata.xml`의 `<release>`는 4.2.0-M2 / 7.2.0-M2(마일스톤)를 가리키므로 GA 근거로 쓰지 말 것.
Spring Security 레퍼런스 현재판 = 7.1.1 (`data-version="7.1.1"`, 경로 `/spring-security/reference/7.1/`).

### 2-2. 최소 Java (Spring Boot 4.1.1 기준)
https://docs.spring.io/spring-boot/system-requirements.html :
> "Spring Boot 4.1.1 requires at least Java 17 and is compatible with versions up to and including Java 26."
> "Spring Framework 7.0.9 or above is also required."
빌드 도구: Maven 3.6.3+, Gradle 8.x(8.14+)·9.x. 서블릿 컨테이너: Tomcat 11.0.x, Jetty 12.1.x (Servlet 6.1).

### 2-3. Boot 프로퍼티 (Spring Boot 4.1.1 기준, Application Properties 부록)
https://docs.spring.io/spring-boot/appendix/application-properties/index.html — `spring.security.oauth2.resourceserver.jwt.*`:
- `audiences` — "Identifies the recipients that the JWT is intended for."
- `issuer-uri` — "URI that can either be an OpenID Connect discovery endpoint or an OAuth 2.0 Authorization Server Metadata endpoint defined by RFC 8414."
- `jwk-set-uri` — "JSON Web Key URI to use to verify the JWT token."
- `jws-algorithms` — 기본값 `RS256`
- 그 외 `authorities-claim-name`, `authorities-claim-delimiter`, `authorities-claim-expressions`, `authority-prefix`, `principal-claim-name`, `public-key-location`

Spring Security 7.1.1 레퍼런스 "OAuth 2.0 Resource Server JWT" https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html :
> "If the authorization server doesn't support any configuration endpoints, or if Resource Server must be able to initialize independently from the authorization server, then the jwk-set-uri can be supplied as well"
> "Consequently, Resource Server will not ping the authorization server at startup."
> "We still specify the issuer-uri so that Resource Server still validates the iss claim on incoming JWTs."
> "Boot also has the audiences property for validating the aud claim; this is who the JWT was sent to."
> "By default, Resource Server configures a clock skew of 60 seconds."

프로그래밍 방식(같은 문서, 원문 코드):
```java
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder.withJwkSetUri(jwkSetUri).build();
}
// aud 검증
OAuth2TokenValidator<Jwt> audienceValidator() {
    return new JwtClaimValidator<List<String>>(AUD, aud -> aud.contains("messaging"));
}
OAuth2TokenValidator<Jwt> withIssuer = JwtValidators.createDefaultWithIssuer(issuerUri);
OAuth2TokenValidator<Jwt> withAudience = new DelegatingOAuth2TokenValidator<>(withIssuer, audienceValidator);
jwtDecoder.setJwtValidator(withAudience);
```
`typ` 헤더: `JwtValidators.createDefault()`가 `JwtTypeValidator.jwt()`를 포함 — 소스(spring-security 7.1.1 `JwtTypeValidator.java`) 주석 > "Require that the `typ` header be `JWT` or absent". Access 토큰 헤더 예시는 `"typ": "JWT"`(아래 2-5)이므로 충돌 없음. (참고: 레퍼런스 문서 예시는 `.validateTypes(false)`로 쓰지만 7.1.1 소스의 빌더 메서드명은 `validateType(boolean)`. 이 책에서 쓸 일은 없음.)

### 2-4. **함정: `Cf-Access-Jwt-Assertion`은 `DefaultBearerTokenResolver`로 못 읽는다 → `HeaderBearerTokenResolver` 사용**

레퍼런스 "Bearer Tokens" (Spring Security 7.1.1 기준) https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/bearer-tokens.html :
> "By default, Resource Server looks for a bearer token in the Authorization header."
> (커스텀 헤더 예) `bearerTokenResolver.setBearerTokenHeaderName(HttpHeaders.PROXY_AUTHORIZATION);`
> "Or, in circumstances where a provider is using both a custom header and value, you can use HeaderBearerTokenResolver instead."

소스 확인 (spring-security 태그 `7.1.1`):
- `DefaultBearerTokenResolver.java` — 헤더 값이 `"bearer"`로 시작하지 않으면 무시하고, 정규식 `^Bearer (?<token>[a-zA-Z0-9-._~+/]+=*)$`(대소문자 무시)로 추출. https://github.com/spring-projects/spring-security/blob/7.1.1/oauth2/oauth2-resource-server/src/main/java/org/springframework/security/oauth2/server/resource/web/DefaultBearerTokenResolver.java
- `HeaderBearerTokenResolver.java` — `return request.getHeader(this.header);` 값 그대로 반환. https://github.com/spring-projects/spring-security/blob/7.1.1/oauth2/oauth2-resource-server/src/main/java/org/springframework/security/oauth2/server/resource/web/HeaderBearerTokenResolver.java
- Access는 `Cf-Access-Jwt-Assertion: <JWT>`처럼 **"Bearer " 접두어 없이** 보낸다(2-5 문서는 "Copy the JWT from the `Cf-Access-Jwt-Assertion` request header"로 원시 JWT를 다룸). 따라서 `setBearerTokenHeaderName("Cf-Access-Jwt-Assertion")`만 하면 토큰을 못 찾는다 → `new HeaderBearerTokenResolver("Cf-Access-Jwt-Assertion")`. [소스 기반 판단, 실행 검증은 저자 예제에서]

저자 작성 예제의 뼈대(공식 예제 아님 — 책에 "저자 작성"으로 명시):
```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: https://<team>.cloudflareaccess.com/cdn-cgi/access/certs
          issuer-uri: https://<team>.cloudflareaccess.com   # iss 검증용
          audiences: <Application AUD tag>
```
```java
@Bean
BearerTokenResolver bearerTokenResolver() {
    return new HeaderBearerTokenResolver("Cf-Access-Jwt-Assertion");
}
```
⚠ `issuer-uri`만 단독으로 두면 Boot가 OIDC discovery(`/.well-known/openid-configuration` 등)를 조회한다. `https://<team>.cloudflareaccess.com`에 discovery 엔드포인트가 있는지는 **미확인** → 반드시 `jwk-set-uri`를 함께 두거나, Java 설정으로 `NimbusJwtDecoder.withJwkSetUri(...)` + `JwtValidators.createDefaultWithIssuer(...)` + `JwtClaimValidator(AUD, ...)` 조합을 쓸 것.

### 2-5. Cloudflare Access JWT 사실 (developers.cloudflare.com)

"Validate JWTs" (Cloudflare One 2026-05-06 기준) https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/ :
> "When Cloudflare sends a request to your origin, the request will include an application token as a `Cf-Access-Jwt-Assertion` request header. Requests made through a browser will also pass the token as a `CF_Authorization` cookie."
> "We recommend validating the `Cf-Access-Jwt-Assertion` header instead of the `CF_Authorization` cookie, since the cookie is not guaranteed to be passed."
> "The public key for the signing key pair is located at `https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/certs`, where `<your-team-name>` is your Cloudflare One team name."
> "By default, Access rotates the signing key every 6 weeks. This means you will need to programmatically or manually update your keys as they rotate. Previous keys remain valid for 7 days after rotation to allow time for you to make the update."
> "You can also manually rotate the key using the API."
- certs 응답 구조: `keys`(두 키, JWK — `"kty": "RSA"`, `"alg": "RS256"`, `"use": "sig"`, `kid`), `public_cert`(현재 키 PEM), `public_certs`(두 키 PEM). → Spring/Nimbus는 표준 `keys` 배열을 JWKS로 읽는다(여분 필드 `public_cert*` 처리 여부는 실행 검증 권장).
> "Do not fetch the current key from `public_cert`, since your origin may inadvertently read an expired value from an outdated cache. Instead, match the `kid` value in the JWT to the corresponding certificate in `public_certs`."
- AUD:
  > "Cloudflare Access assigns a unique AUD tag to each application. The `aud` claim in the token payload specifies which application the JWT is valid for."
  > "The AUD tag will never change unless you delete or recreate the Access application."
  위치: 애플리케이션 → **Additional settings** → **Application Audience (AUD) Tag**.
- 공식 샘플 언어: Workers(TypeScript, `jose`의 `createRemoteJWKSet` + `issuer: env.TEAM_DOMAIN`, `audience: env.POLICY_AUD`), Go(`oidc.NewRemoteKeySet`), Python, Node.js. **Java/Kotlin 샘플 없음**(재확인, 01_reference §11-1과 동일).
- `TEAM_DOMAIN` 형식: > "`https://<your-team-name>.cloudflareaccess.com`, where `<your-team-name>` is replaced with your actual team name."

"Application token" (Cloudflare One 2026-06-25 기준) https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/application-token/ :
- 헤더 예: `"alg": "RS256"`, `"typ": "JWT"`, `kid`.
- 페이로드 예: `"aud": ["32eafc76…"]`(배열), `"iss": "https://yourteam.cloudflareaccess.com"`, `"type": "app"`, `email`, `exp`, `iat`, `nbf`, `sub`, `identity_nonce`, `country`.
- 필드 정의: > "iss | The Cloudflare Access domain URL for the application." / > "sub | The ID of the user. This value is unique to an email address per account."
- 서비스 토큰 인증 시: `common_name` = > "The Client ID of the service token (`CF-Access-Client-Id`)." , > "sub | Contains an empty string when authentication was through a service token." → Spring에서 `principal-claim-name` 기본(`sub`)을 쓰면 서비스 토큰 호출의 principal이 빈 문자열이 됨에 유의(저자 판단).
- 커스텀 클레임: > "Access trims custom attributes and claims when the serialized `custom` claim exceeds roughly 1 KB (1,000 bytes)" / > "Do not rely on custom claims in the JWT for authorization decisions when they may grow large." 전체 신원은 `https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/get-identity`.

---

## 3. (Ch7) JVM/Spring Boot on Cloudflare Containers

> 인스턴스 타입 표·가격은 research/web.md §3-4(Limits 2026-09-30)에 이미 있음. 여기서는 그 외 JVM 실행에 필요한 사실만.

### 3-1. API 선택 — 신규는 Durable Object Container API 권장 (2026-09 변화)
"API" (Containers 2026-09-29 기준) https://developers.cloudflare.com/containers/api/ :
> "For new applications, we recommend the Durable Object Container API. It lets you combine container workloads with the Durable Object's persistent storage, alarms, and request handling. Use `ctx.container` to control the container lifecycle while your Durable Object coordinates application state. The `Container` class remains documented for existing applications."
비교표(원문 셀 요지): 수명 타이머 — DO API `setInactivityTimeout()` vs `Container` 클래스 `sleepAfter`; 트래픽 — `getTcpPort(port).fetch()` vs `fetch()`/`containerFetch()`; 포트 준비 확인 — DO API는 애플리케이션 코드에서 직접 vs `startAndWaitForPorts()`/`waitForPort()`.
> "Starting a container through the Durable Object Container API does not mean its ports are ready."
→ **JVM은 기동이 느리므로 포트 준비 대기 로직이 특히 중요**(저자 판단). `Container` 클래스를 쓰면 `startAndWaitForPorts()`가 이를 처리.

### 3-2. 포트·슬립 설정 (Container class 2026-09-30 기준)
https://developers.cloudflare.com/containers/api/container-class/ :
- > "**`defaultPort`** ( `number`, optional) — the port your container process listens on." → Spring Boot 기본 `server.port=8080`과 맞추면 됨. 공식 예제도 `defaultPort = 8080`.
- > "**`requiredPorts`** ( `number[]`, optional) — ports that must be accepting connections before the container is considered ready."
- > "**`sleepAfter`** ( `string | number`, default: `"10m"`) — how long to keep the container alive without activity before shutting it down. Accepts a number of seconds or a duration string such as `"30s"`, `"5m"`, or `"1h"`."
- > "**`enableInternet`** ( `boolean`, default: `true`)"
- `waitForPort({ portToCheck, retries, waitInterval })` — "Throws if the port does not become available within the retry limit."
최소 형태(API 문서 원문):
```ts
import { Container } from "@cloudflare/containers";
export class MyContainer extends Container {
	defaultPort = 8080;
	sleepAfter = "10m";
}
```
DO Container API (2026-09-30 기준) https://developers.cloudflare.com/containers/api/durable-object-container/ :
- `setInactivityTimeout(durationMs)` — > "The value must be greater than `0` and at most 6 hours ( `21600000`)." > "Without a timeout, Cloudflare stops the container shortly after the Durable Object becomes inactive."
- `start({ instance })` — > "durable_object policy only: Instance size. Pass `"lite"`, `"standard-1"`, `"standard-2"`, `"standard-3"`, `"standard-4"`, or a custom object with `vcpu`, `memoryMib`, and `diskMb` properties. … Defaults to `"lite"`." → **lite = 256 MiB**이므로 JVM은 반드시 인스턴스를 지정해야 함(저자 판단, Limits 표 근거).

### 3-3. 이미지·런타임 제약
- 아키텍처: > "Your container image must be able to run on the `linux/amd64` architecture, but aside from that, has few limitations." (Get started 2026-09-30 기준) https://developers.cloudflare.com/containers/get-started/ ; Lifecycle 문서 > "Containers should be built for the `linux/amd64` architecture, and should stay within size limits." (2026-09-30 기준) https://developers.cloudflare.com/containers/concepts/architecture/ → Apple Silicon에서 빌드 시 `--platform linux/amd64` 필요(저자 판단).
- **최대 이미지 크기 = 인스턴스 디스크 크기** (Limits 2026-09-30 기준) https://developers.cloudflare.com/containers/platform/limits/ : "Image size | Same as instance disk space", 계정 총 이미지 저장 50 GB. 예: `basic` 4 GB, `standard-1` 8 GB.
- 메모리: > "If you run out of memory, your instance will throw an Out of Memory (OOM) error and will be restarted." > "Containers do not use swap memory." (FAQ 2026-10-02 기준) https://developers.cloudflare.com/containers/faq/ → JVM은 `-XX:MaxRAMPercentage` 등으로 힙을 인스턴스 메모리 안쪽으로 묶을 것(저자 판단).
- 디스크: > "All disk is ephemeral by default. When a Container instance goes to sleep, the next time it starts, it uses a fresh disk from the container image." 스냅샷은 `durable_object` 정책에서만.
- 종료 신호: > "1. Sends `SIGTERM` to the main process in the container. 2. Waits up to 15 minutes for that process to exit. 3. Sends `SIGKILL` if the process is still running." > "Cloudflare does not stop a container instance after a fixed maximum runtime." → Spring Boot `server.shutdown=graceful`과 맞물림(저자 판단).
- 콜드 스타트(FAQ 원문, 01_reference C-16과 동일): > "Container cold starts can often be in the 1-3 second range, but this is dependent on image size and code execution time, among other factors." → JVM 기동 시간은 이 범위에 **추가**된다고 서술할 것("entrypoint가 하는 일에 따라 달라진다"는 문서 문장: > "Depending on what this entrypoint does, it will take a variable amount of time to start.").
- 레지스트리: `default` 정책은 `registry.cloudflare.com`·Docker Hub·Amazon ECR·Google Artifact Registry 지원, `durable_object` 정책은 **Cloudflare 관리 레지스트리의 digest 고정 이미지만** (Image Management 2026-09-30 기준) https://developers.cloudflare.com/containers/guides/image-management/ :
  > "The `durable_object` scheduling policy does not support direct image references from external registries. A named `image` source must use a digest-pinned reference from the Cloudflare managed registry."
- Wrangler 설정 신형식 (Containers Wrangler configuration 2026-09-29 기준) https://developers.cloudflare.com/containers/configuration/wrangler/ : 최소 구성이 `containers`(`class_name`, `image: "./Dockerfile"`, `max_instances`) + `durable_objects.bindings` + **`exports`(`"type": "durable-object"`, `"storage": "sqlite"`)**. > "Existing applications that use the legacy `migrations` array can continue to use it. Do not configure `exports` and `migrations` together."
- Workers Builds: > "On the production branch, Workers Builds should run `wrangler deploy` so images and container instances can update. Non-production Workers Builds defaults to `wrangler versions upload`, which does not update images. Containers Workers implement Durable Objects, so preview URLs are not generated for them." (FAQ 2026-10-02)

### 3-4. 비-JS 언어 공식 예제 현황
- 공식 문서 예제 언어: Get started = Go("a simple Golang server that responds to requests on port 8080"), "Static frontend, container backend" = Go(`FROM golang:1.25-alpine`), "Stateless instances" = Node(`FROM node:24-bookworm-slim`). (예제 페이지 2026-10-02 기준) https://developers.cloudflare.com/containers/examples/container-backend/ , https://developers.cloudflare.com/containers/examples/stateless/
- GitHub `cloudflare/containers-demos` (2026-10-03 트리 조회) https://github.com/cloudflare/containers-demos : Dockerfile 데모 11개 — 컨테이너 소스는 Go(`ai`, `compression`, `compression-workflows`, `compute`, `http2`, `load-balancer`, `sqlite`, `websockets`), Python(`marimo`) 등. **Java/Kotlin/JVM 예제 0건.**
- 공식 문서 전반에 "Spring"·"Java" 언급 없음(01_reference §3-4 [추론] 유지). (참고용, 결정적 증거 아님: `gh search code "FROM eclipse-temurin" --owner cloudflare` 결과 0건 — 검색 인덱스 한계 가능. 부재의 근거는 위 예제 언어 목록과 containers-demos 트리.)

---

## 4. (Ch8, 낮은 우선순위)

### 4-1. Hyperdrive × Supabase (Hyperdrive 2026-04-21 기준)
https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/supabase/
> "When connecting to Supabase from Hyperdrive, you should use the **Direct connection** connection string rather than the pooled connection strings. Hyperdrive will perform pooling of connections to ensure optimal access from Workers."
- 전용 사용자 예: `CREATE ROLE hyperdrive_user LOGIN PASSWORD '…'; GRANT postgres to hyperdrive_user;` (문서 주석 "In practice, you want to create a role with lesser privileges.")
- 생성: `npx wrangler hyperdrive create <NAME> --connection-string="postgres://user:password@HOSTNAME_OR_IP_ADDRESS:PORT/database_name"` → `"hyperdrive": [{ "binding": "HYPERDRIVE", "id": "…" }]`
- 지원표(Supported databases and features 2026-09-30 기준) https://developers.cloudflare.com/hyperdrive/reference/supported-databases-and-features/ : "Supabase | ✅ | All | Supabase currently runs Postgres 15.x"

### 4-2. Hyperdrive × AWS RDS/Aurora (Hyperdrive 2026-04-21 기준)
https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/aws-rds-aurora/
> "To allow Hyperdrive to connect to your database, you must allow Cloudflare IPs to be able to access your database. You can either allow-list all IP address ranges (0.0.0.0 - 255.255.255.255) or restrict your IP access control list to the IP ranges used by Hyperdrive."
> "Alternatively, you can connect to your databases over in your private network using Cloudflare Tunnels."
- 콘솔: "Under the **Connectivity** header, ensure **Public access** is set to **Yes**." / > "You must ensure that the VPC security group associated with your database allows public IPv4 access to your database port."
- 엔드포인트: Aurora는 **Writer** 엔드포인트, RDS는 "Connectivity & security"의 Endpoint(기본 5432).
- 권한 예: `CREATE ROLE hyperdrive; GRANT CONNECT ON DATABASE postgres TO hyperdrive; … CREATE ROLE hyperdrive_user LOGIN PASSWORD '…'; GRANT hyperdrive to hyperdrive_user;`
- (참고: 사설 연결의 Workers VPC 경로는 01_reference Changelog 2026-04-29 "Hyperdrive VPC" 항목 참조.)

### 4-3. Hyperdrive 풀링 모드 (공통)
Connection pooling (Hyperdrive 2026-08-20 기준) https://developers.cloudflare.com/hyperdrive/concepts/connection-pooling/ :
> "The Hyperdrive connection pooler operates in transaction mode, where the client that executes the query communicates through a single connection for the duration of a transaction. When that transaction has completed, the connection is returned to the pool."
> "When a connection is returned to the pool, the connection is `RESET` such that the `SET` commands will not take effect on subsequent queries."
> "Hyperdrive supports named prepared statements as implemented in the `postgres.js` and `node-postgres` drivers. Named prepared statements in other drivers may have worse performance or may not be supported."
> "All configurations have a minimum of 5 connections, and with a maximum depending on your Workers plan."
> "The `max_size` parameter acts as a soft limit"
비지원 PostgreSQL 기능 (Supported databases and features 2026-09-30): SQL 수준 `PREPARE`/`DISCARD`/`DEALLOCATE`/`EXECUTE`, advisory locks, `LISTEN`/`NOTIFY`, 문서화되지 않은 세션 상태 변경. > "In cases where you need to issue these unsupported statements from your application, the Hyperdrive team recommends setting up a second, direct client without Hyperdrive."

### 4-4. Stripe 웹훅 on Workers
- **Cloudflare 1차 Stripe 전용 가이드: 없음(확인된 부재).** Workers 문서 전문(`/workers/llms-full.txt`, 2026-10-03 조회)에서 "stripe"는 vinext 관련 한 줄("Library imports that previously required SSR optimizer workarounds, such as Stripe, now resolve without extra configuration.")뿐. 가장 가까운 공식 예제는 HMAC 서명 검증 "Sign requests" https://developers.cloudflare.com/workers/examples/signing-requests/ .
- stripe-node (v23.0.0, 2026-10-01 릴리스) `package.json` exports에 **`"workerd"`** 조건이 있고 `./esm/stripe.esm.worker.js`로 매핑 https://github.com/stripe/stripe-node/blob/master/package.json . 이 워커 빌드의 `WebPlatformFunctions`는 기본 HTTP 클라이언트를 `createFetchHttpClient()`, 기본 암호 공급자를 `createSubtleCryptoProvider()`로 둠 https://github.com/stripe/stripe-node/blob/master/src/platform/WebPlatformFunctions.ts .
- SubtleCrypto는 비동기 전용 → **`constructEventAsync` 필수**. 소스 `src/crypto/SubtleCryptoProvider.ts`: > "This only supports asynchronous operations." / 동기 호출 시 > "SubtleCryptoProvider cannot be used in a synchronous context." `src/Webhooks.ts`의 안내 문구: > "Use `await constructEventAsync(...)` instead of `constructEvent(...)`", `DEFAULT_TOLERANCE: 300, // 5 minutes`.
- 공식 웹 표준 런타임 예제(Deno) — stripe-node `examples/webhook-signing/deno/main.ts`(마지막 변경 2026-09-09):
  ```ts
  const body = await request.text();
  event = await stripe.webhooks.constructEventAsync(body, signature, webhookSecret, undefined);
  ```
  주석 원문: "The .text() method must be used as the verification relies on the raw request body rather than the parsed JSON."
- Stripe 문서 (docs.stripe.com 2026-10-03 조회) https://docs.stripe.com/webhooks :
  > "Stripe requires the raw body of the request to perform signature verification. If you're using a framework, make sure it doesn't manipulate the raw body."
  > "Quickly returns a successful status code (`2xx`) before any complex logic that might cause a timeout."
  수동 검증: 헤더 `t=…,v1=…`(`v0`는 테스트용 가짜), > "Stripe generates signatures using a hash-based message authentication code (HMAC) with SHA-256. To prevent downgrade attacks, ignore all schemes that aren't `v1`." signed_payload = 타임스탬프 + `.` + 원본 JSON 본문. > "To protect against timing attacks, use a constant-time-string comparison" > "Our libraries have a default tolerance of 5 minutes between the timestamp and the current time." > "Don't use a tolerance value of `0`."
  재시도: > "Stripe attempts to deliver events to your destination for up to three days with an exponential backoff in live mode." 중복: > "Webhook endpoints might occasionally receive the same event more than once. You can guard against duplicated event receipts by logging the event IDs you've processed" / 순서: > "Stripe doesn't guarantee the delivery of events in the order that they're generated." / 비동기 처리: > "Configure your handler to process incoming events with an asynchronous queue." → Workers + Queues 패턴의 근거로 쓸 수 있음(저자 연결).
  302 등 리다이렉트는 실패로 처리: > "We consider redirect responses to webhook requests as failures."

### 4-5. R2 × AWS SDK for Java v2
"aws-sdk-java" (R2 2026-04-21 기준) https://developers.cloudflare.com/r2/examples/aws/aws-sdk-java/ :
> "You must set `chunkedEncodingEnabled(false)` in the `S3Configuration` when building your client. The AWS SDK for Java v2 uses chunked transfer encoding by default for `putObject` requests, which causes a signature mismatch error (HTTP 403) with R2. Disabling chunked encoding ensures the request signature is calculated correctly."
원문 클라이언트 구성:
```java
S3Configuration serviceConfiguration = S3Configuration.builder()
    .pathStyleAccessEnabled(true)
    .chunkedEncodingEnabled(false)
    .build();
return S3Client.builder()
    .endpointOverride(URI.create(config.getEndpoint()))   // https://<ACCOUNT_ID>.r2.cloudflarestorage.com
    .credentialsProvider(StaticCredentialsProvider.create(credentials))
    .region(Region.of("auto")) // Required by SDK but not used by R2
    .serviceConfiguration(serviceConfiguration)
    .build();
```
프리사인(`S3Presigner`)도 같은 endpoint·`Region.of("auto")`·`pathStyleAccessEnabled(true)`.

R2 S3 API compatibility (R2 2026-07-31 기준) https://developers.cloudflare.com/r2/api/s3/api/ :
> "When using the S3 API, the region for an R2 bucket is `auto`. For compatibility with tools that do not allow you to specify a region, an empty value and `us-east-1` will alias to the `auto` region."
체크섬 지원표: CRC64NVME = FULL_OBJECT만, CRC32·CRC32C·SHA1·SHA256 = COMPOSITE만. `PutObject` 행에는 체크섬 헤더 항목이 따로 나열돼 있지 않음.

AWS 측 (AWS SDK for Java 2.x 개발자 가이드, 2026-10-03 조회) https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/s3-checksums.html :
> "Beginning with version 2.30.0 of the AWS SDK for Java 2.x, the SDK provides default integrity protections by automatically calculating a `CRC32` checksum for uploads."
> "Along with the release of CRC32 checksum behavior with version 2.30.0, the SDK stopped calculating MD5 checksums on required operations."
끄는 방법: 빌더 `.requestChecksumCalculation(RequestChecksumCalculation.WHEN_REQUIRED)` / `.responseChecksumValidation(ResponseChecksumValidation.WHEN_REQUIRED)`, 환경변수 `AWS_REQUEST_CHECKSUM_CALCULATION=WHEN_REQUIRED`, 시스템 프로퍼티 `aws.requestChecksumCalculation`. `LegacyMd5Plugin`(2.31.32+)은 > "particularly useful … when working with third-party S3-compatible storage providers".
현재 SDK 버전: `software.amazon.awssdk:s3` 2.55.11 (Maven Central metadata lastUpdated 2026-10-02).
⚠ **R2와 SDK 2.30+ 기본 CRC32의 상호작용은 양쪽 1차 문서 어디에도 직접 서술 없음** — Cloudflare 예제는 `chunkedEncodingEnabled(false)`만 요구. 책에는 "403 SignatureDoesNotMatch나 체크섬 오류가 나면 `WHEN_REQUIRED`를 시도"를 저자 실험 결과로만 쓸 것 [리서치 공백].

---

## 5. 충돌·주의 원장 (fact-checker 대조용)

| # | 항목 | 충돌 | 근거 | 책 권장 표현 |
|---|---|---|---|---|
| G-1 | vinext 상태 🕒 | CF 가이드(2026-08-25) "vinext is in beta" ↔ vinext 1.0.0(2026-09-28) ↔ README 여전히 "Under active development … not yet a drop-in replacement" | 1-1, 1-4, 1-5 | "1.0이 나왔지만(2026-09-28) 공식 가이드는 beta 표기(2026-10 기준), README도 모든 앱의 대체품은 아니라고 적는다" |
| G-2 | vinext 설정 파일 🕒 | CF 가이드 "Define bindings in your Wrangler configuration, then generate types with `wrangler types`" ↔ vinext 1.0 기본 `cloudflare.config.ts` + `cf workers types` | 1-2, 1-5, PR #3504 | vinext README·PR을 따른다. 가이드 문장은 1.0 이전 상태로 간주 |
| G-3 | C3 Next.js 산출물 | `c3.ts`(2026-09-25)가 `create-vinext-app`에 위임하면서 `wrangler types` 스크립트를 추가 | 1-6 | 단정 금지. 실행 확인 전엔 "C3로도 만들 수 있다"까지만 |
| G-4 | `"use cache"` | README 표 ✅ ↔ Known gaps "partially implemented" | 1-4 | "파일·함수 수준은 동작, Cache Components 전체 동작은 미완" |
| G-5 | `Cf-Access-Jwt-Assertion` + Spring | `setBearerTokenHeaderName`만으로는 안 됨(Bearer 접두어 요구) | 2-4 소스 | `HeaderBearerTokenResolver` 사용 |
| G-6 | `issuer-uri` 단독 | Access 팀 도메인의 OIDC discovery 존재 미확인 | 2-4 | `jwk-set-uri` 병기 필수 |
| G-7 | Spring "최신" | Maven `<release>` = 마일스톤 | 2-1 | GA = Boot 4.1.1 / Security 7.1.1 (2026-08-20) |
| G-8 | Containers API | 신규 앱 권장이 `Container` 클래스 → DO Container API로 이동(2026-09) | 3-1 | 책 예제가 `Container` 클래스면 "기존 앱용으로 문서화 유지"임을 병기 |
| G-9 | DO Container API 기본 인스턴스 | `start()` 기본 `"lite"`(256 MiB) | 3-2 | JVM 예제는 인스턴스 명시 |
| G-10 | R2 Java 체크섬 | AWS SDK 2.30+ 기본 CRC32 ↔ R2 문서 언급 없음 | 4-5 | 저자 실험으로만 서술 |

---

## 6. 리서치 한계 / [리서치 공백]

1. **C3 `--framework=next`의 현재 산출물**(cf vs Wrangler) — 소스는 1.0 이전 상태, 실행 검증 안 함.
2. **`cf` CLI 버전 번호** — 미수집(01_reference §8과 동일). `cloudflare.config.ts`의 `cf/config` API 전체 레퍼런스(https://developers.cloudflare.com/cf/ 하위)는 이번에 정독하지 않음.
3. **JVM/Spring Boot on Containers 공식 예제·실측 0건** — 공식 예제는 Go·Node·Python뿐. 콜드 스타트 수치는 공식 "1–3초"(이미지·entrypoint 의존)만 있고 JVM 기동 시간 실측 없음 → 저자 실험 필요.
4. **Access JWKS 회전과 Nimbus 키 캐시** — Spring/Nimbus의 JWKS 캐시 TTL·`kid` 미스 시 재조회 동작을 1차로 확인하지 않음. Access 쪽은 "6주 회전, 이전 키 7일 유효"만 확정.
5. **Access 팀 도메인의 OIDC discovery 엔드포인트 존재 여부** 미확인(G-6).
6. **R2 × AWS SDK Java 2.30+ 기본 CRC32 체크섬 호환성** — 양측 1차 서술 없음(G-10).
7. **Hyperdrive × Supabase 세부** — Cloudflare 문서는 "Direct connection 사용"만 말함. Supabase Direct connection의 IPv6 전용 여부·Supavisor session/transaction 모드와의 관계는 Cloudflare 문서에 없음(Supabase 문서 미정독).
8. **Stripe on Workers 1차 Cloudflare 가이드는 없음(확인된 부재)** — 근거는 stripe-node 소스·Deno 예제·Stripe 문서로 대체. Stripe 문서 자체에는 Cloudflare Workers 전용 예제 없음.
9. OpenNext get-started 페이지 날짜 미표시.
10. 한국어 1차 자료 해당 없음(모두 영어 공식 문서·소스).
