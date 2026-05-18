# Ch12. 첫 AArch64 커널 — QEMU에서 "hello, aarch64"
#
# 두 가지 툴체인 중 환경에 있는 쪽을 자동으로 고른다.
#   1) aarch64-elf-gcc  (brew install aarch64-elf-gcc) — 가장 흔한 선택
#   2) clang --target=aarch64-none-elf + ld.lld         — Homebrew lld만 있어도 OK
#
# make        — kernel.elf 빌드
# make run    — QEMU에서 실행 (-nographic, Ctrl+A x 로 종료)
# make debug  — QEMU를 -s -S로 띄워 lldb/gdb 원격 디버깅 대기
# make clean  — 산물 정리

# ---- 툴체인 자동 감지 -----------------------------------------------------

AARCH64_GCC := $(shell command -v aarch64-elf-gcc 2>/dev/null)
LLD         := $(shell command -v ld.lld 2>/dev/null)
QEMU        := $(shell command -v qemu-system-aarch64 2>/dev/null)
ifeq ($(QEMU),)
QEMU := $(firstword $(wildcard /opt/homebrew/Cellar/qemu/*/bin/qemu-system-aarch64))
endif

ifneq ($(AARCH64_GCC),)
  TOOL    = gcc
  CC      = aarch64-elf-gcc
  LD      = aarch64-elf-ld
  CFLAGS  = -ffreestanding -nostdlib -nostartfiles \
            -mgeneral-regs-only -mcpu=cortex-a72 \
            -O2 -g -Wall -Wextra
  LDFLAGS = -T linker.ld -nostdlib
else ifneq ($(LLD),)
  TOOL    = clang
  CC      = clang
  LD      = ld.lld
  CFLAGS  = --target=aarch64-none-elf -ffreestanding -nostdlib \
            -mgeneral-regs-only -mcpu=cortex-a72 \
            -O2 -g -Wall -Wextra
  LDFLAGS = -T linker.ld
else
  $(error 툴체인이 없다. 'brew install aarch64-elf-gcc' 또는 'brew install lld' 중 하나가 필요하다.)
endif

# ---- 빌드 규칙 ------------------------------------------------------------

OBJ = boot.o kernel.o
ELF = kernel.elf

all: $(ELF)
	@echo "툴체인: $(TOOL) ($(CC) + $(LD))"

$(ELF): $(OBJ) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJ)

boot.o: boot.S
	$(CC) $(CFLAGS) -c $< -o $@

kernel.o: kernel.c
	$(CC) $(CFLAGS) -c $< -o $@

run: $(ELF)
ifeq ($(QEMU),)
	@echo "qemu-system-aarch64이 PATH에 없다."
	@echo "  brew install qemu"
	@echo "  설치 후 PATH가 /opt/homebrew/bin 을 가리키는지 확인."
	@exit 1
else
	@echo "QEMU 시작 — 종료는 Ctrl+A 누른 뒤 x"
	$(QEMU) -M virt -cpu cortex-a72 -nographic -kernel $(ELF)
endif

debug: $(ELF)
	@echo "QEMU를 -s -S로 띄운다. 다른 터미널에서 다음 중 하나로 붙는다."
	@echo "  lldb -o 'gdb-remote localhost:1234' $(ELF)"
	@echo "  aarch64-elf-gdb $(ELF) -ex 'target remote :1234'"
	$(QEMU) -M virt -cpu cortex-a72 -nographic -kernel $(ELF) -s -S

clean:
	rm -f $(OBJ) $(ELF)

.PHONY: all run debug clean
