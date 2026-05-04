"""
Cover generator for "꺼내 쓰는 뇌".

Concept: 1안+2안 융합. 종이결 위에 미니멀 신경 그물망(인지망) — 그물망의
한 가닥이 빛으로 변환되며 화면 바깥으로 빠져나오는 모티프 (인출의 시각화).
색감: 따뜻한 아이보리 베이스 + 깊은 인디고 강조 + 띠지에 골드 라인.
타이포: Apple SD Gothic Neo Heavy (본제) + NotoSansKR (부제·저자).
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUTPUT = Path(__file__).parent / "cover.png"
W, H = 1600, 2560

# Color palette — 아이보리·인디고·골드
IVORY = (244, 238, 226)
IVORY_DARK = (228, 218, 200)
INDIGO = (24, 36, 72)
INDIGO_SOFT = (52, 70, 120)
GOLD = (190, 152, 78)
GOLD_LIGHT = (220, 188, 124)
INK = (18, 22, 36)

FONT_DIRS = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Users/tobylee/Library/Fonts/NotoSansKR-VariableFont_wght.ttf",
    "/Users/tobylee/Library/Fonts/NanumGothicExtraBold.otf",
    "/Users/tobylee/Library/Fonts/NanumGothic.otf",
    "/Users/tobylee/Library/Fonts/NanumGothicLight.otf",
]


def load_font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        if path.endswith(".ttc"):
            return ImageFont.truetype(path, size, index=index)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def make_paper_texture(w: int, h: int) -> Image.Image:
    """아이보리 종이결 — 미세 노이즈 + 부드러운 비네팅."""
    base = Image.new("RGB", (w, h), IVORY)
    px = base.load()
    rng = random.Random(7)
    # 미세 노이즈 (종이결)
    for y in range(h):
        for x in range(w):
            n = rng.randint(-6, 6)
            r, g, b = px[x, y]
            px[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n - 1)),
            )
    # 부드러운 가로 결 — blur
    base = base.filter(ImageFilter.GaussianBlur(radius=0.6))
    # 비네팅: 모서리를 살짝 어둡게
    vignette = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vignette)
    for i in range(60):
        alpha = int(70 * (1 - i / 60))
        vd.rectangle(
            [i * (w // 200), i * (h // 200), w - i * (w // 200), h - i * (h // 200)],
            outline=alpha,
        )
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))
    dark = Image.new("RGB", (w, h), IVORY_DARK)
    base = Image.composite(dark, base, vignette)
    return base


def draw_neural_mesh(img: Image.Image) -> None:
    """절제된 신경 그물망. 정돈된 노드 + 가는 인디고 선.
    한 가닥이 골드 광선으로 변형되어 화면 우상단으로 '빠져나간다'."""
    draw = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(11)

    cx, cy = W // 2, int(H * 0.36)  # 그물망 중심을 위로 올림 (제목과 여백 확보)
    radius = 480  # 더 좁힘 — 절제

    # 노드 배치 — 더 적게, 정돈되게 (28개)
    nodes: list[tuple[int, int]] = []
    for _ in range(22):
        angle = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(120, radius)
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle) * 0.78)
        nodes.append((x, y))
    # 중심부 핵심 노드
    for _ in range(4):
        nodes.append(
            (
                cx + rng.randint(-90, 90),
                cy + rng.randint(-70, 70),
            )
        )

    # 엣지: 각 노드와 가까운 2~3개만 연결 (덜 빽빽하게)
    edges: list[tuple[int, int]] = []
    for i, (x1, y1) in enumerate(nodes):
        dists = sorted(
            (
                ((x2 - x1) ** 2 + (y2 - y1) ** 2, j)
                for j, (x2, y2) in enumerate(nodes)
                if j != i
            )
        )
        for _, j in dists[: rng.randint(2, 3)]:
            if (j, i) not in edges:
                edges.append((i, j))

    # 엣지 그리기 — 가는 인디고 선
    for i, j in edges:
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        d = math.hypot(x2 - x1, y2 - y1)
        alpha = max(50, int(170 - d * 0.16))
        draw.line([(x1, y1), (x2, y2)], fill=INDIGO_SOFT + (alpha,), width=2)

    # 노드: 작은 점
    for x, y in nodes:
        size = rng.randint(5, 8)
        draw.ellipse(
            [(x - size, y - size), (x + size, y + size)],
            fill=INDIGO + (220,),
        )

    # 핵심 노드 강조 — 진한 인디고 큰 점 + 골드 외곽 링
    core_nodes = [(cx - 70, cy - 20), (cx + 50, cy + 30), (cx, cy)]
    for x, y in core_nodes:
        draw.ellipse(
            [(x - 14, y - 14), (x + 14, y + 14)],
            fill=INDIGO + (255,),
        )
        draw.ellipse(
            [(x - 22, y - 22), (x + 22, y + 22)],
            outline=GOLD + (180,),
            width=2,
        )

    # === 인출의 가닥 ===
    # 그물망 안쪽에서 시작해 우상단 바깥으로 빠져나가는 골드 곡선
    start = (cx - 20, cy - 5)
    p1 = start
    p2 = (cx + 240, cy - 180)
    p3 = (cx + 460, cy - 380)
    p4 = (W + 100, int(H * 0.04))  # 화면 바깥

    # 베지어 점 샘플링
    def bezier(t: float) -> tuple[float, float]:
        x = (
            (1 - t) ** 3 * p1[0]
            + 3 * (1 - t) ** 2 * t * p2[0]
            + 3 * (1 - t) * t**2 * p3[0]
            + t**3 * p4[0]
        )
        y = (
            (1 - t) ** 3 * p1[1]
            + 3 * (1 - t) ** 2 * t * p2[1]
            + 3 * (1 - t) * t**2 * p3[1]
            + t**3 * p4[1]
        )
        return x, y

    # 글로우 — 두꺼운 골드 라이트로 먼저 그린 뒤 블러
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    pts = [bezier(t / 200) for t in range(201)]
    for w_, alpha in [(28, 90), (16, 140), (8, 220)]:
        glow_draw.line(pts, fill=GOLD_LIGHT + (alpha,), width=w_)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=6))
    img.alpha_composite(glow_layer)

    # 위에 또렷한 골드 가닥
    sharp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sharp)
    sd.line(pts, fill=GOLD + (255,), width=3)
    img.alpha_composite(sharp)

    # 가닥 따라 작은 빛 입자 4~5개
    particle = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particle)
    for t in [0.55, 0.7, 0.82, 0.92]:
        x, y = bezier(t)
        s = 6 + (1 - abs(0.7 - t)) * 6
        pd.ellipse(
            [(x - s, y - s), (x + s, y + s)],
            fill=GOLD_LIGHT + (255,),
        )
    particle = particle.filter(ImageFilter.GaussianBlur(radius=2))
    img.alpha_composite(particle)


def draw_top_band(img: Image.Image) -> None:
    """상단 띠지 — 4대 차별 키워드를 골드 가는 선과 함께 노출."""
    draw = ImageDraw.Draw(img, "RGBA")
    top = 160  # 좀 더 아래로 내림 (위 여백 확보)
    band_h = 90
    # 얇은 골드 라인 두 줄
    draw.line([(160, top), (W - 160, top)], fill=GOLD + (220,), width=2)
    draw.line(
        [(160, top + band_h), (W - 160, top + band_h)], fill=GOLD + (160,), width=1
    )

    font_band = load_font(FONT_DIRS[0], 34, index=2)  # SD Gothic SemiBold
    text = "인코딩 우선  ·  생성적 인출  ·  기회주의적 인출  ·  AI 시대의 메타인지"
    bbox = draw.textbbox((0, 0), text, font=font_band)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, top + 24), text, font=font_band, fill=INDIGO + (230,))


def draw_title_block(img: Image.Image) -> None:
    """본제 + 부제 — 그물망 아래쪽에 큼지막하게 배치."""
    draw = ImageDraw.Draw(img, "RGBA")

    # 본제: '꺼내 쓰는 뇌' — Apple SD Gothic Neo Heavy
    title_font = load_font(FONT_DIRS[0], 260, index=0)  # Heavy, 더 크게
    title = "꺼내 쓰는 뇌"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    title_x = (W - tw) // 2
    title_y = int(H * 0.65)  # 그물망과 충분한 여백
    # 살짝 그림자(종이 질감과 어우러지게 약하게)
    draw.text((title_x + 4, title_y + 4), title, font=title_font, fill=(0, 0, 0, 30))
    draw.text((title_x, title_y), title, font=title_font, fill=INDIGO + (255,))

    # 본제 아래 가는 골드 룰
    rule_y = title_y + th + 70
    draw.line(
        [(W // 2 - 140, rule_y), (W // 2 + 140, rule_y)],
        fill=GOLD + (220,),
        width=3,
    )

    # 부제: 두 줄 줄바꿈
    sub_font = load_font(FONT_DIRS[0], 64, index=2)  # SemiBold
    line1 = "지식을 성과로 바꾸는"
    line2 = "완벽한 기억과 인출의 과학"
    sub_y = rule_y + 70
    for line in (line1, line2):
        bb = draw.textbbox((0, 0), line, font=sub_font)
        lw = bb[2] - bb[0]
        draw.text(
            ((W - lw) // 2, sub_y),
            line,
            font=sub_font,
            fill=INK + (235,),
        )
        sub_y += 95


def draw_author_block(img: Image.Image) -> None:
    """저자명 + 출판 마크 — 표지 하단."""
    draw = ImageDraw.Draw(img, "RGBA")

    # 한 줄 후크 — 저자명 위쪽 (가독 우선순위 → 후크가 위, 저자가 아래)
    hook_font = load_font(FONT_DIRS[0], 32, index=0)  # Regular
    hook = "공부했는데 안 떠오른 적, 있는가?"
    hook_y = H - 280
    bb = draw.textbbox((0, 0), hook, font=hook_font)
    hw = bb[2] - bb[0]
    draw.text(((W - hw) // 2, hook_y), hook, font=hook_font, fill=INK + (170,))

    # 가는 골드 선 — 후크와 저자 사이
    sep_y = hook_y + 70
    draw.line(
        [(W // 2 - 80, sep_y), (W // 2 + 80, sep_y)], fill=GOLD + (200,), width=2
    )

    # 저자명
    author_font = load_font(FONT_DIRS[0], 52, index=2)  # Bold
    author = "Toby-AI"
    bbox = draw.textbbox((0, 0), author, font=author_font)
    aw = bbox[2] - bbox[0]
    draw.text(((W - aw) // 2, sep_y + 30), author, font=author_font, fill=INDIGO + (240,))


def main() -> None:
    img = make_paper_texture(W, H).convert("RGBA")
    draw_neural_mesh(img)
    draw_top_band(img)
    draw_title_block(img)
    draw_author_block(img)
    img.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    print(f"saved: {OUTPUT}")


if __name__ == "__main__":
    main()
