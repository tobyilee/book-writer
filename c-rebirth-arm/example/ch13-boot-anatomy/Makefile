# ch13-boot-anatomy/Makefile
#
# Stage 1 → Stage 2 → Stage 3 차례로 빌드한다. 각 스테이지가 독립
# Makefile을 갖고 있으니 `make stage{1,2,3}` 또는 `make all`로 전체 빌드.

STAGES := stage1-asm-only stage2-bss-stack stage3-main-call

all: stage1 stage2 stage3

stage1:
	$(MAKE) -C stage1-asm-only

stage2:
	$(MAKE) -C stage2-bss-stack

stage3:
	$(MAKE) -C stage3-main-call

# 마지막 스테이지를 QEMU에서 실행한다 — hello, aarch64 출력 확인.
run-stage3:
	$(MAKE) -C stage3-main-call run

# 세 스테이지의 디스어셈블 결과를 차례로 살펴보기.
objdump-all:
	@for s in $(STAGES); do \
		echo "=== $$s ==="; \
		$(MAKE) -C $$s objdump 2>&1 | head -40; \
		echo; \
	done

readelf-all:
	@for s in $(STAGES); do \
		echo "=== $$s ==="; \
		$(MAKE) -C $$s readelf 2>&1 | head -20; \
		echo; \
	done

clean:
	@for s in $(STAGES); do $(MAKE) -C $$s clean; done

.PHONY: all stage1 stage2 stage3 run-stage3 objdump-all readelf-all clean
