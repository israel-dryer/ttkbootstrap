# 2.0 docstring conventions

Frozen rules for the 2.0 docstring review/update pass. Every module, class,
method, and function docstring in `src/` is brought in line with this. The pass
is **accuracy-first**: the main work is verifying each docstring against the
current (2.0) signature and behavior, not prose polish.

## Format

- **Google style** — that's what the docs site renders (`mkdocstrings`, Python
  handler, default config in `mkdocs.yml`). The API reference pages *are* these
  docstrings, so they must render cleanly there.
- Section headers, one spelling each: `Parameters:`, `Returns:`, `Raises:`,
  `Examples:`. (`Parameters:` — not `Args:` — is already dominant; keep it.)
- Triple-double-quote; summary line in the imperative, then a blank line, then
  the body.

## Voice / altitude

- Say what the thing **does**, terse and functional. No design rationale, no
  "canonical" / "the new 2.0 way" narration — that lives in `development/`
  design docs, not docstrings.
- Document behavior a caller needs: what it returns, what it raises, side
  effects, keyword-only-ness where it matters.

## Accuracy (the core work)

- Every documented parameter must exist in the **current** signature with the
  right type and default. 2.0 churned these hard — `snake_case` renames,
  keyword-only constructors, unified dialog returns, `get_date`→None on cancel.
  Assume pre-2.0 docstrings are stale until verified against the code.
- Kill references to removed modules/shims and pre-2.0 names.
- Deprecated aliases: mention only where it helps a user migrate; don't
  exhaustively catalog every legacy spelling in the prose (the `_compat` warnings
  already do that).

## Images

- **Remove all `![](...png/gif)` image links from docstrings.** They're noise
  (often broken) in IDE hover and `help()`. Just delete them — do **not**
  relocate them anywhere. The prose docs pages are being fully rewritten later
  and will re-add visuals themselves.

## Examples

- Keep runnable `Examples:` blocks on the major public widgets/dialogs; **verify
  they use current 2.0 API** and trim duplicates / overlong ones.
- Don't add example blocks to internal helpers or style builders.

## Coverage bar

- **Every module** gets a module docstring (one-paragraph purpose).
- **Every public class** + its `__init__` and public methods get a docstring.
- **`internal/` plumbing and per-widget style builders**: a one-line summary is
  enough; only expand where behavior is non-obvious.

## Validation

- `python -m pytest -q` after each area (should stay green — these aren't
  doctests).
- `mkdocs build` to catch broken cross-references and any docs page relying on a
  removed image path.
