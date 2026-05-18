# Ch5 — 포인터 다섯 시나리오
#
# `make`      — 빌드
# `make run`  — 실행
# `make asan` — ASan/UBSan 켜고 다시 빌드 (디버깅용)

CC := clang
CFLAGS := -std=c23 -Wall -Wextra -Wpedantic -O0 -g

BIN := pointers

.PHONY: all run asan clean

all: $(BIN)

$(BIN): pointers.c
	$(CC) $(CFLAGS) -o $@ $<

run: $(BIN)
	./$(BIN)

asan: CFLAGS += -fsanitize=address,undefined -fno-omit-frame-pointer
asan: clean $(BIN)
	./$(BIN)

clean:
	rm -f $(BIN)
	rm -rf *.dSYM
