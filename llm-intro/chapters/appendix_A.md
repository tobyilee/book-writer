# 부록 A. 환경 세팅 체크리스트

책의 실습은 크게 두 궤도로 달린다. Python으로 모델을 직접 훈련하고 파인튜닝하는 궤도, 그리고 Java로 만들어 놓은 LLM을 서비스에 붙이는 궤도다. 두 궤도 모두 환경이 제각각 틀어져 있으면 본문을 따라오다 중간에 멈추기 쉽다. 이 부록에서 **한 번에 같이 맞춰보자**. 이후 2장부터는 여기서 정리한 환경이 모두 준비돼 있다는 전제로 이야기한다. 아래 항목 중 이미 깔려 있는 것은 버전만 확인하고 넘어가면 된다. 모든 명령은 macOS(Apple Silicon)와 Ubuntu 22.04 이상을 기준으로 삼되, Windows 사용자는 WSL2 위에서 Ubuntu 명령을 따라가는 편이 낫다.

## A.1 Python 환경

**버전·패키지 매니저**

- Python 3.11 이상을 쓴다. 3.10은 `torch`·`bitsandbytes` 최신 휠이 빠질 수 있다.
- 패키지 매니저는 `uv`를 권장한다. `pip`보다 수십 배 빠르고, lock 파일 포맷이 표준에 가깝다.

```bash
# macOS
brew install uv

# Linux / WSL (Homebrew 없을 때)
pip install uv
```

**가상환경 만들기**

저장소를 clone한 뒤 프로젝트 루트에서 아래 3줄이면 된다.

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt
```

`.venv`가 활성화된 상태인지 프롬프트 앞의 `(.venv)` 표시로 확인한다. 활성화를 잊은 채로 `pip install`을 하면 시스템 Python을 오염시키게 되므로 주의해야 한다.

**실습에 쓰는 주요 패키지**

- 토큰화·임베딩: `tiktoken`, `sentence-transformers`
- 모델·학습: `transformers`, `peft`, `trl`, `bitsandbytes`, `datasets`, `accelerate`
- 프레임워크: `torch` (CUDA/MPS 자동 감지), `langchain`, `llama-index`, `chromadb`
- API SDK: `openai`, `anthropic`

`uv.lock` 파일로 버전을 고정해 두었다. "다음 달에도 같은 결과"가 나오도록 하는 약속이다. `uv pip install`은 lock 파일을 먼저 확인한 뒤 설치하므로 추가 작업은 필요 없다.

**확인용 한 줄**

```bash
python -c "import torch, transformers; print(torch.__version__, transformers.__version__)"
```

출력이 정상이면 2장으로 넘어가도 좋다.

## A.2 Java 환경

**JDK와 빌드 도구**

- Java 21(LTS)을 쓴다. Amazon Corretto 또는 Eclipse Temurin 중 하나면 된다.
- 여러 버전을 왕복해야 하는 경우가 많으므로 `sdkman`으로 관리하는 편이 낫다.

```bash
curl -s "https://get.sdkman.io" | bash
sdk install java 21-tem
sdk default java 21-tem
```

- 빌드 도구는 Maven과 Gradle 어느 쪽이든 무방하다. 7·8장 실습 저장소에는 `pom.xml`과 `build.gradle.kts`를 함께 제공한다.

**Spring Boot와 Spring AI**

- Spring Boot 3.3 이상, Spring AI 1.0 이상을 쓴다.
- `pom.xml`에는 의존성이 provider별로 분리돼 있어 **한 줄만 바꾸면 스왑**된다.

```xml
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
</dependency>
<!-- 필요 시 아래로 교체 -->
<!-- spring-ai-anthropic-spring-boot-starter -->
<!-- spring-ai-ollama-spring-boot-starter -->
```

**API 키 주입**

- `application.yml`에는 키를 직접 박지 말고 환경 변수를 참조한다.

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
```

**확인용 한 줄**

```bash
java --version
./mvnw -v
```

## A.3 GPU·가속기 체크

실습 장별로 필요한 VRAM이 다르다. 아래 가이드를 기준으로 본인 장비의 위치를 먼저 찍어보자.

- **4장 (Bigram → 미니 GPT):** 2~4GB VRAM. 노트북 GPU·Colab 무료 T4로 충분하다.
- **6장 (QLoRA Llama 3 8B):** 12~16GB 최소, 24GB 원활. 16GB가 안 되면 Colab T4 + Unsloth 경로로 돌린다.
- **7장 (Ollama Llama 3.1 8B):** Apple Silicon 통합 메모리 8~16GB면 돌아간다. 16GB 권장.
- **8장 (RAG 임베딩):** CPU로도 돌릴 수 있지만 배치 처리가 잦으므로 GPU가 있으면 훨씬 낫다.

**NVIDIA CUDA 확인**

```bash
nvidia-smi           # 드라이버·VRAM·점유 프로세스 한눈에
nvcc --version       # CUDA 툴킷 버전 (12.x 권장)
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

**Apple Silicon MPS 확인**

```bash
python -c "import torch; print(torch.backends.mps.is_available())"
```

`True`가 나오면 `device='mps'`로 학습·추론이 된다. 단, 일부 연산은 아직 CPU fallback이 발생하므로 경고가 뜨더라도 당황할 필요는 없다.

**도커로 돌릴 때**

- NVIDIA Container Toolkit을 설치한 뒤 `docker run --gpus all ...` 플래그로 GPU를 넘긴다.
- Apple Silicon에서는 도커 컨테이너가 MPS에 접근하지 못한다. 4·6장 실습은 도커 바깥(호스트)에서 돌리는 편이 낫다.

## A.4 Ollama (로컬 LLM)

7장 후반과 8장 일부에서 로컬 모델을 API처럼 호출한다. Ollama가 가장 간단하다.

**설치**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

설치 후 `ollama serve`가 백그라운드에서 돈다. 포트는 기본 `localhost:11434`이고, Spring AI Ollama starter는 이 주소를 자동으로 찾는다.

**모델 받기**

```bash
ollama pull llama3.1:8b      # 약 4.7GB
ollama pull qwen2.5:7b       # 약 4.4GB
ollama pull bge-m3           # 임베딩, 약 1.2GB
```

처음 받을 때 4~5GB를 통째로 내려받으므로 네트워크와 디스크 여유를 미리 확인해 두자.

**작동 확인**

```bash
ollama run llama3.1:8b "한 문장으로 자기소개해줘."
```

응답이 나오면 성공이다.

## A.5 실습 저장소

실습 코드·데이터·노트북은 한 저장소에 모아 두었다.

```bash
git clone https://github.com/toby-ai/llm-intro-book.git
cd llm-intro-book
```

> 저장소 주소는 출간 시점에 최종 확정한다. 현재는 가상 주소다.

**디렉터리 구조 한눈에 보기**

```
llm-intro-book/
├── ch02-tokens/        # 토큰화·임베딩 실습
├── ch03-attention/     # 어텐션·트랜스포머 구현
├── ch04-nanogpt/       # 미니 GPT from scratch
├── ch06-qlora/         # Llama 3 8B QLoRA 파인튜닝
├── ch07-api/           # Python·Spring AI·LangChain4j
├── ch08-rag/           # 벡터 DB + RAG 파이프라인
├── datasets/           # 공통 코퍼스·골드셋
└── notebooks/          # 장별 Colab 노트북
```

**한국어 코퍼스 준비 (4장용)**

```bash
python datasets/prepare_corpus.py
```

이 스크립트는 모두의 말뭉치(국립국어원)와 나무위키 덤프 일부를 내려받아 1~3MB 규모로 전처리한다. 처음 돌릴 때만 10~15분 걸린다.

**라이선스 한 줄**

- 책 저장소의 코드는 MIT.
- 데이터셋은 각 원 라이선스를 따른다. 나무위키는 CC BY-NC-SA 2.0, 모두의 말뭉치는 국립국어원 이용 약관. 상용 재배포 전에 반드시 원 약관을 확인해야 한다.

## A.6 API 키와 보안

**`.env` 파일로 관리**

프로젝트 루트에 `.env` 파일을 만들고 아래처럼 채운다.

```dotenv
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HF_TOKEN=hf_...
```

`.gitignore`에 `.env`가 들어 있는지 **반드시** 먼저 확인하자. 실수로 커밋해 리포지토리에 키가 남으면 복구가 번거롭고 찜찜하다.

**더 안전하게 쓰는 두 가지 방법**

- 1Password CLI: `op run --env-file=.env.tpl -- python train.py`
- direnv: 디렉터리 진입 시 `.envrc`를 자동 로드. `brew install direnv` 후 `direnv allow`.

**비용 상한**

OpenAI·Anthropic 대시보드에서 월 한도와 알림을 설정한다. 실습 중 실수로 루프가 돌면 몇 시간 만에 수십 달러가 새는 경우가 있어 처음 쓰는 독자는 낮게 잡아두는 편이 낫다.

## A.7 실패 시 점검 순서

뭔가 안 돌면 아래 순서를 따라가 보자. 대부분은 이 안에서 잡힌다.

**Python 쪽**

- `python --version` — 3.11 이상인가?
- `which python` — `.venv` 안의 파이썬을 가리키는가?
- `uv pip list | grep -E "torch|transformers|peft"` — 버전이 lock과 맞는가?
- ImportError가 날 때는 가상환경이 활성화돼 있는지부터 확인한다.

**Java 쪽**

- `java --version` — 21인가?
- `./mvnw dependency:tree` 또는 `./gradlew dependencies` — Spring AI 버전이 통일돼 있는가? 여러 starter가 다른 버전을 끌어오면 `NoSuchMethodError`가 난다.
- `application.yml`의 env var가 실제로 export돼 있는가? `echo $OPENAI_API_KEY`로 확인.

**GPU 쪽**

- `nvidia-smi`에서 드라이버가 잡히는가?
- `torch.cuda.is_available()` 또는 `torch.backends.mps.is_available()`가 `True`인가?
- VRAM이 꽉 찬 상태라면 `nvidia-smi`에서 점유 프로세스를 확인한 뒤 종료.

**API 호출 쪽**

- 네트워크·프록시: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
- rate limit: 429 응답이면 잠시 기다린 뒤 재시도.
- `finish_reason`이 `length`면 `max_tokens` 부족, `content_filter`면 안전장치 발동.

여기까지 환경이 맞춰졌다면 이제 본문으로 들어가도 좋다. **2장에서 토큰부터 같이 열어보자.**
