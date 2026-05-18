# Top-level Makefile — drives all 15 chapter examples.
#
# Usage:
#   make all       # build every example
#   make clean     # clean every example
#   make verify    # build + sanity-check each (alias for all + brief run)
#   make ch07-ub   # build a single chapter
#
# Host examples (Ch1~Ch11) need only Apple Clang + make.
# Bare-metal examples (Ch12~Ch14) need clang + lld + llvm-objcopy
# (install via: brew install llvm; ensure /opt/homebrew/opt/llvm/bin is on PATH)
# or aarch64-elf-gcc cross toolchain.

HOST_CHAPTERS := \
	ch01-hello-2026 \
	ch02-std-matrix \
	ch03-day0-setup \
	ch04-editor-setup \
	ch05-pointers \
	ch06-memory \
	ch07-ub \
	ch08-linker \
	ch09-sanitizers \
	ch10-libc-gap \
	ch11-freestanding

BARE_CHAPTERS := \
	ch12-aarch64-hello \
	ch13-boot-anatomy \
	ch14-rpi4

INFO_CHAPTERS := ch15-next-steps

ALL_CHAPTERS := $(HOST_CHAPTERS) $(BARE_CHAPTERS) $(INFO_CHAPTERS)

.PHONY: all clean verify host bare info $(ALL_CHAPTERS)

all: host bare

host: $(HOST_CHAPTERS)

bare: $(BARE_CHAPTERS)

info: $(INFO_CHAPTERS)

$(HOST_CHAPTERS) $(BARE_CHAPTERS) $(INFO_CHAPTERS):
	@printf "\n\033[1;34m==> %s\033[0m\n" "$@"
	@$(MAKE) -C $@ all 2>&1 | tail -20 || (echo "BUILD FAIL: $@"; exit 1)

clean:
	@for d in $(ALL_CHAPTERS); do \
		printf "  cleaning %s\n" "$$d"; \
		$(MAKE) -s -C "$$d" clean 2>/dev/null || true; \
	done

verify: all
	@echo ""
	@echo "all 15 chapter examples built."
