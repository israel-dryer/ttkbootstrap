"""Verify every image referenced in `docs/widgets/**/*.md` exists on disk.

Catches the kind of silent breakage we hit historically when paths drifted
(e.g. `_img/` references that pointed at a non-existent directory).

Two reference forms are recognized:

1. Standard Markdown image:  `![alt](relative/path/to/file.png)`
   The path is resolved relative to the .md file's directory. Optional
   query/anchor suffixes (`#only-light`, `?v=1`) are stripped before the
   on-disk check. Absolute URLs (`http://...`, `https://...`) are skipped.

2. Placeholder marker:  `IMAGE: <description>` (typically inside an HTML
   comment like `<!-- IMAGE: ... -->`). These are surfaced separately as
   informational reminders, not failures.

Exit code 0 if all referenced files resolve; 1 if any are missing.
Placeholders alone do not fail the check unless `--strict-placeholders`
is passed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WIDGETS_DIR = REPO_ROOT / "docs" / "widgets"

# Markdown image: ![alt](url)
# Capture: alt (group 1), url (group 2). Greedy on URL stops at the closing ).
_MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# IMAGE: placeholders (used in HTML comments and bare text).
# Capture everything after `IMAGE:` up to the closing `-->` or end of line.
_PLACEHOLDER = re.compile(r"\bIMAGE:\s*(.+?)(?:\s*-->\s*|$)", re.MULTILINE)
# Schemes we skip — these are external and not on-disk assets.
_EXTERNAL = ("http://", "https://", "data:", "mailto:")


def _strip_suffix(url: str) -> str:
    """Drop the `#fragment` and `?query` so we get a real filesystem path."""
    for sep in ("#", "?"):
        idx = url.find(sep)
        if idx >= 0:
            url = url[:idx]
    return url


def find_image_refs(md_file: Path) -> list[tuple[str, Path]]:
    """Return [(raw_url, resolved_path), ...] for every Markdown image ref."""
    text = md_file.read_text(encoding="utf-8")
    refs: list[tuple[str, Path]] = []
    for _alt, raw in _MD_IMG.findall(text):
        url = raw.strip()
        if url.startswith(_EXTERNAL):
            continue
        clean = _strip_suffix(url)
        # Resolve relative to the .md file. Absolute paths starting with /
        # are interpreted relative to docs/ (mkdocs convention).
        if clean.startswith("/"):
            target = REPO_ROOT / "docs" / clean.lstrip("/")
        else:
            target = (md_file.parent / clean).resolve()
        refs.append((url, target))
    return refs


def find_placeholders(md_file: Path) -> list[str]:
    """Return raw `IMAGE: ...` placeholder descriptions."""
    text = md_file.read_text(encoding="utf-8")
    return [m.group(1).strip() for m in _PLACEHOLDER.finditer(text)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Treat IMAGE: placeholders as failures (default: informational).",
    )
    args = parser.parse_args(argv)

    if not WIDGETS_DIR.is_dir():
        print(f"ERROR: widget docs directory not found: {WIDGETS_DIR}", file=sys.stderr)
        return 1

    missing: list[tuple[Path, str, Path]] = []
    placeholders: list[tuple[Path, str]] = []
    files_checked = 0
    refs_checked = 0

    for md_file in sorted(WIDGETS_DIR.rglob("*.md")):
        files_checked += 1
        for raw, target in find_image_refs(md_file):
            refs_checked += 1
            if not target.is_file():
                missing.append((md_file, raw, target))
        for placeholder in find_placeholders(md_file):
            placeholders.append((md_file, placeholder))

    fail = bool(missing) or (args.strict_placeholders and placeholders)

    if missing:
        print(f"FAIL — {len(missing)} broken image reference(s):\n")
        for md, raw, target in missing:
            rel_md = md.relative_to(REPO_ROOT)
            try:
                rel_target = target.relative_to(REPO_ROOT)
            except ValueError:
                rel_target = target
            print(f"  {rel_md}")
            print(f"    ref: {raw}")
            print(f"    looked for: {rel_target}")

    if placeholders:
        label = "FAIL" if args.strict_placeholders else "INFO"
        print(f"\n{label} — {len(placeholders)} IMAGE: placeholder(s) (work-in-progress):\n")
        for md, desc in placeholders:
            rel_md = md.relative_to(REPO_ROOT)
            print(f"  {rel_md}: {desc}")

    print(
        f"\n{files_checked} file(s) checked, {refs_checked} image ref(s), "
        f"{len(missing)} missing, {len(placeholders)} placeholder(s)."
    )
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
