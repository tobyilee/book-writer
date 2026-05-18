# Ch4 — VS Code + clangd 셋업 검증용 미니 라이브러리
#
# `make`         — 라이브러리와 실행 파일 빌드
# `make run`     — 실행
# `make compdb`  — compile_commands.json 직접 생성 (bear 없이)
# `make clean`   — 산물 정리

CC      := clang
CFLAGS  := -std=c23 -Wall -Wextra -Wpedantic -O0 -g
LDFLAGS :=
LDLIBS  := -lm

SRCS := geom.c main.c
OBJS := $(SRCS:.c=.o)
BIN  := geom_demo

.PHONY: all run compdb clean

all: $(BIN)

$(BIN): $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LDLIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

run: $(BIN)
	./$(BIN)

# compile_commands.json을 손으로 만든다. bear가 없거나
# CMake가 부담스러운 작은 프로젝트일 때 쓰는 패턴.
compdb:
	@printf '[\n' > compile_commands.json
	@first=1; for f in $(SRCS); do \
	  if [ $$first -eq 0 ]; then printf ',\n' >> compile_commands.json; fi; \
	  printf '  {"directory":"%s","file":"%s","command":"%s %s -c %s"}' \
	    "$$(pwd)" "$$f" "$(CC)" "$(CFLAGS)" "$$f" >> compile_commands.json; \
	  first=0; \
	done
	@printf '\n]\n' >> compile_commands.json
	@echo "wrote compile_commands.json ($$(wc -c < compile_commands.json) bytes)"

clean:
	rm -f $(OBJS) $(BIN) compile_commands.json
	rm -rf *.dSYM
