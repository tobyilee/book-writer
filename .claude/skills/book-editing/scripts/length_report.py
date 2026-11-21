#!/usr/bin/env python3
"""Count prose characters per chapter, flag outliers, compare with the plan.

Usage: python3 length_report.py {slug} [--chapters]

Source: {slug}/04_manuscript.md when it exists (the text that ships), split on
`# N장` headings. With --chapters, or before the manuscript exists, it reads
{slug}/chapters/{NN}_final.md and falls back to {NN}_draft.md per chapter, so a
writer can measure a draft block.

Prose = chapter text minus fenced blocks (code, mermaid), ::: divs, tables,
block quotes, headings, and HTML comments. Characters are counted with spaces,
without newlines. Flags chapters under 70% or over 150% of the median, chapters
more than 20% off the plan's 예상 분량, and a first chapter below the median.
"""
import glob
import os
import re
import statistics
import sys

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
H1_CHAPTER = re.compile(r"^# (\d+)장")
NUMBER = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(만|천|k|K)?")


def outside_fences(text: str):
    """Yield (line, in_fence) so headings inside code blocks are not misread."""
    marker = None
    for ln in text.splitlines():
        m = FENCE.match(ln)
        if marker is None and m:
            marker = m.group(1)
            yield ln, True
        elif marker is not None:
            if m and m.group(1)[0] == marker[0] and len(m.group(1)) >= len(marker) \
                    and ln.strip() == m.group(1):
                marker = None
            yield ln, True
        else:
            yield ln, False


def prose_chars(text: str) -> int:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    depth = 0
    kept = []
    for ln, in_fence in outside_fences(text):
        if in_fence:
            continue
        s = ln.strip()
        if re.match(r"^:{3,}\s*\S", s):
            depth += 1
            continue
        if re.match(r"^:{3,}$", s):
            depth = max(0, depth - 1)
            continue
        if depth or s.startswith(("|", ">", "#")):
            continue
        kept.append(ln)
    return len("".join(kept))


def from_manuscript(path: str) -> dict[int, str]:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    chapters: dict[int, list[str]] = {}
    current = None
    for ln, in_fence in outside_fences(text):
        if not in_fence and ln.startswith("# "):
            m = H1_CHAPTER.match(ln)
            current = int(m.group(1)) if m else None  # 부록·참고문헌 H1 ends a chapter
            if current is not None:
                chapters[current] = []
            continue
        if current is not None:
            chapters[current].append(ln)
    return {n: "\n".join(lines) for n, lines in chapters.items()}


def from_chapter_files(slug: str) -> dict[int, str]:
    chapters: dict[int, str] = {}
    for kind in ("draft", "final"):  # final overrides draft
        for p in glob.glob(os.path.join(slug, "chapters", f"*_{kind}.md")):
            m = re.match(rf"(\d+)_{kind}\.md$", os.path.basename(p))
            if m:
                with open(p, encoding="utf-8") as f:
                    chapters[int(m.group(1))] = f.read()
    return chapters


def plan_targets(slug: str) -> dict[int, float]:
    """Best-effort parse of `- **예상 분량:** ...` under each `### N장` in the plan."""
    path = os.path.join(slug, "02_plan.md")
    if not os.path.isfile(path):
        return {}
    targets: dict[int, float] = {}
    current = None
    with open(path, encoding="utf-8") as f:
        for ln in f:
            m = re.match(r"^#{2,4}\s*(\d+)장", ln)
            if m:
                current = int(m.group(1))
            elif current is not None and "예상 분량" in ln and current not in targets:
                values = []
                for num, unit in NUMBER.findall(ln.split("예상 분량", 1)[1]):
                    v = float(num.replace(",", ""))
                    v *= {"만": 10000, "천": 1000, "k": 1000, "K": 1000}.get(unit, 1)
                    if v >= 500:  # skip stray small numbers (e.g. "3개 절")
                        values.append(v)
                if values:
                    targets[current] = sum(values[:2]) / len(values[:2])
    return targets


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: length_report.py {slug} [--chapters]")
    slug = args[0]
    manuscript = os.path.join(slug, "04_manuscript.md")
    if "--chapters" not in sys.argv and os.path.isfile(manuscript):
        chapters, source = from_manuscript(manuscript), "04_manuscript.md"
    else:
        chapters, source = from_chapter_files(slug), "chapters/*_final.md (없으면 draft)"
    if not chapters:
        sys.exit(f"no chapters found under {slug} ({source})")

    rows = [(n, prose_chars(chapters[n])) for n in sorted(chapters)]
    median = statistics.median(c for _, c in rows)
    targets = plan_targets(slug)
    notes = []

    print("| 장 | 산문 글자 수 | 중앙값 대비 | 계획 대비 | 판정 |")
    print("|----|-------------|------------|----------|------|")
    for n, c in rows:
        ratio = c / median if median else 0
        flags = []
        if ratio < 0.7:
            flags.append("⚠️ 짧음")
        elif ratio > 1.5:
            flags.append("⚠️ 김")
        plan_cell = "—"
        if n in targets:
            diff = c / targets[n] - 1
            plan_cell = f"{diff:+.0%} ({targets[n]:,.0f}자)"
            if abs(diff) > 0.2:
                flags.append("⚠️ 계획 ±20% 밖")
        print(f"| {n}장 | {c:,} | {ratio:.0%} | {plan_cell} | {' · '.join(flags) or 'OK'} |")
    first_n, first_c = rows[0]
    if len(rows) > 1 and first_c < median:
        notes.append(f"{first_n}장이 중앙값 아래다 ({first_c / median:.0%}) — 첫인상을 만드는 장이다.")
    if not targets:
        notes.append("02_plan.md에서 장별 예상 분량을 읽지 못했다 — 계획 대비는 직접 확인한다.")

    total = sum(c for _, c in rows)
    print()
    print(f"출처: {source} · 중앙값: {median:,.0f}자 · 합계: {total:,}자 "
          "(표·코드·mermaid·::: 블록·인용·헤딩 제외, 공백 포함)")
    if targets:
        planned = sum(targets.values())
        print(f"계획 합계: {planned:,.0f}자 · 실측/계획: {total / planned:.0%}")
    for note in notes:
        print(f"- {note}")


if __name__ == "__main__":
    main()
