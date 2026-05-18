# Ch10. 표준 라이브러리의 빈자리 — vec(동적 배열) + map(해시맵)
#
# make        — ASan + UBSan 켠 디버그 빌드
# make run    — 빌드 후 실행
# make clean  — 산물 정리

CC      ?= clang
CFLAGS  ?= -std=c17 -Wall -Wextra -Wpedantic -g -O1 \
           -fsanitize=address,undefined -fno-omit-frame-pointer
LDFLAGS ?= -fsanitize=address,undefined

SRC = vec.c map.c main.c
OBJ = $(SRC:.c=.o)
BIN = ch10-demo

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $(OBJ)

%.o: %.c vec.h map.h
	$(CC) $(CFLAGS) -c $< -o $@

run: $(BIN)
	./$(BIN)

clean:
	rm -f $(OBJ) $(BIN)

.PHONY: all run clean
