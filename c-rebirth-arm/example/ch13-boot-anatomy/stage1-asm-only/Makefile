# Stage 1 — assembly only, infinite loop.

include ../../bare-toolchain.mk

CFLAGS  := $(CFLAGS_BASE)
LDFLAGS := -T linker.ld

OBJS    := boot.o

all: kernel.elf

kernel.elf: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

%.o: %.S
	$(CC) $(CFLAGS) -c $< -o $@

run: kernel.elf
	@echo "Stage 1: 화면에 아무것도 안 나오는 게 정상이다. (5초 후 자동 종료)"
	-timeout 5 $(QEMU) -M virt -cpu cortex-a72 -nographic -kernel kernel.elf || true

objdump: kernel.elf
	$(OBJDUMP) -d $<

readelf: kernel.elf
	$(READELF) -h $<

clean:
	rm -f *.o *.elf

.PHONY: all run objdump readelf clean
