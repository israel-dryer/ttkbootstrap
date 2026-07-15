# 2.0 Docs — How-To band (handoff)

Self-contained handoff to finish the **How-To** band of the docs (Workstream H).
Written 2026-07-14. Pair with `development/2_0_docs_design.md` (the IA) and the
feature-guide accuracy pass (PR #1222) as the method precedent.

## Where the docs stand

The **feature guides are done**: typography + variables got a rigorous pass, and
the other eight (dialogs, validation, localization, theming, custom-styles, events,
icons, menus) were audited + fixed in **PR #1222**. The **Getting Started**,
**Foundations**, **Widgets catalog**, and the whole **Reference** layer are
content-complete and merged. The two remaining Workstream-H threads are:

1. **The How-To band** (this doc).
2. The deferred **screenshot slice** (Windows-canonical capture tooling; postponed).

## How-To — current state

Band lives in `docs/user-guide/how-to/`. The index
(`docs/user-guide/how-to/index.rst`) still carries a *"being written for 2.0"*
note and lists both authored pages (as `:doc:` links) and planned recipes (plain
bold, no link).

**Authored pages (7)** — need an accuracy/quality pass, not authoring:

| Page | Subject |
|---|---|
| `working-with-images.rst` | `PhotoImage` + Pillow, the keep-a-reference gotcha, `apply_icon` |
| `scrollable.rst` | `ScrolledFrame` / `ScrolledText` |
| `multiple-windows.rst` | a second `Toplevel`, a modal that returns a value, the close button |
| `threads.rst` | `after` + worker threads, updating widgets from the main loop |
| `clipboard.rst` | copy/paste, reading the selection |
| `error-handling.rst` | `report_callback_exception`, `TclError` |
| `feedback.rst` | system beep + busy overlay |

**Planned recipes in the index (decide fate, then act):**

- **Lay out widgets** (pack/grid/place) and **Wire events and variables** (bind /
  `command=` / variable classes) — these overlap heavily with the **Foundations**
  pages (`layout-with-grid`/`layout-with-pack`/`arranging-widgets`,
  `events-and-callbacks`, `state-and-variables`/`variables`). Recommend **NOT**
  authoring duplicate how-tos: convert these index entries to **cross-references**
  to the Foundations/feature pages, exactly as **Menus** and **Message boxes and
  dialogs** already are in the index (they point at their guides, no page).
- **Validate a form** — largely covered by the Validation feature guide; either
  cross-reference it or write a short task-shaped recipe that *builds a form and
  submits it* (don't duplicate the guide's rule catalog).
- **Animate a GIF** *(salvage from the old cookbook)*, **Splash screen**
  (borderless `window_type`), **Application icon** (window/taskbar icon) — these
  are genuinely how-to-shaped and **not** covered elsewhere. Author them (short,
  one-task each). Confirm the APIs live: `PhotoImage(format="gif -index N")` frame
  animation via `after`; `Toplevel(window_type="splash")` / `overrideredirect`;
  `App(iconphoto=...)` / `wm_iconphoto` / `.ico` on Windows.

## The method (same as PR #1222 — it works)

1. **Audit** the 7 authored pages with grounded read-only agents — one per page.
   Each: read the full page; **probe every claim + run every snippet headlessly**
   (`.venv/bin/python`, `import ttkbootstrap as ttk`, build widgets, no
   `mainloop()`); cross-check tkinter concepts against the **Tcl/Tk 8.6 manuals**
   (tcl.tk/man/tcl8.6/TkCmd/…); and flag the standing-rule violations below.
   Return a ranked, tagged report (`[ACCURACY | BROKEN-SNIPPET | RULE-VIOLATION |
   QUALITY-GAP]`) with evidence + a concrete fix.
2. **Fix** page-by-page from the reports; verify each new/changed snippet
   headlessly; keep the build green.
3. **Resolve the index**: author the 3 real recipes, convert the overlapping
   entries to cross-references, drop the *"being written"* note, and make sure
   every listed item either links a page or cross-references a guide.
4. **One consolidated PR** off `2.0` (like #1222), or split authored-vs-audit if it
   grows large.

## Standing docs rules (check for violations)

- **No** implementation-detail / "under the hood" / "internally," / "re-exported …
  for convenience" asides; **no** design-pattern jargon (the #1222 audits caught
  "observer pattern", "deferred-config seam", "facade", "re-exported", "surfaced").
- `App` examples use **`theme=`** (not `themename=`) + **curated** theme names
  (`bootstrap-dark`, not `darkly`). No `\` line-continuations.
- **No nested inline markup** — `` ``code`` `` inside `**bold**` renders literal
  backticks (`-W` does NOT catch it; sweep with
  `grep -nE '\*\*``|``\*\*' <file>`).
- **See-also / Reference** = bulleted `link — description` lists linking **our**
  reference; python.org only for genuinely-stdlib surfaces we don't document.
- **Task-shaped, teach-by-building** — a how-to solves one concrete job; not an
  option-tour. Short titles that don't wrap.

## Build gate

`.venv/bin/python -m sphinx -b html -W -q -E docs /tmp/ttkdocs-out` must exit 0
(`-W` warnings-as-errors, `-E` fresh build). Every runnable snippet verified
headlessly first.

## Not this band

The **screenshot slice** is the other open thread (placeholders in place across
catalog + guides; capture tooling is Windows-canonical, so it's postponed on
macOS). Track B odds/ends (Linux/x11, DPI matrix) are optional.
