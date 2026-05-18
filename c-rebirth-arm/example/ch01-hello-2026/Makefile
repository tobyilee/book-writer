# 1장. C89와 C23으로 같은 인사를 두 번 빌드한다.
#
# 사용:
#   make c89    # 옛 표준으로 빌드, 결과 실행
#   make c23    # 모던 표준으로 빌드, 결과 실행
#   make both   # 두 표준 빌드를 한 번에
#   make clean

CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic

.PHONY: both c89 c23 clean

both: c89 c23

c89: hello_c89
	@echo "--- C89 빌드 결과 실행 ---"
	./hello_c89

c23: hello_c23
	@echo "--- C23 빌드 결과 실행 ---"
	./hello_c23

hello_c89: hello.c
	$(CC) -std=c89 $(WARN) $< -o $@

hello_c23: hello.c
	$(CC) -std=c23 $(WARN) $< -o $@

clean:
	rm -f hello_c89 hello_c23
