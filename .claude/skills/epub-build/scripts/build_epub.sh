#!/usr/bin/env bash
# Build EPUB 3 from manuscript + cover + manifest.
# Usage: build_epub.sh <slug>
#   Reads: <slug>/04_manuscript.md
#          <slug>/cover.png
#          <slug>/book_manifest.json
#   Writes: <title-slug>-v<version>.epub (project root)
#           <slug>/build_log.md

set -euo pipefail

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "usage: build_epub.sh <slug>" >&2
  exit 2
fi

WS="${SLUG}"
MANUSCRIPT="${WS}/04_manuscript.md"
COVER="${WS}/cover.png"
MANIFEST="${WS}/book_manifest.json"
LOG="${WS}/build_log.md"

for f in "$MANUSCRIPT" "$MANIFEST"; do
  [[ -f "$f" ]] || { echo "missing: $f" >&2; exit 3; }
done

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not installed. Run: brew install pandoc" >&2
  exit 4
fi

# Extract metadata one field per call (avoids shell quoting issues with non-ASCII).
read_field() {
  python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2], ''))" "$MANIFEST" "$1"
}
TITLE=$(read_field title)
AUTHOR=$(read_field author)
LANG=$(read_field language)
VERSION=$(read_field version)
PUB_DATE=$(read_field pub_date)
IDENTIFIER=$(read_field identifier)
DESCRIPTION=$(read_field description)
LICENSE=$(read_field license)
GENRE=$(read_field genre)
HARNESS_VERSION=$(read_field harness_version)
RIGHTS=$(read_field rights)
COVER_ALT=$(read_field cover_alt)

# cover_alt default: "{title} 표지" — backs the EPUB a11y alternativeText claim.
if [[ -z "$COVER_ALT" ]]; then
  COVER_ALT="${TITLE} 표지"
fi

if [[ -z "$AUTHOR" ]]; then
  AUTHOR="Toby-AI"
  echo "info: manifest author empty — falling back to default 'Toby-AI'" >&2
fi

# License default: harness-wide CC BY-NC-SA 4.0 unless manifest overrides.
if [[ -z "$LICENSE" ]]; then
  LICENSE="CC BY-NC-SA 4.0"
fi

# Harness version: prefer manifest, fall back to /VERSION at CWD (project root).
if [[ -z "$HARNESS_VERSION" && -f "VERSION" ]]; then
  HARNESS_VERSION=$(tr -d '[:space:]' < VERSION)
fi
HARNESS_VERSION="${HARNESS_VERSION:-unknown}"

# Rights string: construct from author + license if not set in manifest.
if [[ -z "$RIGHTS" ]]; then
  RIGHTS="© $(date +%Y) ${AUTHOR} — Licensed under ${LICENSE}"
fi

# Genre default: tech-book unless manifest specifies. Exposed as dc:subject.
if [[ -z "$GENRE" ]]; then
  GENRE="tech-book"
fi

# Identifier minting/preservation: minted ONCE per new book, then immutable.
# Mint only when empty OR the literal placeholder, and persist back to manifest.
if [[ -z "$IDENTIFIER" || "$IDENTIFIER" == "urn:uuid:..." ]]; then
  IDENTIFIER=$(python3 -c "import uuid;print('urn:uuid:'+str(uuid.uuid4()))")
  python3 -c "
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d['identifier'] = sys.argv[2]
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)
" "$MANIFEST" "$IDENTIFIER"
  echo "info: minted EPUB identifier ${IDENTIFIER} (written back to manifest — immutable across rebuilds)" >&2
fi

# Warn if a previous build used a DIFFERENT identifier (identifier must persist).
PREV_MANIFEST=$(ls -t _prev/*book_manifest*.json 2>/dev/null | head -1 || true)
if [[ -n "$PREV_MANIFEST" && -f "$PREV_MANIFEST" ]]; then
  PREV_ID=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('identifier',''))" "$PREV_MANIFEST" 2>/dev/null || echo "")
  if [[ -n "$PREV_ID" && "$PREV_ID" != "$IDENTIFIER" ]]; then
    echo "warning: previous manifest identifier (${PREV_ID}) differs from current (${IDENTIFIER}) — identifier should be preserved across rebuilds" >&2
  fi
fi

# Slugify title for filename. Collapse Unicode dashes/whitespace to single '-',
# optionally drop a trailing subtitle after the first em-dash/colon (so only the
# main title forms the filename), strip Windows-illegal chars, trim leading/
# trailing hyphens, cap to ~60 chars. The paired book-intro .md must share this stem.
FILENAME_TITLE=$(python3 -c "
import re, sys
t = sys.argv[1]
# Drop trailing subtitle after the first em-dash or colon — keep main title only.
t = re.split(r'\s*[—:]\s*', t, maxsplit=1)[0]
# Collapse Unicode dash runs and whitespace runs to a single hyphen.
t = re.sub(r'[\s‐-―]+', '-', t)
# Strip the Windows-illegal set.
t = re.sub(r'[\\\\/:*?\"<>|]', '', t)
# Trim leading/trailing hyphens and cap length.
t = t.strip('-')[:60].strip('-')
print(t)
" "$TITLE")

OUTPUT="${FILENAME_TITLE}-v${VERSION}.epub"

# If output exists, move previous to _prev/.
if [[ -f "$OUTPUT" ]]; then
  mkdir -p "_prev"
  mv "$OUTPUT" "_prev/$(basename "$OUTPUT" .epub)-$(date +%Y%m%d%H%M%S).epub"
fi

# Build metadata YAML for pandoc.
META_YAML="${WS}/.meta.yaml"
cat > "$META_YAML" <<YAML
---
title: "${TITLE}"
author: "${AUTHOR}"
lang: "${LANG}"
date: "${PUB_DATE}"
identifier: "${IDENTIFIER}"
description: "${DESCRIPTION}"
subject: "${GENRE}"
rights: "${RIGHTS}"
---
YAML

# Build cover arg (optional).
COVER_ARG=()
if [[ -f "$COVER" ]]; then
  COVER_ARG+=(--epub-cover-image="$COVER")
fi

# Bundled stylesheet (next to this script): base typography + scoped block
# classes. pandoc 3.x --css REPLACES the default EPUB stylesheet, so this file
# also carries table/code/blockquote/heading typography. Still genre-safe.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSS_FILE="${SCRIPT_DIR}/../styles/epub.css"
CSS_ARG=()
if [[ -f "$CSS_FILE" ]]; then
  CSS_ARG+=(--css="$CSS_FILE")
fi

# Mermaid figure pre-pass (OPTIONAL, fully graceful). If mmdc is installed,
# convert ```mermaid fenced blocks in the manuscript into SVGs under
# {slug}/figures/fig-NN.svg and rewrite each fence to an image + caption.
# If mmdc is absent, leave fences untouched (rendered as code) and log a warning.
# Never a hard dependency — mirrors the optional epubcheck pattern.
PANDOC_INPUT="$MANUSCRIPT"
MERMAID_NOTE="not present in manuscript"
if grep -q '```mermaid' "$MANUSCRIPT" 2>/dev/null; then
  if command -v mmdc >/dev/null 2>&1; then
    mkdir -p "${WS}/figures"
    RENDERED_INPUT="${WS}/.manuscript.mermaid.md"
    # Python splits the manuscript on ```mermaid fences, renders each block to
    # an SVG with mmdc, and rewrites the fence to ![caption](figures/fig-NN.svg).
    # The caption is taken from a following "그림 N. ..." line if present.
    if MMDC_BIN="$(command -v mmdc)" python3 - "$MANUSCRIPT" "$RENDERED_INPUT" "${WS}/figures" <<'PYMERMAID' 2>"${WS}/.mermaid_err"
import os, re, subprocess, sys, tempfile
src, dst, figdir = sys.argv[1], sys.argv[2], sys.argv[3]
mmdc = os.environ["MMDC_BIN"]
text = open(src, encoding="utf-8").read()
pat = re.compile(r"```mermaid[ \t]*\n(.*?)\n```", re.DOTALL)
n = 0
def repl(m):
    global n
    n += 1
    code = m.group(1)
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False, encoding="utf-8") as tf:
        tf.write(code)
        tfname = tf.name
    out = os.path.join(figdir, "fig-%02d.svg" % n)
    try:
        subprocess.run([mmdc, "-i", tfname, "-o", out], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        os.unlink(tfname)
    return "![](figures/fig-%02d.svg)" % n
new = pat.sub(repl, text)
open(dst, "w", encoding="utf-8").write(new)
PYMERMAID
    then
      PANDOC_INPUT="$RENDERED_INPUT"
      MERMAID_NOTE="rendered to figures/fig-NN.svg via mmdc"
    else
      MERMAID_NOTE="mmdc present but pre-pass failed — fences left as code (see ${WS}/.mermaid_err)"
      echo "warning: mermaid pre-pass failed — leaving diagrams as code fences" >&2
    fi
  else
    MERMAID_NOTE="mmdc not installed — diagrams left as code fences"
    echo "warning: mermaid: mmdc not installed — diagrams left as code fences" >&2
  fi
fi

# Run pandoc. --resource-path lets relative image paths (e.g. figures/fig-NN.svg)
# resolve against the slug dir.
set +e
pandoc "$PANDOC_INPUT" \
  --from markdown \
  --to epub3 \
  --metadata-file="$META_YAML" \
  --resource-path="${WS}" \
  ${COVER_ARG[@]+"${COVER_ARG[@]}"} \
  ${CSS_ARG[@]+"${CSS_ARG[@]}"} \
  --toc --toc-depth=2 \
  --split-level=1 \
  --output "$OUTPUT" 2>"${WS}/.pandoc_err"
PANDOC_EXIT=$?
set -e

SIZE=0
if [[ -f "$OUTPUT" ]]; then
  SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null || echo 0)
fi

# Cover alt-text post-process (OPTIONAL, fully graceful — failure must not abort
# the build). The EPUB's a11y alternativeText claim must be backed by real alt
# text: for a raw <img> cover add alt="${COVER_ALT}"; for pandoc's SVG-wrapped
# cover add role="img" + aria-label + an SVG <title>. Re-zips with mimetype
# stored first (EPUB OCF requirement) via python zipfile.
COVER_ALT_NOTE="not applied"
if [[ $PANDOC_EXIT -eq 0 && -f "$OUTPUT" && -f "$COVER" ]]; then
  COVER_ALT_PY="${WS}/.coveralt.py"
  cat > "$COVER_ALT_PY" <<'PYALT'
import html, os, re, sys, zipfile, tempfile, shutil
epub = sys.argv[1]
alt = os.environ.get("COVER_ALT_TXT", "")
alt_attr = html.escape(alt, quote=True)
tmp = tempfile.mkdtemp()
changed = False
try:
    with zipfile.ZipFile(epub) as z:
        names = z.namelist()
        z.extractall(tmp)
    # Find the cover xhtml (pandoc puts it under EPUB/text/cover.xhtml).
    target = None
    for root, _, files in os.walk(tmp):
        for fn in files:
            if not fn.lower().endswith((".xhtml", ".html")):
                continue
            p = os.path.join(root, fn)
            body = open(p, encoding="utf-8").read()
            if ("cover" in fn.lower() or 'id="cover' in body) and ("<image" in body or "<img" in body):
                target = p
                break
        if target:
            break
    if target:
        body = open(target, encoding="utf-8").read()
        new = body
        # Raw <img>: add alt if missing.
        def add_img_alt(m):
            tag = m.group(0)
            if re.search(r'\balt\s*=', tag):
                return tag
            return tag[:-1] + ' alt="%s"' % alt_attr + tag[-1:]
        new = re.sub(r'<img\b[^>]*?>', add_img_alt, new)
        # SVG cover: <image> takes no alt. Give the wrapping <svg> an accessible
        # name via role="img" + aria-label, and add a <title> child for readers
        # that honor SVG titles. Only if not already labelled.
        if "<svg" in new and "aria-label" not in new:
            def label_svg(m):
                tag = m.group(0)
                return tag[:-1] + ' role="img" aria-label="%s"' % alt_attr + tag[-1:]
            new = re.sub(r'<svg\b[^>]*?>', label_svg, new, count=1)
            new = re.sub(r'(<svg\b[^>]*?>)',
                         r'\1<title>%s</title>' % alt_attr, new, count=1)
        if new != body:
            open(target, "w", encoding="utf-8").write(new)
            changed = True
    if changed:
        # Re-zip: mimetype first, STORED (OCF requirement), rest DEFLATED.
        tmpepub = epub + ".tmp"
        with zipfile.ZipFile(tmpepub, "w") as z:
            mt = os.path.join(tmp, "mimetype")
            if os.path.exists(mt):
                z.write(mt, "mimetype", compress_type=zipfile.ZIP_STORED)
            for name in names:
                if name == "mimetype":
                    continue
                full = os.path.join(tmp, name)
                if os.path.isfile(full):
                    z.write(full, name, compress_type=zipfile.ZIP_DEFLATED)
        os.replace(tmpepub, epub)
    print("changed" if changed else "no-change")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PYALT
  COVER_ALT_OUT=""
  if COVER_ALT_OUT="$(COVER_ALT_TXT="$COVER_ALT" python3 "$COVER_ALT_PY" "$OUTPUT" 2>"${WS}/.coveralt_err")"; then
    if [[ "$COVER_ALT_OUT" == "changed" ]]; then
      COVER_ALT_NOTE="injected alt=\"${COVER_ALT}\""
    else
      COVER_ALT_NOTE="cover already labelled — left as is"
    fi
  else
    COVER_ALT_NOTE="skipped — post-process failed (see ${WS}/.coveralt_err), build unaffected"
    echo "warning: cover alt-text injection failed — build unaffected" >&2
  fi
fi

# Re-stat size (cover-alt re-zip may have changed it).
if [[ -f "$OUTPUT" ]]; then
  SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null || echo 0)
fi

# epubcheck gate. A FAILED epubcheck is a build FAILURE, not a footnote.
# EPUBCHECK_STRICT (default on) → exit non-zero (5) when present+failed, AFTER
# the build log is written. When epubcheck is ABSENT the EPUB ships UNVALIDATED.
EPUBCHECK_STRICT="${EPUBCHECK_STRICT:-1}"
EPUBCHECK_FAILED=0
if command -v epubcheck >/dev/null 2>&1 && [[ -f "$OUTPUT" ]]; then
  if epubcheck "$OUTPUT" >"${WS}/.epubcheck.log" 2>&1; then
    CHECK_RESULT="passed"
  else
    CHECK_RESULT="FAILED — see ${WS}/.epubcheck.log"
    EPUBCHECK_FAILED=1
  fi
else
  CHECK_RESULT="SKIPPED (NOT INSTALLED — EPUB UNVALIDATED)"
  echo "WARNING: epubcheck not installed — EPUB is UNVALIDATED. Run: brew install epubcheck" >&2
fi

# Write build log.
{
  echo "# Build Log — ${TITLE} v${VERSION}"
  echo ""
  echo "- **Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- **Output:** \`${OUTPUT}\`"
  echo "- **Size:** ${SIZE} bytes"
  echo "- **Pandoc exit:** ${PANDOC_EXIT}"
  echo "- **epubcheck:** ${CHECK_RESULT}"
  echo "- **epubcheck strict:** ${EPUBCHECK_STRICT}"
  echo "- **mermaid:** ${MERMAID_NOTE}"
  echo "- **cover alt:** ${COVER_ALT_NOTE}"
  echo ""
  echo "## Metadata"
  echo "- title: ${TITLE}"
  echo "- author: ${AUTHOR}"
  echo "- language: ${LANG}"
  echo "- version: ${VERSION}"
  echo "- pub_date: ${PUB_DATE}"
  echo "- identifier: ${IDENTIFIER}"
  echo "- license: ${LICENSE}"
  echo "- genre: ${GENRE}"
  echo "- cover_alt: ${COVER_ALT}"
  echo "- stylesheet: $([[ -f "$CSS_FILE" ]] && echo "epub.css" || echo "none")"
  echo "- harness_version: ${HARNESS_VERSION}"
  echo "- rights: ${RIGHTS}"
  if [[ $PANDOC_EXIT -ne 0 ]]; then
    echo ""
    echo "## Pandoc stderr"
    echo '```'
    cat "${WS}/.pandoc_err"
    echo '```'
  fi
} > "$LOG"

# Cleanup (temp artifacts only — figures/ and the EPUB are kept).
rm -f "$META_YAML" "${WS}/.pandoc_err" "${WS}/.manuscript.mermaid.md" \
      "${WS}/.mermaid_err" "${WS}/.coveralt_err" "${WS}/.coveralt.py"

if [[ $PANDOC_EXIT -ne 0 ]]; then
  echo "build failed — see $LOG" >&2
  exit $PANDOC_EXIT
fi

# epubcheck strict gate: a FAILED validation is a build failure. Exit AFTER the
# build log has been written so the failure is recorded.
if [[ $EPUBCHECK_FAILED -eq 1 && "$EPUBCHECK_STRICT" != "0" ]]; then
  echo "build failed — epubcheck reported errors (see ${WS}/.epubcheck.log). Set EPUBCHECK_STRICT=0 to downgrade to a warning." >&2
  exit 5
fi

if [[ $SIZE -lt 50000 ]]; then
  echo "warning: output is suspiciously small (${SIZE} bytes)" >&2
fi

echo "built: $OUTPUT ($SIZE bytes)"
