# Stage 3 — Ch12와 동등한 완성형. `make run`이 시리얼에 hello 출력.

include ../../bare-toolchain.mk

CFLAGS  := $(CFLAGS_BASE)
LDFLAGS := -T linker.ld

OBJS    := boot.o kernel.o

all: kernel.elf

kernel.elf: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

%.o: %.S
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

run: kernel.elf
	@echo "Stage 3: 시리얼에 'hello, aarch64'가 찍히면 성공. (Ctrl-A x 로 종료)"
	$(QEMU) -M virt -cpu cortex-a72 -nographic -kernel kernel.elf

objdump: kernel.elf
	$(OBJDUMP) -d $<

readelf: kernel.elf
	$(READELF) -h $<

debug: kernel.elf
	$(QEMU) -M virt -cpu cortex-a72 -nographic -kernel kernel.elf -s -S

clean:
	rm -f *.o *.elf

.PHONY: all run objdump readelf debug clean
