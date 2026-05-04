"""
시니어의 학습법 — 표지 생성 스크립트 (Concept A: 미니멀 타이포 + 6레이어 도식)

색상:
  - 배경: 깊은 인디고 #181a3a
  - 메인 활자: 따뜻한 오프화이트 #f1ece0
  - 부제/보조: 머스터드 라이트 #d6b96a (한 점 강조)
  - 레이어 라인: 오프화이트 + 30% alpha (서브 톤)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("/Users/tobylee/workspace/ai/book-writer/ultimate-focus-super-learning/cover.png")

W, H = 1600, 2560

# Palette
BG = (24, 26, 58)            # 깊은 인디고
INK = (241, 236, 224)        # 오프화이트
SUB = (214, 185, 106)        # 머스터드 (강조 한 점)
DIM = (160, 158, 188)        # 부제용 라벤더 그레이
LINE = (241, 236, 224, 110)  # 레이어 선 (반투명 — RGBA용)

# Fonts
KO_BOLD = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # AppleSDGothicNeo Bold
KO_REG  = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
LATIN   = "/System/Library/Fonts/Helvetica.ttc"

def load(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

# AppleSDGothicNeo.ttc 인덱스: 0=Thin, 1=UltraLight, 2=Light, 3=Regular, 4=Medium, 5=SemiBold, 6=Bold, 7=ExtraBold, 8=Heavy
title_font    = load(KO_BOLD, 200, index=6)   # Bold
title_font_sm = load(KO_BOLD, 200, index=5)
sub_kor_font  = load(KO_REG, 60, index=4)     # Medium
abbr_font     = load(LATIN, 64, index=2)      # Helvetica Bold (대략)
small_font    = load(LATIN, 38, index=0)
author_font   = load(KO_REG, 40, index=4)
tag_font      = load(LATIN, 28, index=2)

# Canvas
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# --- Top: small label "A LEARNING OPERATING SYSTEM"
top_label = "A  L E A R N I N G   O P E R A T I N G   S Y S T E M"
tw = draw.textlength(top_label, font=tag_font)
draw.text(((W - tw) / 2, 240), top_label, font=tag_font, fill=SUB)

# Thin divider under top label
draw.line([(W/2 - 80, 300), (W/2 + 80, 300)], fill=SUB, width=2)

# --- Title: 두 줄
# 시니어의 / 학습법
title_l1 = "시니어의"
title_l2 = "학습법"

t1w = draw.textlength(title_l1, font=title_font)
t2w = draw.textlength(title_l2, font=title_font)

draw.text(((W - t1w) / 2, 460), title_l1, font=title_font, fill=INK)
draw.text(((W - t2w) / 2, 700), title_l2, font=title_font, fill=INK)

# --- Subtitle (영문 약어가 시각적 무게중심)
abbr_line = "FIT  ·  PACER  ·  RAIL"
aw = draw.textlength(abbr_line, font=abbr_font)
draw.text(((W - aw) / 2, 1010), abbr_line, font=abbr_font, fill=SUB)

sub_kor_font = load(KO_REG, 66, index=4)
sub_l1 = "다시 짜는 집중과 학습의 운영체제"
s1w = draw.textlength(sub_l1, font=sub_kor_font)
draw.text(((W - s1w) / 2, 1110), sub_l1, font=sub_kor_font, fill=DIM)

# --- 6레이어 도식: 6개의 가는 수평선이 누적 (운영체제 스택 메타포)
# 각 라인 옆에 1글자 라벨 (F·E·R·S·A·M)

layer_labels = [
    ("F", "Focus"),
    ("E", "Encoding"),
    ("R", "Retrieval"),
    ("S", "Skill"),
    ("A", "AI"),
    ("M", "Metacognition"),
]

stack_top = 1380
stack_gap = 110
stack_left = 480
stack_right = 1120
label_x = stack_right + 60
word_x = label_x + 90

# 위 -> 아래로 누적되는 레이어. M(Metacognition)이 맨 아래 = "기반층"
# 책 메시지: 메타인지가 모든 것을 떠받친다
for i, (letter, word) in enumerate(layer_labels):
    y = stack_top + i * stack_gap
    # 가는 가로선
    draw.line([(stack_left, y), (stack_right, y)], fill=INK, width=2)
    # 좌측 letter (대문자)
    letter_font = load(LATIN, 56, index=2)
    lw = draw.textlength(letter, font=letter_font)
    draw.text((stack_left - 70 - lw, y - 35), letter, font=letter_font, fill=INK)
    # 우측 word (서브 톤)
    word_font = load(LATIN, 32, index=0)
    draw.text((stack_right + 40, y - 22), word, font=word_font, fill=DIM)

# 맨 아래 레이어 강조 — Metacognition 라인을 머스터드로 두껍게
last_y = stack_top + (len(layer_labels) - 1) * stack_gap
draw.line([(stack_left, last_y), (stack_right, last_y)], fill=SUB, width=4)

# --- 하단: 저자 + 보조 라벨
# 가는 수평 디바이더
draw.line([(W/2 - 40, H - 320), (W/2 + 40, H - 320)], fill=SUB, width=2)

# Toby-AI
au = "Toby — AI"
auw = draw.textlength(au, font=author_font)
draw.text(((W - auw) / 2, H - 280), au, font=author_font, fill=INK)

# 매우 작은 태그
foot = "F O R   S E N I O R   E N G I N E E R S"
fw = draw.textlength(foot, font=tag_font)
draw.text(((W - fw) / 2, H - 200), foot, font=tag_font, fill=DIM)

# Save
img.save(OUT, "PNG", optimize=True)
print(f"saved: {OUT}  ({W}x{H})")
