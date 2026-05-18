# Ch12 예제 — QEMU에서 "hello, aarch64"

이 디렉토리의 네 파일이 협력해서 책의 정점을 만든다.

| 파일 | 역할 |
|------|------|
| `boot.S` | 진입점 `_start`. primary core 골라내기, 스택 설정, `.bss` 클리어, `kernel_main` 호출 |
| `kernel.c` | `kernel_main()` — PL011 UART에 `"hello, aarch64\n"`을 한 글자씩 송신 |
| `linker.ld` | 섹션 배치 — `.text.boot`이 맨 앞, 로드 주소 `0x40080000`, 스택 64KB |
| `Makefile` | 툴체인 자동 감지 + QEMU 실행 |

## 사전 준비

### macOS (Apple Silicon)

두 길 중 하나만 있으면 빌드가 통과한다.

```bash
# 길 A — 정통 베어메탈 GCC (권장)
brew install aarch64-elf-gcc qemu

# 길 B — clang + lld (이미 LLVM 도구가 깔려 있다면 더 빠른 경로)
brew install lld qemu
```

`Makefile`은 `aarch64-elf-gcc`가 PATH에 있으면 그쪽을, 없고 `ld.lld`만 있으면
clang 경로를 자동으로 고른다. 둘 다 없으면 명확한 에러를 던진다.

### Linux

```bash
sudo apt install gcc-aarch64-linux-gnu qemu-system-arm
# 또는 베어메탈 전용을 원하면
sudo apt install gcc-aarch64-none-elf qemu-system-arm
```

Linux의 `aarch64-linux-gnu-gcc`도 `-ffreestanding -nostdlib`이면 무난히 동작한다.
다만 Makefile은 `aarch64-elf-gcc`를 찾으니 심볼릭 링크를 잡아주거나
`CC=aarch64-linux-gnu-gcc make`로 덮어쓰면 된다.

## 빌드와 실행

```bash
make            # kernel.elf 생성
make run        # QEMU에서 부팅 → 시리얼에 "hello, aarch64" 출력
make clean      # 산물 정리
```

`make run`이 성공하면 화면에 다음이 보인다.

```
hello, aarch64
```

그 뒤로는 커널이 `wfe`로 잠잠히 멈춰 있다. 종료는 다음 순서.

1. `Ctrl + A` (Mac에서는 fn 키 무관하게 control + a)
2. 손을 떼고 `x` 한 번

`-nographic` 모드에서 QEMU 자체 단축키가 `Ctrl+A` 접두어다. `Ctrl+A h`를 누르면
도움말이 나오니 한 번 봐두는 편이 낫다.

## 디버깅

```bash
make debug      # QEMU가 -s -S로 정지한 상태로 대기
```

다른 터미널에서 한 줄로 붙는다.

```bash
lldb -o 'gdb-remote localhost:1234' kernel.elf
# 또는
aarch64-elf-gdb kernel.elf -ex 'target remote :1234'
```

`b kernel_main` → `c` → `n` 한 단계씩 따라가 보면 우리가 쓴 코드가
정말 ARM CPU 위에서 한 명령씩 흐르고 있다는 걸 손으로 확인할 수 있다.

## 잘 안 될 때

| 증상 | 진단 |
|------|------|
| `make run`에서 화면이 까맣고 아무것도 안 보인다 | QEMU가 떴는지 의심하지 말 것 — `-nographic`이라 그래픽 창은 없다. 터미널 그 자체가 시리얼이다 |
| 글자가 깨져 보인다 | 커널이 `\r`을 안 보내 줄바꿈이 어긋났을 가능성. `uart_puts`의 `\r` 처리가 살아 있는지 확인 |
| `aarch64-elf-gcc not found` | 길 A를 안 깔았으면 `brew install aarch64-elf-gcc`. 그래도 없으면 `brew install lld`로 길 B로 가자 |
| `error: invalid linker name in argument '-fuse-ld=lld'` | Apple Clang 안에는 lld가 없다. `brew install lld`로 Homebrew lld를 따로 깔자 — Makefile은 자동으로 그쪽을 쓴다 |

이 디렉토리는 Ch13 부팅 흐름 해부의 출발점이기도 하다. 같은 코드를 한 줄씩
뜯어 보는 일이 다음 장에서 기다린다.
