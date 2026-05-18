# ch13-boot-anatomy — 부팅 코드 3단계 분해

13장의 본문에서 한 줄씩 해부한 `boot.S`와 `linker.ld`를 **세 단계로 점진적으로 쌓아 올리는** 예제다. 같은 코드 베이스를 처음에는 가장 단순한 골격으로, 다음에는 BSS·스택을 더해서, 마지막에는 Ch12와 동등한 완성형으로 만들어본다.

## 세 단계

| 디렉토리 | 추가된 것 | 결과 |
|---------|----------|------|
| `stage1-asm-only/`  | `_start` + primary core 선택 + 무한 루프 | 화면 출력 없음. 부팅의 최소 단위. |
| `stage2-bss-stack/` | + SP 셋업 + BSS 클리어 + 링커 심볼 | 화면 출력 없음. C 함수 호출 준비 완료. |
| `stage3-main-call/` | + `kernel.c` + `bl kernel_main` | 시리얼에 `hello, aarch64` 출력. |

각 디렉토리에는 자체 `boot.S`/`linker.ld`/`Makefile`이 있고, Stage 3에만 `kernel.c`가 더해진다. 한 디렉토리 안에서 `make` → `make run` → `make objdump` → `make readelf` 흐름으로 손에 익혀보자.

## 빌드 환경

`aarch64-elf-gcc` 크로스 도구가 필요하다.

**macOS:**

```sh
brew install --cask gcc-aarch64-embedded
# 또는
brew install aarch64-elf-gcc
```

**Ubuntu/Debian:**

```sh
sudo apt install gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu
# 이 경우 CROSS 접두사가 다르므로 다음과 같이 호출
make CROSS=aarch64-linux-gnu-
```

**WSL:** Ubuntu 패키지와 동일.

QEMU도 함께 필요하다.

```sh
brew install qemu        # macOS
sudo apt install qemu-system-arm   # Ubuntu
```

## 빠른 실행

```sh
# 세 스테이지 전체 빌드
make all

# Stage 3을 QEMU에서 실행 — 시리얼에 hello, aarch64 출력
make run-stage3
# (종료: Ctrl-A 다음에 x)

# 세 스테이지의 디스어셈블 비교
make objdump-all
```

## 한 스테이지씩 들여다보기

각 스테이지 디렉토리에 들어가서 직접 빌드해보자.

```sh
cd stage1-asm-only
make
aarch64-elf-objdump -d kernel.elf | head -20
aarch64-elf-readelf -h kernel.elf
```

`objdump -d` 결과의 첫 줄에서 `_start`가 0x40000000에 자리잡았는지 확인하자. `readelf -h`의 `Entry point address`가 0x40000000과 정확히 일치하면 링커 스크립트의 약속이 ELF에 그대로 반영된 것이다.

Stage 2에서는 BSS 클리어 루프(`clear_bss:` 레이블)가 디스어셈블에 등장해야 하고, Stage 3에서는 `bl <kernel_main>` 명령이 새로 보여야 한다. **세 스테이지의 디스어셈블 결과를 나란히 두고 비교하면 어셈블리 한 줄이 바뀐다는 것의 의미가 손에 박힌다.**

## 트러블슈팅

- **`aarch64-elf-gcc: command not found`** — 크로스 도구가 설치되지 않았다. 위 빌드 환경 절을 참고.
- **`undefined reference to '__bss_start'`** — Stage 1의 `boot.S`에서는 이 심볼을 참조하지 않는다. Stage 2부터다.
- **QEMU가 멈춘 채로 응답 없음** — Stage 1·Stage 2는 화면 출력이 없는 게 정상이다. 5초 timeout이 자동 종료시킨다.
- **macOS Apple Clang으로 빌드하고 싶다** — Apple Clang은 베어메탈 AArch64 ELF 생성을 직접 지원하지 않는다. 호스트 dyld와 macho 포맷을 가정한다. 반드시 `aarch64-elf-gcc` 같은 베어메탈용 크로스 GCC를 쓰자.

## 다음 단계

세 스테이지가 모두 빌드되고 Stage 3이 QEMU에서 `hello, aarch64`를 찍으면, Ch14로 넘어가서 라즈베리 파이 4 보드용으로 같은 코드를 조정해보자. 시작 주소, UART 베이스, 빌드 산출물 포맷이 바뀌지만 부팅의 일곱 줄 약속은 그대로 통한다.
