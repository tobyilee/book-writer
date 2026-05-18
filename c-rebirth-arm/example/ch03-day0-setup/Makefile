# 3장. Apple Silicon Day 0 — 환경 점검과 첫 실행 파일 한 줄.
#
# 사용:
#   make check   # 깔린 도구 일람 (없어도 멈추지 않고 끝까지 본다)
#   make run     # triple.c 빌드·실행 — 컴파일러의 자기 인식 정보 출력
#   make clean

CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic
STD      = -std=c17

.PHONY: all check run clean

all: triple

check:
	@bash check_env.sh

run: triple
	@./triple

triple: triple.c
	$(CC) $(STD) $(WARN) $< -o $@

clean:
	rm -f triple
