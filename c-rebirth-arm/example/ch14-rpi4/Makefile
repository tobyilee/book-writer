# Raspberry Pi 4 베어메탈 hello.
#
# 빌드 산출물:
#   kernel.elf  — 디버깅용 ELF (objdump/readelf에 쓴다)
#   kernel8.img — SD카드 또는 QEMU raspi4b에 올릴 flat binary

include ../bare-toolchain.mk

CFLAGS  := $(CFLAGS_BASE)
LDFLAGS := -T linker.ld

OBJS    := boot.o kernel.o

all: kernel8.img

# ELF → flat binary
kernel8.img: kernel.elf
	$(OBJCOPY) -O binary $< $@

kernel.elf: $(OBJS) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

%.o: %.S
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# QEMU raspi4b 머신에서 실행 — 보드 없이도 검증 가능.
qemu: kernel8.img
	@echo "QEMU raspi4b로 부팅. 시리얼에 hello, raspi4!가 보이면 성공. (Ctrl-A x)"
	$(QEMU) -M raspi4b -kernel kernel8.img -serial stdio -display none

# SD카드에 복사할 파일들을 dist/ 디렉토리에 모은다.
# config.txt는 직접 포함, 펌웨어 파일들은 사용자가 별도로 다운로드 필요.
sd-files: kernel8.img
	mkdir -p dist
	cp kernel8.img config.txt dist/
	@echo "dist/ 에 kernel8.img + config.txt 가 준비됐다."
	@echo "추가로 https://github.com/raspberrypi/firmware/tree/master/boot 에서"
	@echo "  start4.elf, fixup4.dat 를 받아 dist/ 에 함께 넣자."
	@echo "그 다음 SD카드를 FAT32로 포맷하고 dist/ 의 모든 파일을 복사한다."

objdump: kernel.elf
	$(OBJDUMP) -d $<

readelf: kernel.elf
	$(READELF) -h $<

clean:
	rm -rf *.o *.elf *.img dist

.PHONY: all qemu sd-files objdump readelf clean
