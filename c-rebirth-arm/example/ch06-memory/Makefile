# Ch6 — 메모리 관리: 세 시나리오 분리 빌드
#
# `make leak`  — 의도된 누수. macOS는 `make leak-check`로 점검.
# `make uaf`   — 해제 후 사용. ASan이 정확히 잡아 준다.
# `make ok`    — 정상 동작. ASan이 켜져도 깨끗하다.
# `make all`   — 셋 다 빌드.
# `make demo`  — 셋을 순서대로 시연 (uaf는 실패가 정상)
# `make leak-check` — macOS 내장 `leaks --atExit`로 누수 점검
# `make clean` — 산물 정리

CC      := clang
CFLAGS  := -std=c23 -Wall -Wextra -Wpedantic -O0 -g \
           -fsanitize=address,undefined -fno-omit-frame-pointer
LDFLAGS := -fsanitize=address,undefined

# macOS ASan은 LSan 모듈이 없어 누수 옵션을 켤 수 없다.
# UAF·OOB는 정상 동작하므로 ASan은 그대로 두고, 누수는
# 본문에서 `leaks --atExit`로 안내한다.
ASAN_OPTS := ASAN_OPTIONS=abort_on_error=0

.PHONY: all leak uaf ok demo leak-check clean

all: leak uaf ok

leak: leak.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

uaf: uaf.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

ok: ok.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# 셋을 순서대로 보여준다. uaf는 ASan이 잡고 비정상 종료해도
# 데모 흐름은 계속 가도록 `|| true`로 받아 둔다.
demo: all
	@echo "=== [ok] 정상 동작 ===" && $(ASAN_OPTS) ./ok
	@echo
	@echo "=== [leak] 누수 — 코드는 동작하지만 종료 시 잔량이 남는다 ==="
	@$(ASAN_OPTS) ./leak || true
	@echo
	@echo "=== [uaf] 해제 후 사용 — ASan이 잡는다 ==="
	@$(ASAN_OPTS) ./uaf || true

# macOS 내장 도구로 누수 점검. ASan과 함께 쓰지 말 것 — 충돌 가능.
leak-check: leak.c
	$(CC) -std=c23 -Wall -Wextra -O0 -g -o leak_noasan leak.c
	leaks --atExit -- ./leak_noasan || true
	rm -f leak_noasan

clean:
	rm -f leak uaf ok
	rm -rf *.dSYM
