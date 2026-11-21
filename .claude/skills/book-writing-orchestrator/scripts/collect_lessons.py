#!/usr/bin/env python3
"""Collect book-lessons records from every branch and print the latest ones.

Usage: python3 collect_lessons.py [--genre tech-book] [--limit 5]

Each book is produced on its own branch, so its lessons record is committed
there and never reaches main. Reading only the working tree would show a new
book none of the earlier lessons. This script gathers `book-lessons.md` from
the working tree, `.omc/`, and every local/remote branch, de-duplicates the
records (a record = one `## ` section), and prints the most recent ones.

--genre keeps records that mention that genre (records with no genre line are
kept too). --limit 0 prints everything.
"""
import argparse
import os
import re
import subprocess

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def sources() -> list[str]:
    texts = []
    for path in ("book-lessons.md", os.path.join(".omc", "book-lessons.md")):
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                texts.append(f.read())
    refs = git("for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes")
    for ref in refs.split():
        if ref.endswith("/HEAD"):
            continue
        text = git("show", f"{ref}:book-lessons.md")
        if text:
            texts.append(text)
    return texts


def records(text: str) -> list[str]:
    parts = re.split(r"^(?=## )", text, flags=re.M)
    return [p.strip() for p in parts if p.startswith("## ")]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--genre", default="")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()

    seen: dict[str, str] = {}
    for text in sources():
        for rec in records(text):
            heading = re.sub(r"\s+", " ", rec.splitlines()[0])
            # Same record seen on several branches: keep the longest copy.
            if len(rec) > len(seen.get(heading, "")):
                seen[heading] = rec

    picked = []
    for rec in seen.values():
        # Older records name the genre without a "genre:" label, so match on
        # the genre names themselves; records naming no genre are kept.
        named = [g for g in ("tech-book", "narrative", "practical", "essay") if g in rec]
        if args.genre and named and args.genre not in named:
            continue
        m = DATE.search(rec.splitlines()[0]) or DATE.search(rec)
        picked.append((m.group(0) if m else "0000-00-00", rec))
    picked.sort(key=lambda x: x[0], reverse=True)
    if args.limit > 0:
        picked = picked[: args.limit]

    if not picked:
        print("(교훈 레코드 없음)")
        return
    print("\n\n".join(rec for _, rec in picked))


if __name__ == "__main__":
    main()
