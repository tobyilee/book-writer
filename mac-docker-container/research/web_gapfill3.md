<!-- 검색 시점: 2026-07-26 기준 -->
<!-- 3차 표적 보강 리서치 (gap-fill 3, `W3`) — 03_review_log.md Critical 1·2 해소 -->

# 웹 리서치 3차 보강: K8s 오브젝트 모델 · 배포 동선 · 레지스트리 인증 · 이미지 스토어 판정

> **이 문서의 목적.** `03_review_log.md`의 **Critical 1**(12장 K8s 오브젝트 모델·앱 배포 단계 근거 0건)과 **Critical 2**(요구 2의 "배포" — `docker login`·push 근거 0건), 그리고 C1이 함께 올린 **6장 그림 1의 판정 명령 부재**를 닫기 위한 표적 확보다.
>
> **⭐ 이번 회차의 방법론적 돌파 — `W2 §B-8`의 4회 실패를 해결했다.** WebFetch가 긴 페이지에서 TRUNCATED로 실패하는 문제를, **`curl`로 published HTML을 통째로 받아 태그를 벗겨 grep하는 경로**로 우회했다. 이 방식은 이 책의 남은 모든 1차 소스 확보에 재사용 가능하다. 절차:
> ```bash
> curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" "{URL}" -o page.html
> # <main> 추출 → script/style 제거 → <pre> 마킹 → 태그 제거 → html.unescape → grep -n -B2 -A8
> ```
>
> **⛔ 인용 원천 규율 (이번 회차에서 특별히 엄격히 지켰다).** `kubernetes/website` 저장소의 `main` 브랜치 마크다운은 **미발행 문서**다. 그것을 읽고 `kubernetes.io/docs/...`를 출처로 다는 것은 이 리서치가 막으려는 바로 그 오류다. 따라서 **`main` 마크다운은 위치 탐색(locator)에만 쓰고, 이 문서에 실린 모든 축자는 `curl`로 받은 published 페이지에서 나왔다.** (§T2에서 두 원천이 일치함을 교차 확인했다.)
>
> **소스 규율 승계.** 개인 블로그·Medium·Stack Overflow **0건 채택**. WebSearch 요약문 **0건 채택**(이번 회차는 WebSearch를 아예 쓰지 않았다 — 모든 URL이 지정됐거나 공식 사이트 내부 링크였다). 기존 `research/*.md`·`01_reference.md`·`02_plan.md`·`03_review_log.md` **수정·삭제 없음.**

---

## T1. Kubernetes 오브젝트 모델 — Pod / Deployment / ReplicaSet

- **상태:** ✅ **확보** (정의·최소 매니페스트·명령·롤링 업데이트 전부)

### T1-1. Deployment의 공식 정의와 ReplicaSet·Pod 관계

- **1차 소스:** Kubernetes — "Deployments" — https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ (발행일 미노출 — kubernetes.io/docs는 본문에 날짜를 인쇄하지 않는다. **검색: 2026-07-26**)
- **축자 인용:**
  > "A Deployment manages a set of Pods to run an application workload, usually one that doesn't maintain state."

  > "A Deployment provides declarative updates for Pods and ReplicaSets."

  > "You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments."

  ⭐ **경고 문장(축자) — 3층 관계를 독자가 오해하지 않게 하는 근거:**
  > "Do not manage ReplicaSets owned by a Deployment."

  ⭐ **3층이 실제로 어떻게 이어지는지 보여주는 축자(이 한 줄이 그림 1의 뼈대다):**
  > "The following is an example of a Deployment. It creates a ReplicaSet to bring up three nginx Pods"

  ReplicaSet 이름 규칙(축자):
  > "Notice that the name of the ReplicaSet is always formatted as [DEPLOYMENT-NAME]-[HASH]. This name will become the basis for the Pods which are created."
- **1차 소스 (ReplicaSet 쪽):** Kubernetes — "ReplicaSet" — https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/ (검색: 2026-07-26)
- **축자 인용:**
  > "A ReplicaSet's purpose is to maintain a stable set of replica Pods running at any given time. Usually, you define a Deployment and let that Deployment manage ReplicaSets automatically."

  ⭐ **왜 자바 독자가 ReplicaSet을 직접 쓰지 않아도 되는가(축자) — 소절 분량을 아끼는 결정적 문장:**
  > "A ReplicaSet ensures that a specified number of pod replicas are running at any given time. However, a Deployment is a higher-level concept that manages ReplicaSets and provides declarative updates to Pods along with a lot of other useful features. Therefore, we recommend using Deployments instead of directly using ReplicaSets, unless you require custom update orchestration or don't require updates at all."

  > "This actually means that you may never need to manipulate ReplicaSet objects: use a Deployment instead, and define your application in the spec section."

  소유 관계의 기계적 근거(축자):
  > "A ReplicaSet is linked to its Pods via the Pods' metadata.ownerReferences field, which specifies what resource the current object is owned by."

  > "Deployment is an object which can own ReplicaSets and update them and their Pods via declarative, server-side rolling updates." / "Deployments own and manage their ReplicaSets."
- **주의:**
  - "Deployment → ReplicaSet → Pod"는 **공식 문서가 직접 세우는 계층**이다. 다만 문서 어디에도 "3층 구조"라는 표현은 없다 — 저자의 도해 언어로 쓰되 **각 층의 관계 문장은 위 축자로 대라.**
  - `ownerReferences`는 ReplicaSet↔Pod 링크에 대한 서술이다. **Deployment↔ReplicaSet 링크가 같은 필드로 구현된다는 문장은 확인한 페이지에 없다** — "Deployments own and manage their ReplicaSets"까지만 쓰라.

### T1-2. ⭐ 최소 Deployment YAML — 공식 예제 전문 (축자)

- **1차 소스:** 위 Deployment 페이지, 예제 파일 이름은 문서에 `controllers/nginx-deployment.yaml`로 표기됨.
- **YAML 전문 (published 페이지에서 축자 추출 — `apiVersion`부터 한 글자도 바꾸지 않았다):**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment
    labels:
      app: nginx
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: nginx
    template:
      metadata:
        labels:
          app: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.14.2
          ports:
          - containerPort: 80
  ```
- **필드별 공식 해설(축자 — 저술가가 각 줄을 설명할 때 이 문장들을 그대로 쓰면 된다):**
  > "A Deployment named nginx-deployment is created, indicated by the .metadata.name field. This name will become the basis for the ReplicaSets and Pods which are created later."

  > "The Deployment creates a ReplicaSet that creates three replicated Pods, indicated by the .spec.replicas field."

  > "The .spec.selector field defines how the created ReplicaSet finds which Pods to manage. In this case, you select a label that is defined in the Pod template (app: nginx). However, more sophisticated selection rules are possible, as long as the Pod template itself satisfies the rule."

  > "The Pod template's specification, or .spec field, indicates that the Pods run one container, nginx, which runs the nginx Docker Hub image at version 1.14.2."

  ⛔ 라벨 충돌 경고(축자 — 실습 함정):
  > "You must specify an appropriate selector and Pod template labels in a Deployment (in this case, app: nginx). Do not overlap labels or selectors with other controllers (including other Deployments and StatefulSets). Kubernetes doesn't stop you from overlapping, and if multiple controllers have overlapping selectors those controllers might conflict and behave unexpectedly."
- **⭐ 두 번째 공식 예제 (더 짧고, 주석이 교육적이다 — 12장 실습에 이쪽이 더 맞을 수 있다):**
  - **1차 소스:** Kubernetes — "Run a Stateless Application Using a Deployment" — https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/ (검색: 2026-07-26). 문서 내 파일명 표기 `application/deployment.yaml`.
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment
  spec:
    selector:
      matchLabels:
        app: nginx
    replicas: 2 # tells deployment to run 2 pods matching the template
    template:
      metadata:
        labels:
          app: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.14.2
          ports:
          - containerPort: 80
  ```
  - ⚠️ **두 예제는 서로 다르다**(`labels` 유무, `replicas` 3 vs 2, 필드 순서). **섞지 마라.** 하나를 골라 그 페이지를 출처로 달아야 한다.
- **주의:** `nginx:1.14.2`는 **공식 문서가 쓰는 예제 태그**다. 그대로 옮겨도 되지만, 이 책은 9장에서 태그 고정을 가르치므로 **"공식 예제가 태그를 박아 쓴다"는 점을 오히려 회수 지점으로 쓸 수 있다.** ⛔ 다만 `nginx:1.14.2`가 "최신"이거나 "권장"이라고 쓰면 ❌ — 문서는 그런 말을 하지 않는다.

### T1-3. `kubectl apply` → `get` → `describe` → `rollout status` 공식 실행 흐름 (축자)

- **1차 소스:** 위 Deployment 페이지 + run-stateless 페이지 (둘 다 검색: 2026-07-26)
- **명령·출력 축자 (Deployment 페이지, 순서대로):**
  ```bash
  kubectl apply -f https://k8s.io/examples/controllers/nginx-deployment.yaml
  ```
  ```
  NAME               READY   UP-TO-DATE   AVAILABLE   AGE
  nginx-deployment   0/3     0            0           1s
  ```
  컬럼 해설(축자 — 독자가 `READY 0/3`을 보고 당황하지 않게 하는 근거):
  > "NAME lists the names of the Deployments in the namespace." / "READY displays how many replicas of the application are available to your users. It follows the pattern ready/desired." / "UP-TO-DATE displays the number of replicas that have been updated to achieve the desired state." / "AVAILABLE displays how many replicas of the application are available to your users." / "AGE displays the amount of time that the application has been running."

  ```bash
  kubectl rollout status deployment/nginx-deployment
  ```
  ```
  Waiting for rollout to finish: 2 out of 3 new replicas have been updated...
  deployment "nginx-deployment" successfully rolled out
  ```
  ```
  NAME               READY   UP-TO-DATE   AVAILABLE   AGE
  nginx-deployment   3/3     3            3           18s
  ```
  ⭐ **ReplicaSet이 실제로 생겼음을 독자가 눈으로 확인하는 지점(축자):**
  ```bash
  kubectl get rs
  ```
  ```
  NAME                          DESIRED   CURRENT   READY   AGE
  nginx-deployment-75675f5897   3         3         3       18s
  ```
  ```bash
  kubectl get pods --show-labels
  ```
  ```
  NAME                                READY     STATUS    RESTARTS   AGE       LABELS
  nginx-deployment-75675f5897-7ci7o   1/1       Running   0          18s       app=nginx,pod-template-hash=75675f5897
  nginx-deployment-75675f5897-kzszj   1/1       Running   0          18s       app=nginx,pod-template-hash=75675f5897
  nginx-deployment-75675f5897-qqcnn   1/1       Running   0          18s       app=nginx,pod-template-hash=75675f5897
  ```
  > "The created ReplicaSet ensures that there are three nginx Pods."
- **`kubectl describe deployment` 출력 (run-stateless 페이지 축자, 발췌):**
  ```
  Name:     nginx-deployment
  Namespace:    default
  Labels:     app=nginx
  Annotations:    deployment.kubernetes.io/revision=1
  Selector:   app=nginx
  Replicas:   2 desired | 2 updated | 2 total | 2 available | 0 unavailable
  StrategyType:   RollingUpdate
  MinReadySeconds:  0
  RollingUpdateStrategy:  1 max unavailable, 1 max surge
  ...
  NewReplicaSet:    nginx-deployment-1771418926 (2/2 replicas created)
  ```
  ⭐ **`StrategyType: RollingUpdate`가 출력에 그대로 찍힌다** — T1-4의 "기본값이다"를 독자가 자기 화면에서 확인한다.
  ```bash
  kubectl describe deployment nginx-deployment
  kubectl get pods -l app=nginx
  kubectl describe pod <pod-name>
  ```
- **⛔ 주의:** run-stateless 페이지의 `describe` 출력 예시는 **`CreationTimestamp: Tue, 30 Aug 2016`** 로 낡았다. 컬럼·필드 이름만 인용하고 **날짜·해시 값은 그대로 옮기지 마라**(`W2 §A-7`의 `docker history` 주의와 같은 성격).

### T1-4. 롤링 업데이트가 기본 전략이라는 근거 + 이미지 태그를 바꿔 배포하는 공식 방법

- **1차 소스:** 위 Deployment 페이지 (검색: 2026-07-26)
- **⭐ 기본값 축자 (이 한 문장이 근거다):**
  > ".spec.strategy specifies the strategy used to replace old Pods by new ones. .spec.strategy.type can be \"Recreate\" or \"RollingUpdate\". \"RollingUpdate\" is the default value."

  > "The Deployment updates Pods in a rolling update fashion (gradually scale down the old ReplicaSets and scale up the new one) when .spec.strategy.type==RollingUpdate."

  > "All existing Pods are killed before new ones are created when .spec.strategy.type==Recreate."

  기본 파라미터(축자): `maxUnavailable` — "The default value is 25%." / `maxSurge` — "The default value is 25%."
- **⭐ 롤아웃이 언제 트리거되는가 (축자 — 실습에서 가장 자주 오해하는 지점):**
  > "A Deployment's rollout is triggered if and only if the Deployment's Pod template (that is, .spec.template) is changed, for example if the labels or container images of the template are updated. Other updates, such as scaling the Deployment, do not trigger a rollout."
- **이미지 교체 — 공식 3경로 (전부 축자):**
  1. `kubectl set image`
     ```bash
     kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.16.1
     ```
     또는
     ```bash
     kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
     ```
     문서 해설(축자): "where deployment/nginx-deployment indicates the Deployment, nginx indicates the Container the update will take place and nginx:1.16.1 indicates the new image and its tag."
     출력(축자): `deployment.apps/nginx-deployment image updated`
  2. `kubectl edit`
     ```bash
     kubectl edit deployment/nginx-deployment
     ```
     출력(축자): `deployment.apps/nginx-deployment edited`
  3. **매니페스트 수정 후 재-apply** (run-stateless 페이지 축자):
     > "You can update the deployment by applying a new YAML file. This YAML file specifies that the deployment should be updated to use nginx 1.16.1."
     ```yaml
     image: nginx:1.16.1 # Update the version of nginx from 1.14.2 to 1.16.1
     ```
     ```bash
     kubectl apply -f https://k8s.io/examples/application/deployment-update.yaml
     ```
  - 결과 확인(축자): "Run kubectl get rs to see that the Deployment updated the Pods by creating a new ReplicaSet and scaling it up to 3 replicas, as well as scaling down the old ReplicaSet to 0 replicas."
- **⭐ Phase 2·4 활용:** **9장(태그·digest) → 12장의 회수 사슬이 여기서 완성된다.** "태그를 바꿔 apply하면 새 ReplicaSet이 생기고 옛것이 0으로 내려간다"는 것이 공식 축자로 확보됐고, `W2 §A-5`의 `imagePullPolicy` 4갈래가 그 위에 얹힌다. **다만 두 사실을 인과로 잇는 문장은 저자 해석이다** — 공식 문서가 "태그를 안 바꾸고 같은 태그로 재-apply하면 어떻게 되는가"를 서술한 문장은 **확인한 페이지에 없다**(NOT_PRESENT). ⛔ **"같은 태그로 apply하면 롤아웃이 안 일어난다"고 단정하지 마라** — 위 "if and only if `.spec.template` is changed"에서 독자가 스스로 유추하게 두고, 유추임을 밝혀라.

### T1-5. Pod의 공식 정의

- **1차 소스:** Kubernetes — "Pods" — https://kubernetes.io/docs/concepts/workloads/pods/ (검색: 2026-07-26)
- **⭐ 축자 (첫 문장이 곧 "가장 작은 배포 단위"의 근거다):**
  > "Pods are the smallest deployable units of computing that you can create and manage in Kubernetes."

  > "A Pod (as in a pod of whales or pea pod) is a group of one or more containers, with shared storage and network resources, and a specification for how to run the containers. A Pod's contents are always co-located and co-scheduled, and run in a shared context. A Pod models an application-specific \"logical host\": it contains one or more application containers which are relatively tightly coupled."

  ⭐ **2장(네임스페이스·cgroups)의 회수 지점 — 축자:**
  > "The shared context of a Pod is a set of Linux namespaces, cgroups, and potentially other facets of isolation - the same things that isolate a container."

  > "A Pod is similar to a set of containers with shared namespaces and shared filesystem volumes."

  컨테이너 여러 개(축자, 두 용법):
  > "Pods that run a single container. The \"one-container-per-Pod\" model is the most common Kubernetes use case; in this case, you can think of a Pod as a wrapper around a single container; Kubernetes manages Pods rather than managing the containers directly."

  > "Pods that run multiple containers that need to work together. A Pod can encapsulate an application composed of multiple co-located containers that are tightly coupled and need to share resources."

  ⛔ 남용 경고(축자 — 자바 개발자가 사이드카를 남발하지 않도록):
  > "Grouping multiple co-located and co-managed containers in a single Pod is a relatively advanced use case. You should use this pattern only in specific instances in which your containers are tightly coupled."

  > "You don't need to run multiple containers to provide replication (for resilience or capacity); if you need multiple replicas, see Workload management."

  ⭐ **왜 독자가 Pod를 직접 만들지 않는가(축자) — Deployment로 넘어가는 이음말:**
  > "Pods are generally not created directly and are created using workload resources."

  > "Usually you don't need to create Pods directly, even singleton Pods. Instead, create them using workload resources such as Deployment or Job."
- **최소 Pod YAML (축자, 문서 내 파일명 `pods/simple-pod.yaml`):**
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: nginx
  spec:
    containers:
    - name: nginx
      image: nginx:1.14.2
      ports:
      - containerPort: 80
  ```
- **주의:** ⭐ 2장 회수용으로 특히 좋은 축자 — Pod 페이지가 **"a set of Linux namespaces, cgroups"**를 명시적으로 말한다. 이 책이 2장에서 심은 개념이 12장에서 K8s 용어로 되돌아오는 근거를 **저자 해석 없이** 댈 수 있다.

### T1-6. 초심자용 Deployment 서술 (튜토리얼 — 자기치유 프레이밍)

- **1차 소스:** Kubernetes — "Using kubectl to Create a Deployment" — https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/ (검색: 2026-07-26)
- **축자:**
  > "A Deployment is responsible for creating and updating instances of your application."

  ⭐ **자기치유(축자) — "왜 Pod를 직접 안 만드는가"의 실무적 답:**
  > "Once the application instances are created, a Kubernetes Deployment controller continuously monitors those instances. If the Node hosting an instance goes down or is deleted, the Deployment controller replaces the instance with an instance on another Node in the cluster. This provides a self-healing mechanism to address machine failure or maintenance."

  > "In a pre-orchestration world, installation scripts would often be used to start applications, but they did not allow recovery from machine failure."

  kubectl 문법 규정(축자):
  > "The common format of a kubectl command is: kubectl action resource."
- **⭐⭐ 이 책에 특히 중요한 축자 — 튜토리얼 자체가 아키텍처 경고를 단다:**
  > "This tutorial uses a container that requires the AMD64 architecture. If you are using minikube on a computer with a different CPU architecture, you could try using minikube with a driver that can emulate AMD64. For example, the Docker Desktop driver can do this."

  → **쿠버네티스 공식 입문 튜토리얼조차 Apple Silicon 독자에게 별도 안내를 단다.** 이 책의 논제("맥은 다르다")를 **공식 문서 스스로 증언**하는 재료다. 12장 오프닝 또는 「앱을 띄운다」 소절의 도입에 강력하다.
- **주의:** 이 페이지는 `kubectl create deployment`(명령형)를 쓴다. **이 책은 `kubectl apply -f`(선언형)로 가는 편이 낫다** — `W2 §A-5`의 `imagePullPolicy` 4갈래와 9장의 매니페스트 논의가 전부 선언형 전제다. 명령형 경로를 실습에 섞으면 축이 흔들린다.

---

## T2. Service — `W2 §B-8`이 4회 실패한 페이지, **우회 성공**

- **상태:** ✅ **완전 확보** — **`W2 §F-1`이 폐기했던 NodePort 기본 포트 범위를 되살렸다.**

### T2-0. 시도 경로 기록 (정직하게)

| # | 경로 | 결과 |
|---|---|---|
| 1 | `curl` → `raw.githubusercontent.com/kubernetes/website/main/content/en/docs/concepts/services-networking/service.md` | ✅ HTTP 200, 45,284 bytes 수신. **위치 탐색 성공 — 그러나 `main` 브랜치는 미발행 문서이므로 인용 원천으로 채택하지 않았다.** |
| 2 | `python urllib` → `kubernetes.io/docs/concepts/services-networking/service/` | ❌ `SSLCertVerificationError` (로컬 CA 번들 문제) |
| 3 | **`curl -sL` → 같은 published URL → HTML 태그 제거 → grep** | ✅ **HTTP 200, 576,194 bytes. 전문 확보. 이 문서의 모든 T2 축자는 여기서 나왔다.** |
| 4 | 경로 1과 경로 3의 교차 대조 (NodePort 범위·타입 4종) | ✅ **두 원천이 일치.** `main`에만 있는 미발행 변경으로 인한 오염 없음 |

→ **`W2 §B-8`의 실패는 페이지의 문제가 아니라 도구(WebFetch 길이 절단)의 문제였다.** 같은 URL이 `curl`로는 한 번에 열린다.

### T2-1. Service의 공식 정의 + 왜 필요한가 (Pod IP 불안정성)

- **1차 소스:** Kubernetes — "Service" — https://kubernetes.io/docs/concepts/services-networking/service/ (발행일 미노출. **검색: 2026-07-26**)
- **⭐⭐ 축자 (동기 부분 전문 — 소절 오프닝으로 그대로 쓸 수 있다):**
  > "In Kubernetes, a Service is a method for exposing a network application that is running as one or more Pods in your cluster."

  > "If you use a Deployment to run your app, that Deployment can create and destroy Pods dynamically. From one moment to the next, you don't know how many of those Pods are working and healthy; you might not even know what those healthy Pods are named."

  ⭐ **Pod IP가 불안정하다는 공식 근거(축자):**
  > "Kubernetes Pods are created and destroyed to match the desired state of your cluster. Pods are ephemeral resources (you should not expect that an individual Pod is reliable and durable). Each Pod gets its own IP address (Kubernetes expects network plugins to ensure this). For a given Deployment in your cluster, the set of Pods running in one moment in time could be different from the set of Pods running that application a moment later."

  ⭐ **문제 제기 문장(축자) — 그대로 옮기면 소절이 열린다:**
  > "This leads to a problem: if some set of Pods (call them \"backends\") provides functionality to other Pods (call them \"frontends\") inside your cluster, how do the frontends find out and keep track of which IP address to connect to, so that the frontend can use the backend part of the workload?"

  > "Enter Services."

  API 규정(축자):
  > "The Service API, part of Kubernetes, is an abstraction to help you expose groups of Pods over a network. Each Service object defines a logical set of endpoints (usually these endpoints are Pods) along with a policy about how to make those pods accessible."

  > "The set of Pods targeted by a Service is usually determined by a selector that you define."

  Ingress와의 관계(축자 — `W2 §B-2`와 이어진다):
  > "Ingress is not a Service type, but it acts as the entry point for your cluster."
- **주의:** "Pod IP는 바뀐다"를 **"Pod가 재시작되면 IP가 바뀐다"로 좁혀 쓰지 마라** — 확인한 페이지는 그 인과를 직접 말하지 않는다. 문서가 말하는 것은 "Pod는 ephemeral하고, 각각 자기 IP를 갖고, 어느 시점의 Pod 집합이 다음 시점과 다를 수 있다"까지다.

### T2-2. ⭐ 최소 Service YAML — 공식 예제 전문 (축자)

- **1차 소스:** 위 Service 페이지, 문서 내 파일명 표기 `service/simple-service.yaml`.
- **YAML 전문 (축자):**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: my-service
  spec:
    selector:
      app.kubernetes.io/name: MyApp
    ports:
      - protocol: TCP
        port: 80
        targetPort: 9376
  ```
- **문서의 해설(축자 — `selector`/`port`/`targetPort` 관계를 이 문장들로 설명하라):**
  > "For example, suppose you have a set of Pods that each listen on TCP port 9376 and are labelled as app.kubernetes.io/name=MyApp. You can define a Service to publish that TCP listener"

  ⭐ **기본 타입이 `ClusterIP`라는 근거 #1 (축자):**
  > "Applying this manifest creates a new Service named \"my-service\" with the default ClusterIP service type. The Service targets TCP port 9376 on any Pod with the app.kubernetes.io/name: MyApp label."

  > "Kubernetes assigns this Service an IP address (the cluster IP), that is used by the virtual IP address mechanism."

  ⭐ **컨트롤러의 동작(축자) — "Service가 Pod를 어떻게 계속 따라가는가":**
  > "The controller for that Service continuously scans for Pods that match its selector, and then makes any necessary updates to the set of EndpointSlices for the Service."

  ⭐ **`port` ↔ `targetPort` 관계(축자):**
  > "A Service can map any incoming port to a targetPort. By default and for convenience, the targetPort is set to the same value as the port field."

  이름 붙인 포트(축자):
  > "Port definitions in Pods have names, and you can reference these names in the targetPort attribute of a Service."
- **이름 붙인 포트 예제 (축자, Service + Pod 한 쌍 — 자바 앱 실습에 그대로 응용 가능):**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: nginx-service
  spec:
    selector:
      app.kubernetes.io/name: proxy
    ports:
    - name: name-of-service-port
      protocol: TCP
      port: 80
      targetPort: http-web-svc

  ---
  apiVersion: v1
  kind: Pod
  metadata:
    name: nginx
    labels:
      app.kubernetes.io/name: proxy
  spec:
    containers:
    - name: nginx
      image: nginx:stable
      ports:
        - containerPort: 80
          name: http-web-svc
  ```
  포트 이름 규칙(축자): "names for ports must only contain lowercase alphanumeric characters and -. Port names must also start and end with an alphanumeric character. For example, the names 123-abc and web are valid, but 123_abc and -web are not."

### T2-3. ⭐ Service 타입 4종 — 공식 설명 전문 (축자)

- **1차 소스:** 동일 페이지, "Service type" 섹션.
- **축자 (4종 전문. 원문이 정의 목록(`<dl>`) 구조라 태그 제거 시 항목명이 설명에 붙어 나온다 — 아래는 항목별로 분리해 옮긴 것이며 문장은 원문 그대로다):**
  > "For some parts of your application (for example, frontends) you may want to expose a Service onto an external IP address, one that's accessible from outside of your cluster. Kubernetes Service types allow you to specify what kind of Service you want."

  | 타입 | 공식 설명 (축자) |
  |---|---|
  | **`ClusterIP`** | "Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. **This is the default that is used if you don't explicitly specify a type for a Service.** You can expose the Service to the public internet using an Ingress or a Gateway." |
  | **`NodePort`** | "Exposes the Service on each Node's IP at a static port (the NodePort). To make the node port available, Kubernetes sets up a cluster IP address, the same as if you had requested a Service of `type: ClusterIP`." |
  | **`LoadBalancer`** | "Exposes the Service externally using an external load balancer. **Kubernetes does not directly offer a load balancing component; you must provide one, or you can integrate your Kubernetes cluster with a cloud provider.**" |
  | **`ExternalName`** | "Maps the Service to the contents of the externalName field (for example, to the hostname api.foo.bar.example). The mapping configures your cluster's DNS server to return a CNAME record with that external hostname value. No proxying of any kind is set up." |

  ⭐ **타입이 중첩 구조라는 축자 (그림 1의 계단식 표현 근거):**
  > "The type field in the Service API is designed as nested functionality - each level adds to the previous. However there is an exception to this nested design. You can define a LoadBalancer Service by disabling the load balancer NodePort allocation."

  ⭐ **`ClusterIP`가 기본값이라는 근거 #2·#3 (축자):**
  > "type: ClusterIP — This default Service type assigns an IP address from a pool of IP addresses that your cluster has reserved for that purpose. Several of the other types for Service build on the ClusterIP type as a foundation."

  > "you make a Service with .spec.type set to ClusterIP (which is also the default for type)"
- **주의:** `ClusterIP`가 기본값이라는 사실은 **같은 페이지에서 세 군데가 독립적으로 말한다**(위 #1·#2·#3). fact-checker 대조에 여유가 있다.

### T2-4. ⭐⭐ NodePort 기본 포트 범위 — **되살렸다 (30000–32767)**

> **`W2 §F-1`은 이 값을 "4개 페이지에서 시도 실패, ⛔ 책에 쓰지 마라"로 폐기했다. 이번 회차에서 published 페이지 축자로 확인했으므로 판정을 뒤집는다.**

- **상태:** ✅ **확보 — 인용 허용.** 같은 published 페이지에서 **세 곳이 독립적으로 이 값을 인쇄한다.**
- **1차 소스:** 동일 Service 페이지 "type: NodePort" 섹션 (검색: 2026-07-26)
- **축자 #1 (기본 범위 — 이것이 근거다):**
  > "If you set the type field to NodePort, the Kubernetes control plane allocates a port from a range specified by `--service-node-port-range` flag (default: 30000-32767). Each node proxies that port (the same port number on every Node) into your Service. Your Service reports the allocated port in its `.spec.ports[*].nodePort` field."
- **축자 #2 (YAML 주석 안에 다시 등장):**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: my-service
  spec:
    type: NodePort
    selector:
      app.kubernetes.io/name: MyApp
    ports:
      - port: 80
        # By default and for convenience, the `targetPort` is set to
        # the same value as the `port` field.
        targetPort: 80
        # Optional field
        # By default and for convenience, the Kubernetes control plane
        # will allocate a port from a range (default: 30000-32767)
        nodePort: 30007
  ```
  문서 해설(축자): "Here is an example manifest for a Service of `type: NodePort` that specifies a NodePort value (30007, in this example)."
- **축자 #3 (밴드 분할 — ⚠️ 이게 붙어 있으므로 "30000–32767"만 떼어 쓰면 불완전하다):**
  > "To avoid this problem, the port range for NodePort services is divided into two bands. Dynamic port assignment uses the upper band by default, and it may use the lower band once the upper band has been exhausted. Users can then allocate from the lower band with a lower risk of port collision."

  > "When using the default NodePort range 30000-32767, the bands are partitioned as follows: Static band: 30000-30085 / Dynamic band: 30086-32767"
- **직접 지정 시 주의(축자):**
  > "If you want a specific port number, you can specify a value in the nodePort field. The control plane will either allocate you that port or report that the API transaction failed. This means that you need to take care of possible port collisions yourself."
- **⛔ 주의 — 이 값을 쓸 때의 정확한 표현:**
  - **"30000–32767"은 `--service-node-port-range` 플래그의 *기본값*이다.** 클러스터 운영자가 바꿀 수 있다. **"쿠버네티스의 NodePort는 30000–32767이다"라고 조건 없이 쓰면 부정확하다.** 정확한 서술: "기본값은 30000–32767이며, `--service-node-port-range`로 바뀔 수 있다."
  - **정적/동적 밴드 분할(30000–30085 / 30086–32767)은 같은 섹션에 붙어 있는 조건이다.** 책이 "직접 `nodePort`를 박아라"라고 권한다면 이 밴드를 언급하지 않는 편이 오히려 안전하다 — 언급하려면 축자 #3 전체를 병기하라. **부분 인용이 가장 위험한 지점이다.**
  - `PROBE`·`REF` 등 기존 문서의 "🕒 미확인 / 쓰지 말 것" 표기는 **이 문서(`W3 §T2-4`)로 대체된다.** 저술가는 `W2 §B-8`·`§F-1`이 아니라 여기를 근거로 삼아라.

### T2-5. 로컬 클러스터에서 `LoadBalancer`가 pending에 머무는 근거

- **상태:** ⚠️ **부분 — 공식 Service 페이지는 "pending"이라는 단어를 쓰지 않는다.** 원인만 말하고 증상은 말하지 않는다.
- **1차 소스:** 동일 Service 페이지, "type: LoadBalancer" 섹션 (검색: 2026-07-26)
- **축자 (원인 쪽 — 이것이 공식 근거의 전부다):**
  > "Exposes the Service externally using an external load balancer. **Kubernetes does not directly offer a load balancing component; you must provide one, or you can integrate your Kubernetes cluster with a cloud provider.**"

  > "On cloud providers which support external load balancers, setting the type field to LoadBalancer provisions a load balancer for your Service. The actual creation of the load balancer happens asynchronously, and information about the provisioned balancer is published in the Service's `.status.loadBalancer` field."

  > "To implement a Service of type: LoadBalancer, Kubernetes typically starts off by making the changes that are equivalent to you requesting a Service of type: NodePort. The cloud-controller-manager component then configures the external load balancer to forward traffic to that assigned node port."
- **LoadBalancer 예제 YAML (축자 — `status.loadBalancer.ingress`가 채워진 상태를 보여준다):**
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: my-service
  spec:
    selector:
      app.kubernetes.io/name: MyApp
    ports:
      - protocol: TCP
        port: 80
        targetPort: 9376
    clusterIP: 10.0.171.239
    type: LoadBalancer
  status:
    loadBalancer:
      ingress:
      - ip: 192.0.2.127
  ```
- **⛔ 주의 — 두 근거를 어떻게 조합할 것인가 (fact-checker 대비):**
  - **"pending"이라는 관측 증상의 축자는 여전히 minikube 문서에만 있다** — `W2 §B-6`: "Note that without minikube tunnel, Kubernetes will show the external IP as 'pending'."
  - 따라서 정확한 서술은 **2층으로 쌓는 것**이다: ① *왜* — "쿠버네티스는 로드 밸런서 컴포넌트를 직접 제공하지 않는다. 직접 대거나 클라우드 프로바이더와 통합해야 한다"(**Service 공식 문서 축자, `W3 §T2-5`**) → ② *그래서 화면에는* — "`minikube tunnel` 없이는 external IP가 `pending`으로 표시된다"(**minikube 공식 문서 축자, `W2 §B-6`**).
  - ⛔ **Service 공식 문서를 "pending"의 출처로 달지 마라.** 확인한 페이지에 그 단어가 없다.
  - `cloud-provider-kind`(`W2 §B-3b`)가 존재하는 이유도 정확히 이 구멍이다 — "must provide one"의 그 "one"을 kind 환경에 대신 대주는 것. **이 연결은 저자 해석이지만 두 문서 축자가 나란히 있으므로 안전하다.**

---

## T3. 앱을 클러스터에 올리는 최소 동선 — `kubectl` 레퍼런스와 트러블슈팅

- **상태:** ✅ **확보** (핵심 명령 전부 + 세 가지 실패 상태 전부 공식 정의 확보)

### T3-1. `kubectl` 핵심 명령 — 공식 치트시트 축자

- **1차 소스:** Kubernetes — "kubectl Quick Reference" — https://kubernetes.io/docs/reference/kubectl/quick-reference/ (발행일 미노출. **검색: 2026-07-26**)
- **`kubectl apply`의 공식 위상(축자 — 선언형을 고르는 근거):**
  > "apply manages applications through files defining Kubernetes resources. It creates and updates resources in a cluster through running kubectl apply. **This is the recommended way of managing Kubernetes applications on production.**"
- **명령 축자 (전부 원문 주석 포함):**
  ```bash
  kubectl apply -f ./my-manifest.yaml                 # create resource(s)
  kubectl apply -f ./my1.yaml -f ./my2.yaml           # create from multiple files
  kubectl apply -f ./dir                              # create resource(s) in all manifest files in dir
  ```
  ```bash
  # Get commands with basic output
  kubectl get services                          # List all services in the namespace
  kubectl get pods --all-namespaces             # List all pods in all namespaces
  kubectl get pods -o wide                      # List all pods in the current namespace, with more details
  kubectl get deployment my-dep                 # List a particular deployment
  kubectl get pods                              # List all pods in the namespace
  kubectl get pod my-pod -o yaml                # Get a pod's YAML

  # Describe commands with verbose output
  kubectl describe nodes my-node
  kubectl describe pods my-pod
  ```
  ```bash
  kubectl logs my-pod                                 # dump pod logs (stdout)
  kubectl logs my-pod --previous                      # dump pod logs (stdout) for a previous instantiation of a container
  kubectl logs my-pod -c my-container                 # dump pod container logs (stdout, multi-container case)
  kubectl logs -f my-pod                              # stream pod logs (stdout)
  kubectl logs -l name=myLabel                        # dump pod logs, with label name=myLabel (stdout)
  ```
  ```bash
  kubectl exec my-pod -- ls /                         # Run command in existing pod (1 container case)
  kubectl exec --stdin --tty my-pod -- /bin/sh        # Interactive shell access to a running pod (1 container case)
  kubectl exec my-pod -c my-container -- ls /         # Run command in existing pod (multi-container case)
  kubectl attach my-pod -i                            # Attach to Running Container
  kubectl debug my-pod -it --image=busybox:1.28       # Create an interactive debugging session within existing pod and immediately attach to it
  ```
  ```bash
  kubectl delete -f ./pod.json                        # Delete a pod using the type and name specified in pod.json
  kubectl delete pod unwanted --now                   # Delete a pod with no grace period
  kubectl delete pod,service baz foo                  # Delete pods and services with same names "baz" and "foo"
  kubectl delete pods,services -l name=myLabel        # Delete pods and services with label name=myLabel
  ```
  ⭐ **워크로드 축약형 (축자 — Deployment 이름만 알면 되는 형태. 12장 실습에 이쪽이 편하다):**
  ```bash
  kubectl logs deploy/my-deployment                         # dump Pod logs for a Deployment (single-container case)
  kubectl logs deploy/my-deployment -c my-container         # dump Pod logs for a Deployment (multi-container case)
  kubectl exec deploy/my-deployment -- ls                   # run command in first Pod and first container in Deployment (single- or multi-container cases)
  ```
- **주의:** ⛔ `kubectl debug`·`kubectl attach`는 이 책의 범위 밖일 가능성이 높다. **`--image=busybox:1.28`을 실습으로 실으려면 arm64 지원 여부를 별도 확인해야 한다(🕒 미확인).** 안 쓰는 편이 안전하다.

### T3-2. ⭐ `kubectl port-forward` — 맥 독자의 주 경로

- **상태:** ✅ 확보 (`W2 §B-8`의 generated 레퍼런스 + 이번 회차의 치트시트 예제로 **`svc/` 형태가 보강**됐다)
- **1차 소스:** 위 quick-reference (검색: 2026-07-26) / 문법 축자는 `W2 §B-8`(https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/)
- **⭐ `svc/` 형태 축자 (task가 요구한 정확한 문법 — 치트시트에서 확보):**
  ```bash
  kubectl port-forward svc/my-service 5000                  # listen on local port 5000 and forward to port 5000 on Service backend
  kubectl port-forward svc/my-service 5000:my-service-port  # listen on local port 5000 and forward to Service target port with name <my-service-port>
  kubectl port-forward deploy/my-deployment 5000:6000       # listen on local port 5000 and forward to port 6000 on a Pod created by <my-deployment>
  kubectl port-forward my-pod 5000:6000                     # Listen on port 5000 on the local machine and forward to port 6000 on my-pod
  ```
- **`W2 §B-8`에서 승계할 축자 (중복 조사하지 않았다):** Synopsis `kubectl port-forward TYPE/NAME [options] [LOCAL_PORT:]REMOTE_PORT ...` / "Forward one or more local ports to a pod." / ⭐ 함정: "The forwarding session ends when the selected pod terminates, and a rerun of the command is needed to resume forwarding." / `kubectl port-forward service/myservice 8443:https`
- **⛔ 주의 — `LOCAL_PORT:REMOTE_PORT`의 의미가 대상에 따라 다르다:**
  - `svc/my-service 5000:my-service-port` — 오른쪽이 **Service의 target port 이름**이다.
  - `deploy/my-deployment 5000:6000` — 오른쪽이 **Pod의 포트**다("forward to port 6000 on a Pod created by").
  - **"Service의 `port`로 포워딩된다"고 뭉뚱그리지 마라.** 치트시트가 대상별로 다르게 설명한다.
  - ⭐ **왜 이게 맥 독자의 주 경로인가:** `LoadBalancer`는 로컬에서 뜨지 않고(§T2-5), kind의 LoadBalancer IP는 **맥에서 도달 불가**다(`W2 §B-3b`). `port-forward`만이 추가 컴포넌트·`sudo` 없이 작동한다. **다만 "port-forward가 맥에서 권장 경로다"라는 공식 문장은 없다 — 저자의 결론임을 밝혀라.**

### T3-3. ⭐ `kubectl config current-context` / `use-context` — 실습 전 컨텍스트 확인

- **상태:** ✅ 확보
- **1차 소스:** 위 quick-reference, "Kubectl context and configuration" 섹션 (검색: 2026-07-26)
- **축자 (원문 주석 포함):**
  ```bash
  kubectl config get-contexts                          # display list of contexts
  kubectl config get-contexts -o name                  # get all context names
  kubectl config current-context                       # display the current-context
  kubectl config use-context my-cluster-name           # set the default context to my-cluster-name
  ```
  ```bash
  # permanently save the namespace for all subsequent kubectl commands in that context.
  kubectl config set-context --current --namespace=ggckad-s2
  ```
  ⭐ **공식 치트시트가 직접 싣는 alias (축자 — 계획 12장의 "처방 스펙트럼 7단계"에 붙일 공식 재료):**
  ```bash
  alias kx='f() { [ "$1" ] && kubectl config use-context $1 || kubectl config current-context ; } ; f'
  alias kn='f() { [ "$1" ] && kubectl config set-context --current --namespace $1 || kubectl config view --minify | grep namespace | cut -d" " -f6 ; } ; f'
  ```
  치트시트 주석(축자): "short alias to set/show context/namespace (only works for bash and bash-compatible shells, current context to be set before using kn to set namespace)"
- **⛔ 주의:** **"실습 전에 컨텍스트를 확인해야 한다"는 규범적 문장은 공식 문서에 없다(NOT_PRESENT).** 확보한 것은 *명령의 존재와 용법*뿐이다. 당위는 `REF §3 A11`(운영 배포를 실수로 지운 사고담)과 `PROBE §5`(실측: 로컬 클러스터가 둘인데 활성 컨텍스트가 원격 EKS)로 대야 한다 — **그 재료는 이미 계획 12장 소절 4에 배정돼 있다.** 이 절은 그 소절의 *명령 근거*만 보탠다.

### T3-4. 트러블슈팅 — `describe`의 Events / `Pending` / `ImagePullBackOff` / `CrashLoopBackOff`

- **상태:** ✅ **확보 — 세 상태 모두 공식 정의를 찾았다** (단, 서로 **다른 세 페이지**에 흩어져 있다)

#### (a) 디버깅의 첫 걸음 — `kubectl describe`

- **1차 소스:** Kubernetes — "Debug Pods" — https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/ (검색: 2026-07-26)
- **축자:**
  > "The first step in debugging a Pod is taking a look at it. Check the current state of the Pod and recent events with the following command:"
  ```bash
  kubectl describe pods ${POD_NAME}
  ```
  > "Look at the state of the containers in the pod. Are they all Running? Have there been recent restarts? Continue debugging depending on the state of the pods."

  > "The first step in troubleshooting is triage. What is the problem? Is it your Pods, your Replication Controller or your Service?"

#### (b) `Pending`

- **1차 소스:** 동일 debug-pods 페이지
- **⭐ 축자 (전문):**
  > "**My pod stays pending** — If a Pod is stuck in Pending it means that it can not be scheduled onto a node. Generally this is because there are insufficient resources of one type or another that prevent scheduling. Look at the output of the `kubectl describe ...` command above. There should be messages from the scheduler about why it can not schedule your pod. Reasons include:"

  > "**You don't have enough resources**: You may have exhausted the supply of CPU or Memory in your cluster, in this case you need to delete Pods, adjust resource requests, or add new nodes to your cluster."

  > "**You are using hostPort**: When you bind a Pod to a hostPort there are a limited number of places that pod can be scheduled. In most cases, hostPort is unnecessary, try using a Service object to expose your Pod."
- **⭐ 맥 독자에게 특히 중요:** "insufficient resources"는 **로컬 클러스터에 할당한 VM 메모리·CPU가 모자랄 때 그대로 나타나는 증상**이다. `W2 §B-4`의 최소 요구사항 표(minikube 2 CPU/2GB, Colima 기본 2 CPU/2GiB)와 **직접 이어진다.** ⚠️ 다만 그 인과("맥의 VM 할당이 작아서 Pending이 난다")를 말한 공식 문장은 없다 — 저자 해석임을 밝혀라.

#### (c) `Waiting` → 이미지 pull 실패

- **1차 소스:** 동일 debug-pods 페이지
- **⭐ 축자 (전문 — 12장의 "내가 빌드한 이미지를 클러스터가 못 본다"와 정확히 맞물린다):**
  > "**My pod stays waiting** — If a Pod is stuck in the Waiting state, then it has been scheduled to a worker node, but it can't run on that machine. Again, the information from `kubectl describe ...` should be informative. **The most common cause of Waiting pods is a failure to pull the image.** There are three things to check:"
  > - "Make sure that you have the name of the image correct."
  > - "Have you pushed the image to the registry?"
  > - "Try to manually pull the image to see if the image can be pulled. For example, if you use Docker on your PC, run `docker pull <image>`."
- **⭐⭐ Phase 2·4 활용 — 이것이 12장 소절 3의 정확한 근거다.** kind는 Docker image store와 호환되지 않아 로컬 빌드 이미지를 못 보고, 그래서 `kind load docker-image`가 필요하다(계획 12장 소절 3, `W2 §B-5`). 그 단계를 건너뛴 독자가 **실제로 보게 되는 화면**이 이 `Waiting`이다. 공식 문서의 체크리스트 3항목이 그대로 독자의 진단 절차가 된다.

#### (d) `ImagePullBackOff`

- **1차 소스:** Kubernetes — "Images" — https://kubernetes.io/docs/concepts/containers/images/ (검색: 2026-07-26. `W2 §A-5`가 `imagePullPolicy` 4갈래를 확보한 바로 그 페이지 — **같은 페이지의 다른 섹션이다**)
- **⭐ 축자 (전문):**
  > "**ImagePullBackOff** — When a kubelet starts creating containers for a Pod using a container runtime, it might be possible the container is in Waiting state because of ImagePullBackOff."

  > "The status ImagePullBackOff means that a container could not start because Kubernetes could not pull a container image (for reasons such as invalid image name, or pulling from a private registry without imagePullSecret). The BackOff part indicates that Kubernetes will keep trying to pull the image, with an increasing back-off delay. Kubernetes raises the delay between each attempt until it reaches a compiled-in limit, **which is 300 seconds (5 minutes)**."
- **⭐ 주의 — 이 축자가 C2와도 이어진다.** "pulling from a private registry without imagePullSecret"이 **`imagePullSecrets`에 대해 확보된 유일한 1차 언급**이다(`03_review_log.md` C2가 "코퍼스 전체에 0건"으로 지적한 항목). ⛔ **단, 이것은 원인 나열의 한 항목일 뿐 `imagePullSecrets`의 설정 방법·YAML은 이 문장에 없다.** 7장에서 "프라이빗 레지스트리는 K8s 쪽에도 자격증명이 필요하다(12장/범위 밖)"는 **한 줄 언급까지만** 가능하고, **`imagePullSecrets` 매니페스트를 지어내면 ❌.**
- **300초 한계는 인용해도 좋다** — 축자로 확인됐다. 다만 "compiled-in limit"이므로 **설정 가능한 값처럼 쓰지 마라.**

#### (e) `CrashLoopBackOff`

- **1차 소스:** Kubernetes — "Pod Lifecycle" — https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (검색: 2026-07-26)
- **⭐ 축자 (메커니즘 전문):**
  > "Kubernetes manages container failures within Pods using a restartPolicy defined in the Pod spec. This policy determines how Kubernetes reacts to containers exiting due to errors or other reasons, which falls in the following sequence:"
  > - "**Initial crash**: Kubernetes attempts an immediate restart based on the Pod restartPolicy."
  > - "**Repeated crashes**: After the initial crash Kubernetes applies an exponential backoff delay for subsequent restarts, described in restartPolicy. This prevents rapid, repeated restart attempts from overloading the system."
  > - "**CrashLoopBackOff state**: This indicates that the backoff delay mechanism is currently in effect for a given container that is in a crash loop, failing and restarting repeatedly."
  > - "**Backoff reset**: If a container runs successfully for a certain duration (e.g., 10 minutes), Kubernetes resets the backoff delay, treating any new crash as the first one."

  > "In practice, a CrashLoopBackOff is a condition or event that might be seen as output from the kubectl command, while describing or listing Pods, when a container in the Pod fails to start properly and then continually tries and fails in a loop."

  ⭐ **원인 목록(축자) — 자바 앱에 그대로 해당한다:**
  > "The CrashLoopBackOff can be caused by issues like the following: Application errors that cause the container to exit. Configuration errors, such as incorrect environment variables or missing configuration files. **Resource constraints, where the container might not have enough memory or CPU to start properly.**"

  ⭐ **"Status"와 "phase"를 혼동하지 말라는 공식 경고(축자) — 정확성 규율의 시범 재료:**
  > "When a pod is failing to start repeatedly, CrashLoopBackOff may appear in the Status field of some kubectl commands. Similarly, when a pod is being deleted, Terminating may appear in the Status field of some kubectl commands. **Make sure not to confuse Status, a kubectl display field for user intuition, with the pod's phase.** Pod phase is an explicit part of the Kubernetes data model and of the Pod API."

  출력 예시(축자):
  ```
  NAMESPACE               NAME               READY   STATUS             RESTARTS   AGE
  alessandras-namespace   alessandras-pod    0/1     CrashLoopBackOff   200        2d9h
  ```
- **⭐⭐ Phase 2 활용 (강력):** "Resource constraints, where the container might not have enough memory or CPU to start properly" — **8장(JVM이 cgroup을 읽는다, `MaxRAMPercentage`)과 4장(자원 한도)이 12장에서 회수되는 지점이다.** 힙을 잘못 잡은 스프링 앱이 K8s에서 어떻게 보이는지가 이 한 줄로 이어진다. ⚠️ 단, **공식 문서는 자바·JVM을 언급하지 않는다.** 확장 서술 금지 — 연결은 저자 해석으로 명시하라.
- **⛔ 주의 — 세 상태가 서로 다른 층위다.** `Pending`은 **Pod phase**, `Waiting`은 **container state**, `CrashLoopBackOff`·`ImagePullBackOff`는 **kubectl이 보여주는 Status 문자열**이다. 위 축자("Make sure not to confuse Status ... with the pod's phase")가 그것을 직접 경고한다. **네 개를 한 표에 "Pod 상태"로 나란히 놓으면 부정확하다.** 표를 만들려면 층위 열을 두거나, 산문으로 "어디에 찍히는 값인가"를 구분해 써라.

---

## T4. 레지스트리 배포 — `docker login` / tag / push (요구 2의 "배포")

- **상태:** ✅ **확보** (Docker Hub·자체 호스팅·GHCR·ECR 전부 + 자격증명 저장 위치 + 평문 경고)

### T4-1. `docker login` — 문법·옵션·인증 방식

- **1차 소스:** Docker Docs — "docker login" — https://docs.docker.com/reference/cli/docker/login/ (발행일·버전 마커 미노출. **검색: 2026-07-26**)
- **축자:**
  > Description: "Authenticate to a registry." / Usage: `docker login [OPTIONS] [SERVER]`

  > "You can authenticate to any public or private registry for which you have credentials. Authentication may be required for pulling and pushing images."
- **옵션 표 (축자):**

  | Option | Default | Description |
  |---|---|---|
  | `-p`, `--password` | | Password or Personal Access Token (PAT), or `-` to read from stdin |
  | `--password-stdin` | | Take the Password or Personal Access Token (PAT) from stdin |
  | `-u`, `--username` | | Username |

- **⭐ `--password-stdin` 권장 근거 (축자 — 이유가 문서에 명시돼 있다):**
  > "To run the docker login command non-interactively, you can set the `--password-stdin` flag to provide a password through STDIN. **Using STDIN prevents the password from ending up in the shell's history, or log-files.**"
  ```console
  $ cat ~/my_password.txt | docker login --username foo --password-stdin
  ```
  ```console
  $ cat ~/my_password.txt | docker login --username foo --password -
  ```
- **Docker Hub 기본 흐름(축자 — 2026 현재는 브라우저 디바이스 코드가 기본이다):**
  > "For Docker Hub, the docker login command uses a device code flow by default, unless the `--username` flag is specified."
  ```console
  $ docker login

  USING WEB-BASED LOGIN
  To sign in with credentials on the command line, use 'docker login -u <username>'

  Your one-time device confirmation code is: LNFR-PGCJ
  Press ENTER to open your browser or submit your device code here: https://login.docker.com/activate

  Waiting for authentication in the browser…
  ```
- **자체 호스팅 레지스트리(축자):**
  ```console
  $ docker login registry.example.com
  $ docker login registry.example.com:1337
  ```
  > "By default, the docker login command assumes that the registry listens on port 443 or 80."

  ⛔ 함정(축자):
  > "Registry addresses should not include URL path components, only the hostname and (optionally) the port. Registry addresses with URL path components may result in an error. For example, `docker login registry.example.com/foo/` is incorrect, while `docker login registry.example.com` is correct."

### T4-2. ⭐ 자격증명 저장 위치 — 맥은 키체인, 아니면 **base64 평문**

- **1차 소스:** 동일 페이지 (검색: 2026-07-26)
- **⭐⭐ 축자 (task가 요청한 "평문 저장 경고" — 확보했다):**
  > "Authentication credentials are stored in the configured credential store. **If you use Docker Desktop, credentials are automatically saved to the native keychain of your operating system.** If you're not using Docker Desktop, you can configure the credential store in the Docker configuration file, which is located at `$HOME/.docker/config.json` on Linux or `%USERPROFILE%/.docker/config.json` on Windows. **If you don't configure a credential store, Docker stores credentials in the config.json file in a base64-encoded format. This method is less secure than configuring and using a credential store.**"

  > "The Docker Engine can keep user credentials in an external credential store, such as the native keychain of the operating system. **Using an external store is more secure than storing credentials in the Docker configuration file.**"

  헬퍼 목록(축자): "Helpers are available for the following credential stores: D-Bus Secret Service / **Apple macOS keychain** / Microsoft Windows Credential Manager / pass"

  ⭐ **맥 사용자는 이미 설정돼 있다(축자):**
  > "With Docker Desktop, the credential store is already installed and configured for you. Unless you want to change the credential store used by Docker Desktop, you can skip the following steps."

  기본 동작(축자):
  > "By default, Docker looks for the native binary on each of the platforms, i.e. **osxkeychain on macOS**, wincred on Windows, and pass on Linux. A special case is that on Linux, Docker will fall back to the secretservice binary if it cannot find the pass binary. **If none of these binaries are present, it stores the base64-encoded credentials in the config.json configuration file.**"

  설정 예시(축자):
  ```json
  {
    "credsStore": "osxkeychain"
  }
  ```
  > "You need to specify the credential store in `$HOME/.docker/config.json` to tell the Docker Engine to use it. The value of the config property should be the suffix of the program to use (i.e. everything after `docker-credential-`)."

  > "If you are currently logged in, run docker logout to remove the credentials from the file and run docker login again."
- **⭐⭐ Phase 2 활용 — 맥 독자에게 정확히 맞는 재료다.** 공식 문서가 **`osxkeychain`을 이름으로 지목**하고, Docker Desktop이면 자동 설정된다고 말한다. 이 책의 논제("맥은 다르다")가 여기서는 **드물게 맥에 유리한 방향**으로 나타난다 — CI 서버(Desktop 없음)에서는 base64 평문이 되는데 맥 개발 머신에서는 키체인이다. **이 대비를 7장 배포 소절의 한 문단으로 쓰면 좋다.**
- **⛔ 주의:** `$HOME/.docker/config.json` 경로는 문서가 **"on Linux"**로 한정해 말한다. macOS 경로는 **확인한 페이지에 명시되지 않았다**(Linux와 Windows만 언급). ⛔ **"맥에서도 `$HOME/.docker/config.json`이다"라고 쓰지 마라** — 사실일 가능성이 높지만 **이 페이지가 말하지 않는다.** 안전한 서술: "Docker Desktop을 쓰면 OS 키체인에 저장된다(공식 축자). 설정 파일 경로는 문서가 Linux/Windows만 명시한다."

### T4-3. ⭐ 태그를 레지스트리 경로로 붙이는 공식 규칙

- **1차 소스:** Docker Docs — "docker image tag" — https://docs.docker.com/reference/cli/docker/image/tag/ (검색: 2026-07-26)
- **축자:**
  > Description: "Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE" / Usage: `docker image tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]` / Alias: `docker tag`

  ⭐ **참조 문법 전문(축자) — task가 요청한 바로 그 규칙이다:**
  > "A Docker image reference consists of several components that describe where the image is stored and its identity. These components are:"
  ```
  [HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
  ```
  구성요소 설명(축자):
  > **HOST** — "Specifies the registry location where the image resides. **If omitted, Docker defaults to Docker Hub (docker.io).**"
  > **PORT** — "An optional port number for the registry, if necessary (for example, :5000)."
  > **NAMESPACE/REPOSITORY** — "The namespace (optional) usually represents a user or organization. The repository is required and identifies the specific image. **If the namespace is omitted, Docker defaults to library, the namespace reserved for Docker Official Images.**"
  > **TAG** — "An optional identifier used to specify a particular version or variant of the image. **If no tag is provided, Docker defaults to latest.**"

  ⭐ **분해 예시(축자 전문) — 표로 그대로 옮길 수 있다:**
  > "`example.com:5000/team/my-app:2.0` — Host: example.com / Port: 5000 / Namespace: team / Repository: my-app / Tag: 2.0"
  > "`alpine` — Host: docker.io (default) / Namespace: library (default) / Repository: alpine / Tag: latest (default)"

  > "For more information on the structure and rules of image naming, refer to the Distribution reference as the canonical definition of the format."
- **예제(축자):**
  ```console
  $ docker tag 0e5574283393 fedora/httpd:version1.0
  $ docker tag httpd fedora/httpd:version1.0
  ```
- **⭐⭐ Phase 2 활용 — 9장과 7장을 잇는 최고의 재료.** "태그를 생략하면 `latest`가 된다"가 **Docker 공식 문서 축자**로 확보됐다. `W2 §A-5`의 K8s 축자("if you omit the imagePullPolicy field, and you don't specify the tag for the container image, imagePullPolicy is automatically set to Always")와 **완벽하게 짝을 이룬다** — 도커 쪽에서 태그를 생략하면 `latest`가 되고, 쿠버네티스 쪽에서 태그를 생략하면 `Always`가 된다. **두 생략이 같은 방향으로 위험하다.**

### T4-4. `docker push` — 문법·옵션·전체 흐름

- **1차 소스:** Docker Docs — "docker image push" — https://docs.docker.com/reference/cli/docker/image/push/ (검색: 2026-07-26)
- **축자:**
  > Description: "Upload an image to a registry" / Usage: `docker image push [OPTIONS] NAME[:TAG]` / Alias: `docker push`

  > "Use docker image push to share your images to the Docker Hub registry or to a self-hosted one."

  > "Refer to the docker image tag reference for more information about valid image and tag names."

  ⭐ **인증과의 관계(축자 — 한 줄로 §T4-1과 이어진다):**
  > "**Registry credentials are managed by docker login.**"

  진행 표시줄 함정(축자):
  > "Progress bars are shown during docker push, which show the uncompressed size. The actual amount of data that's pushed will be compressed before sending, so the uploaded size will not be reflected by the progress bar."
- **⭐ 태그 → push 전체 흐름 (축자, 자체 호스팅 레지스트리 예제):**
  > "Now, push the image to the registry using the image ID. In this example the registry is on host named registry-host and listening on port 5000. To do this, tag the image with the host name or IP address, and the port of the registry:"
  ```console
  $ docker image tag rhel-httpd:latest registry-host:5000/myadmin/rhel-httpd:latest

  $ docker image push registry-host:5000/myadmin/rhel-httpd:latest
  ```
- **옵션 표 (축자):**

  | Option | Description |
  |---|---|
  | `-a`, `--all-tags` | Push all tags of an image to the repository |
  | `--platform` | **API 1.46+** — "Push a platform-specific manifest as a single-platform image to the registry. Image index won't be pushed, meaning that other manifests, including attestations won't be preserved. 'os[/arch[/variant]]': Explicit platform (eg. linux/amd64)" |
  | `-q`, `--quiet` | Suppress verbose output |

- **⭐⭐ `--platform` 옵션이 이 책에 특히 중요하다.** 축자가 직접 경고한다 — **"Image index won't be pushed, meaning that other manifests, including attestations won't be preserved."** 즉 `docker push --platform`으로 밀면 **멀티플랫폼 인덱스가 사라진다.** 7장의 배포 소절이 "내가 올린 태그가 어느 플랫폼들을 담고 있는가"를 `imagetools inspect`로 확인하는 이유에 **공식 근거 하나가 더 붙는다.** ⚠️ `API 1.46+`은 문서가 명시한 조건이므로 **반드시 병기**하라.
- **주의:** 문서의 첫 예제는 `docker container commit`으로 이미지를 만든다(축자: "First save the new image by finding the container ID ... and then committing it"). ⛔ **이 책은 `commit` 경로를 가르치지 않는다** — 태그·push 부분만 떼어 쓰고 `commit`은 옮기지 마라. 이름 제약 축자만 유용: "only a-z0-9-_. are allowed when naming images".

### T4-5. `docker logout`

- **1차 소스:** Docker Docs — "docker logout" — https://docs.docker.com/reference/cli/docker/logout/ (검색: 2026-07-26)
- **축자 (페이지 전체가 이게 전부다 — 매우 짧다):**
  > Description: "Log out from a registry." / Usage: `docker logout [SERVER]`
  > "If no server is specified, the default is defined by the daemon."
  ```console
  $ docker logout localhost:8080
  ```
- **주의:** ❌ **`docker logout` 페이지에는 자격증명 보안 경고가 없다.** 그 경고는 `docker login` 페이지에 있다(§T4-2). 출처를 섞지 마라. `docker login` 페이지의 관련 축자: "If you are currently logged in, run docker logout to remove the credentials from the file and run docker login again."

### T4-6. ⭐ GHCR (GitHub Container Registry) — PAT 로그인

- **상태:** ✅ 확보 — **`W2 §A-2`가 "태그 불변성 언급이 전혀 없다"고 판정한 바로 그 페이지에, 로그인 절차는 명확히 있다.** (두 판정은 모순이 아니다: 페이지에 없는 것은 *태그 불변성*이고, 있는 것은 *인증*이다.)
- **1차 소스:** GitHub Docs — "Working with the Container registry" — https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry (발행일 미노출. **검색: 2026-07-26**)
- **⭐ 축자 (인증 제약 — 중요):**
  > "**GitHub Packages only supports authentication using a personal access token (classic).**"

  필요 스코프(축자):
  > "A personal access token (classic) with at least `read:packages` scope to install packages associated with other private repositories"

  ⛔ **스코프 함정(축자) — 실무자가 실제로 밟는 지뢰:**
  > "By default, when you select the `write:packages` scope for your personal access token (classic) in the user interface, the `repo` scope will also be selected. The repo scope offers unnecessary and broad access, which we recommend you avoid using for GitHub Actions workflows in particular. As a workaround, you can select just the `write:packages` scope for your personal access token (classic) in the user interface with this url: `https://github.com/settings/tokens/new?scopes=write:packages`."

  Actions 권고(축자):
  > "if your GitHub Actions workflow is using a personal access token to authenticate to a registry, we highly recommend you update your workflow to use the `GITHUB_TOKEN`."
- **⭐ 로그인·push 명령 전문 (축자):**
  ```bash
  export CR_PAT=YOUR_TOKEN
  ```
  ```console
  $ echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
  > Login Succeeded
  ```
  ```bash
  docker push ghcr.io/NAMESPACE/IMAGE_NAME:latest
  ```
  ```bash
  docker push ghcr.io/NAMESPACE/IMAGE_NAME:2.5
  ```
  > "Replace NAMESPACE with the name of the personal account or organization to which you want the image to be scoped."

  digest로 pull(축자 — 9장 회수):
  ```bash
  docker pull ghcr.io/NAMESPACE/IMAGE_NAME@sha256:82jf9a84u29hiasldj289498uhois8498hjs29hkuhs
  ```
  ⚠️ 기본 공개 범위(축자): "When you first publish a package, the default visibility is private."
  ⚠️ 리포지터리 연결(축자): "When you push a container image from the command line, the image is not linked to a repository by default. This is the case even if you tag the image with a namespace that matches the name of the repository, such as `ghcr.io/octocat/my-repo:latest`."
- **⭐ Phase 2 활용:** GHCR 예제는 **`--password-stdin` 권장 사용례가 실제로 어떻게 생겼는지 보여주는 완벽한 샘플**이다(§T4-1의 원칙 + 여기의 실물). 7장 배포 소절에 **Docker Hub 대신 GHCR을 주 예제로 쓰는 것도 합리적이다** — 자바 개발자 대부분이 GitHub 계정을 이미 갖고 있고, PAT 발급이 신용카드 없이 된다.

### T4-7. ⭐ ECR — `aws ecr get-login-password | docker login --password-stdin`

- **상태:** ✅ 확보
- **1차 소스:** AWS — "Private registry authentication in Amazon ECR" — https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html (발행일 미노출 — AWS 문서는 본문에 날짜를 인쇄하지 않는다. **검색: 2026-07-26**)
- **⭐ 축자 (명령 전문):**
  ```
  aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
  ```
  (PowerShell 판, 축자: `(Get-ECRLoginCommand).Password | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com`)
- **설명 축자:**
  > "An authorization token's permission scope matches that of the IAM principal used to retrieve the authentication token. An authentication token is used to access any Amazon ECR registry that your IAM principal has access to and **is valid for 12 hours**. To obtain an authorization token, you must use the GetAuthorizationToken API operation to retrieve a base64-encoded authorization token containing the username AWS and an encoded password. The AWS CLI `get-login-password` command simplifies this by retrieving and decoding the authorization token which you can then pipe into a `docker login` command to authenticate."

  > "When passing the authentication token to the docker login command, **use the value AWS for the username** and specify the Amazon ECR registry URI you want to authenticate to. **If authenticating to multiple registries, you must repeat the command for each registry.**"

  ⚠️ 크리덴셜 헬퍼 제약(축자): "The Amazon ECR Docker credential helper doesn't support multi-factor authentication (MFA) currently."
- **⭐ "12시간 유효"가 실무적으로 중요하다.** 자바 백엔드 개발자가 ECR을 쓰면 **하루에 한 번은 다시 로그인해야 한다.** 이 사실이 "왜 CI에서는 매번 login 스텝이 있는가"를 설명한다. ⚠️ 다만 그 인과 서술은 문서에 없다 — 저자 해석.
- **주의:** `region`·`aws_account_id`는 **문서가 그대로 쓰는 플레이스홀더**다. 책에 옮길 때 실제 값을 지어내지 말고 플레이스홀더를 유지하거나 `<리전>` 식으로 표기하라. ⛔ `W2 §A-2`의 ECR 태그 불변성 자기모순 경고는 **여전히 유효하다** — 이 페이지는 인증만 다루며 태그 불변성 서술은 없다.

---

## T5. 이미지 스토어 판정 명령 — 6장 그림 1의 분기를 독자가 직접 판정하게

- **상태:** ✅ **확보 — 계획 `§0-5 #4`가 "`W3` 대기"로 남겨 둔 판정 명령을 찾았다.** 아울러 계획 정정 11·13(제품 라인별 기본값)의 1차 소스 축자도 함께 확보했다.

### T5-1. ⭐⭐ 판정 명령 — `docker info -f '{{ .DriverStatus }}'`

- **1차 소스:** Docker Docs — "containerd image store" (Docker Engine 매뉴얼) — https://docs.docker.com/engine/storage/containerd/ (발행일·버전 마커 미노출. **검색: 2026-07-26**)
- **⭐ 축자 (명령과 출력 전문 — 이것이 판정 근거다):**
  > "After restarting the daemon, verify you're using the containerd image store:"
  ```console
  $ docker info -f '{{ .DriverStatus }}'
  [[driver-type io.containerd.snapshotter.v1]]
  ```
  > "Docker Engine uses the overlayfs containerd snapshotter by default."
- **활성화 설정(축자 — Linux 데몬 기준):**
  ```json
  {
    "features": {
      "containerd-snapshotter": true
    }
  }
  ```
  > "Add the following configuration to your `/etc/docker/daemon.json` file" → `sudo systemctl restart docker`
- **⛔⛔ 주의 — 이 명령을 책에 쓸 때 반드시 지킬 것 (fact-checker가 잡을 지점):**
  1. **이 명령은 문서의 "Enable containerd image store on Docker Engine" 섹션(= 리눅스 데몬 설정 절차)에 실려 있다.** 확인한 페이지는 **macOS/Docker Desktop에서 같은 출력이 나온다고 말하지 않는다.** ⛔ **"맥에서 이 명령을 치면 `[[driver-type io.containerd.snapshotter.v1]]`이 나온다"고 단정하지 마라.** 안전한 서술: **"공식 문서가 containerd 이미지 스토어를 쓰고 있는지 확인하는 방법으로 제시하는 명령은 이것이다"** + "출력이 다르면 클래식 스토어일 수 있다"까지.
  2. **클래식 스토어일 때의 출력은 확인한 페이지에 없다(NOT_PRESENT).** ⛔ `overlay2`가 어떻게 찍히는지 지어내지 마라. **독자에게 "직접 쳐 보고 `io.containerd.snapshotter.v1`이 보이는지 확인하라"고 안내하는 형태**가 유일하게 안전한 서술이다. (이것은 8장의 `-XX:+PrintFlagsFinal` 처방과 같은 교육 패턴이다 — 값을 알려주는 대신 확인하는 법을 가르친다.)
  3. **`Storage Driver` 필드는 이 페이지에 나오지 않는다.** task가 후보로 든 `Storage Driver`는 **확인 실패**다. 확보된 필드는 **`DriverStatus`** 하나다.

### T5-2. Docker Desktop에서 켜고 끄는 방법 + 현재 기본값 (계획 정정 11·13의 1차 소스 재확인)

- **1차 소스:** Docker Docs — "containerd image store" (Docker Desktop 매뉴얼) — https://docs.docker.com/desktop/features/containerd/ (발행일 미노출. **검색: 2026-07-26**)
- **⭐⭐ 축자 (기본값 — 이게 정정이다):**
  > "**Docker Desktop uses containerd as its image store by default.** The image store is the component responsible for pushing, pulling, and storing images on your filesystem. The containerd image store supports features like multi-platform images, image attestations, and alternative snapshotters."

  > "**The containerd image store is enabled by default in Docker Desktop version 4.34 and later.** To switch between image stores:"
  > 1. "Navigate to **Settings** in Docker Desktop."
  > 2. "In the **General** tab, check or clear the **Use containerd for pulling and storing images** option."
  > 3. "Select **Apply**."

  ⭐ 전환 시 함정(축자):
  > "Docker Desktop maintains separate image stores for the classic and containerd image stores. When switching between them, images and containers from the inactive store remain on disk but are hidden until you switch back."
- **⭐⭐ Docker Engine 쪽 기본값 (축자, §T5-1 페이지):**
  > "**The containerd image store is the default storage backend for Docker Engine 29.0 and later on fresh installations.** If you upgraded from an earlier version, your daemon continues using the legacy graph drivers (overlay2) until you enable the containerd image store."
- **클래식 스토어의 규정(축자):**
  > "The classic image store is Docker's legacy storage backend, replaced by the containerd image store. **It doesn't support image indices or manifest lists, so you can't load multi-platform images locally or build images with attestations.** Most users have no reason to use the classic image store. It's available for cases where you need to match older behavior or have compatibility requirements."
- **⭐ `--load` 제약의 실제 에러 메시지 (축자 — `W1 §8-6`·`W2`가 확보한 제약의 *증상*이다. 중복 서술 말고 이 출력만 쓰라):**
  ```console
  $ docker build --platform=linux/amd64,linux/arm64 .
  [+] Building 0.0s (0/0)
  ERROR: Multi-platform build is not supported for the docker driver.
  Switch to a different driver, or turn on the containerd image store, and try again.
  Learn more at https://docs.docker.com/go/build-multi-platform/
  ```
  문서 해설(축자): "The containerd image store lets you build multi-platform images and load them to your local image store" / "Building multi-platform images with the classic image store is not supported"
- **⛔ 주의 — 두 기본값 진술이 서로 다른 제품 라인이다.** **Docker Desktop 4.34+** ≠ **Docker Engine 29.0+**. 계획 `§0-4` 정정 11("제품 라인 구분")이 여기에도 적용된다. ⛔ **"도커는 4.34부터 containerd가 기본"이라고 뭉뚱그리면 ❌.**
- **⚠️ 부수 사실 (확보, 6장·9장에 유용):** containerd 스토어는 디스크를 더 쓴다 — 축자: "The containerd image store uses more disk space than the legacy storage drivers for the same images. This is because containerd stores images in both compressed and uncompressed formats, while the legacy drivers stored only the uncompressed layers." + "containerd uses a separate storage path from the Docker data directory."

### T5-3. 이 발견이 계획에 미치는 영향

> **⚠️ 먼저 명확히 — 이 절은 "사실 정정"이 아니다.** `02_plan.md`(개정 2026-07-26)를 직접 열어 6장·7장 소절 본문을 대조한 결과, **계획은 이미 이 사실들을 정확히 담고 있다.** 이번 회차가 하는 일은 **계획이 스스로 대기 상태로 표시해 둔 항목 하나를 닫는 것**뿐이다. 계획에 수정을 요구하는 항목은 **없다.**

| # | 계획의 현재 상태 (축자) | 이번 회차 결과 | 조치 |
|---|---|---|---|
| **1** | 계획 6장 소절 「어디에 담을 것인가」: **"⏳ 내 스토어가 무엇인지 확인하는 명령은 `W3` 대기 항목이다(§0-5 #4) … `W3`로 `docker info` 출력 필드가 확보되면 여기 합류시키고, 실패하면 `(사실 확인 필요)`로 남긴 채 조건부 서술만 한다. 명령을 지어내지 말 것."** | ✅ **확보.** `docker info -f '{{ .DriverStatus }}'` → `[[driver-type io.containerd.snapshotter.v1]]` (`W3 §T5-1`) | **계획이 지정한 대로 "합류"시키면 된다.** `(사실 확인 필요)` 폴백은 발동하지 않는다. 단 §T5-1의 3가지 제약(리눅스 섹션 출처·클래식 출력 미확인·`Storage Driver` 필드 부재)을 병기 |
| **2** | 계획 6장 같은 소절, 정정 11·13: **"Docker Desktop과 Docker Engine 29.0+ 신규 설치는 기본이 containerd라 맥의 이 책 독자는 대체로 로컬에 담을 수 있다"** / **"'Docker Desktop 4.34+'와 'Docker Engine 29.0+'는 제품 라인이 달라서 나온 두 숫자다"** | ✅ **1차 소스로 재확인됨.** 두 진술 모두 공식 축자와 일치한다(`W3 §T5-2`) | **변경 없음.** 이 절은 계획의 기존 서술에 **축자 근거를 보태는 역할**이다. 저술가는 §T5-2의 축자를 그대로 인용하면 된다 |

**⚠️ 서술상의 주의 하나 (정정이 아니라 표현 권고).** 계획 7장 소절 제목 「**체크박스 하나가** 빌드를 깨뜨리는 메커니즘」은, 기본값이 이미 켜짐(Desktop 4.34+)이라는 사실과 나란히 놓으면 **"내가 켰더니 깨졌다"로 읽힐 여지**가 있다. 계획 본문은 우회를 "**스토어 토글 임시 해제**"로 정확히 적어 두었으므로 — 즉 이미 켜져 있음을 전제하므로 — **내용에는 문제가 없다.** 제목만 저술 시점에 한 번 점검하면 된다. ⛔ **`spring-boot#46674` 보고자의 Docker Desktop 버전은 미확인**이므로, "보고자도 기본값이었다"고 쓰지 마라.

---

## Z. 판정표 — **C1·C2가 해소됐는가**

### Z-1. C1 — 12장 K8s 실습 동선

> **판정: ✅ 가능. 끊김 없이 저술 가능하다.**

계획 12장의 실습 동선을 **소절 단위로** 대조했다(`02_plan.md` 12장 소절 목록 기준).

| 동선 단계 | 계획상 위치 | 근거 상태 | 근거 |
|---|---|---|---|
| 클러스터를 띄운다 | 소절 1 「클러스터를 띄우는 두 갈래」 | ✅ 기존 확보 | `W2 §B-5`(kind v0.32.0), `§B-7`(Colima), `REF §2-6` |
| **오브젝트 모델을 세운다**(Pod·Deployment·ReplicaSet·Service) | **신규 소절 「앱을 띄운다 — Deployment와 Service」** | ✅ **이번 회차 확보** | `W3 §T1-1`·`§T1-5`·`§T2-1`·`§T2-3` |
| **매니페스트를 쓴다** | 동일 신규 소절 | ✅ **이번 회차 확보 — YAML 축자 전문 2종(Deployment·Service)** | `W3 §T1-2`, `§T2-2`, `§T2-4` |
| 이미지를 클러스터에 넣는다 | 소절 3 | ✅ 기존 확보 | `W2 §B-5`(`kind load docker-image`), `§A-5`(pull 정책 4갈래) |
| **apply 하고 확인한다** | 동일 신규 소절 | ✅ **이번 회차 확보 — 명령·출력 전문** | `W3 §T1-3`(`apply`/`get`/`get rs`/`describe`/`rollout status`), `§T3-1` |
| 컨텍스트를 확인한다 | 소절 4 | ✅ **이번 회차 보강** | `W3 §T3-3` + 기존 `PROBE §5`·`REF §3 A11` |
| **밖에서 닿아본다** | 소절 5 | ✅ 기존 + **이번 회차 보강** | `W2 §B-3b`·`§B-6` + `W3 §T3-2`(`port-forward svc/`), `§T2-5`(LoadBalancer 원인) |
| **트러블슈팅한다** | 소절 5 또는 신규 소절 꼬리 | ✅ **이번 회차 확보 — 4상태 전부** | `W3 §T3-4` (`describe`·`Pending`·`Waiting`/`ImagePullBackOff`·`CrashLoopBackOff`) |

**신규 소절 「앱을 띄운다 — Deployment와 Service」(1,500~2,000자)가 이제 전부 1차 소스로 저술 가능하다.** 필요한 재료가 전부 있다:
- Pod 정의 축자 → Deployment 정의 축자 → ReplicaSet은 "직접 만지지 않는다"는 공식 권고 축자(분량 절약)
- Deployment YAML 축자 전문 → `kubectl apply` → `get deployments`(컬럼 해설 축자) → `get rs`(3층이 눈에 보이는 지점) → `get pods --show-labels`
- Service 정의 축자("Enter Services.") → Service YAML 축자 전문 → 타입 4종 표 축자 → `ClusterIP` 기본값 3중 근거
- 실패했을 때: `describe` → `Pending`/`Waiting`/`ImagePullBackOff`/`CrashLoopBackOff` 축자

**계획 `§6` 그림 1(「K8s 오브젝트 관계 — Deployment → ReplicaSet → Pod → Service(ClusterIP/NodePort/LoadBalancer) → Ingress」)도 그릴 수 있다.** 각 노드와 화살표의 근거:
- Deployment→ReplicaSet: "A Deployment provides declarative updates for Pods and ReplicaSets" + "Deployments own and manage their ReplicaSets"
- ReplicaSet→Pod: "A ReplicaSet's purpose is to maintain a stable set of replica Pods" + `ownerReferences`
- Pod←Service: "The controller for that Service continuously scans for Pods that match its selector"
- Service 타입 계단: "The type field in the Service API is designed as nested functionality - each level adds to the previous"
- Service→Ingress: "Ingress is not a Service type, but it acts as the entry point for your cluster" (+ `W2 §B-2`의 frozen 서술)

**저술가에게 남는 제약 (우회 아님 — 서술 규율):**
1. 두 Deployment 예제(§T1-2의 A안·B안)를 **섞지 마라.** 하나 고르고 그 페이지를 출처로.
2. "같은 태그로 재-apply하면 롤아웃이 안 일어난다"는 **유추임을 밝혀라**(§T1-4).
3. `Pending`/`Waiting`/`CrashLoopBackOff`는 **층위가 다르다**(§T3-4 말미). 한 표에 "Pod 상태"로 뭉치지 마라.
4. NodePort 30000–32767은 **`--service-node-port-range`의 기본값**이라고 반드시 조건을 붙여라(§T2-4).

### Z-2. C2 — 7장 「배포」 소절

> **판정: ✅ 가능.** 리뷰가 제안한 **2소절 분할**(「레지스트리에 올리기 — 인증·태그·`--push`」 / 「배포 대상에서 내려받아 돌리기」) 중 **첫 소절이 이번 회차로 완전히 채워졌다.**

| 항목 | 근거 상태 | 근거 |
|---|---|---|
| 레지스트리 인증 — Docker Hub | ✅ **확보** (디바이스 코드 흐름 + `-u` 경로) | `W3 §T4-1` |
| 레지스트리 인증 — 자체 호스팅 | ✅ **확보** (포트 지정 + URL path 함정) | `W3 §T4-1` |
| 레지스트리 인증 — **GHCR** | ✅ **확보** (PAT 제약·스코프 함정·명령 전문) | `W3 §T4-6` |
| 레지스트리 인증 — **ECR** | ✅ **확보** (`get-login-password` 파이프 전문·12시간) | `W3 §T4-7` |
| `--password-stdin` 권장 근거 | ✅ **확보** (이유가 문서에 명시) | `W3 §T4-1` |
| **자격증명 저장 위치 · 평문 경고** | ✅ **확보** (맥은 키체인, 미설정 시 base64) | `W3 §T4-2` |
| 태그를 레지스트리 경로로 붙이는 규칙 | ✅ **확보** (`[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]` 축자 + 3중 기본값) | `W3 §T4-3` |
| `docker push` 사용례 | ✅ **확보** (tag→push 흐름 전문) | `W3 §T4-4` |
| `--push`(buildx) | ✅ 기존 확보 | `REF §8-1`·`W1` |
| `imagetools inspect`로 플랫폼 확인 | ✅ 기존 확보 | `W2 §A-4`, `REF §6` |
| `docker manifest` 인덱스 합성 (Paketo 경로) | ✅ 기존 확보 | `REF §8-1` 실무 결론 2 |
| `docker logout` | ✅ **확보** | `W3 §T4-5` |
| **배포 대상 아키텍처 확인** | ✅ 기존 + **보강** | `REF §3 A3`·`C2 §L-3` + `W3 §T4-4`(`--push --platform`이 인덱스를 버린다는 축자) |

**⚠️ 부분 — 하나만 남았다: `imagePullSecrets`.**
- 확보된 것은 **원인 나열 안의 한 구절**뿐이다 — "pulling from a private registry without imagePullSecret"(`W3 §T3-4(d)`).
- ❌ **설정 방법·매니페스트 예제는 여전히 0건.**
- **저술가의 우회 (지정):** 7장에서는 **"프라이빗 레지스트리를 쓰면 쿠버네티스 쪽에도 별도 자격증명이 필요하다(`imagePullSecrets`) — 이 책의 범위 밖이다"**라는 **한 줄 고지**까지만. ⛔ **매니페스트를 지어내면 BLOCKING이다.** 12장에서도 마찬가지 — `ImagePullBackOff` 설명 안에서 원인 목록의 한 항목으로 언급하는 것까지만 허용.

**저술가에게 남는 제약:**
1. `$HOME/.docker/config.json`을 **맥 경로로 단정하지 마라**(§T4-2 — 문서가 Linux/Windows만 명시).
2. `docker push` 문서의 `docker container commit` 예제를 **옮기지 마라**(§T4-4).
3. `--push --platform`의 `API 1.46+` 조건을 **반드시 병기**하라(§T4-4).

### Z-3. 6장 그림 1 (C1이 함께 올린 5번 항목)

> **판정: ✅ 가능.** 판정 명령 확보(`W3 §T5-1`). 계획 `§0-5 #4`의 대기 항목이 닫혔고, 계획 6장 소절이 지정한 폴백(`(사실 확인 필요)` + 조건부 서술)은 **발동하지 않는다.**
>
> ⚠️ **다만 판정의 절반만 확보됐다** — containerd일 때의 출력은 축자로 있으나 **클래식일 때의 출력은 없다.** 그림 1의 분기를 "출력이 A면 왼쪽, B면 오른쪽"으로 그리지 말고, **"이 출력이 보이면 containerd다"** 한 방향으로만 그려라. 나머지는 독자가 "안 보이면 아니다"로 읽는다.

---

## Y. 수집 한계 (정직한 목록)

**🕒 이번 회차에서 확인하지 못한 것 (추측으로 채우지 않음):**
1. **클래식 이미지 스토어일 때의 `docker info -f '{{ .DriverStatus }}'` 출력** — containerd 쪽만 문서에 인쇄돼 있다.
2. **`docker info`의 `Storage Driver` 필드** — task가 후보로 들었으나 **확인한 두 페이지(engine/storage/containerd, desktop/features/containerd) 어디에도 없다.**
3. **macOS/Docker Desktop에서 `DriverStatus` 출력이 동일한지** — 문서가 리눅스 데몬 절차 안에서만 이 명령을 보여준다.
4. **`imagePullSecrets`의 설정 방법·매니페스트** — 원인 나열 안의 한 구절 외에는 0건.
5. **macOS의 `.docker/config.json` 경로** — `docker login` 문서가 Linux/Windows만 명시.
6. **같은 태그로 재-apply했을 때의 롤아웃 동작** — "if and only if `.spec.template` is changed"에서 유추만 가능.
7. **`spring-boot#46674` 보고자의 Docker Desktop 버전** — 4.34+ 기본값 변경 이전인지 이후인지 미확인(§T5-3 말미 주의).
8. **`busybox:1.28`의 arm64 지원 여부** — `kubectl debug` 예제를 실습에 실으려면 필요.
9. **Docker Desktop이 언제부터 containerd 스토어를 "기본"으로 문구를 바꿨는지의 릴리스 노트** — 문서는 "4.34 and later"만 말한다(릴리스 노트 미조회).
10. **kubernetes.io 페이지들의 발행일·문서 버전** — 페이지에 인쇄되지 않는다(`W2`와 동일 조건). "검색: 2026-07-26 기준"으로만 표기 가능.

**❌ 부재확정 (확인한 페이지에 없음 — "존재하지 않음"이 아니다):**
- Service 공식 문서의 **"pending"** 이라는 단어 (LoadBalancer 섹션에 없음 — 원인만 서술)
- debug-pods 페이지의 **`ImagePullBackOff`·`CrashLoopBackOff` 정의** (`Pending`·`Waiting`만 있음 — 두 상태는 각각 images / pod-lifecycle 페이지에 있다)
- `docker logout` 페이지의 **보안 경고** (login 페이지에 있음)
- ECR `registry_auth` 페이지의 **태그 불변성 서술** (별도 페이지, `W2 §A-2`)
- Deployment 페이지의 **"3층 구조(three-tier)"라는 표현** (관계 문장은 있으나 그 용어는 없음)

**⛔ 판정이 뒤집힌 항목 (`W2`를 갱신한다):**

| 항목 | `W2`의 판정 | `W3`의 판정 | 근거 |
|---|---|---|---|
| **NodePort 기본 포트 범위 30000–32767** | ❌ "4개 페이지에서 확인 실패. **책에 쓰지 마라**"(`§B-8`, `§F-1`) | ✅ **확보 — 인용 허용** (published 페이지에서 3중 확인, 밴드 분할 조건 병기 필수) | `W3 §T2-4` |
| **Service 개념 페이지 접근** | ❌ 4회 TRUNCATED 실패 | ✅ **`curl` 우회로 전문 확보** | `W3 §T2-0` |
| **이미지 스토어 판정 명령** | ❌ 계획 6장이 "공식 문서로 확인되지 않았다"고 자기 신고 | ✅ **`docker info -f '{{ .DriverStatus }}'` 확보** (3가지 제약 병기) | `W3 §T5-1` |

**방침 준수 기록:**
- 이 문서에서 **이번 회차에 새로 확보한 축자는 전부 `curl`로 받은 published 페이지에서 나왔다.** `kubernetes/website` `main` 브랜치 마크다운은 **위치 탐색과 교차 검증에만** 썼고, 인용 원천으로 채택하지 않았다(§T2-0). ⚠️ **예외 1건:** §T3-2가 `W2 §B-8`의 축자(WebFetch로 확보한 `kubectl_port-forward` generated 레퍼런스)를 **재수집 없이 승계**한다 — 중복 조사 금지 지시에 따른 것이며, 그 축자의 원천은 `W2`다. §T3-2가 새로 확보한 것은 quick-reference의 `svc/`·`deploy/` 예제뿐이다.
- **`W1` 별칭 확인:** `02_plan.md §0-1` 별칭표에 `W1` = `research/web_gapfill.md`로 등재돼 있음을 대조했다(§T5-2의 `W1 §8-6` 참조는 유효).
- **계획 대조:** `02_plan.md`의 §0-1 별칭표·§0-5 대기 목록·6장·7장·12장 소절 본문을 **직접 열어** 대조했다. 이 문서가 계획에 요구하는 수정은 **없다**(§T5-3).
- **WebSearch 0회 사용.** 모든 URL이 지정됐거나 공식 사이트 내부 경로였다.
- 개인 블로그·Medium·Stack Overflow **0건 채택.**
- 기존 `research/*.md`·`01_reference.md`·`02_plan.md`·`03_review_log.md` **수정·삭제 없음.** 이 파일은 신규 산출물이다.
