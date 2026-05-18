# Ch11. Freestanding C — 호스트 OS 없는 세계의 손풀기
#
# 빌드 결과는 정적 라이브러리 libmini.a 하나뿐이다.
# main이 없는 것은 의도된 모양 — freestanding에서는 진입점조차
# 우리가 정하는 것이다. 이 라이브러리는 Ch12에서 다시 만난다.
#
# make        — 호스트 환경에서 -ffreestanding -nostdlib로 libmini.a 만들기
# make verify — libmini.a의 심볼을 nm으로 확인 (libc 의존이 없는지 검사)
# make clean  — 산물 정리

CC      ?= clang
AR      ?= ar
# host build with freestanding semantics; we still target the host triple,
# but turn off stdlib expectations and builtins so the compiler doesn't
# silently call into libc helpers.
CFLAGS  ?= -std=c17 -Wall -Wextra -Wpedantic -O2 -g \
           -ffreestanding -fno-builtin -fno-stack-protector \
           -fno-asynchronous-unwind-tables

OBJ = mini.o
LIB = libmini.a

all: $(LIB)

$(LIB): $(OBJ)
	$(AR) rcs $@ $(OBJ)

mini.o: mini.c mini.h
	$(CC) $(CFLAGS) -c mini.c -o mini.o

verify: $(LIB)
	@echo "--- libmini.a 안의 정의된 심볼 (T = text/code) ---"
	@nm $(LIB) | grep " T " | sort || true
	@echo
	@echo "--- libmini.a가 외부로 부르는 함수 (U = undefined) ---"
	@echo "비어 있으면 libc 의존이 0이라는 뜻 — 베어메탈에 그대로 가져다 쓸 수 있다."
	@nm $(LIB) | grep " U " | sort || true

clean:
	rm -f $(OBJ) $(LIB)

.PHONY: all verify clean
