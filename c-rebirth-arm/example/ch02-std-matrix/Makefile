# 2장. 표준 매트릭스 — 같은 코드를 다섯 표준으로 빌드한다.
#
# 사용:
#   make matrix           # std_demo.c를 c89/c99/c11/c17/c23로 다섯 번 빌드
#   make c23-only         # C23 전용 데모를 빌드·실행 (성공해야 정상)
#   make c23-only-as-c17  # 같은 코드를 C17로 빌드 시도 (에러 나는 게 정상)
#   make clean

CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic

# 표준 매트릭스
STDS     = c89 c99 c11 c17 c23

.PHONY: all matrix c23-only c23-only-as-c17 clean

all: matrix c23-only

matrix:
	@for s in $(STDS); do \
		echo "--- -std=$$s 빌드 ---"; \
		$(CC) -std=$$s $(WARN) std_demo.c -o std_demo_$$s && ./std_demo_$$s; \
	done

c23-only: c23_only
	@echo "--- C23 전용 데모 실행 ---"
	./c23_only

c23_only: c23_only.c
	$(CC) -std=c23 $(WARN) $< -o $@

# 일부러 실패하는 타깃. 에러 메시지를 그대로 보여주려고 `-` 접두로 빌드 실패를 허용한다.
c23-only-as-c17:
	@echo "--- 같은 코드를 -std=c17로 빌드 시도 (에러 나는 게 정상) ---"
	-$(CC) -std=c17 $(WARN) c23_only.c -o /dev/null 2>&1 || \
	   echo "(예상대로 컴파일이 거부되었다. 이게 표준 차이의 증거다.)"

clean:
	rm -f std_demo_c89 std_demo_c99 std_demo_c11 std_demo_c17 std_demo_c23 c23_only
