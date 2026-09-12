# CLAUDE.md

Guidance for working in the ttkbootstrap repository.

## What this is

ttkbootstrap is a theming extension for tkinter/ttk: it generates flat,
Bootstrap-inspired themes on demand and adds a `bootstyle` keyword API to ttk
widgets. Pure Python; the only runtime dependency is Pillow. Public entry point
is `src/ttkbootstrap/__init__.py`, imported as `import ttkbootstrap as ttk`.

- Metadata and version: `pyproject.toml` (src layout, `requires-python >=3.10`).
- Docs: Sphinx + `pydata_sphinx_theme` in `docs/`, served by Read the Docs at
  **`www.ttkbootstrap.org`**. 1.x lives on the `release/v1` branch and at
  `/en/version-1/`; `/en/latest/` is 2.x.

**Scope is a real constraint:** ttkbootstrap is a **styling extension for vanilla
tkinter, not a widget library.** The forward-looking framework is the sibling
project **bootstack** (`D:/Development/bootstack`) — borrow its *mechanisms*
(repaint, positioning, docs infra), never its style API.

The users are mostly **scientific and utility developers already on clam**:
aesthetic polish is a nice-to-have, and a small value tweak usually beats
restructuring layout.

## Status

- **Latest release: 2.2.2.** `master` also carries unreleased **2.2.3** work
  (#1347, the PyInstaller hook).
- **Open milestones:** `2.2.x` (#7, the rolling bucket for patch releases) and
  `3.0` (#2, holding #1276). When `master` moves to a new minor, move whatever is
  still open in `2.2.x` to the next milestone.
- **Change log in progress:** `development/2_2_3_changes.md`, relative to 2.2.2.
  Log each user-visible change as it lands, and keep entries short — what changed
  and who it affects, not an essay.

## Where the record lives

- **`development/*_changes.md`** — user-facing change log per release; frozen once
  shipped. The source for release notes.
- **`development/2_0_breaking_changes.md`** — every 1.x→2.x behavior change. Still
  the place to log a break.
- **`development/*_design.md`** — design passes holding the *why* behind settled
  decisions. Read the relevant one before reopening a decision.
- **GitHub releases and closed milestones** — what shipped when.
- **Git history** — the session narrative of the 2.x work.

## 3.0

Milestone `3.0` holds deferred breaking work of two kinds:

- **Code shims** marked `removed in 3.0`. Find them with
  `grep -r "removed in 3.0" src` — deliberately not listed anywhere, since a
  hand-kept list drifts.
- **Design decisions with no shim**, each tracked as its own issue (#1276).

Don't build a 3.0 removal checklist until 3.0 is scoped.

## Repository layout

```
src/ttkbootstrap/
  __init__.py        # public exports; the concrete widget subclasses
                     #   (`class Button(BootMixin, ttk.Button)`) carrying `bootstyle` and
                     #   fluent pack/grid/place. Classic tk widgets with `autostyle`:
                     #   Tk/Text/Canvas/Listbox/TkFrame/TkLabel. `LabelFrame` is the ttk
                     #   alias for `Labelframe`, not the tk widget. The global monkey-patch
                     #   is opt-in via enable_global_api().
  __init__.pyi       # GENERATED widget type stub (tools/generate_widget_stubs.py)
  style/             # the theme/style engine (see below)
  window.py          # App / Window / Toplevel
  constants.py       # constants + the single bootstyle vocabulary source of truth
  colorutils.py      # color math
  validation.py      # the Validation namespace
  menu.py            # ttk.Menu + the native macOS application menu
  cli.py             # `ttkb` command: version / demo / convert-theme / creator
  convert_theme.py   # 1.x theme file -> Theme(...).register() source; pure text, no Tk
  __main__.py        # the widget demo (`ttkb demo`)
  themes/            # builtin.py (curated 2.x themes), standard.py + legacy.py (pre-2.0
                     #   Bootswatch names, migration path only; removed in 3.0)
  widgets/           # custom widgets: dateentry, meter, floodgauge, tableview, scrolled,
                     #   tooltip, toast, labeledscale
  dialogs/           # message, query, colorchooser, colordropper, datepicker, fontdialog,
                     #   filedialog (the in-house themed one; X11 default)
  utils/             # PUBLIC helpers: color, config (pre-root deferred setters), fonts,
                     #   platform, scaling
  localization/      # msgcat-based i18n (msgcat.py, api.py, msgs.py translations)
  internal/          # PRIVATE plumbing, no back-compat: busy, configure_delegation,
                     #   positioning, publisher, utility, wheel (scroll normalization)
  utility.py         # deprecation shim -> utils/ (removed in 3.0)
  publisher.py       # deprecation shim -> internal/publisher.py (removed in 3.0)
  assets/            # PACKAGE DATA: icons/ (Bootstrap Icons font, glyphmap, metrics),
                     #   elements/ (ttk element rasters + manifest), app_icons/
  _pyinstaller/      # PyInstaller hook, registered via the `pyinstaller40` entry point.
                     #   The hook must assign `datas`; tests/test_pyinstaller_hook.py checks.
tests/               # HEADLESS pytest only, CI-run
examples/            # manual visual gates (need a display; not collected by pytest)
docs/, gallery/      # documentation and showcase apps
tools/               # generators and manual verification gates
```

### internal/ vs public

`src/ttkbootstrap/internal/` (named `internal`, not `_internal`) has no
back-compat guarantee.

When moving something public→internal, leave a thin shim at the old path that
re-exports and emits a `DeprecationWarning` ("…moved to …; removed in 3.0"), as
`ttkbootstrap.publisher` does. **Importing `ttkbootstrap` itself must stay
warning-free** — shims warn only when the old path is used. Edit real
implementations, never a shim.

## The style engine (`style/`)

`ttkbootstrap.style` re-exports the package surface. Modules:

- **`engine.py` — `Style`**, the process-wide singleton (`Style.get_instance()`,
  subclasses `ttk.Style`). Owns theme definitions, the active theme, the durable
  user-override layer, the image cache, and `theme_use()`.
- **`builders_ttk.py` — `StyleBuilderTTK`**, the per-theme coordinator: color
  helpers, surfaces, `build_style(variant, widget_family, colorname)`, and
  `create_default_style()`.
- **`builders/`** — one module of ttk style **recipes** per widget family
  (`button.py`, `entry.py`, …), each registered with
  `@register_builder(variant, widget_family)` in `builders/registry.py`. A recipe
  configures its style through `builder.configure` and calls
  `builder.register_ttkstyle`.
- **`builders_tk.py` — `StyleBuilderTK`** styles the classic tk widgets.
- **`bootstyle.py` — `Bootstyle`**, the resolver (`update_ttk_widget_style()` maps
  a `bootstyle`/`style` string to a built style), plus `BootMixin` /
  `AutoStyleMixin` and `enable_global_api()`.
- **`theme.py`** — `Colors`, `ThemeDefinition`, `Theme`.
- **`icons.py`, `elements.py`, `assets.py`, `layout.py`, `scaling.py`** — glyph
  rendering, element raster recoloring, the image toolkit, layout helpers, and
  logical-unit scaling.
- **`_compat.py`** — quarantine for legacy bootstyle spellings (tuple/list forms;
  warn and normalize through 2.x).

**The bootstyle parser is a tokenizer over a closed vocabulary**, slot order
`[color-][modifier-]<base-type>[-orient]`. Unknown tokens warn by default and
raise under `set_bootstyle_strict(True)` or `TTKBOOTSTRAP_STRICT=1`. It accepts two
dialects: space/dash bootstyle strings (strict) and already-built dotted ttk style
names (lenient). The vocabulary lives in `constants.py`; the `BootStyle` `Literal`
and the docs table are generated by `tools/generate_bootstyle_reference.py`.

### Styles are built lazily

A style is built the first time a widget needs it. At theme load,
`create_default_style()` configures the root `.` style and builds a small eager
set: button, entry, combobox, menubutton and scrollbar (native dialogs use them
without the app ever creating one), the link button, and the tooltip label.

`theme_use()` bumps a theme version and walks the mounted widget tree, rebuilding
only the styles live widgets reference; durable user overrides are replayed per
theme.

**Consequence:** native or third-party ttk widgets the app never creates (e.g.
the buttons inside Tk's Linux file dialog) show bare clam unless their base style
is in the eager set. That is the fix pattern.

## Gotchas

- **`Style` is a singleton bound to the first Tk root.** Creating and destroying
  separate roots in one process mis-binds it and theming silently no-ops. Tests
  share one root (see "Writing tests").
- **Themes are clam-derived** (`theme_create(name, TTK_CLAM)`): an unbuilt style
  shows clam's look.
- **Framework code uses `_build_configure` (via `builder.configure`), never the
  public `Style.configure`.** The public method records values as durable *user*
  overrides and replays them after every build.
- **Durable ≠ honored.** The override layer persists any allowlisted option,
  including ones the widget never reads: ttk `Entry`/`Combobox`/`Spinbox` take
  `font` from the widget or `TkTextFont`, not the style; `sashthickness` works only
  on the pseudo-style `"Sash"`. And **a recipe that `map`s an option for all
  states masks `configure` entirely** — check before adding one.
- **Works ≠ API.** Option passthrough to a composite widget's container frame
  (`borderwidth`/`relief`/`padding` on DateEntry, Meter, LabeledScale, Tableview)
  is not API — don't document it. Designed delegates (DateEntry `state`/`width`)
  are.
- **`bootstyle` on a widget with its own ttk class** warns and keeps the current
  style. An explicit base type (`"info-frame"`) borrows a recipe. Composite
  internals follow the theme; the accent is not fanned out — `apply_bootstyle` on
  the child is the designed path.

## Platform & Tk facts

Measured, not assumed. Read these before touching geometry, scaling, assets or
event bindings.

### Monitors and window placement

- **Tk has no monitor enumeration.** On X11 `winfo screenwidth` is the union of all
  displays and `vrootwidth` usually equals it, so Tk can't find a monitor seam. On
  Windows `screenwidth` is the primary monitor and `vrootwidth` the virtual
  desktop.
- `internal/positioning.py` resolves the layout **`screeninfo` → X11 Xinerama via
  ctypes → Tk vroot**. **Use ctypes, never `subprocess`** (no shelling out to
  `xrandr`).
- **macOS multi-monitor is untested.** Without `screeninfo` aqua has no
  enumeration; the fallback is guaranteed safe (never straddles or goes off-edge)
  but may choose the wrong display.
- **`withdraw()` before building a window's contents.** Building shows the window,
  and re-showing it lets the WM re-place it.
- **Track "ever shown", don't infer it.** A never-mapped window is 1×1 on X11, but
  a win32 root reports its initial size. `_ever_shown` is set from
  `<Map>`/`<Configure>`.
- **On X11 a `geometry()` readback is the WM's placement**, not what you applied.
  Record the call.
- **A withdrawn dialog measures its content request**, not its mapped size — clamp
  against the minsize/geometry it will actually get.
- **WSLg reports a `-32730` sentinel position** until the compositor maps the
  window. Wait before measuring.

### Tcl/Tk versions

- **Tk 9 moved the aqua scaling baseline from 72 to 96 dpi**, and changed scroll
  events: `<TouchpadScroll>` for trackpads, wheel deltas normalized to ±120, no
  Button-4/5 on X11 (`internal/wheel.py`).
- **CI is Tk 8.6 only.** Run Tk 9 by hand for scaling, asset, geometry or binding
  changes — on the Mac, Homebrew `python3.14` is Tk 9.
- **A CPython patch release can change Tk behavior on the same Tk patchlevel**
  (3.13.15 started mapping menu bars on Tk 8.6.14). Record the build with
  `tools/report_tk_build.py` rather than reasoning from version strings.

### Widget behavior

- **`tk busy` is a no-op on aqua** and tkinter's busy methods are 3.13+
  (`internal/busy.py` backports). Don't emulate on aqua: Tk has no transparent
  color, so any shield hides the UI.
- **`tk.Menu` has no border color.** A flat hairline means painting the menu in
  the border color and each entry in the surface color — right for popups, wrong
  for a menu bar. Refuse menu bars by asking whether the menu is a window's
  `-menu` (or the `-type menubar` clone), not by inferring from `<Map>`.
- **A style `lookup` can return a `Tcl_Obj`** once built, and padding reads as
  `'10 4'` or `(10, 4)`. Compare as numbers.
- **Uninstalled font families don't round-trip** — Tk substitutes.
- **`-topmost` is a hint the WM may decline.** Assert it at the kwargs seam.
- **`event_generate` bypasses hit-testing**, so it can't prove input is blocked —
  use `winfo_containing` plus a positive control.

## Dev environment & commands

**Several boxes, each its own working copy and venvs.** Confirm which one you are
on first.

| Box | Notes |
| --- | --- |
| **Windows** | Screenshot-capture box, 100% scaling (1×). Two Windows accounts share the checkout and each owns different venvs (`.venv`, `.venv-home`, `.venv314`, …); a venv from the other account won't launch. Check `pyvenv.cfg`'s `home` to see whose it is. `gh` is installed. |
| **macOS** | `.venv` is Tk 8.6, `.venv314` is Tk 9. Retina (2×). The only box for native aqua menu shots. |
| **WSL2 / Linux** | Checkout at `/home/iddryer/ttkbootstrap` with its own Linux venv. No `gh`. |

- **Suite:** `python -m pytest -q`.
- **Docs:** `python -m sphinx -b html -W -q -E docs <out>` must exit 0 (RTD sets
  `fail_on_warning`). Deps in `docs/requirements.txt`.
- **Local gate set:** `pip install -r requirements.txt` (pytest, `screeninfo`, docs
  deps).
- **An editable install wins over a worktree's `src/`** — set `PYTHONPATH` to the
  worktree's `src` when testing a branch checked out elsewhere. An editable
  install's metadata (version, entry points) is also frozen at install time;
  reinstall after changing `pyproject.toml`.
- **`examples/` isn't collected by pytest**, so deprecations there go unnoticed —
  sweep them when you deprecate something.
- **Regenerate the type stub** after adding a widget or editing an `Options` table
  on a `docs/reference/api/` page: `python tools/generate_widget_stubs.py`.
  `tests/test_widget_stubs.py` fails until the stub matches (it regenerates in a
  subprocess, because another test enables the global API), and it audits those
  tables against the live Tk option set.
- **Stub tooltips are a separate manual gate:** `python tools/verify_hover.py`
  (needs `pyright` and `jedi`). PyCharm can't be scripted — check by hand when a
  report names it.

### CI

`.github/workflows/ci.yml` runs on push to `master` and on every PR: the suite on
ubuntu, windows and macOS (py3.13) plus ubuntu py3.10, and the docs under `-W`.

- `fail-fast` is off so one platform can't hide another's failure.
- **Every job should report identical test counts** — platform branches are forced
  probes, not `skipif`.
- `screeninfo` is deliberately not installed (it exercises the fallback layout
  path), and Xvfb is pinned to 96 dpi.
- Each job prints its Tcl/Tk patchlevel. There is no Tk 9 job and nothing visual.
- **A red job on a branch that touches no `src/`:** re-run `master`'s workflow
  before blaming the branch.

### Generators and gates (`tools/`)

Generated artifacts are never hand-edited — a hand-kept parallel copy drifts.

- **`generate_widget_stubs.py`** → `__init__.pyi`, from the `docs/reference/api/`
  pages (options and descriptions).
- **`generate_bootstyle_reference.py`** → the `BootStyle` `Literal` and docs table.
  Sync-tested.
- **`generate_style_reference.py`** → per-widget styling partials for the API pages.
- **`generate_icon_metrics.py`** → `assets/icons/icon_metrics.json`.
- **`make_app_ico.py`** → the packaged app icons from `assets/app_icons/` at the repo
  root.
- **`verify_positioning.py`** — PASS/FAIL placement checks. Run with and without
  `screeninfo`.
- **`verify_hover.py`** — editor hover and completion via pyright and jedi.
- **`report_tk_build.py`** — platform, Python and Tcl/Tk patchlevel.
- **`check_dist.py`** — opens a built wheel and sdist: required package data
  (font, element rasters, `py.typed`, stub, PyInstaller hook), no `docs/` or
  `development/` in the sdist, and `--expect-version`.
- **`docs/scripts/take_screenshots.py`** — scenes in `docs/screenshots/<page>.py`,
  captured per theme. Keep full pixel density and pin `:width: <logical>px` on
  every image directive (the harness prints it). `theme_gallery.py` captures the
  Themes catalog cards.

**Eyeball gates in `examples/`**, one per visual subsystem, each with a light/dark
toggle: `color_states_preview.py`, `surface_preview.py`, `icon_preview.py`,
`icon_button_preview.py`, `recolor_assets_preview.py` (`--scale`),
`value_token_preview.py`, `themed_file_dialog.py`,
`file_dialog_default_routing.py`, `neutral_preview.py`, and
`prerelease_visual_review.py` (the whole widget set, before a release). Check color
or asset changes against the matching one.

### Releasing

Releases are cut from `master`; `release/*` branches exist only for superseded
majors. **A pushed `vX.Y.Z` tag publishes:** `.github/workflows/publish.yml` runs
the suite, builds, `twine check`s, runs `check_dist.py --expect-version <tag>`, and
uploads via PyPI Trusted Publishing (no stored token). `gh workflow run
publish.yml` is a dry run — everything except the upload.

1. Bump `version` in `pyproject.toml` on `master`. It is the only place the version
   is written.
2. Fold `development/<version>_changes.md` into the release notes.
3. Push `master` and confirm CI is green. Build the docs under `-W` if they changed
   (publishing doesn't gate on docs).
4. Push an annotated tag `vX.Y.Z` and **watch the run** (`gh run watch`). PyPI
   refuses re-uploads, so a bad artifact burns the version number.
5. Create a GitHub release `vX.Y.Z` from the notes.
6. Verify with a clean-environment `pip install ttkbootstrap==X.Y.Z`.

**Building by hand:** `dist/` and `.pytest_cache/` may be owned by the other Windows
account and undeletable — build to a throwaway `--outdir`. `build` and `twine`
aren't in every venv. A local docs build reports the editable install's stale
version; RTD installs fresh.

### Writing tests

`tests/` is headless-only. **Take the `root` fixture** from `tests/conftest.py`
(one shared root, reset per test) instead of creating a window — a second root
mis-binds the `Style` singleton. Read a built style with
`app.tk.call("ttk::style", "lookup", "<Style>", "-<option>")`. Visual demos go in
`examples/`, extending the existing gate for the subsystem.

- **The shared root is pinned to `Scaling.baseline`**, so the suite is
  density-independent. No bare pixel assertions that only hold at 1×.
- **Force platform probes instead of `skipif`**, so every box runs every branch.
- **Global style state leaks across tests** — a test that mutates it can pass alone
  and fail in the suite.
- **Prove a new check fails by reverting the fix**, not by reading the code. Guards
  here have passed vacuously before.

## Documentation

Full IA and charters: `development/2_0_docs_design.md`. **The docs teach tkinter
itself, in the ttkbootstrap dialect** — a self-sufficient learning source.

- **Bands sort by depth:** Getting Started · Foundations · Feature guides · How-To.
  No band index pages.
- **Teach by building, not option tours.** Feature guides cover a subsystem end to
  end; **a How-To does one job**, with a short task-shaped title.
- **No internal jargon or implementation asides.** State what a thing is; the
  rationale for a limitation belongs in git.
- **In examples:** `theme=` (not `themename=`), curated 2.x theme names, spaces in
  multi-token `bootstyle` (`"primary outline"`, except `inverse-<color>`),
  `ttkb <command>` for the CLI, no backslash continuations.
- **In table cells, don't `/`-join items** — one per line via an rST line block,
  with a blank line before it inside a list-table cell.
- **Every snippet is run before it ships**, and every code block runs on its own.

**`-W` misses three rST defects:** nested inline markup inside `**bold**`; a line
block in a list-table cell without a preceding blank line; and an inline literal
not preceded by whitespace or an opener (e.g. two literals joined by `..`). **The
catch-all:** strip tags from the built pages and search the text for surviving
double backticks.

## Conventions

- Match the style of the file you're editing.
- **Public-name casing:** ttkbootstrap-authored names use `snake_case` (`apply_icon`,
  `icon_size`); names forwarded to a real Tk option or method keep Tk's spelling
  (`iconphoto`, `minsize`, `themename`). `bootstyle`/`autostyle` are grandfathered.
- Custom widgets generate image assets through the style builder / Pillow
  pipeline; prefer native ttk/clam mechanisms where both work.
- **Commit messages:** `type: imperative subject` (`fix:`, `docs:`, `build:`,
  `ci:`, `release:`), referencing the issue where there is one.
- Branch and PR per change, targeting `master` (1.x: `release/v1`).
- **Milestone every issue and PR that ships something** — the milestone is how
  "which release is this in" gets answered. No `Version x` labels.

### Working with git here

- **Check `git branch --show-current` before pushing.**
- **Commits use `israel.dryer@gmail.com`.** Check `git config user.email` in a new
  checkout — a checkout-local override has put the wrong address on pushed
  commits.
- **Pushing to a contributor's PR branch:** `gh pr checkout <n>` sets the push
  remote to their fork, but an IDE push or `git push -u origin` sends it to
  `origin` instead. Afterwards confirm
  `gh pr view <n> --json headRefOid` matches `git rev-parse HEAD`.
- **`git merge-tree | grep '^<<<<<<<'` is not a conflict check** — do a throwaway
  trial merge, which is also the only way to test two PRs combined.
- **Large deletions in `git diff master..<branch>`** mean the branch is behind.
- **PRs here are merged both ways (merge commit and squash)**, so `git branch -d`
  may call a merged branch "not fully merged" and `git cherry` can mislead too.
  Look before assuming it's unmerged.
- **`git reset --hard` destroys the author's uncommitted WIP.** The author keeps
  live WIP in the tree — leave files you didn't touch alone, and stash first.
- **Push is not merge**, and a commit pushed after a PR merged doesn't land —
  verify the merge includes your last push.

### Reviews

- **A review finding is a hypothesis with a reproduction**, not a verdict. The
  reproduction proves the defect, not the proposed fix — probe the fix against
  real data too.
- **Self-review has missed real defects every round.** Budget for it.
- **Probe what the user experiences** — type-checking can't see a bad tooltip, and
  CI can't see a build artifact that never runs.

### Writing for people

- **Release notes, PR bodies and issue comments go unwrapped** so the web reflows
  them; repo source docs stay wrapped.
- **Unwrapped is not unstructured** — use headings and bullet lists, and rewrite
  wrapped change-log paragraphs as single lines rather than pasting them.
