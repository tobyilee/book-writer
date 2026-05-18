# 9장. 같은 한 소스를 빌드 매트릭스로 다섯 번 도는 예제.
#
# 사용:
#   make asan       # ASan + 디버그 정보 — off-by-one 을 잡는다
#   make ubsan      # UBSan 도 함께 — null/overflow/oob 류 UB
#   make msan      # MSan (clang 필수, macOS는 제한적)
#   make release    # sanitizer 끄고 빌드 — 침묵하는 걸 확인
#   make clang-tidy # 정적 분석으로 같은 버그를 잡아 보기
#   make format     # clang-format 검사
#   make scan       # scan-build 가 깔려 있을 때
#   make matrix     # 위 매트릭스를 한 번에 돌려 비교
#   make clean

# clang 을 명시적으로 잡는다 — MSan 은 Apple Clang에서 빠져 있을 수 있다.
CC      ?= clang
WARN     = -Wall -Wextra -Wpedantic -g -fno-omit-frame-pointer
CSTD     = -std=c17

ASAN_FLAGS  = -fsanitize=address $(WARN) $(CSTD)
UBSAN_FLAGS = -fsanitize=address,undefined $(WARN) $(CSTD)
MSAN_FLAGS  = -fsanitize=memory $(WARN) $(CSTD)
REL_FLAGS   = -O2 -DNDEBUG -Wall -Wextra $(CSTD)

.PHONY: all asan ubsan msan release clang-tidy format scan matrix clean

all: bug_asan bug_ubsan bug_release

asan: bug_asan
	@echo "--- asan run (off-by-one 을 ASan 이 잡는다) ---"
	-./bug_asan

ubsan: bug_ubsan
	@echo "--- ubsan run (ASan + UBSan) ---"
	-./bug_ubsan

msan: bug_msan
	@echo "--- msan run (macOS 에서는 제한적) ---"
	-./bug_msan

release: bug_release
	@echo "--- release run (도구 없이 침묵하는지 확인) ---"
	-./bug_release

bug_asan: bug.c
	$(CC) $(ASAN_FLAGS) bug.c -o bug_asan

bug_ubsan: bug.c
	$(CC) $(UBSAN_FLAGS) bug.c -o bug_ubsan

bug_msan: bug.c
	$(CC) $(MSAN_FLAGS) bug.c -o bug_msan

bug_release: bug.c
	$(CC) $(REL_FLAGS) bug.c -o bug_release

clang-tidy:
	@echo "--- clang-tidy 정적 분석 ---"
	clang-tidy bug.c -- $(CSTD) $(WARN)

format:
	@echo "--- clang-format 검사 (수정은 -i) ---"
	clang-format --dry-run --Werror bug.c

scan:
	@echo "--- scan-build (없으면 스킵) ---"
	@command -v scan-build >/dev/null && scan-build $(CC) $(WARN) $(CSTD) -c bug.c -o /tmp/bug_scan.o || \
	  echo "scan-build not found, skipping."

matrix: asan ubsan release
	@echo
	@echo "=== matrix 요약 ==="
	@echo "asan/ubsan 빌드에서는 ASan 이 stack-buffer-overflow 를 잡았어야 한다."
	@echo "release 빌드에서는 우연한 값으로 sum 이 찍혔을 가능성이 높다 (침묵)."

clean:
	rm -f bug_asan bug_ubsan bug_msan bug_release
