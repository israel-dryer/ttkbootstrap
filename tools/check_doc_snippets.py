"""Extract and validate Python code blocks from all ``docs/**/*.md`` files.

Two validation passes run against every fenced ```python block:

1. **Compile check** (always) — ``compile()`` each snippet to catch syntax
   errors.  No display or ttkbootstrap import is required; this is safe for
   CI.

2. **Runtime check** (opt-in via ``--run``) — execute *self-contained*
   snippets in a fresh subprocess and report non-zero exit codes.  A snippet
   is considered self-contained when it contains ``import ttkbootstrap``
   (implying it sets up its own context).  Before execution, ``app.mainloop()``
   calls are patched to ``app.after(50, app.destroy); app.mainloop()`` so the
   process exits without hanging.  Requires a Tk-capable display.

Output format::

    FAIL  docs/widgets/actions/dropdownbutton.md  block 1
          SyntaxError: invalid syntax (line 3)

    FAIL  docs/guides/dialogs.md  block 4
          TypeError: ContextMenuItem.__init__() got unexpected keyword
          argument 'separator'

Exit code 0 if every checked snippet passes; 1 if any fail.

Skip patterns
-------------
* Files under ``docs/_template/`` — template stubs, not real examples.
* Snippets that ``compile()`` but would need surrounding context to run
  (no ``import ttkbootstrap`` line) are compile-checked only, never executed.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"

_FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)
# Snippets whose mainloop() we patch before running so they exit cleanly.
# Match any variable name before .mainloop() (app, shell, root, etc.).
_MAINLOOP = re.compile(r"\b(\w+)\.mainloop\(\)")


def extract_snippets(md_file: Path) -> list[str]:
    """Return the source text of every ```python block in *md_file*.

    Dedents each block so snippets nested inside admonitions (which MkDocs
    requires to be indented 4 spaces) compile without spurious indent errors.
    """
    text = md_file.read_text(encoding="utf-8")
    return [textwrap.dedent(m.group(1)) for m in _FENCE.finditer(text)]


def is_self_contained(code: str) -> bool:
    """True if the snippet creates its own App context and is safe to run.

    Requires both ``import ttkbootstrap`` and some form of app-window
    creation (``ttk.App(``, ``ttk.AppShell(``) so that partial snippets
    which show call shapes in isolation are not run as if they were complete
    programs.

    Also skips:
    - Snippets with relative imports (``from . import ...``) — package-level
      code that can't run standalone.
    - Snippets that call ``MessageBox.*`` or ``QueryBox.*`` static methods,
      which internally open a blocking modal that the ``.show()`` patch
      does not reach.
    """
    if "import ttkbootstrap" not in code:
        return False
    if re.search(r"from \.", code):
        return False
    if re.search(r"\b(MessageBox|QueryBox)\.\w+\(", code):
        return False
    return bool(re.search(r"\bttk\.(App|AppShell)\(", code))


def patch_for_run(code: str) -> str:
    """Replace blocking mainloop/show calls so snippets exit cleanly."""
    # Patch <var>.mainloop() for any variable name.
    code = _MAINLOOP.sub(r"\1.after(50, \1.destroy)\n\1.mainloop()", code)
    # Patch <expr>.show() → <expr>  (preserves construction, skips blocking show).
    # This keeps AttributeErrors on unknown classes while avoiding modal loops.
    code = re.sub(r"\.show\(\)", "", code)
    return code


def compile_check(code: str, label: str) -> str | None:
    """Return an error string if *code* has a syntax error, else None.

    Snippets that use ``return`` at the top level (a common tutorial pattern
    for "inside a function" context) are retried wrapped in a ``def``.  If the
    wrapped version compiles, the snippet is considered valid.
    """
    try:
        compile(code, label, "exec")
        return None
    except SyntaxError as exc:
        # Retry once inside a function body — catches 'return outside function'
        # and similar function-context snippets that are correct as written.
        if exc.msg and "outside function" in exc.msg:
            indented = textwrap.indent(code, "    ")
            try:
                compile(f"def _():\n{indented}", label, "exec")
                return None  # valid function-context snippet
            except SyntaxError:
                pass
        return f"SyntaxError: {exc.msg} (line {exc.lineno})"


def run_check(code: str, timeout: int = 15) -> str | None:
    """Run *code* in a subprocess.  Return error string on failure, else None."""
    patched = patch_for_run(code)
    try:
        result = subprocess.run(
            [sys.executable, "-c", patched],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            # Strip the full traceback — keep only the final error line(s)
            # so the output stays readable.
            stderr = result.stderr.strip()
            lines = stderr.splitlines()
            # Find the first non-blank line that isn't "Traceback" boilerplate.
            error_lines: list[str] = []
            in_traceback = False
            for line in lines:
                if line.startswith("Traceback"):
                    in_traceback = True
                    continue
                if in_traceback and line.startswith("  "):
                    continue
                error_lines.append(line)
            return "\n".join(error_lines) if error_lines else stderr
        return None
    except subprocess.TimeoutExpired:
        return "TIMEOUT (>15 s) — likely a blocking call not caught by the mainloop patch"


def _is_acceptable_error(msg: str) -> bool:
    """Return True for errors that are example limitations, not API drift.

    FileNotFoundError on illustrative asset paths (``icon.png``, ``logo.png``,
    ``locales/en.json``, etc.) is expected — docs show representative paths that
    don't exist in the repo.
    """
    if "FileNotFoundError" in msg and any(
        ext in msg
        for ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".json", ".db", ".sqlite")
    ):
        return True
    return False


def _iter_md_files() -> list[Path]:
    skipped_dirs = {"_template"}
    return sorted(
        p
        for p in DOCS_DIR.rglob("*.md")
        if not any(part in skipped_dirs for part in p.parts)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute self-contained snippets in subprocess (requires a Tk display).",
    )
    parser.add_argument(
        "--file",
        metavar="GLOB",
        help="Restrict to .md files whose path contains GLOB (substring match).",
    )
    args = parser.parse_args(argv)

    md_files = _iter_md_files()
    if args.file:
        md_files = [f for f in md_files if args.file in str(f)]
        if not md_files:
            print(f"No .md files matched --file={args.file!r}", file=sys.stderr)
            return 1

    failures: list[tuple[Path, int, str, str]] = []  # (file, block_idx, kind, msg)
    files_checked = 0
    snippets_total = 0
    snippets_run = 0

    for md_file in md_files:
        snippets = extract_snippets(md_file)
        if not snippets:
            continue
        files_checked += 1
        snippets_total += len(snippets)

        for idx, code in enumerate(snippets, start=1):
            label = f"{md_file.relative_to(REPO_ROOT)}:block{idx}"

            # Pass 1 — compile check (always)
            err = compile_check(code, label)
            if err:
                failures.append((md_file, idx, "syntax", err))
                continue  # no point running a snippet that won't compile

            # Pass 2 — runtime check (opt-in, self-contained only)
            if args.run and is_self_contained(code):
                snippets_run += 1
                err = run_check(code)
                if err and not _is_acceptable_error(err):
                    failures.append((md_file, idx, "runtime", err))

    # ── Report ─────────────────────────────────────────────────────────────
    if failures:
        print(f"FAIL — {len(failures)} snippet(s) failed:\n")
        for md_file, idx, kind, msg in failures:
            rel = md_file.relative_to(REPO_ROOT)
            print(f"  [{kind.upper()}]  {rel}  block {idx}")
            for line in msg.splitlines():
                print(f"        {line}")
            print()

    run_note = f", {snippets_run} executed" if args.run else " (compile-only; use --run to execute)"
    print(
        f"{files_checked} file(s), {snippets_total} snippet(s){run_note}, "
        f"{len(failures)} failure(s)."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
