# 논문 리서치: Vercel·서버리스 엣지 인프라

Vercel 자체에 대한 학술 논문은 거의 없다. 대신 Vercel이 의존하는 핵심 기술 영역(serverless cold start, edge computing, FaaS 비용 모델, ISR/렌더링 전략) 의 이론적 기반과 실증 연구를 정리한다. 대상 독자가 비학문 개발자임을 고려해 결론·직관 중심으로 요약한다.

## 논문 1: Cold Start Latency in Serverless Computing — A Systematic Review, Taxonomy, and Future Directions
- 저자·연도: Mahmoudi, Khazaei et al., 2024 (개정판 v2)
- 발표처: ACM Computing Surveys
- DOI/arXiv: arXiv:2310.08437 / https://dl.acm.org/doi/abs/10.1145/3700875
- 요약: 100여 편 논문을 메타분석한 cold start systematic review. (1) caching 기반 (pre-warm, keep-alive), (2) application-level optimization (lightweight runtime, snapshot/restore), (3) AI/ML 예측 기반 prewarm 의 세 카테고리로 taxonomy.
- 핵심 결과: cold start는 함수 first invocation의 50-90%를 차지할 수 있음. snapshot/restore (Firecracker microVM 등) 가 latency를 100ms 이하로 떨어뜨리는 데 가장 효과적.
- 인용 가능한 문장: "cold start remains the dominant tail-latency contributor in production FaaS workloads."
- 독자 전달: Vercel Fluid compute가 cold start 영향 85% 절감을 주장하는 배경 (다중 요청 단일 인스턴스 + bytecode 최적화 + pre-warming) — 이 논문이 분류한 caching + application-level 접근의 결합. "Vercel이 새로 발명한 게 아니라, 학계가 분류해둔 모범 답안을 묶은 제품화"라고 설명할 수 있음.

## 논문 2: Serverless Edge Computing — A Taxonomy, Systematic Literature Review, Current Trends and Research Challenges
- 저자·연도: Cassel, Calheiros et al., 2025
- DOI/arXiv: arXiv:2502.15775
- 요약: serverless+edge가 결합한 시스템의 architectural design, QoS metric, 통신 모달리티 정리. Edge가 cloud-native serverless를 어떻게 변형시키는지 모델.
- 핵심 결과: edge serverless는 function placement·cold start·data locality 세 축의 trade-off가 핵심. 대부분 시스템은 둘만 잘하고 셋째를 희생.
- 인용: "the placement-cost-latency triangle remains the unsolved core of edge serverless."
- 독자 전달: Vercel Edge Functions/Middleware가 placement(전 세계 PoP)와 latency(<50ms)에 강하지만 data locality(DB가 멀면 의미 없음)를 사용자가 풀어야 한다는 점. Edge Config·Marketplace Storage가 그 빈틈을 메우려는 시도라고 해석.

## 논문 3: Performance Optimization for Edge-Cloud Serverless Platforms via Dynamic Task Placement
- 저자·연도: Aslanpour, Toosi et al., 2020
- DOI/arXiv: arXiv:2003.01310
- 요약: edge와 cloud 사이 함수 배치 최적화 휴리스틱. cold start, network RTT, 비용을 결합한 cost function.
- 핵심 결과: edge-only 또는 cloud-only 정책 대비 dynamic placement가 평균 latency 30-40% 감소.
- 독자 전달: "왜 Edge Function만 쓰면 만능이 아닌가" — 데이터·외부 API와 가까운 region에 두는 것이 latency 측면에서 더 나은 케이스가 많음. Vercel이 Node runtime을 region pinning 가능하게 둔 이유.

## 논문 4: Latency and Resource Consumption Analysis for Serverless Edge Analytics
- 저자·연도: Pinto et al., 2023
- 발표처: Journal of Cloud Computing (Springer)
- DOI: 10.1186/s13677-023-00485-9
- 요약: edge analytics 시나리오에서 serverless의 자원 소비·지연 패턴을 실측.
- 핵심 결과: 짧은 요청(50ms 미만)에서는 cloud serverless가, 1초 이상 처리에서는 edge가 우위. payload 크기가 1MB 넘으면 edge 우위가 사라짐.
- 독자 전달: Vercel Edge Function의 sweet spot — auth 검증·redirect·A/B 라우팅 같이 짧고 cacheable한 작업. 데이터 변환·파일 처리는 Node runtime이 정답.

## 논문 5: Green or Fast? Learning to Balance Cold Starts and Idle Carbon in Serverless Computing
- 저자·연도: 2026
- DOI/arXiv: arXiv:2602.23935
- 요약: keep-alive 시간을 길게 두면 cold start↓·탄소배출↑, 짧게 두면 반대. RL로 동적 튜닝하는 LACE-RL 프레임워크 제안.
- 핵심 결과: latency p99 12% 개선 + idle carbon 22% 감소 동시 달성.
- 독자 전달: serverless가 "탄소 친화적"이라는 통념을 흔드는 결과. Fluid compute의 multi-request-per-instance가 같은 문제를 우회하는 또 다른 답.

## 논문 6: Cold-Start Mitigation via Snapshot Restore (Firecracker microVM)
- 저자·연도: Agache et al., 2020
- 발표처: NSDI '20 (USENIX)
- 요약: AWS Lambda·Fargate가 사용하는 Firecracker microVM의 설계. 125ms 미만 부팅, snapshot resume.
- 인용: "We boot tens of thousands of microVMs per second, each in well under 125ms."
- 독자 전달: Vercel의 Node runtime이 어떤 인프라 위에서 도는지 — 결국 어딘가 비슷한 microVM/container 기반. cold start 자체는 사라지지 않고, 분산되고 가려질 뿐.

## 논문 7: ISR·rendering 전략 비교 (산업 분석)
- 학술 논문보다는 Vercel·Next.js팀의 RFC·기술 블로그가 일차 자료. PPR 정식 학술 발표는 없으나, 관련 캐싱 전략은 Akamai·Cloudflare의 stale-while-revalidate (RFC 5861, 2010) 에 뿌리.
- RFC 5861: https://datatracker.ietf.org/doc/html/rfc5861
- 독자 전달: ISR/PPR이 "마법"처럼 보여도 본질은 RFC 5861의 stale-while-revalidate를 framework 레벨로 통합한 것. 책에서 "근본은 15년 된 표준이다"라고 하나 짚으면 좋음.

## 수집 한계
- Vercel 자체를 분석한 peer-reviewed 논문은 거의 없음. 산업 white paper와 학술 cold start/edge serverless 연구를 매핑해 책의 이론적 깊이를 더하는 데 사용.
- PPR·ISR의 정량적 성능 비교 연구는 아직 학계에 거의 없음. 책은 Vercel/Cloudflare 자체 벤치마크를 인용하되 "공급자 자체 데이터"임을 명시 권장.
- 비용 모델(GB-hours·invocations)에 관한 학술 분석은 부재. Pricing 분석은 산업 자료가 일차 출처.
