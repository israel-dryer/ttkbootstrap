# CLAUDE.md

Guidance for working in the ttkbootstrap repository.

## What this is

ttkbootstrap is a theming extension for tkinter/ttk: it generates modern,
flat, Bootstrap-inspired themes on demand and adds a `bootstyle` keyword
API to ttk widgets. Pure Python; the only runtime dependency is Pillow
(used for image-based widget assets). Public API entry point is
`src/ttkbootstrap/__init__.py`, typically imported as `import ttkbootstrap as ttk`.

- Package version / metadata: `pyproject.toml` (src layout, `requires-python >=3.10`).
- Docs site: mkdocs (`mkdocs.yml`, `docs/`), published to readthedocs.

## Direction: 2.0 cleanup (read before large changes)

The active initiative is a **2.0 cleanup/consolidation release — no new
features.** Goals: remove cruft, standardize/normalize the API (aggressive/
breaking is OK when meaningful, paired with a migration path), fix memory leaks
and theme-switch perf, make user-defined custom styles easy, and overhaul the
docs. ttkbootstrap stays a **styling extension for vanilla tkinter** — not a
widget library (the forward-looking framework is a separate project, bootstack).

The full worklist (locked decisions + workstreams) lives in
**`development/2_0_plan.md` on the `docs/2.0-plan` branch.** Headlines: mixin-
hybrid API (replace the import-time monkey-patch), single canonical `bootstyle`
string (no tuple/list/alt-order), semantic-anchor theme model, deterministic
version-stamped theme walk + image-cache cleanup (mechanisms borrowed from
bootstack, not its API), and a centralized `_compat.py` quarantine for all
legacy normalization + deprecation warnings. Consult that doc before starting
2.0 work.

## Repository layout

```
src/ttkbootstrap/
  __init__.py        # public exports; re-exports ttk widgets + TYPE_CHECKING stubs that
                     #   advertise the `bootstyle`/`autostyle` kwargs. Calls
                     #   Bootstyle.setup_ttkbootstrap_api() at import to install overrides.
  style.py           # THE CORE — theme/style engine (see below). Largest, most important file.
  window.py          # Window / Toplevel classes
  constants.py       # re-exported constants (PRIMARY, SUCCESS, BOTH, YES, ...) via `from ...constants import *`
  colorutils.py      # color math (Colors helpers, make_transparent, contrast)
  themes/standard.py # STANDARD_THEMES dict: every built-in theme's color definitions
  themes/user.py     # user-defined themes
  widgets/           # CANONICAL custom widgets: dateentry, meter, floodgauge, tableview,
                     #   scrolled, tooltip, toast, labeledscale
  dialogs/           # Messagebox, Querybox, colorchooser, datepicker, fontdialog, etc.
  localization/      # msgcat-based i18n (msgs.py holds translations)
tests/               # mostly INTERACTIVE demo scripts (run by hand, call mainloop);
                     #   a few headless test_*.py use a withdrawn root and assert
docs/, gallery/, cookbook/   # documentation and examples
```

### Deprecated module shims (important)

Several top-level modules are thin deprecation shims that re-export from
`widgets/` and emit a `DeprecationWarning`:
`ttkbootstrap.scrolled`, `ttkbootstrap.tableview`, `ttkbootstrap.toast`,
`ttkbootstrap.tooltip` (~14 lines each). **Edit the real implementation in
`src/ttkbootstrap/widgets/`**, not the shim. New code should import from
`ttkbootstrap.widgets.<name>`.

## The style engine (`style.py`)

Everything visual flows through here. Key classes:

- **`Style`** — singleton (`Style.get_instance()`), subclasses `ttk.Style`.
  Owns theme definitions, the active theme, and the style registry
  (`_style_registry`, `_theme_styles`). `theme_use()` switches themes and
  rebuilds every registered style.
- **`StyleBuilderTTK`** — holds `create_*_style(colorname)` methods (e.g.
  `create_button_style`, `create_outline_toolbutton_style`). These build a
  ttk style and call `_register_ttkstyle()`.
- **`StyleBuilderTK`** — styles legacy `tk.*` widgets (Menu, Text, Canvas, …).
- **`Bootstyle`** — installs the API: overrides ttk widget `__init__` /
  `configure` / `__setitem__` so `bootstyle=`/`style=` resolve to a built
  ttk style via `update_ttk_widget_style()`.

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

- **`Style` is a process-wide singleton tied to one Tk root.** Creating a
  second `ttk.Window`/root in the same process is unsupported and produces
  wrong results (e.g. styles not tracking theme changes). Tests must use a
  single root — see `tests/widget_styles/test_default_button_style.py`.
- **Themes are clam-derived** (`theme_create(name, TTK_CLAM)`). An unstyled
  base ttk style shows clam's default appearance until ttkbootstrap configures it.

## Dev environment & commands

A virtualenv with an editable install lives at `.venv-home/`
(`.venv-home/Scripts/python.exe`). The package is also importable by running
with `PYTHONPATH=src`.

- Run a headless test (script form):
  `PYTHONPATH=src .venv-home/Scripts/python.exe tests/widget_styles/test_default_button_style.py`
- pytest is **not** installed in the env by default. Tests under `tests/` that
  begin with `test_` and use `def test_*()` + `assert` are pytest-compatible;
  the rest are interactive demos that call `mainloop()` and require a display.
- Build docs: `mkdocs serve` (deps in `requirements.txt`).

### Writing tests

Prefer headless tests: create one `ttk.Window`, call `app.withdraw()`, assert,
then `app.destroy()` in a `finally`. Make the file runnable both via pytest and
as a `python <file>` script (a `if __name__ == "__main__":` block that calls the
test functions). Query a built style's value with
`app.tk.call("ttk::style", "lookup", "<Style>", "-<option>")`.

## Conventions

- Match the style of the file you're editing (comment density, naming).
- Custom widgets that need image assets generate them through the style
  builder / Pillow pipeline; favor native ttk/clam mechanisms over images
  where both are viable (perf and cross-platform consistency).
- Commit messages: imperative subject; reference the issue (`fixes #NNNN`)
  where applicable.
- Branch + PR per change (default branch is `master`).