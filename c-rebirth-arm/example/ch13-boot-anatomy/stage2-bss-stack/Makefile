# Stage 2 — BSS 클리어 + 스택 셋업.

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
	@echo "Stage 2: 출력은 없지만 SP/BSS 셋업이 끝난 상태로 halt에 머문다."
	-timeout 5 $(QEMU) -M virt -cpu cortex-a72 -nographic -kernel kernel.elf || true

objdump: kernel.elf
	$(OBJDUMP) -d $<

readelf: kernel.elf
	$(READELF) -h $<

clean:
	rm -f *.o *.elf

.PHONY: all run objdump readelf clean
