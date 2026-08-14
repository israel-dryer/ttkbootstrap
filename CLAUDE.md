# CLAUDE.md

Guidance for working in the ttkbootstrap repository.

## What this is

ttkbootstrap is a theming extension for tkinter/ttk: it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle` keyword
API to ttk widgets. Pure Python; the only runtime dependency is Pillow
(used for image-based widget assets). Public API entry point is
`src/ttkbootstrap/__init__.py`, typically imported as `import ttkbootstrap as ttk`.

- Package version / metadata: `pyproject.toml` (src layout, `requires-python >=3.10`).
- Docs site: Sphinx + `pydata_sphinx_theme` (`docs/`, config in `docs/conf.py`),
  published to Read the Docs. (Was mkdocs pre-2.0.)

**Scope, and it is a real constraint:** ttkbootstrap is a **styling extension for
vanilla tkinter — not a widget library.** The forward-looking framework is a
separate project, **bootstack** (sibling repo at `D:/Development/bootstack`).
Mine bootstack for *mechanisms* — memory/repaint, positioning, docs infra — and
never for its style API.

The user base is predominantly **scientific and utility developers already on
clam**, which is why aesthetic polish is a nice-to-have rather than a
requirement, and why a small value tweak usually beats restructuring layout.

## Direction

> **STATUS (2026-08-14): ttkbootstrap 2.2.1 is RELEASED.** Tagged `v2.2.1`, on
> [PyPI](https://pypi.org/project/ttkbootstrap/2.2.1/), GitHub release live,
> verified by a clean-environment install. **`master` reads 2.2.1**, and per the
> standing convention **`master` is always the most recent release**.
>
> **Only one milestone is open: `3.0`**, holding **#1276** (make `DateEntry`
> `value=None` the default). No open issues besides it, no open PRs.
>
> **The next user-visible change starts a new change log.** Create
> `development/2_3_changes.md` (or `2_2_2_` for a patch) when the first one
> lands, scoped **relative to 2.2.1**, and log there as you land — not at release
> time. It is the release-notes source, and the release audits it against
> `git diff v2.2.1..master`.
>
> **Don't file against a `2.2.x` bucket.** A patch is cut from `master` and
> `release/*` exists only for *superseded majors*, so the moment `master` reads
> 2.3.0 there is no branch a 2.2.2 could come from and anything left on `2.2.x`
> can never ship. This stranded #1322 on `2.1.x` and had to be unwound at release
> time.
>
> **Publishing is still manual, and should not stay that way.** 2.2.1 was built
> and uploaded by hand from a developer box; the standing intent is to build and
> publish from the **tag** in CI for the next release. See "Releasing" below.

### The 2.x line

| Release | Date | What it was |
| --- | --- | --- |
| **2.0.0** | 2026-07-19 | The cleanup/consolidation rebuild — no new features. Mixin API replacing the import-time monkey-patch, canonical `bootstyle` grammar, semantic-anchor themes, a version-stamped repaint engine, font-glyph icons, and a from-scratch Sphinx docs site. |
| **2.0.1** | 2026-07-23 | Two Tcl/Tk 9 fixes and nothing else: the scroll-event contract and the aqua scaling baseline. |
| **2.1.0** | 2026-07-30 | Durable style options, `bootstyle` value tokens, the in-house themed file dialog, and multi-monitor-correct dialog positioning. |
| **2.1.1** | 2026-08-02 | Typing/docs patch — the widget type stubs came back (2.0 had dropped them, silently disabling keyword checking). |
| **2.2.0** | 2026-08-06 | `ttkb` command line, 1.x theme converter, pre-root `Theme.register()`, `__version__`. |
| **2.2.1** | 2026-08-14 | One fix: a menu bar is never painted in the border color, whatever the Tk build does (an X11 regression surfaced by CPython 3.13.15 mapping menu bars). |

**1.x is preserved** on the `release/v1` branch and as the `version-1` Read the
Docs version (`/en/version-1/`); `latest` serves the 2.x Sphinx docs. 1.x
maintenance, if any, targets `release/v1`. RTD redirect map for the old mkdocs
URLs: `development/2_0_rtd_redirects.md`.

### Where the record lives

This file used to carry a session-by-session narrative of the whole 2.x
initiative — about 2,160 lines. It was condensed once 2.2 shipped, because a
finished release log is background, not an active worklist, and it crowded out
the durable facts. **The narrative is in git history**; what survived is
redistributed into the topical sections below, where the next person will
actually look for it. When you need the detail:

- **`development/*_changes.md`** — the user-facing change log per release
  (`2_1_changes.md`, `2_1_1_changes.md`, `2_2_changes.md`). Frozen once shipped.
- **`development/2_0_breaking_changes.md`** — every 1.x→2.x behavior change, with
  rationale. Still the place to log a break.
- **`development/*_design.md`** — 26 design passes (engine, theme anchors,
  bootstyle grammar, docs IA, durable options, value tokens, file dialog, …).
  These hold the *why*, and several were gates the author confirmed before
  implementation. Read the relevant one before reopening a settled decision.
- **`development/2_0_plan.md`** — the original 2.0 worklist and locked decisions.
- **GitHub releases + closed milestones** — what shipped when, per PR.

### 3.0 (future major)

Milestone **#2 (`3.0`)** is the home for deferred breaking work. Two kinds:

- The **code shims** marked `removed in 3.0` (32 across 18 source files at 2.2).
  They are **grep-discoverable** (`grep -r "removed in 3.0" src`), so
  deliberately *not* enumerated in a meta-issue — a hand-maintained list would
  only drift, which is the same reasoning that deleted `AGENTS.md`.
- **Design decisions with no code shim** — the fragile ones, which get their own
  tracked issues. First is **#1276**.

Don't build a full 3.0 removal checklist until 3.0 is actually scoped.

## Repository layout

```
src/ttkbootstrap/
  __init__.py        # public exports; defines the concrete BootMixin/AutoStyleMixin widget
                     #   subclasses (e.g. `class Button(BootMixin, ttk.Button)`) that carry the
                     #   `bootstyle`/`autostyle` api + fluent pack/grid/place (return self). No
                     #   import-time monkey-patch (2.0, PR 3) — opt into it via enable_global_api().
                     #   Blessed tk widgets: Tk/Menu/Text/Canvas/Listbox/TkFrame/TkLabel.
                     #   `LabelFrame` is the ttk alias for `Labelframe` (matching tkinter.ttk),
                     #   NOT the classic tk widget (that 1.x meaning was dropped — see
                     #   development/2_0_breaking_changes.md).
  style/             # THE CORE — theme/style engine package (see below). Split from the old
                     #   style.py in 2.0 (PR 4); public import path `ttkbootstrap.style` unchanged.
                     #   theme.py (Colors, ThemeDefinition), builders_tk.py (StyleBuilderTK),
                     #   builders_ttk.py (StyleBuilderTTK — the bulk), engine.py (Style),
                     #   bootstyle.py (Keywords, Bootstyle, tokenizer, FluentGeometryMixin +
                     #     BootMixin/AutoStyleMixin, delivery),
                     #   _compat.py (legacy-form quarantine: normalize_bootstyle, strictness).
  window.py          # Window / Toplevel classes
  constants.py       # constants (PRIMARY, SUCCESS, ...) + the single bootstyle vocab source of
                     #   truth: BOOTSTYLE_* tuples, BootColor/BootType/BootBase, generated BootStyle
  colorutils.py      # color math (Colors helpers, make_transparent, contrast)
  validation.py      # the Validation namespace (text/numeric/range/regex/add)
  menu.py            # ttk.Menu + the native macOS application menu (no-ops off macOS)
  cli.py             # the `ttkb` / `ttkbootstrap` command (version/demo/convert-theme/creator)
  convert_theme.py   # 1.x theme file -> Theme(...).register() source. Pure text, no Tk.
  __main__.py        # the widget demo (`ttkb demo`)
  themes/standard.py # STANDARD_THEMES dict: pre-2.0 (Bootswatch) color defs, kept only for
                     #   the legacy theme-name migration path (removed in 3.0)
  themes/builtin.py  # CURATED_THEMES: the curated 2.0 semantic-anchor Theme families
                     #   (custom themes live in user code via Theme(...).register(), not here)
  widgets/           # CANONICAL custom widgets: dateentry, meter, floodgauge, tableview,
                     #   scrolled, tooltip, toast, labeledscale
  dialogs/           # Messagebox, Querybox, colorchooser, colordropper, datepicker,
                     #   fontdialog, filedialog (the in-house themed one; X11 default)
  utils/             # PUBLIC utilities: config (deferred-apply seam), fonts, localization
  localization/      # msgcat-based i18n (msgs.py holds translations)
  internal/          # PRIVATE plumbing (no underscore in the name): publisher.py, utility.py,
                     #   positioning.py, configure_delegation.py, busy.py (tkinter busy shim).
                     #   No back-compat guarantee. See "internal/ vs public" below.
  utility.py         # PUBLIC utility funcs: enable_high_dpi_awareness, scale_size
  publisher.py       # deprecation shim -> internal/publisher.py (warns; removed in 3.0)
  assets/icons/      # vendored Bootstrap Icons font + glyphmap (package data — a wheel
                     #   missing it installs fine and dies at first render)
tests/               # HEADLESS pytest only, CI-runnable. ~37 test_*.py + conftest.py,
                     #   plus widget_styles/, widgets/, cli/, localization/ subpackages.
examples/            # manual visual gates — one mainloop() app per visual subsystem (color
                     #   states, surfaces, icons, recolored assets, value tokens, file dialog).
                     #   Need a display; NOT collected by pytest. Per-widget tours and API
                     #   demos were removed in 2.2 — `ttkb demo` and the docs cover those.
docs/, gallery/      # documentation and showcase apps
tools/               # generators + manual verification gates (see Dev environment below)
```

### internal/ vs public (important — new in 2.0)

Implementation-detail modules live in **`src/ttkbootstrap/internal/`** (the
name is `internal`, *not* `_internal`). Anything under it has no
back-compat guarantee.

When moving something public→internal, leave a thin shim at the old public path
that re-exports from `internal/` and emits a `DeprecationWarning` ("…moved to
ttkbootstrap.internal.X; removed in 3.0") — e.g. `ttkbootstrap.publisher`. For a
module that stays public but sheds internal helpers (e.g. `utility.py`), forward
the moved names via module-level `__getattr__` with the same warning instead of
a whole shim module. **Importing `ttkbootstrap` itself must stay warning-free**
— shims warn only when an old path is actually used.

The older top-level shims (`ttkbootstrap.scrolled/tableview/toast/tooltip`,
`dialogs/dialogs.py`) were **removed** in #1068 — import from
`ttkbootstrap.widgets.<name>` / `ttkbootstrap.dialogs`. Edit real
implementations in `src/ttkbootstrap/widgets/`, never a shim.

## The style engine (`style/` package)

Everything visual flows through here. Split from the old monolithic `style.py`
in 2.0 (PR 4) into a `style/` package; `ttkbootstrap.style` re-exports the full
surface, so the import path is unchanged. The submodules layer downward
(`theme` → `builders_tk` → `builders_ttk` → `engine` → `bootstyle`), with a few
function-local back-edge imports. Key classes (by module):

- **`Style`** (`engine.py`) — singleton (`Style.get_instance()`), subclasses
  `ttk.Style`. Owns theme definitions and the active theme. `theme_use()`
  switches themes and runs the version-stamped theme walk (PR 1) that repaints
  only stale mounted widgets — styles rebuild lazily/O(mounted), not all up front.
- **`StyleBuilderTTK`** (`builders_ttk.py`) — holds `create_*_style(colorname)`
  methods (e.g. `create_button_style`, `create_outline_toolbutton_style`). These
  build a ttk style and call `_register_ttkstyle()`.
- **`StyleBuilderTK`** (`builders_tk.py`) — styles legacy `tk.*` widgets (Menu,
  Text, Canvas, …).
- **`Colors` / `ThemeDefinition`** (`theme.py`) — the color model + theme
  container.
- **`Bootstyle`** (`bootstyle.py`) — the resolver: `update_ttk_widget_style()` maps a
  `bootstyle=`/`style=` string to a built ttk style. Two delivery paths feed it
  (2.0, PR 3): the default `BootMixin`/`AutoStyleMixin` concrete subclasses
  (in `__init__.py`), and the opt-in global monkey-patch
  (`enable_global_api()` → `setup_ttkbootstrap_api()`). As of 2.0 the
  parser is a real **tokenizer over a closed vocabulary** (fixed slot order
  `[color-][modifier-]<base-type>[-orient]`), not a substring regex: unknown
  tokens fail loudly (warn by default; `set_bootstyle_strict(True)` /
  `TTKBOOTSTRAP_STRICT=1` raises). It handles **two input dialects** —
  dash/space bootstyle strings (loud) vs already-built dotted ttk style names
  from the theme walk / `Style.configure` / custom styles (lenient). The vocab
  lives once in `constants.py`; the reference (`BootStyle` `Literal` + docs
  table) is generated by `tools/generate_bootstyle_reference.py`, sync-tested.
  Legacy forms (tuple/list bootstyle) are quarantined in `style/_compat.py`
  (warn-and-normalize through 2.x, removed in 3.0).

### Lazy style building — the model to keep in mind

Styles are built **on demand**, not up front. The base `TButton`, `TEntry`,
etc. are only configured the first time a widget that needs them is created
(or via `_create_ttk_styles_on_theme_change` for already-registered styles).
At theme load, `create_default_style()` configures the root `.` style plus a
small set of always-needed styles.

Consequence (and a real past bug, #1062): native/third-party ttk widgets the
app never instantiates directly — e.g. the `ttk::button` widgets inside Tk's
file dialog on Linux — fall back to the bare clam look if no corresponding
ttkbootstrap widget has been created. The fix pattern is to build the needed
base style eagerly in `create_default_style()`.

## Gotchas

- **`Style` is a process-wide singleton (`Style.instance`) tied to the first Tk
  root.** Creating and destroying separate roots in one process leaves the
  singleton mis-bound, so later theming silently no-ops. Tests share ONE root
  via the `root` fixture in `tests/conftest.py` — see "Writing tests" below.
  (Properly fixing the singleton is part of the deferred `style.py` engine
  rewrite.)
- **Themes are clam-derived** (`theme_create(name, TTK_CLAM)`). An unstyled
  base ttk style shows clam's default appearance until ttkbootstrap configures it.
- **Framework code uses `_build_configure`, never the public `Style.configure`.**
  The durable style-options layer captures public `configure` calls as *user*
  overrides and re-applies them after every build, so a recipe or an internal
  helper calling the public method miscaptures its own values as a fake user
  override. Two real cases were fixed this way (`create_default_style`'s
  `symbol.Link.TButton`/`tooltip.TLabel`, and `apply_icon`'s derived style).
- **Durability ≠ the widget honoring the option.** The layer faithfully persists
  any allowlisted option, including ones the widget never reads. Probed: ttk
  `Entry`/`Combobox`/`Spinbox` read `font` from the widget or the named
  `TkTextFont`, **not** the style, so `configure("TEntry", font=…)` persists and
  never renders; `sashthickness` works only on the global pseudo-style `"Sash"`,
  because `ttk::panedwindow` is a C widget querying that literal name. A third
  class is self-inflicted: **a recipe that `map`s an option for *all* states
  masks `configure` entirely** — audit for that shape before adding a map.
- **"Works ≠ designed surface."** A composite widget's container-`Frame` option
  passthrough (`borderwidth`/`relief`/`padding` on DateEntry/Meter/LabeledScale/
  Tableview) happens to work and is **not API** — don't document it. Designed
  delegates (DateEntry `state`/`width`) are.
- **`bootstyle` on a widget with its own ttk class** warns and keeps the current
  style rather than raising. Full vocabulary applies to standard ttk classes; an
  explicit base type (`"info-frame"`) borrows a recipe. Composite internals
  follow the theme on their own — only the accent isn't fanned out, and
  `apply_bootstyle` on the child is the designed path.

## Platform & Tk facts

Measured, not assumed — each of these cost a real bug. Anything touching
geometry, scaling, assets or event bindings should be read against them.

### Monitor layout and window placement

- **Tk exposes no monitor enumeration on any platform.** On X11 `winfo
  screenwidth` reports the **union of every display**, and `winfo vrootwidth`
  falls back to that same value unless a virtual-root WM is running (nothing
  modern sets `__SWM_VROOT`) — so Tk's own metrics can never locate a monitor
  seam there, which is how a clamp against them let a dialog straddle two
  screens. Windows differs: `winfo screenwidth` is the primary monitor,
  `winfo vrootwidth` the virtual desktop, and the difference derives the grid.
- `internal/positioning.py` resolves the layout **`screeninfo` → X11 Xinerama
  via ctypes → Tk vroot**. **The library has never used `subprocess`** — ctypes
  is the house pattern (same as the Windows DPI and shell APIs); don't shell out
  to `xrandr`. Verified 4/4 on dual-monitor Windows and 5/5 on dual-monitor X11.
- **macOS multi-monitor is taken on trust** (no second display to test with).
  With `screeninfo` installed everything after the layout is
  platform-independent arithmetic already covered elsewhere; without it aqua has
  no enumeration at all, and the fallback is made *safe* rather than merely
  untested by `test_placement_stays_on_screen_when_no_layout_is_available` —
  worst case is landing on the wrong display, never straddling or off-edge. The
  real closure is the deferred `CGGetActiveDisplayList` ctypes call.
- **`withdraw()` goes before you build a window's contents, not after.** Building
  widgets *shows* the window, and re-showing an already-shown window is a fresh
  placement the WM decides for itself (measured drifting hundreds of px, differently
  each run). Reproduced in pure tkinter, so it is the window manager, not us.
- **"Has this window ever been shown?" must be tracked, not inferred.** A
  never-mapped window reports 1×1 on x11, but on **win32 the root reports the
  size Tk started it at** — so a `winfo_width() > 1` test is x11 reasoning that
  centers the wrong box on Windows. `_ever_shown` is set from a `<Map>`/
  `<Configure>` handler instead.
- **A `geometry()` readback is not the position you applied on X11** — a
  withdrawn window reports the WM's own placement (asked `+4460+20`, reads back
  `+32+32`). Record the call instead of reading it back.
- **A dialog positioned while withdrawn measures its content request, not the
  size it will map at** — clamp against the minsize/geometry floor it will
  actually get, or the button column lands off-screen.
- **WSLg reports a `-32730` sentinel position** until the compositor has mapped a
  window, so a `geometry()` + `update()` then measure sequence parks the window
  nowhere. Settle-wait before measuring, or a check passes vacuously.

### Tcl/Tk versions

- **Tk 9 moved the aqua scaling baseline from 72 to 96 dpi** — every asset and
  padding rendered 33% larger than designed while text stayed put. Tk 9 also
  changed the scroll-event contract: trackpads fire `<TouchpadScroll>`, wheel
  deltas need normalizing to ±120, and X11 no longer delivers Button-4/5.
- **CI is Tk 8.6 everywhere**, so a Tk 9 run is a manual step — worth doing for
  anything touching scaling, assets, geometry or event bindings. On the Mac,
  Homebrew `/opt/homebrew/bin/python3.14` is Tk 9.

### Widget-level behavior

- **`tk busy` is a no-op on macOS/Aqua**, and tkinter's busy methods are
  **3.13+** (`internal/busy.py` shims the older line). The macOS no-op is
  deliberately not emulated: Tk's busy window is a *transparent* input shield and
  Tk has no transparent color, so any emulation is opaque and hides the UI.
- **`tk.Menu` has no border color of its own** — no `highlightthickness`,
  `relief="solid"` is hardcoded black, and the 3D reliefs derive both shades from
  `-background`. The only route to a flat hairline is painting the *menu* in the
  border color and each *entry* in the surface color. That holds for a popup and
  **not** a menu bar (whose entries cover only the left of the bar), so a menu
  bar must be refused explicitly — ask whether the menu is installed as a
  window's `-menu` (or is the `-type menubar` clone). It used to be inferred
  from `<Map>`, on the measurement that **Tk displays a menu bar through a
  clone** so the widget you style never maps. **That is a property of the build,
  not a guarantee** — under CPython 3.13.15 it maps, which painted every X11 menu
  bar in the border color. **Not a Tk version difference**: CI's py3.10 job does
  *not* map it on the same **Tk 8.6.14**, so the interpreter is part of it and
  the exact mechanism is still unidentified. Which is the lesson — a behavioral
  Tk fact is worth re-deriving rather than leaning on, and worth designing out
  when the invariant can be asked for directly instead.
- **A style `lookup` can return a `_tkinter.Tcl_Obj`** once the style is *built*
  (`int()` rejects it, `str()` renders the number), and padding reads as `'10 4'`
  or `(10, 4)` depending on whether a rebuild has happened. Compare as numbers.
- **Font families that are not installed do not round-trip** — Tk substitutes, so
  asserting `== "Georgia"` asserts the host's font inventory.
- **`-topmost` is a hint a window manager may decline.** Assert it at the kwargs
  seam, not by reading it back.
- **`event_generate` bypasses pointer hit-testing** and can never prove input is
  blocked — probe with `winfo_containing` plus a positive control.

## Dev environment & commands

A virtualenv with an editable install lives at `.venv/` (Python 3.x on macOS;
`python` on PATH resolves to it). The package is also importable with
`PYTHONPATH=src`.

**This project is developed across several boxes, each a separate working copy
with its own venv — none of it carries over.** Start a session by confirming
which one you are on rather than assuming:

| Box | Notes |
| --- | --- |
| **Windows** | The canonical screenshot-capture box, and the only one where the demo has been eyeballed. Two profiles: `.venv-home` belongs to the `Israel Dryer` profile, `.venv` to `Logistiview` — each is unusable from the other, and neither is stale. `gh` is installed. Runs at 100% scaling = 1× density. |
| **macOS** | One venv per Tk line: `.venv` is Tk 8.6, `.venv314` is Tk 9. Retina = 2× density. The only box that can capture native aqua menus or the application-menu shot. |
| **WSL2 / Linux** | Checkout at `/home/iddryer/ttkbootstrap` with a *Linux* venv. **`gh` is not installed** — a PR can still be opened by reading the token from the credential helper the pushes use and POSTing to the API, but installing `gh` would make it a one-liner. |

- Run the headless suite: `python -m pytest -q` (config in `pyproject.toml`
  under `[tool.pytest.ini_options]`; `testpaths = ["tests"]`).
- pytest is installed in `.venv`. If a fresh env lacks it: `pip install pytest`.
- The visual gates in `examples/` call `mainloop()` and need a display — they are
  NOT collected by pytest, so nothing catches a deprecation that lands in them.
  Sweep them when you deprecate something (2.2 found tuple `bootstyle`, legacy
  Bootswatch theme names and the `inverse` modifier still in there).
- Build docs: `python -m sphinx -b html -W -q -E docs <out>` (must exit 0 — the
  docs are kept warning-clean; RTD enforces `fail_on_warning`). Deps in
  `docs/requirements.txt`. **`.venv-home` belongs to the author's other Windows
  profile** (its base interpreter lives under `C:\Users\Israel Dryer\...`), so it
  is unusable from the `Logistiview` profile — the docs deps were installed into
  `.venv` there on 2026-07-27. Use whichever venv matches the profile you are on;
  neither is stale.
- `pip install -r requirements.txt` (root) installs the local gate set — pytest,
  `screeninfo`, and the docs deps. RTD reads `docs/requirements.txt` directly.
- **An editable install wins over a worktree's own `src/`.** A branch suite run
  from a `git worktree` silently tests the *main* checkout's code; pin
  `PYTHONPATH` to the worktree's `src` when testing a branch checked out
  elsewhere.
- **Regenerate the type stub** after adding a widget or editing an `Options`
  table on a `docs/reference/api/` page: `python tools/generate_widget_stubs.py`
  (writes `src/ttkbootstrap/__init__.pyi`; `--output` targets somewhere else).
  `tests/test_widget_stubs.py` fails until the committed stub matches, and it
  regenerates in a **subprocess** — an in-process run would read the `(*args,
  **kwargs)` wrappers `enable_global_api()` installs on the tkinter classes,
  since another test in the suite enables it. The same file also audits the
  reference tables against the live Tk option set, so an undocumented option
  fails there rather than becoming a false positive in a user's type checker.
- **The stub's *tooltip* is a separate, manual gate:**
  `python tools/verify_hover.py` (needs `pip install pyright jedi`). A stub can
  type-check perfectly and still show the wrong hover — the first working
  version put the `Args:` docstring on the class, so editors read `__init__`,
  found nothing, and fell back to `BootMixin.__init__`'s "*args, \*\*kwargs"
  text. The script drives **pyright over LSP** (`textDocument/hover`, i.e. what
  VS Code/Pylance renders) and **jedi** for signature + `bootstyle=`
  completion. **PyCharm is not covered and cannot be scripted** — check it by
  hand when a report names it, as #1327 did.
- **CI runs the two automatable gates** (`.github/workflows/ci.yml`, #1317) on
  push to `master` and every PR: the suite on **all three windowing systems** —
  Linux, Windows and macOS on py3.13, plus the py3.10 floor from
  `pyproject.toml` (macOS added in #1319) — and the docs under `-W`.
  `fail-fast` is off so one platform's failure cannot hide another's — the whole
  reason it exists, after a Windows-only failure sat on `master` for two days
  (#1315). All three report **identical counts**, which is the signal to watch:
  the suite's platform branches are forced probes (the #1229 convention), not
  `skipif`, so every box runs the whole matrix and the numbers should match.
  **`screeninfo` is left uninstalled on purpose** (it is optional at runtime, so
  omitting it exercises the more fragile fallback layout path), and the Xvfb
  display is pinned to 96 dpi to be a standard-density screen.
- **CI does not cover Tk 9 or anything visual.** Every runner is **Tk 8.6** — the
  workflow reports the Tcl/Tk build per job (`tools/report_tk_build.py`) rather
  than leaving it inferred from the Python version, because 8.6-vs-9 is the split
  behind the aqua dpi baseline and the scroll-event contract. Adding a Tk 9 job is
  not free: `setup-python` ships no interpreter built against it. Visual gates stay
  manual and still need the right box — see `tools/verify_positioning.py` and the
  screenshot harness.
- **The report includes the Tk *patchlevel*, because `tk=8.6` is not a build.**
  A CPython **patch** release can change behavior: 3.13.14 → 3.13.15 started
  mapping menu bars and broke `test_a_never_posted_menu_is_not_painted` on ubuntu
  py3.13 alone. The patchlevel then showed it is **not** a Tk-version story — both
  ubuntu jobs run **Tk 8.6.14** and only the 3.13 one mapped — so record the build
  and let it correct you rather than reasoning from the version string. Observed
  spread: linux 8.6.14, win32 8.6.15, darwin 8.6.18.
- **A red job on a branch that touches no `src/` deserves a control run.**
  Re-run **`master`'s own workflow** before believing the branch caused it — CI
  had not run on `master` for 8 days, and the identical failure there is what
  established the drift in one step.

### Generators and manual gates (`tools/`)

Several artifacts are **generated, not hand-maintained** — the recurring lesson
being that a hand-kept parallel copy only drifts (it is also why `AGENTS.md` was
deleted and why the 3.0 shim list stays grep-discoverable).

- **`generate_widget_stubs.py`** → `src/ttkbootstrap/__init__.pyi`. Which classes
  need stubbing is *discovered* (an exported mixin subclass with a generic ctor),
  and each one's options **and description** come from the authored
  `docs/reference/api/` pages, so tooltip and documentation cannot drift.
- **`generate_bootstyle_reference.py`** → the `BootStyle` `Literal` and the docs
  reference table, from vocab × registry. Sync-tested.
- **`verify_positioning.py`** — a PASS/FAIL line per placement check. Its
  docstring explains why a green run on one box proves little; it has been run
  green on Windows, X11 and macOS (both Tk lines), twice each — **with and
  without `screeninfo`**, since forcing it off is the only way to exercise the
  fallback layout path.
- **`verify_hover.py`** — drives pyright over LSP and jedi. **PyCharm cannot be
  scripted**; check it by hand when a report names it.
- **`report_tk_build.py`** — platform, Python, and the Tcl/Tk **patchlevel**. Run
  it on a box before blaming its Tk for something; CI runs it per job.
- **`docs/scripts/take_screenshots.py`** — scene files in
  `docs/screenshots/<page>.py` mirroring each page's own code blocks, captured
  per theme. PNGs keep the capture box's full pixel density and every rST image
  directive pins `:width: <logical>px` (the harness prints it) — never downscale,
  never leave unpinned.

The **eyeball** gates live in `examples/` rather than `tools/` — one app per
visual subsystem, each with a light/dark toggle, to be looked at rather than
asserted: `color_states_preview.py` (every color × state across the widget set),
`surface_preview.py` (the elevation scale), `icon_preview.py` /
`icon_button_preview.py` (the icon engine), `recolor_assets_preview.py`
(`--scale 1.0|1.25|1.5|2.0`, the one gate that takes an argument),
`value_token_preview.py`, `themed_file_dialog.py` /
`file_dialog_default_routing.py`, `neutral_preview.py`, and
`prerelease_visual_review.py` (the whole-widget-set sweep, run before a release).
They are the re-runnable proof behind the design docs' recorded PASSes, so a
color or asset change should be checked against the matching one.

### Releasing

No CI publishes; the upload is manual, with credentials in a gitignored
repo-root `.pypirc`. **`master` is always the most recent release** — a patch
release is cut from `master`, so the version bump lands there naturally;
`release/*` exists only for *superseded* majors.

**The intent is to retire this manual path**: build and publish from the pushed
**tag** in CI (Trusted Publishing, no long-lived token), leaving only the bump,
the change log and the tag as human steps. Not done yet — the checklist below is
still the live procedure.

**Building is per-box, and the Windows two-profile split bites here.** `dist/`
and `.pytest_cache/` in this checkout are owned by the `Israel Dryer` profile;
from `Logistiview` they cannot be deleted or even `Get-Acl`'d, so step 4's
"empty `dist/` first" simply fails. Build to a throwaway `--outdir` instead —
which satisfies the same intent (no stale artifact in the upload set) more
strongly than emptying does. `dist/` therefore still holds superseded wheels, so
the **explicit version glob on upload is load-bearing, not belt-and-braces**.
`build` and `twine` are also **not** installed in every venv — 2.2.0 shipped from
the other profile's, and `.venv` needed `pip install build twine` at 2.2.1.

1. Bump `version` in `pyproject.toml`, **at release time, on `master`**. It is the
   only place the version is written — nothing under `src/`, `docs/` or `tools/`
   hardcodes it. 2.0.1 shipped its bump on a throwaway `release/2.0` branch and
   `master` kept claiming 2.0.0 for days — don't repeat that branch.
   `docs/conf.py` reads the *installed* distribution's version through
   `importlib.metadata` into `release`/`version`. Neither is rendered anywhere
   today (`html_title` is a fixed string and there is no version switcher), so a
   wrong value is latent rather than visible — but do not read a local docs build
   as confirmation of the bump: an editable install keeps whatever metadata it was
   built with, and this checkout's has read **2.0.0a1** for the whole 2.x cycle.
   RTD is unaffected; it installs fresh, so it reports the real version.
2. Fold `development/2_<x>_changes.md` into the release notes.
3. Run the gates: the full suite, and the docs build under `-W`.
4. **Empty `dist/` first**, then `python -m build`, then `twine check dist/*`, then
   upload **by explicit version glob** — `twine upload dist/ttkbootstrap-X.Y.Z*`.
   `dist/` is gitignored, so it keeps whatever the last release built: at 2.1.0 it
   still held the 2.0.0 wheel and sdist from July 19, and a bare `dist/*` upload
   would have tried to re-publish 2.0.0 alongside the new version. Worth spending
   a minute on the artifact while you are there — `twine check` validates metadata
   but not contents, so confirm the wheel carries `ttkbootstrap/assets/icons/`
   (the vendored Bootstrap Icons font is package data, and a wheel missing it
   installs and then fails at first render) and that the sdist has no `docs/` or
   `development/` in it.
5. Annotated tag `vX.Y.Z`, plus a GitHub release titled the same way.
6. Verify with a clean-environment `pip install ttkbootstrap==X.Y.Z`.

### Writing tests

`tests/` is headless-only. New GUI tests should **take the `root` fixture** from
`tests/conftest.py` (one shared session root; widgets and theme are reset per
test) instead of creating their own `ttk.Window` — creating your own root
re-triggers the singleton mis-binding above. Query a built style's value with
`app.tk.call("ttk::style", "lookup", "<Style>", "-<option>")`. Put any
interactive/visual demo in `examples/`, not `tests/` — but `examples/` is a
curated set of subsystem gates, not a dumping ground. Extend the gate that
already covers the subsystem before adding a file to it.

- **The shared root is pinned to `Scaling.baseline`**, so the suite is
  density-independent and passes at 1.0, 1.4, 1.6667 and 2.0. Don't reintroduce
  a bare pixel assertion that only holds at 1×.
- **Force a platform probe rather than `skipif`.** Every platform branch is
  asserted on every box, so all CI jobs report **identical counts** — a `skipif`
  would leave a Mac dev running neither branch.
- **A test that mutates global style state passes alone and fails in the suite.**
  Style overrides leak across tests (something already leaves `Link.TButton`
  padding at `40 2`), so `create_default_style` is idempotent at session start
  and *not* once styles carry overrides.
- **Prove a new check fails against the bug by reverting the fix, never by
  reading the code.** Two guards in this repo passed vacuously for weeks — one
  searched for strings that lived *inside* the function it was guarding, so
  deleting the call site left it green.

## Documentation

Full IA, charters and the curriculum map: `development/2_0_docs_design.md`.
The governing principle: **the docs teach tkinter itself, in the ttkbootstrap
dialect** — a self-sufficient learning source. Teach, don't defer.

- **Bands sort by depth:** Getting Started · Fundamentals · Feature guides ·
  How-To. There is **no "Concepts" band**. **No band index pages** — the sidebar
  and the user-guide cards already do that job.
- **Teach by building, never option-tours.** Feature guides are build-a-real-flow
  guides. **One job per How-To**, with a task-shaped title short enough not to
  wrap.
- **No internal jargon or implementation asides** — including "under the hood"
  notes that re-expose what an API hides. State what a thing **is**, not what it
  isn't; the rationale for a limitation belongs in git, not on the page.
- **In examples:** `theme=` (not `themename=`), curated 2.x theme names (not
  legacy Bootswatch), spaces in multi-token `bootstyle` values (`"primary
  outline"`, except `inverse-<color>`), `ttkb <command>` for CLI invocations, and
  **no backslash line-continuations** — assign to a variable and reuse.
- **Don't `/`-join items in a table cell** — one per line via an rST line block
  (prose slashes are fine). A line block inside a list-table cell needs a **blank
  line before it**.
- **Every snippet is run headlessly before it ships**, and a code block must be
  runnable on its own — a block that ends by using a name it never bound is a
  defect, even when it reads as a continuation of the block above.

**Three rST defect classes `-W` does not flag** — a clean build is not evidence
the markup parsed:

1. Nested inline markup inside `**bold**` leaks literal backticks.
2. A line block inside a list-table cell without a preceding blank line leaks a
   literal `|`.
3. **An inline-literal start-string not preceded by whitespace never parses.**
   Two rST literals joined by `..` ship raw backticks to the page, because rST
   only begins inline markup after whitespace or an opener (`(` `[` `<` `-` `:`)
   and `.` is not one. The *closing* backticks are fine, so the line renders
   half-correct.

**The cheap catch-all for all three:** strip tags from every built page and
search the body text for surviving double backticks.

## Conventions

- Match the style of the file you're editing (comment density, naming).
- **Public-name casing (2.0 standardization):** ttkbootstrap-authored identifiers
  (functions, methods, new kwargs) use `snake_case` (`apply_icon`, `icon_size`,
  `high_dpi`, `window_type`); names that pass through to a real Tk/ttk option or
  method keep Tk's spelling verbatim (`iconphoto`, `minsize`/`maxsize`, `compound`,
  `themename`); `bootstyle`/`autostyle` are grandfathered brand tokens, not a
  template for new names. Test: "am I forwarding a real Tk name?" — yes → Tk
  spelling; no → snake_case.
- Custom widgets that need image assets generate them through the style
  builder / Pillow pipeline; favor native ttk/clam mechanisms over images
  where both are viable (perf and cross-platform consistency).
- Commit messages: imperative subject; reference the issue (`fixes #NNNN`)
  where applicable.
- Branch + PR per change. **Work targets `master`**; 1.x maintenance, if any,
  targets **`release/v1`**.
- **Set a milestone on every issue AND every PR** — not just issues. The
  milestone is the single source of truth for "which release is this in"
  ([[feedback_no_version_labels]] is the other half: no `Version x` labels), and
  it is only as good as its coverage. Most 2.1 PRs went unmilestoned, so
  `gh pr list --search "milestone:2.1"` returned 17 when 19 code changes had
  shipped — the milestone stopped being usable for exactly the question it
  exists to answer, and reconstructing the release required diffing merged PR
  numbers against the change log by hand. Set it when you open the PR;
  `gh pr edit <n> --milestone "2.1"` after the fact works but is easy to forget.

### Working with git here

Each of these cost real rework at least once.

- **Verify `git branch --show-current` before pushing.** A
  `checkout -b … || checkout …` fallback once left commits on a second branch
  while `git push origin <name>` pushed a different ref — a PR merged without the
  work reported in it.
- **`git merge-tree | grep '^<<<<<<<'` is not a conflict check** on modern git
  (it reported 0 conflicts for two branches that then conflicted). Do a
  **throwaway trial merge**. It is also the only way to gate the *combined*
  result of two PRs, which neither PR's own CI covers.
- **A branch showing large deletions in `git diff master..<branch>` is behind**,
  not carrying removals.
- **GitHub may squash-merge**, so the merge commit is a new SHA and
  `git branch -d` reports "not fully merged". `git cherry master <branch>`
  matches by patch-id and still reports 0 for a squash whose content landed — a
  non-zero count means *look*, not *unmerged*. Don't assume the squash behavior
  either: some merges here are real merge commits.
- **`git reset --hard` discards uncommitted WIP, including the author's.** Being
  careful not to *commit* someone's WIP is not the same as not *destroying* it —
  stash first, or use a plain `git reset`, when the tree is dirty.
- **"Push" is not "merge."** Push the branch; merging is a separate decision.
- **A commit pushed to a PR branch after the PR merged does not land** — verify
  the merge SHA includes your latest push.
- **The author keeps live WIP in the working tree.** Leave modified files you did
  not touch alone.

### Reviews

- **A review finding is a hypothesis with a reproduction attached, not a
  verdict.** The reproduction proves the *defect*; it does not make the proposed
  *fix* right. Probe the recommendation against real data before implementing it
  — one confident finding here reasoned from the PR's own test fixture and would
  have washed out selection backgrounds across every converted theme.
- **A careful self-review has missed real defects in every round so far**, and
  several were the artifact being *wrong* rather than merely narrow. Budget for
  the review; don't treat it as a formality.
- **Type-checking cannot see a bad tooltip**, and a passing test cannot see a
  filtering constructor. Probe the thing a user actually experiences.

### Writing for people

- **Release notes, PR bodies and issue comments go unwrapped** so the web
  reflows them; repo source docs keep their wrapped convention.
- **Unwrapped is not unstructured** — notes need real section headings and bullet
  lists. Folding a *wrapped* change log into them means rewriting each paragraph
  as one long line, never pasting it through.
