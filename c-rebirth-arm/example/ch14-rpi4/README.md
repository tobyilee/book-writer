# ch14-rpi4 — Raspberry Pi 4 베어메탈 hello

QEMU 가상 보드에서 손에 익힌 부팅 코드를 **진짜 라즈베리 파이 4 모델 B**에서 깨우는 예제다. SD카드 한 장과 USB-시리얼 어댑터 한 개만 있으면 책의 두 번째 정점에 도달할 수 있다.

## 파일

| 파일 | 역할 |
|------|------|
| `boot.S`      | AArch64 어셈블리 진입점 (Ch13의 일곱 줄 약속을 그대로 사용) |
| `kernel.c`    | PL011 UART 초기화 + `hello, raspi4!` 출력 |
| `linker.ld`   | 시작 주소 0x80000 (라즈베리 파이 4 64비트 적재 위치) |
| `Makefile`    | `kernel.elf` → `kernel8.img` 변환, QEMU 실행 타깃 |
| `config.txt`  | 부팅 설정 — `arm_64bit=1`, `enable_uart=1`, `dtoverlay=disable-bt` |

## 빌드 환경

`aarch64-elf-gcc` 크로스 도구가 필요하다.

**macOS:**

```sh
brew install --cask gcc-aarch64-embedded
# 또는
brew install aarch64-elf-gcc
```

**Ubuntu/Debian/WSL:**

```sh
sudo apt install gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu
make CROSS=aarch64-linux-gnu-
```

QEMU 9.0 이상이 필요하다 (`raspi4b` 머신).

```sh
brew install qemu        # macOS — 보통 최신 버전
sudo apt install qemu-system-arm   # Ubuntu — 패키지 버전 확인 필요
```

## 빠른 실행 — QEMU에서 먼저

```sh
make            # kernel8.img 생성
make qemu       # QEMU raspi4b 에서 부팅 → 시리얼에 hello, raspi4!
                # (종료: Ctrl-A x)
```

`qemu-system-aarch64 -M raspi4b` 머신이 라즈베리 파이 4 모델 B를 흉내내준다. 실기로 옮기기 전에 여기서 한 번 검증하는 것이 디버깅 시간을 크게 줄여준다.

## SD카드 부팅 — 실기로 옮기기

### 1. SD카드 파일 준비

```sh
make sd-files   # dist/ 디렉토리에 kernel8.img + config.txt 준비
```

추가로 라즈베리 파이 재단의 공식 firmware 저장소에서 두 파일을 받아 `dist/` 에 넣어야 한다.

- `start4.elf`
- `fixup4.dat`

다운로드 URL: <https://github.com/raspberrypi/firmware/tree/master/boot>

```sh
curl -L -o dist/start4.elf https://github.com/raspberrypi/firmware/raw/master/boot/start4.elf
curl -L -o dist/fixup4.dat https://github.com/raspberrypi/firmware/raw/master/boot/fixup4.dat
```

라즈베리 파이 4는 1차 부트로더가 EEPROM에 있으므로 `bootcode.bin`은 필요 없다 (Pi 3 이전 모델과 다른 점).

### 2. SD카드 포맷 및 복사 (macOS)

```sh
# SD카드 디바이스 확인 — 신중하게!
diskutil list

# 마운트 해제 (예시 — 실제 디바이스 번호로 바꿀 것)
diskutil unmountDisk /dev/disk5

# FAT32로 포맷
diskutil eraseDisk FAT32 RPI4 MBRFormat /dev/disk5

# 파일 복사
cp dist/* /Volumes/RPI4/

# 안전하게 추출
diskutil eject /dev/disk5
```

> **경고:** `diskutil list`로 SD카드의 디스크 번호를 반드시 확인하자. 잘못된 디스크를 지정하면 호스트 디스크가 지워진다.

### Linux:

```sh
lsblk
sudo umount /dev/sdX1
sudo mkfs.vfat -F 32 -n RPI4 /dev/sdX1
sudo mount /dev/sdX1 /mnt
sudo cp dist/* /mnt/
sudo sync
sudo umount /mnt
```

### 3. USB-시리얼 배선

| 보드 핀 번호 | 신호           | USB-시리얼 어댑터 |
|------------|----------------|------------------|
| 6번         | GND             | GND               |
| 8번 (GPIO14) | TX              | RX                |
| 10번 (GPIO15)| RX              | TX                |

**전원선(5V/3.3V)은 연결하지 않는다.** 보드는 USB-C 자체 전원, 어댑터는 PC USB 자체 전원. GND만 공유하고 데이터선은 교차 연결.

### 4. 시리얼 콘솔 열기

**macOS:**

```sh
ls /dev/cu.usbserial-*       # 디바이스 확인
screen /dev/cu.usbserial-AB0LXTZH 115200
# 종료: Ctrl-A 다음 k, y
```

**Linux:**

```sh
ls /dev/ttyUSB*
sudo screen /dev/ttyUSB0 115200
# 또는: sudo minicom -D /dev/ttyUSB0 -b 115200
```

### 5. 보드 전원 인가

SD카드를 보드에 꽂고, USB-시리얼을 PC에 꽂고, 시리얼 콘솔을 연 다음 보드에 USB-C 전원을 연결한다. 2~3초 후 시리얼 콘솔에 `hello, raspi4!`가 떠오르면 성공.

## 트러블슈팅

- **시리얼 콘솔이 침묵한다** — 다음 다섯 가지를 차례로 확인.
  1. ACT LED가 깜빡이는가? (안 깜빡이면 SD카드 펌웨어 파일 누락 가능성)
  2. `config.txt`에 `enable_uart=1`과 `dtoverlay=disable-bt`가 모두 있는가?
  3. USB-시리얼 배선이 교차로 연결됐는가 (TX↔RX)?
  4. 보레이트가 115200인가?
  5. 모든 부팅 파일이 SD카드 **루트**(서브디렉토리 아님)에 있는가?

- **글자가 깨져 나온다** — 보레이트 불일치. `enable_uart=1`이 없으면 UART 클럭이 흔들린다.

- **QEMU에서는 동작하는데 보드에서 안 된다** — SD카드, 배선, `config.txt` 쪽 문제. 코드 자체는 아님.

- **`aarch64-elf-gcc: command not found`** — 빌드 환경 절을 참고.

## 다음 단계

`hello, raspi4!`가 시리얼에 떴다면 책의 두 번째 정점에 도달한 것이다. 다음으로 가고 싶다면 `ch15-next-steps/` 의 README를 참고하자 — 인터럽트, MMU, 컨텍스트 스위치, 시스템 콜로 가는 네 갈래 길의 안내가 있다.
