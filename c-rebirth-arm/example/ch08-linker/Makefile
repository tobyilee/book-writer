# 8장. 다중 파일 빌드 — 분리 컴파일과 링크를 손에 익힌다.
#
# 사용:
#   make            # main, util, extern_global을 따로 .o로 만든 뒤 링크
#   make run        # 실행
#   make symbols    # objdump/nm 으로 각 .o의 심볼을 들여다본다
#   make compile-commands  # compile_commands.json의 directory 필드를 실제 경로로 채운다
#   make lldb       # lldb로 main에 break 걸어 step 실행
#   make stages     # 전처리(.i)·어셈블리(.s)·오브젝트(.o) 산물을 남긴다
#   make clean

CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic -g
CFLAGS   = -std=c17 $(WARN)

# macOS는 objdump/nm 모두 LLVM 도구가 보통 깔려 있다.
OBJDUMP ?= objdump
NM      ?= nm

OBJS = main.o util.o extern_global.o

.PHONY: all run symbols compile-commands lldb stages clean

all: app

app: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o app

%.o: %.c util.h
	$(CC) $(CFLAGS) -c $< -o $@

run: app
	./app

symbols: $(OBJS)
	@echo "=== nm: 각 .o가 공급하는 / 요구하는 심볼 ==="
	@for o in $(OBJS); do \
		echo "--- $$o ---"; \
		$(NM) $$o; \
	done
	@echo
	@echo "=== objdump -t: 심볼 테이블 ==="
	@for o in $(OBJS); do \
		echo "--- $$o ---"; \
		$(OBJDUMP) -t $$o 2>/dev/null || echo "(objdump unavailable)"; \
	done

compile-commands:
	@here="$$(pwd)"; \
	sed "s|REPLACE_WITH_ABS_PATH|$$here|g" compile_commands.json > compile_commands.local.json; \
	echo "wrote compile_commands.local.json with directory=$$here"

lldb: app
	@echo "lldb 시나리오: 'b main' 으로 main 진입에 break,"
	@echo "  'r' 로 실행, 's' 로 한 줄씩 진행, 'p g_call_count' 로 전역 확인."
	lldb -o "b main" -o "r" ./app

stages: main.c util.c extern_global.c
	@echo "=== 전처리(.i) ==="
	$(CC) $(CFLAGS) -E main.c -o main.i
	@echo "=== 어셈블리(.s) ==="
	$(CC) $(CFLAGS) -S main.c -o main.s
	@echo "=== 오브젝트(.o) ==="
	$(CC) $(CFLAGS) -c main.c -o main.o
	@echo "각 산물의 크기:"
	@wc -l main.i main.s
	@ls -l main.o

clean:
	rm -f *.o app main.i main.s compile_commands.local.json
