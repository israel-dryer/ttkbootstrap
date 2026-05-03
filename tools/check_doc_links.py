"""Verify every Markdown link in docs/ resolves to an existing file.

Catches stale cross-links that occur when pages are renamed, moved, or
deleted — the kind that silently produce 404s in the rendered site.

What is checked:
  [text](relative/path/to/file.md)        — resolved relative to the
                                             .md file's directory
  [text](relative/path/to/file.md#anchor) — fragment stripped; file
                                             existence checked
  [text](/absolute/path.md)               — resolved from docs/ root
                                             (mkdocs convention)

What is skipped:
  [text](http://...)  / [text](https://...) — external URLs
  [text](#anchor)                           — same-page anchors
  [text](mailto:...)                        — email links

Exit code 0 if all referenced files resolve; 1 if any are missing.

Usage:
  python tools/check_doc_links.py
  python tools/check_doc_links.py --dir docs/widgets
  python tools/check_doc_links.py --file docs/capabilities/index.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"

# Inline Markdown link: [text](url)
_MD_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

# Reference-style link definition: [id]: url
_MD_REF_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)

# Fenced code blocks (``` ... ``` or ~~~ ... ~~~)
_CODE_BLOCK = re.compile(r"^(`{3,}|~{3,}).*?^\1", re.MULTILINE | re.DOTALL)

# Inline code spans (`...`)
_CODE_SPAN = re.compile(r"`+.+?`+", re.DOTALL)

# Schemes we skip
_EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "//")


def _is_external(url: str) -> bool:
    return any(url.startswith(p) for p in _EXTERNAL_PREFIXES)


def _strip_fragment(url: str) -> str:
    """Remove #fragment (and ?query) from a URL to get the bare file path."""
    for sep in ("#", "?"):
        idx = url.find(sep)
        if idx >= 0:
            url = url[:idx]
    return url


def _resolve(url: str, source_file: Path) -> Path:
    """Resolve a link URL to an absolute filesystem path."""
    bare = _strip_fragment(url).strip()
    if bare.startswith("/"):
        # Absolute path from docs root (mkdocs convention)
        return (DOCS_DIR / bare.lstrip("/")).resolve()
    else:
        return (source_file.parent / bare).resolve()


def _scrub_code(text: str) -> str:
    """Replace code blocks and inline spans with spaces to avoid false positives."""
    text = _CODE_BLOCK.sub(lambda m: " " * len(m.group(0)), text)
    text = _CODE_SPAN.sub(lambda m: " " * len(m.group(0)), text)
    return text


def check_file(md_file: Path) -> list[tuple[str, Path]]:
    """Return [(raw_url, resolved_path)] for every broken link in md_file."""
    raw_text = md_file.read_text(encoding="utf-8")
    text = _scrub_code(raw_text)
    broken: list[tuple[str, Path]] = []

    seen: set[str] = set()

    def _check(raw_url: str) -> None:
        url = raw_url.strip()
        if not url or _is_external(url):
            return
        bare = _strip_fragment(url)
        if not bare:
            # Same-page anchor only — skip
            return
        if bare in seen:
            return
        seen.add(bare)
        target = _resolve(url, md_file)
        if not target.exists():
            broken.append((raw_url, target))

    for _text, url in _MD_LINK.findall(text):
        _check(url)

    for url in _MD_REF_DEF.findall(text):
        _check(url)

    return broken


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dir", metavar="PATH", help="Scan a specific docs subdirectory.")
    group.add_argument("--file", metavar="PATH", help="Check a single .md file.")
    args = parser.parse_args(argv)

    if args.file:
        files = [Path(args.file).resolve()]
    elif args.dir:
        scan_dir = Path(args.dir).resolve()
        files = sorted(scan_dir.rglob("*.md"))
    else:
        files = sorted(DOCS_DIR.rglob("*.md"))

    all_broken: list[tuple[Path, str, Path]] = []
    files_checked = 0

    for md_file in files:
        if not md_file.is_file():
            print(f"WARNING: not a file: {md_file}", file=sys.stderr)
            continue
        files_checked += 1
        for raw, target in check_file(md_file):
            all_broken.append((md_file, raw, target))

    if all_broken:
        print(f"FAIL — {len(all_broken)} broken link(s) across {files_checked} file(s):\n")
        current_file: Path | None = None
        for md, raw, target in sorted(all_broken, key=lambda x: (x[0], x[1])):
            if md != current_file:
                rel = md.relative_to(REPO_ROOT)
                print(f"  {rel}")
                current_file = md
            try:
                rel_target = target.relative_to(REPO_ROOT)
            except ValueError:
                rel_target = target
            print(f"    link:  {raw}")
            print(f"    resolves to: {rel_target}  [NOT FOUND]")
        return 1
    else:
        print(f"OK — {files_checked} file(s) checked, 0 broken links.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
