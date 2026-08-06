# 2.2 changes

Scope: changes relative to **2.1.1**. Log entries here as they land, not at
release time.

---

## Added

### `python -m ttkbootstrap.convert_theme` — carry a 1.x custom theme forward

A custom theme saved by ttkbootstrap 1.x now converts to the 2.x
`Theme(...).register()` form with one command:

```bash
python -m ttkbootstrap.convert_theme user.py -o brand.py
```

It reads any input a 1.x user could be holding — ttkcreator had three save
paths, and each one's artifact converts:

- a **`user.py`** containing a `USER_THEMES` dict — what 1.x ttkcreator's
  **Export** button produced (it copied the in-package `themes/user.py`);
- a **`.py`** holding a `ThemeDefinition(...)` call — what its **Export theme
  definition** wrote, and the one most likely to be sitting in a user's own
  project, since the other two live inside the installed package;
- a **JSON** file in the `Style.load_user_themes` format.

Every theme in the file converts, under a single `import`. Output goes to
standard output, or to `-o <file>`.

**What carries over:** the five accent anchors, the optional `secondary`, and
the theme's `background`/`foreground`.

**What does not, deliberately:**

- The plumbing colors — `border`, `inputbg`, `inputfg`, `selectbg`, `selectfg`,
  `active` — are dropped, because `Theme` derives all six from the anchors and
  the surface. (Not the same as `theme_from_legacy_dict`, which the built-in
  legacy themes go through: that one regenerates only `border`, `inputbg` and
  `active`, and passes the other three verbatim.)
- The `light` and `dark` accents, because 2.x derives that pair from the
  `neutral` ramp. A converted theme takes the default gray; `Theme(neutral=...)`
  tunes it. Note `neutral` is the ramp *base*, not the pale `light` accent —
  1.x's near-white `light` corresponds to ramp step `[100]`, so passing it
  through as `neutral` would wash out `selectbg` and an uncolored `secondary`
  along with it.
- The opposite mode. A 1.x theme declares one mode, so the generated family
  declares that one and leaves the other commented out rather than inventing
  colors for it.

Converted output is close but not pixel-identical: an accent is re-derived per
mode for contrast, so a dark theme's authored `#6a5acd` resolves to `#887bd7`.

The module is pure text transformation — no Tk, no display, importable and
runnable headlessly. `tests/test_convert_theme.py` (+23) covers all three input
formats, the loud-failure paths, the escaping of what it emits, and an
end-to-end check that the emitted Python actually registers a theme and styles
real widgets.

### `ttkbootstrap.__version__`

`import ttkbootstrap; ttkbootstrap.__version__` raised `AttributeError` — it had
never existed, in any release. It now reports the installed distribution's
version, read from the package metadata so `pyproject.toml` stays the one place
the literal lives. The consequence of reading metadata is that it reports what
was *installed*: an editable install keeps whatever metadata it was built with
until it is reinstalled.

It is also declared in the type stub. A `.pyi` replaces the module for type
checkers, and the stub's re-export pass sources every name from an import
statement in `__init__.py`; `__version__` is an assignment, so without an
explicit declaration `ttk.__version__` was an attribute error under pyright even
though it worked at runtime.

### The `ttkb` command line

Installing ttkbootstrap now installs a command — under two names, `ttkb` and
`ttkbootstrap`, that run the same thing:

| Command | What it does |
| --- | --- |
| `ttkb version` | Print the installed version |
| `ttkb demo` | Open the widget demo (was `python -m ttkbootstrap`) |
| `ttkb convert-theme <file>` | Convert a 1.x theme file (was `python -m ttkbootstrap.convert_theme`) |
| `ttkb creator` | Open ttkcreator (was `python -m ttkcreator`) |

Each of those already existed as its own `python -m` invocation, which nothing
surfaced; every `python -m` spelling still works, and is what to use when the
scripts directory is not on `PATH`. The converter's arguments are defined once
and shared by both spellings, so they cannot drift apart. New
`docs/reference/cli.rst`; `tests/test_cli_api.py` (+12).

### Registering a theme before the app exists

`Theme(...).register()` raised `RuntimeError: No Style instance yet` unless an
`App` was already running — but a theme is declared at the top of a file, which
is exactly where no app exists. Worse, it made the theme unusable as an
`App(theme=...)` argument: registration needed the app, and the app needed the
name. It now queues on the existing deferred-config seam (the one
`set_default_button` uses) and registers when the root comes up, which is early
enough for `App(theme="brand-light")` to select it. Registering with an app
already running still applies immediately.

```python
import ttkbootstrap as ttk
import brand                       # a converted theme module

app = ttk.App(theme="acme-light")  # selectable straight away
```

The theme is still *validated* at the `register()` call, so a missing anchor
raises where it is written rather than later out of a window constructor.
`install_legacy_themes()` gained the same treatment, and keeps warning from the
call site whether or not the work is deferred.

## Testing

- **The suite is density-independent** (#1322). Four asset-geometry tests assert
  exact unscaled pixel sizes, so they passed only where the scaling factor was
  exactly 1.0 — a contributor on Windows at 125% (the factory default on most
  laptops) got four one-pixel failures on a clean checkout. The shared root is
  now pinned to standard density in `tests/conftest.py`, rather than four
  assertions being patched: that covers any other test carrying the same latent
  assumption, and demotes CI's `-dpi 96` from load-bearing to belt-and-braces.
  Verified by simulating 1.0, 1.4, 1.6667 and 2.0 — the whole suite passes at
  every one, and the four failures reproduce exactly as filed with the pin
  removed. `test_test_root_runs_at_baseline_density` pins the invariant.

## Documentation

- **Reference › Command line** is a new page: the four subcommands, what each
  one replaces, and the two-names/`python -m` note.
- **Installation** and **Theming & Colors** now reach the demo and ttkcreator
  through `ttkb demo` / `ttkb creator`; the converter is `ttkb convert-theme`
  everywhere.
- **Theming & Colors** and **Migrating to 2.0** no longer say a theme must be
  registered after the `App` exists — they show the top-of-file form.
- The **icons** guide and the README now point at
  [tkinter-icons](https://github.com/israel-dryer/tkinter-icons), the extension's
  current name (it was `ttkbootstrap-icons`).
- **Migrating to 2.0** gained *Saved themes move into your code*: the
  `themes/user.py` store and ttkcreator's Import/Export buttons are gone, the
  converter command, what carries over vs. what 2.x regenerates, and a note
  that `Style.load_user_themes` still reads the 1.x JSON (thinner — verbatim
  plumbing, single mode, nothing for `toggle_theme()` to flip to).
  This removal shipped in 2.0 but was never written down; the gap is what
  prompted the converter.
- **Theming & Colors** gained a *Coming from 1.x* annotation under the visual
  editor pointing at the converter.
- **Reference › Theming** gained a *Converting a 1.x theme* section.
- `Style.load_user_themes` had a one-line docstring (`"Load user themes saved
  in json format"`) that never stated the file format; it now specifies the
  JSON shape, the verbatim-colors/single-mode behavior, and points at the
  converter.
- **Reference › Scrollbar** — `set()`'s description shipped raw double backticks
  to the rendered page. In ``` ``first``..``last`` ``` the second literal's
  start-string is not preceded by whitespace, and rST only begins inline markup
  after whitespace or an opener (`.` is not one), so it never parsed. A clean
  `-W` build does not flag this class of defect.
