# Shared bare-metal AArch64 toolchain detection.
#
# Include from a chapter Makefile with:
#   include ../bare-toolchain.mk
# or (for ch13 stages, two levels deep):
#   include ../../bare-toolchain.mk
#
# After include, the following variables are set:
#   CC, LD, OBJCOPY, OBJDUMP, READELF, CFLAGS, LDFLAGS
#
# Override CROSS or any of the above to use a different toolchain.

AARCH64_GCC := $(shell command -v aarch64-elf-gcc 2>/dev/null)
LLD         := $(shell command -v ld.lld 2>/dev/null)
LLVM_OBJCOPY := $(shell command -v llvm-objcopy 2>/dev/null)
ifeq ($(LLVM_OBJCOPY),)
LLVM_OBJCOPY := $(firstword $(wildcard /opt/homebrew/opt/llvm/bin/llvm-objcopy))
endif
LLVM_OBJDUMP := $(shell command -v llvm-objdump 2>/dev/null)
ifeq ($(LLVM_OBJDUMP),)
LLVM_OBJDUMP := $(firstword $(wildcard /opt/homebrew/opt/llvm/bin/llvm-objdump))
endif
LLVM_READELF := $(shell command -v llvm-readelf 2>/dev/null)
ifeq ($(LLVM_READELF),)
LLVM_READELF := $(firstword $(wildcard /opt/homebrew/opt/llvm/bin/llvm-readelf))
endif
# Fallbacks via aarch64-linux-gnu binutils (from messense/macos-cross-toolchains)
GNU_OBJCOPY := $(shell command -v aarch64-linux-gnu-objcopy 2>/dev/null)
GNU_OBJDUMP := $(shell command -v aarch64-linux-gnu-objdump 2>/dev/null)
GNU_READELF := $(shell command -v aarch64-linux-gnu-readelf 2>/dev/null)

ifneq ($(AARCH64_GCC),)
  TOOL    := aarch64-elf-gcc
  CC      := aarch64-elf-gcc
  LD      := aarch64-elf-ld
  OBJCOPY := aarch64-elf-objcopy
  OBJDUMP := aarch64-elf-objdump
  READELF := aarch64-elf-readelf
  CFLAGS_BASE := -ffreestanding -nostdlib -nostartfiles \
                 -mgeneral-regs-only -mcpu=cortex-a72 \
                 -Wall -Wextra -O2
else ifneq ($(LLD),)
  TOOL    := clang+lld
  CC      := clang
  LD      := ld.lld
  OBJCOPY := $(or $(LLVM_OBJCOPY),$(GNU_OBJCOPY),llvm-objcopy)
  OBJDUMP := $(or $(LLVM_OBJDUMP),$(GNU_OBJDUMP),llvm-objdump)
  READELF := $(or $(LLVM_READELF),$(GNU_READELF),llvm-readelf)
  CFLAGS_BASE := --target=aarch64-none-elf -ffreestanding -nostdlib \
                 -mgeneral-regs-only -mcpu=cortex-a72 \
                 -Wall -Wextra -O2
else
  $(error AArch64 cross toolchain not found. Install with: brew install aarch64-elf-gcc — or — brew install llvm lld)
endif

QEMU := $(shell command -v qemu-system-aarch64 2>/dev/null)
ifeq ($(QEMU),)
QEMU := $(firstword $(wildcard /opt/homebrew/Cellar/qemu/*/bin/qemu-system-aarch64))
endif
