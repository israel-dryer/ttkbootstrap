# AGENTS.md — orientation for AI coding agents (Codex et al.)

This file is the entry point for an AI agent picking up work in this repo. It is
checked into git, so it travels with the repo across machines. Read it first,
then the docs it points to.

> `CLAUDE.md` is the authoritative record of where the project stands and why.
> This file is the shorter door in: the project's shape, how to build and test
> it, and the working rules that a per-user memory store would otherwise hold
> (which does **not** travel between machines). Where the two disagree,
> `CLAUDE.md` is newer.

## What this project is

ttkbootstrap is a **theming extension for tkinter/ttk** — it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle=` keyword API to
ttk widgets. Pure Python; the only runtime dependency is **Pillow** (image-based
widget assets). Public entry point: `src/ttkbootstrap/__init__.py`, imported as
`import ttkbootstrap as ttk`. src layout, `requires-python >= 3.10`.

ttkbootstrap stays a **styling extension for vanilla tkinter** — NOT a widget
library. The forward-looking widget framework is a **separate** project,
**bootstack** (www.bootstack.org). Several 2.0 mechanisms are *ported from*
bootstack (the asset render pipeline, the icon renderer) — port the mechanism,
not bootstack's API.

## Where things stand

**2.0.0 shipped 2026-07-19; 2.0.1 followed on 2026-07-23. The active milestone
is 2.1** (GitHub milestone #1). 2.0 was a cleanup/consolidation release — no new
features — and it is done: the engine rewrite, the mixin API, the `style/` split,
the asset/icon toolkit, the semantic-anchor theme model, the canonical
`bootstyle` grammar, and a from-scratch Sphinx documentation rebuild all landed.
Everything since is 2.1 work.

**`CLAUDE.md` is the authoritative record** — its status banner carries the
session-by-session history, the locked decisions, and the current punch list.
Read it before starting anything; this file only adds orientation that a
per-machine memory store would otherwise hold.

Supporting documents, as relevant:

- **`development/2_1_changes.md`** — the running log of user-visible 2.1
  changes, and the source for the 2.1 release notes. **Log there as you land,
  not at release time.** Scope is relative to the latest released 2.0.x, so a
  regression introduced and fixed inside the 2.1 cycle never reached a user and
  belongs in the dev log instead.
- **`development/2_0_plan.md`** — the durable worklist, including the
  "Post-2.0 (2.1) backlog" framing.
- `development/2_1_*_design.md` — per-slice design passes (durable style
  options, bootstyle value tokens, the themed file dialog).
- `development/2_0_*_design.md` — the 2.0 design record. Historical, but the
  engine, toolkit, icons, theme-anchor, and docs documents still explain why
  the current code is shaped the way it is.
- `development/2_0_breaking_changes.md` — what 2.0 changed for users.

**Labels carry no version.** The milestone conveys the target release; tag
issues and PRs topically (`enhancement`/`bug`) and set the milestone.

## How to work here

### Build / test / run
- Headless test suite: `python -m pytest -q` (config in `pyproject.toml`,
  `testpaths = ["tests"]`). Keep it green. **There is no CI** — no
  `.github/workflows/` exists — so every gate below is a manual step.
- Docs: `python -m sphinx -b html -W -q -E docs <out>` **must exit 0**. The docs
  are kept warning-clean and Read the Docs enforces `fail_on_warning`. A clean
  build is necessary but not sufficient: `-W` does not flag a leaked literal
  ``` `` ``` from nested inline markup, nor a line block indented wrongly inside
  a list-table cell. Check the built HTML for anything layout-shaped.
- Docstrings feed `autodoc` through napoleon in **Google** style (`Parameters:`,
  `Returns:`, `Examples:`). The docs are **Sphinx + rST**, so do not write
  mkdocs `!!!` admonitions — use napoleon sections (`Warning:`, `Note:`).
  Markdown ```` ```python ```` fences in existing docstrings survive via a
  build-time shim in `docs/conf.py`; do not add new ones.
- A virtualenv with an editable install lives at `.venv/`. The package is also
  importable with `PYTHONPATH=src` — and note that an editable install **wins
  over a worktree's own `src/`**, so pin `PYTHONPATH` when testing a branch
  checked out elsewhere.
- `tests/` is **headless pytest only**. Interactive `mainloop()` demos live in
  `examples/` and are NOT collected by pytest. Put any visual/manual check there.
- Anything touching scaling, assets, geometry, or event bindings deserves a
  **Tk 9** run as well as 8.6; the two differ on aqua's dpi baseline and on
  scroll events.

### Branch + PR model
- **`master` is the mainline and always tracks the most recent release.** Cut
  work from `master` and PR into it. `release/*` branches exist only for
  *superseded* majors (`release/v1`, `release/v0.5`) — a patch release is cut
  from `master`, so its version bump lands there naturally.
- One change per branch/PR. Imperative commit subjects; reference issues
  (`fixes #NNNN`) where applicable. Do not exceed a PR's designed scope without
  revisiting its design doc.
- **Verify `git branch --show-current` before pushing.** A
  `checkout -b … || checkout …` fallback once left commits on a second branch
  while the push named a different ref, and the PR merged without its work.
- **"Push" is not "merge."** Push the branch; merging is a separate decision
  that belongs to the author. GitHub squash-merges, so the merge commit is a new
  SHA and `git branch -d` will report "not fully merged" — confirm the content
  landed, then `-D`.
- **A trial merge is the only reliable conflict check.**
  `git merge-tree | grep '^<<<<<<<'` reported zero conflicts for two branches
  that then conflicted for real.

### Releasing
No CI publishes; the upload is manual, with credentials in a gitignored
repo-root `.pypirc`.

1. Bump `version` in `pyproject.toml` — **at release time, on `master`**. The
   literal is load-bearing beyond packaging: `docs/conf.py` reads it through
   `importlib.metadata`, so a stale value mislabels the docs. 2.0.1 shipped its
   bump on a throwaway branch and `master` kept claiming 2.0.0 for days.
2. Fold `development/2_<x>_changes.md` into the release notes.
3. Run the gates: full suite, and the docs build under `-W`.
4. `python -m build`, then `twine check dist/*`, then `twine upload dist/*`.
5. Annotated tag `vX.Y.Z` plus a GitHub release titled the same way.
6. Verify with a clean-environment `pip install ttkbootstrap==X.Y.Z`.

### Hard rules / gotchas (these have bitten before)
- **Do not start style-engine work as ad-hoc coding.** New public surface or
  engine changes get a **design pass first** (a design doc + user sign-off),
  like the engine/split/toolkit/icons did. The recolor strand follows this.
- **`Style` is a process-wide singleton tied to the first Tk root.** Creating +
  destroying separate roots in one process mis-binds it and later theming
  silently no-ops. Tests must take the shared **`root` fixture** from
  `tests/conftest.py` — never create their own `ttk.Window`.
- **`import ttkbootstrap` must stay warning-free.** Deprecation shims warn only
  when an old path is actually used. Private plumbing lives in
  `src/ttkbootstrap/internal/` (the name is `internal`, no underscore) with no
  back-compat guarantee; old public paths get warn-and-reexport shims removed in
  3.0.
- **Styles build lazily, on demand** (not all up front) — see CLAUDE.md "Lazy
  style building". A widget the app never instantiates can fall back to the bare
  clam look; the fix is to build the base style eagerly in
  `create_default_style()`.
- **Python 3.14 / PEP 649**: lazy annotations can mask a missing
  annotation-only import. An "does it import?" check is insufficient — run an
  annotation force-evaluation sweep when moving code (pattern noted in the PR 4
  design doc).
- **Don't kill blocking modal dialogs externally to test them.** Tk modal
  `show()` calls closed via threads/`after` produce misleading errors. Read the
  code or ask the user instead.
- **Framework code configures styles through `_build_configure`, never the
  public `Style.configure`.** That seam is what lets the durable style-options
  layer tell a user's override from a recipe's own write; calling the public
  method internally miscaptures library values as fake user overrides.
- **Durability is not the same as the widget honoring an option.** The layer
  persists anything allowlisted, including options a widget never reads —
  `font` on `Entry`/`Combobox`/`Spinbox` (they read the widget or `TkTextFont`)
  and `sashthickness` anywhere but the global `"Sash"` pseudo-style. A recipe
  that `map`s an option for *every* state also masks `configure` entirely; audit
  for that shape before adding a map.
- **We wrap a wrapper: prefer documenting a lower-layer caveat over detecting
  it at runtime.** A warning that is sometimes wrong about whether ttk/Tk will
  honor something is worse than no warning.
- **ctypes is the house pattern for platform APIs — the library has never used
  `subprocess`.** Windows DPI and shell calls, and X11's `XineramaQueryScreens`,
  are all reached that way; don't shell out to `xrandr` and friends.
- **`withdraw()` goes before you build a window's contents, not after.**
  Building widgets shows the window, and re-showing an already-shown window is a
  fresh placement the window manager decides for itself — measured drifting
  hundreds of px, differently each run. Reproduced in pure tkinter, so it is the
  WM, not us.
- **What a window reports before its first map is platform-specific.** x11 says
  1x1; win32 reports the size Tk started it at, which is a plausible number
  unrelated to what the content will map at. Never infer "has this been shown?"
  from a reported size. On x11 a `geometry()` readback is not the position you
  applied, either — record the call instead.
- **`event_generate` bypasses pointer hit-testing**, so it can never prove input
  is blocked. Probe with `winfo_containing` plus a positive control.
- **Force a platform probe in tests rather than `skipif`.** Tests that assert
  x11-only and aqua-only behavior should force `windowing_system` both ways, so
  the whole matrix runs on every box; `skipif` leaves a developer running
  neither branch.
- **Prove a new check fails against the bug by reverting the fix**, never by
  reading the code. A positioning check passed against a live bug for weeks
  because it exercised the explicitly-sized path the bug never touched.

### Repo map (essentials)
```
src/ttkbootstrap/
  __init__.py        # public exports; concrete BootMixin/AutoStyleMixin widget subclasses
  style/             # THE CORE engine package (split from style.py in 2.0):
    theme.py         #   Colors, ThemeDefinition
    builders_tk.py   #   StyleBuilderTK (legacy tk.* widgets)
    builders_ttk.py  #   StyleBuilderTTK per-theme coordinator + registry dispatch
    builders/        #   private widget-family ttk style recipes + frozen registry
    engine.py        #   Style singleton: theme walk, _image_cache, durable _user_options
    bootstyle.py     #   Keywords, Bootstyle resolver, tokenizer, BootMixin/AutoStyleMixin
    assets.py        #   PUBLIC toolkit: Assets (circle/rect/rounded_rect/icon/image)
    layout.py        #   PUBLIC toolkit: El/layout, image_element, statespec/state_map, register_style
    elements.py      #   shared element construction
    icons.py         #   IconRenderer + Icon atom + icon_element (Bootstrap Icons glyphs)
    scaling.py       #   windowing_system + high-dpi / geometry scaling
    _compat.py       #   legacy normalization + deprecation quarantine (removed in 3.0)
  menu.py            # ttk.Menu + the native macOS application-menu API
  validation.py      # PUBLIC Validation namespace (Validation.text/numeric/range/add)
  utils/             # PUBLIC utilities package (+ utility.py/colorutils.py shims)
  assets/icons/      # vendored Bootstrap Icons font + glyphmap + metrics (package data)
  widgets/, dialogs/, themes/, internal/, localization/
tests/               # headless pytest only
examples/            # interactive demos
tools/               # offline generators (bootstyle reference) + verify_positioning.py
docs/                # Sphinx + rST; docs/screenshots/ holds the capture scenes
development/         # design docs, the 2.x change logs, and the session handoffs
```
