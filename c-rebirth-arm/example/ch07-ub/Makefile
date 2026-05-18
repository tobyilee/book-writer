# 7장. UB 표본실.
#
# 사용:
#   make ubsan          # UBSan + ASan 켜고 빌드
#   make unsafe         # 그냥 빌드 (도구 없이는 침묵하는 걸 보기)
#   make run-all-ubsan  # ubsan 빌드로 네 시나리오 차례로
#   make clean

CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic -g

.PHONY: all ubsan unsafe run-all-ubsan clean

all: ub_zoo ub_zoo_unsafe

ubsan: ub_zoo
unsafe: ub_zoo_unsafe

# UBSan은 strict aliasing 위반은 직접 잡지 않는다.
# alias 데모는 ASan + -Werror=strict-aliasing 경고로 본다.
ub_zoo: ub_zoo.c
	$(CC) -std=c17 $(WARN) -fsanitize=undefined,address \
	      -fno-omit-frame-pointer \
	      -fno-strict-aliasing \
	      ub_zoo.c -o ub_zoo

ub_zoo_unsafe: ub_zoo.c
	$(CC) -std=c17 $(WARN) -O2 ub_zoo.c -o ub_zoo_unsafe

run-all-ubsan: ub_zoo
	-./ub_zoo overflow
	-./ub_zoo alias
	-./ub_zoo null
	-./ub_zoo oob

clean:
	rm -f ub_zoo ub_zoo_unsafe
