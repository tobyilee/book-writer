#!/usr/bin/env bash
# check_env.sh — 3장. Apple Silicon 위 C 개발 환경 점검
#
# 깔려 있는 도구의 존재 여부와 버전을 한꺼번에 보여준다.
# 어떤 도구가 빠져 있는지를 눈으로 확인하는 게 목적이라, 빠진 게 있어도 멈추지 않는다.

set -u

probe() {
    local cmd="$1"
    local label="${2:-$1}"
    if command -v "$cmd" >/dev/null 2>&1; then
        local ver
        ver=$("$cmd" --version 2>&1 | head -n 1)
        printf "  [ok ] %-22s : %s\n" "$label" "$ver"
    else
        printf "  [ -- ] %-22s : (없음 — 필요하면 brew/xcode-select로 깔자)\n" "$label"
    fi
}

echo "--- 호스트 도구 ---"
probe clang
probe lldb
probe make
probe git
probe cmake
probe ninja
probe pkg-config

echo
echo "--- 베어메탈 / 에뮬레이션 ---"
probe aarch64-elf-gcc
probe arm-none-eabi-gcc
probe qemu-system-aarch64

echo
echo "--- LLVM 도구 (Homebrew LLVM 경로에 있는 게 보통) ---"
probe clangd
probe clang-tidy
probe clang-format

echo
echo "--- Homebrew 접두어 (Apple Silicon은 /opt/homebrew, Intel은 /usr/local) ---"
if command -v brew >/dev/null 2>&1; then
    echo "  HOMEBREW_PREFIX = $(brew --prefix)"
else
    echo "  brew가 깔려 있지 않다. 호스트 셋업의 출발점이라 깔아두는 편이 낫다."
fi
