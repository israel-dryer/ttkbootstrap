"""Check that widget docs contain the required H2 sections from their template.

Each docs/widgets/<category>/ directory maps to a template in docs/_template/.
This script verifies every .md file in each mapped category contains all the
H2 headings required by its template.

Usage:
    python tools/check_doc_structure.py [--fix]

Exit code 0 if all files pass; 1 if any required sections are missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = REPO_ROOT / "docs" / "_template"
WIDGETS_DIR = REPO_ROOT / "docs" / "widgets"

# Maps widget category directory name to the template file stem.
# Categories not listed here are skipped (no template applies).
CATEGORY_TEMPLATE_MAP: dict[str, str] = {
    "actions": "widget-action-template",
    "data-display": "widget-data-display-template",
    "dialogs": "widget-dialog-template",
    "inputs": "widget-input-template",
    "layout": "widget-layout-template",
    "navigation": "widget-navigation-template",
    "overlays": "widget-overlay-template",
    "selection": "widget-selection-template",
    "views": "widget-navigation-template",
}

# Files to skip within a category (index pages, deprecation stubs, etc.)
# - navigationview.md is a 6-line deprecation redirect for SideNav
#   (NavigationView is a back-compat alias; see widgets/composites/sidenav/__init__.py).
#   Holding it to the navigation template would force template content into a
#   page whose only job is to point readers at the new name.
SKIP_FILES = {"index.md", "navigationview.md"}


def extract_h2s(text: str) -> list[str]:
    """Return all H2 headings found in markdown text."""
    return re.findall(r"^## (.+)$", text, re.MULTILINE)


def extract_h1(text: str) -> str | None:
    """Return the first H1 heading in markdown text, if any."""
    m = re.search(r"^# (.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def load_required_h2s(template_stem: str) -> list[str]:
    """Return the H2 headings from a template file that pages must include.

    Templates may mark a section as optional by placing italic prose
    starting with ``*Optional`` as the first non-empty line under the
    heading. Such sections are dropped from the required list — pages
    may include them, but pages without them still pass.
    """
    path = TEMPLATE_DIR / f"{template_stem}.md"
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    required: list[str] = []
    for i, line in enumerate(lines):
        m = re.match(r"^## (.+)$", line)
        if not m:
            continue
        heading = m.group(1)
        # Find the first non-empty line under this heading.
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        first = lines[j].strip().lower() if j < len(lines) else ""
        if first.startswith("*optional"):
            continue
        required.append(heading)
    return required


def check_file(
    md_file: Path,
    required: list[str],
) -> list[str]:
    """Return a list of missing H2 headings for a single file.

    Templates may use the literal token ``WidgetName`` as a placeholder
    in their H2s (e.g. ``## When should I use WidgetName?``). For each
    page, the placeholder is substituted with the page's H1 before
    comparison so individual pages can use the real widget name.
    """
    text = md_file.read_text(encoding="utf-8")
    present = set(extract_h2s(text))
    widget_name = extract_h1(text) or md_file.stem
    return [h for h in required if h.replace("WidgetName", widget_name) not in present]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--category",
        metavar="NAME",
        help="Check only this category (e.g. 'inputs')",
    )
    args = parser.parse_args()

    failures: list[tuple[Path, list[str]]] = []
    checked = 0

    categories = (
        [args.category] if args.category else sorted(CATEGORY_TEMPLATE_MAP)
    )

    for category in categories:
        if category not in CATEGORY_TEMPLATE_MAP:
            print(f"Unknown category: {category}", file=sys.stderr)
            return 1

        template_stem = CATEGORY_TEMPLATE_MAP[category]
        try:
            required = load_required_h2s(template_stem)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

        cat_dir = WIDGETS_DIR / category
        if not cat_dir.is_dir():
            print(f"WARNING: category directory not found: {cat_dir}", file=sys.stderr)
            continue

        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name in SKIP_FILES:
                continue
            checked += 1
            missing = check_file(md_file, required)
            if missing:
                failures.append((md_file, missing))

    # Report
    if failures:
        print(f"FAIL — {len(failures)} file(s) missing required sections:\n")
        for path, missing in failures:
            rel = path.relative_to(REPO_ROOT)
            print(f"  {rel}")
            for h in missing:
                print(f"    - ## {h}")
        print(f"\n{checked} files checked, {len(failures)} failed.")
        return 1
    else:
        print(f"OK — {checked} files checked, all pass.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
