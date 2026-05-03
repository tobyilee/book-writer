# 참고문헌

본문 16개 챕터의 각주에서 인용한 모든 자료를 카테고리별로 묶어 한 자리에 모았다. 발행 연도가 명시된 자료는 함께 적었다. 한국어 자료는 별도 카테고리로 묶어 검색 동선을 줄였다.

## 학술 논문

- Cui, M. et al. ["Is unsafe an Achilles' Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming" (arXiv:2308.04785, 2023)](https://arxiv.org/abs/2308.04785).
- deepSURF authors. ["deepSURF: Detecting Memory Safety Vulnerabilities in Rust" (IEEE S&P 2026, arXiv:2506.15648)](https://arxiv.org/html/2506.15648v2).
- Gäher, L. et al. ["RefinedRust: A Type System for High-Assurance Verification of Rust Programs" (PLDI 2024)](https://plv.mpi-sws.org/refinedrust/paper-refinedrust.pdf).
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. ["Stacked Borrows: An Aliasing Model for Rust" (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf).
- Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. ["RustBelt: Securing the Foundations of the Rust Programming Language" (POPL 2018)](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf); [CACM 2021 정리본](https://iris-project.org/pdfs/2021-rustbelt-cacm-final.pdf).
- "Rust for Embedded Systems: Current State and Open Problems" [(arXiv:2311.05063, 2023)](https://arxiv.org/html/2311.05063v2).
- "A Grounded Conceptual Model for Ownership Types in Rust" [(arXiv:2309.04134, 2023)](https://arxiv.org/pdf/2309.04134).
- Villani, N., Hostert, J., Dreyer, D., Jung, R. ["Tree Borrows" (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf); [블로그 소개 — Ralf Jung](https://www.ralfj.de/blog/2023/06/02/tree-borrows.html).
- Xu, H. et al. ["Memory-Safety Challenge Considered Solved? An In-Depth Study with All Rust CVEs" (arXiv:2003.03296, 2020)](https://arxiv.org/abs/2003.03296v1).

## 공식 문서·정부 보고서

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/) — Steve Klabnik, Carol Nichols.
- [The Cargo Book](https://doc.rust-lang.org/cargo/).
- [The Rustonomicon — Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html).
- [The Rust Reference — Macros](https://doc.rust-lang.org/reference/macros.html).
- [Tokio docs](https://docs.rs/tokio/), [tokio.rs Tutorial](https://tokio.rs/tokio/tutorial).
- [axum docs](https://docs.rs/axum/).
- [sqlx repo](https://github.com/launchbadge/sqlx); [sqlx 매크로 레퍼런스](https://docs.rs/sqlx/latest/sqlx/macro.query.html).
- [Diesel — diesel.rs](https://diesel.rs/); [Diesel relations](https://diesel.rs/guides/relations.html).
- [SeaORM — sea-ql.org](https://www.sea-ql.org/SeaORM/).
- [clap docs](https://docs.rs/clap/); [clap derive 튜토리얼](https://docs.rs/clap/latest/clap/_derive/_tutorial/index.html).
- [tracing docs](https://docs.rs/tracing); [tracing-opentelemetry docs](https://docs.rs/tracing-opentelemetry).
- [JEP 442 / 454 — Foreign Function & Memory API](https://openjdk.org/jeps/454).
- [Workspaces — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html).
- [White House ONCD: "Back to the Building Blocks: A Path Toward Secure and Measurable Software" (2024-02)](https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf).
- [NSA: "Memory Safe Languages — Reducing Vulnerabilities in Modern Software Development" (2025-06)](https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF).

## 산업 사례 — 회사 엔지니어링 블로그

- AWS: [Firecracker GitHub](https://github.com/firecracker-microvm/firecracker); [Firecracker AWS Blog](https://aws.amazon.com/blogs/aws/firecracker-lightweight-virtualization-for-serverless-computing/); [Firecracker Open Source Blog](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/); [Firecracker NSDI 논문](https://assets.amazon.com/96/c6/302e527240a3b1f86c86c3e8fc3d/firecracker-lightweight-virtualization-for-serverless-applications.pdf).
- Cloudflare: ["How we built Pingora"](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/); ["20-percent internet upgrade"](https://blog.cloudflare.com/20-percent-internet-upgrade/).
- Convex: ["A Tale of Three Rust Codebases"](https://news.convex.dev/a-tale-of-three-codebases/).
- Discord: ["Why Discord is switching from Go to Rust"](https://discord.com/blog/why-discord-is-switching-from-go-to-rust).
- Dropbox: ["Inside the Magic Pocket"](https://dropbox.tech/infrastructure/inside-the-magic-pocket); ["Why we built a custom Rust library for Capture"](https://dropbox.tech/application/why-we-built-a-custom-rust-library-for-capture); [InfoQ Magic Pocket 정리](https://www.infoq.com/articles/dropbox-magic-pocket-exabyte-storage/).
- Figma: ["Rust in production at Figma"](https://www.figma.com/blog/rust-in-production-at-figma/); ["Making multiplayer more reliable"](https://www.figma.com/blog/making-multiplayer-more-reliable/); ["Faster File Load Times with Memory Optimizations in Rust"](https://www.figma.com/blog/supporting-faster-file-load-times-with-memory-optimizations-in-rust/).
- Microsoft: ["Microsoft's Rust Bet — The New Stack"](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/); ["Russinovich: All-in on Rust — Thurrott"](https://www.thurrott.com/dev/317950/russinovich-microsoft-is-all-in-on-rust); ["Microsoft is rewriting core Windows libraries in Rust — The Register"](https://www.theregister.com/2023/04/27/microsoft_windows_rust/).

## 산업 사례 — 마이그레이션·후기 (Medium / DEV.to / HN)

- ["I Replaced My Spring Boot Microservice with Rust and Go" — Medium](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494).
- ["I Rewrote A Java Microservice In Rust And Lost My Job" — Medium](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca).
- Kasun Ranasinghe ["Before moving to Rust from Java" — Medium](https://keazkasun.medium.com/before-moving-to-rust-from-java-2b87a70654c0).
- ["How Discord Moved from Go to Rust" — OpenSourceScribes (Medium)](https://medium.com/sourcescribes/how-discord-moved-from-go-to-rust-ad98cf0a1d59).
- [Hacker News: Why Discord is switching from Go to Rust (2020)](https://news.ycombinator.com/item?id=26227339).
- [Hacker News: Rust in production at Figma (2018)](https://news.ycombinator.com/item?id=16977932).
- [Hacker News: Spring-rs is a microservice framework in Rust (2024)](https://news.ycombinator.com/item?id=41274138).
- [Hacker News: Ask HN — How to structure Rust, Axum, and SQLx for clean architecture?](https://news.ycombinator.com/item?id=40294092).

## 블로그·기술 매체 (개념·비교)

- [Rust Blog: "2024 State of Rust Survey Results" (2025-02)](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/).
- [Rust Blog: "Rust compiler performance survey 2025 results" (2025-09)](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/).
- [Rust Blog: "2025 State of Rust Survey Results" (2026-03)](https://blog.rust-lang.org/2026/03/02/2025-State-Of-Rust-Survey-results/).
- [Rust Blog: "Announcing async fn and RPIT in traits" (2023-12)](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/).
- [The New Stack: "Survey: Memory-Safe Rust Gains 45% of Enterprise Development"](https://thenewstack.io/survey-memory-safe-rust-gains-45-of-enterprise-development/).
- [The New Stack: "Nearly half of all companies now use Rust in production"](https://thenewstack.io/rust-enterprise-developers/).
- [JetBrains RustRover Blog: "The State of Rust Ecosystem 2025" (2026-02)](https://blog.jetbrains.com/rust/2026/02/11/state-of-rust-2025/).
- [JetBrains RustRover Blog: "The Evolution of Async Rust" (2026-02)](https://blog.jetbrains.com/rust/2026/02/17/the-evolution-of-async-rust-from-tokio-to-high-level-applications/).
- [Stack Overflow Blog: "In Rust We Trust? White House Office urges memory safety" (2024-12)](https://stackoverflow.blog/2024/12/30/in-rust-we-trust-white-house-office-urges-memory-safety/).
- [2025 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2025/).
- [corrode: "Migrating from Java to Rust"](https://corrode.dev/learn/migration-guides/java-to-rust/).
- [corrode: "Flattening Rust's Learning Curve"](https://corrode.dev/blog/flattening-rusts-learning-curve/).
- [corrode: "The State of Async Rust — Runtimes"](https://corrode.dev/blog/async/).
- [Without Boats: "Why async Rust?"](https://without.boats/blog/why-async-rust/); [Without Boats: "Pin"](https://without.boats/blog/pin/); [Without Boats: "Three problems of pinning"](https://without.boats/blog/three-problems-of-pinning/).
- [fasterthanlime: "Catching up with async Rust"](https://fasterthanli.me/articles/catching-up-with-async-rust); [fasterthanlime: "Surviving Rust async interfaces"](https://fasterthanli.me/articles/surviving-rust-async-interfaces); [fasterthanlime: "Pin and suffering"](https://fasterthanli.me/articles/pin-and-suffering); [fasterthanlime: "Some mistakes Rust doesn't catch"](https://fasterthanli.me/articles/some-mistakes-rust-doesnt-catch).
- [Niko Matsakis: baby steps blog](https://smallcultfollowing.com/babysteps/).
- [Tokio Blog: "Making the Tokio scheduler 10x faster"](https://tokio.rs/blog/2019-10-scheduler).
- [Tokio Blog: "Announcing Axum"](https://tokio.rs/blog/2021-07-announcing-axum).
- [Bit Bashing: "Async Rust Is A Bad Language"](https://bitbashing.io/async-rust.html).
- [Rust for Java Developers — tkaitchuck](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html).
- [softwaremill: "Rust Static vs. Dynamic Dispatch"](https://softwaremill.com/rust-static-vs-dynamic-dispatch/).
- [Comprehensive Rust — Java interop (Google)](https://google.github.io/comprehensive-rust/android/interoperability/java.html).
- [jni-rs GitHub](https://github.com/jni-rs/jni-rs); [jni-rs docs](https://docs.rs/jni).
- [Tweede golf: "Mix in Rust with Java (or Kotlin!)"](https://tweedegolf.nl/en/blog/147/mix-in-rust-with-java-or-kotlin).
- [Loco.rs](https://loco.rs/); [Loco GitHub](https://github.com/loco-rs/loco); [Loco InfoQ 소개](https://www.infoq.com/news/2024/02/loco-new-framework-rust-rails/); [Loco Hello World](https://loco.rs/blog/hello-world/); ["Introducing Loco" — Shuttle](https://www.shuttle.dev/blog/2023/12/20/loco-rust-rails).
- [Leapcell: "Unpacking the Tower Abstraction Layer in Axum and Tonic"](https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic).
- [Leapcell: "Unraveling sqlx Macros"](https://leapcell.io/blog/unraveling-sqlx-macros-compile-time-sql-verification-and-database-connectivity-in-rust).
- [Leapcell: "Building Minimal and Secure Rust Web Applications with Docker"](https://leapcell.io/blog/building-minimal-and-secure-rust-web-applications-with-docker).
- [Frankel: "Introduction to Tower"](https://blog.frankel.ch/introduction-tower/); [Frankel: "Rust and the JVM"](https://blog.frankel.ch/start-rust/7/).
- [Datadog: "How to monitor your Rust applications with OpenTelemetry"](https://www.datadoghq.com/blog/monitor-rust-otel/).
- [Phoronix: "Cloudflare Ditches Nginx For In-House, Rust-Written Pingora"](https://www.phoronix.com/news/CloudFlare-Pingora-No-Nginx).
- [Aarambh Dev Hub: "Rust Web Frameworks in 2026"](https://aarambhdevhub.medium.com/rust-web-frameworks-in-2026-axum-vs-actix-web-vs-rocket-vs-warp-vs-salvo-which-one-should-you-2db3792c79a2); [Aarambh Dev Hub: "Rust ORMs in 2026"](https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3).
- [Tech Tonic / Medium: "Spring Boot Webflux vs Rust (Axum)"](https://medium.com/deno-the-complete-reference/spring-boot-webflux-vs-rust-axum-hello-world-performance-28611da8bfc2).
- [JavaRevisited: "Rust vs Spring Boot vs Quarkus"](https://medium.com/javarevisited/rust-vs-spring-boot-vs-quarkus-the-performance-truth-nobody-talks-about-09941b196f8e).
- [Substack: "Goodbye Async-Std, Welcome Smol"](https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol).
- [Substack: "Tree Borrows Just Landed"](https://weeklyrust.substack.com/p/tree-borrows-just-landed).
- [BigGo News: "Rust's Learning Curve Debate"](https://biggo.com/news/202502181925_rust-learning-curve-debate).
- [byteiota: "Rust 2025 Survey: 45.5% Adoption, 41.6% Worry Complexity"](https://byteiota.com/rust-2025-survey-45-5-adoption-41-6-worry-complexity/).
- [muslrust GitHub](https://github.com/clux/muslrust); [Chainguard: "Distroless container images"](https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/).
- [Java Code Geeks: "Memory Safety and Performance — Rust's Theoretical Edge"](https://www.javacodegeeks.com/2025/12/memory-safety-and-performance-rusts-theoretical-edge-over-traditional-languages.html).
- [Rust Magazine: "How Tokio schedules tasks — A hard lesson learnt"](https://rustmagazine.org/issue-4/how-tokio-schedule-tasks/).
- [woodruff.dev: "The Borrow Checker — Rust's Tough-Love Mentor"](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/).
- [DEV.to: "Rust ownership and borrows: Fighting the borrow-checker"](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3).
- [DEV.to / Leapcell: "Rust Error Handling Compared: anyhow vs thiserror vs snafu"](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003).
- [DEV.to / Leapcell: "Rust Web Frameworks Compared: Actix vs Axum vs Rocket"](https://dev.to/leapcell/rust-web-frameworks-compared-actix-vs-axum-vs-rocket-4bad).
- [Shuttle: "A Guide to Rust ORMs in 2025"](https://www.shuttle.dev/blog/2024/01/16/best-orm-rust).

## 한국어 자료

- [한국 러스트 사용자 그룹 (rust-kr.org)](https://rust-kr.org/).
- [The Rust Programming Language 한국어판 — rinthel](https://rinthel.github.io/rust-lang-book-ko/).
- [Rust 한국어판 공식 (doc.rust-kr.org)](https://doc.rust-kr.org/).
- 김대현. ["Rust를 업무용 언어로 쓰다" — HappyProgrammer (Medium)](https://medium.com/happyprogrammer-in-jeju/rust%EB%A5%BC-%EC%97%85%EB%AC%B4%EC%9A%A9-%EC%96%B8%EC%96%B4%EB%A1%9C-%EC%93%B0%EB%8B%A4-7723cd2c0a59).
- Jinwoo Park. ["Rust를 회사 업무로 쓰고난지 5개월 정도"](https://pmnxis.github.io/posts/five_mothes_ago_from_using_rust_as_work_kr/).
- Option::None. ["4년간의 Rust 사용 후기" — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/).
- appleseed. ["일주일만에 Rust에 매료되다"](https://blog.appleseed.dev/post/fascinated-by-rust-in-a-week/).
- SmileCat. ["Rust 찍먹후기"](https://blog.smilecat.dev/posts/research-rust/).
- 비브로스 기술 블로그. ["웹프론트엔드 개발자의 Rust 돌려까기"](https://boostbrothers.github.io/experience/2022/03/28/rust-trun-around/).
- 이랜서 블로그. ["왜 많은 개발자들이 Rust로 이동할까?"](https://www.elancer.co.kr/blog/detail/808).
- scalalang2. ["Rust의 소유권 이야기" — CURG (Medium)](https://medium.com/curg/rust%EC%9D%98-%EC%86%8C%EC%9C%A0%EA%B6%8C-%EC%9D%B4%EC%95%BC%EA%B8%B0-a4c19c1b2c10).
- sangjinsu. ["🦀 Rust로 실전 백엔드 개발을 경험하다" (velog)](https://velog.io/@sangjinsu/Rust%EB%A1%9C-%EC%8B%A4%EC%A0%84-%EB%B0%B1%EC%97%94%EB%93%9C-%EA%B0%9C%EB%B0%9C%EC%9D%84-%EA%B2%BD%ED%97%98%ED%95%98%EB%8B%A4).
- Indo Yoon. ["실전 백엔드 러스트 Axum 프로그래밍 — 책 소개"](https://devbull.xyz/blog/axum-book).
- [한국 채용 — 디지털헬스케어 Rust 백엔드 개발자 (랠릿)](https://www.rallit.com/positions/3247/).
- [namu.wiki: Rust(프로그래밍 언어)](https://namu.wiki/w/Rust(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)); [Rust(프로그래밍 언어)/비판](https://namu.wiki/w/Rust(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)/%EB%B9%84%ED%8C%90).
