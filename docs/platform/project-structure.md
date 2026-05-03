---
title: Project Structure
---

# Project Structure

ttkbootstrap is designed to be used as a framework: build views, hold
shared state, ship through PyInstaller. A predictable project layout
makes that path smooth — the `ttkb` CLI scaffolds one for you, but the
underlying structure works just as well if you set it up by hand.

This page covers two things: the canonical CLI-generated layouts (the
default starting point), and the principles that hold whether you use
the CLI or not — `src/` layout, resource resolution, asset packaging,
and PyInstaller-friendly conventions.

For the CLI's commands, see [CLI (`ttkb`)](cli.md). For runtime
configuration, see [Guides → App Settings](../guides/app-settings.md).

---

## CLI-generated layouts

`ttkb start <name>` creates one of two layouts depending on the
`--template` flag:

```
# basic (default)                       # appshell
my_app/                                 my_app/
├── src/my_app/                         ├── src/my_app/
│   ├── __init__.py                     │   ├── __init__.py
│   ├── main.py                         │   ├── main.py
│   └── views/                          │   └── pages/
│       ├── __init__.py                 │       ├── __init__.py
│       └── main_view.py                │       ├── home_page.py
├── assets/                             │       └── settings_page.py
├── ttkb.toml                           ├── assets/
└── README.md                           ├── ttkb.toml
                                        └── README.md
```

The two differ only in the inner organization (`views/` vs `pages/`)
and the entry point `main.py` writes — `basic` builds an `App` with a
single view, `appshell` builds an `AppShell` with sidebar navigation.

Both layouts share three load-bearing properties:

- **`src/` layout** so editable installs and PyInstaller don't pick
  up the project root by accident.
- **`ttkb.toml`** at the root for project-level configuration (theme,
  language, build settings).
- **`assets/` at the root** for application resources (icons, images,
  themes, translations).

The CLI tracks which template you used in `[app].template` so other
commands (`ttkb add page`, `ttkb add view`) know what to scaffold and
where.

---

## Manual layout

If you'd rather not use the CLI, this is a solid starting structure
that supports the same packaging story:

```
my_app/
├── pyproject.toml
├── README.md
├── src/
│   └── my_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py              # App() construction + wiring
│       ├── settings.py         # configuration defaults
│       ├── state.py            # shared signals
│       ├── views/              # screens / page composition
│       │   ├── __init__.py
│       │   └── main_window.py
│       ├── widgets/            # optional: custom composites
│       │   └── __init__.py
│       ├── services/           # optional: IO / data / network
│       │   └── __init__.py
│       └── resources.py        # asset path resolution
├── assets/
│   ├── icons/
│   └── images/
├── i18n/                       # optional translations
│   ├── en.po
│   └── en.mo
├── tests/
└── scripts/
    └── build.py                # optional helper
```

The structure differs from the CLI's only in two ways: it uses
`pyproject.toml` for packaging metadata (which the CLI also generates
when you call `ttkb promote`), and the entry is `python -m my_app`
via `__main__.py` rather than running `main.py` directly. Both work.

See [Guides → App Structure](../guides/app-structure.md) for how the
runtime classes (App, AppShell, AppSettings) wire together inside
this layout.

---

## Entry point conventions

Whether you use `main.py` or `__main__.py`, keep the entry function
small and explicit:

```python
# src/my_app/__main__.py  (or main.py)
from .app import main

if __name__ == "__main__":
    main()
```

```python
# src/my_app/app.py
import ttkbootstrap as ttk

from .settings import settings
from .views.main_window import MainWindow


def main() -> None:
    app = ttk.App(title=settings.title, theme=settings.theme)
    MainWindow(app).pack(fill="both", expand=True)
    app.mainloop()
```

`ttkb run` adds `<project>/src` to `PYTHONPATH` automatically and
exports `TTKB_THEME` from `[settings].theme`, so the CLI-generated
`main.py` can pick up the configured theme without hardcoding it.

---

## `ttkb.toml`

When you scaffold with `ttkb start`, the CLI writes a `ttkb.toml` at
the project root that other CLI commands read:

```toml
[app]
name = "MyApp"
id = "com.example.myapp"
entry = "src/myapp/main.py"
template = "basic"            # or "appshell"

[settings]
theme = "cosmo"
language = "en"
appearance = "system"

[layout]
default_container = "grid"

# Added later by `ttkb promote --pyinstaller`:
[build]
backend = "pyinstaller"
windowed = true
onefile = false

[build.icon]
# path = "assets/icon.ico"

[build.datas]
include = ["assets/**", "locales/**", "themes/**", "ttkb.toml"]
```

`ttkb.toml` is optional. Without it, your application code is
authoritative at runtime via `AppSettings` (see
[Guides → App Settings](../guides/app-settings.md)). With it, you
also get `ttkb run`, `ttkb add page`, `ttkb add theme`, `ttkb build`,
and `ttkb doctor` for free.

---

## Resolving asset paths

Hardcoding paths relative to the working directory breaks under
PyInstaller — the working directory at runtime isn't where you
expect, especially in `--onefile` mode where assets are extracted to
a temporary directory. The cure is a single helper, used everywhere:

```python
# src/my_app/resources.py
from pathlib import Path

def resource_path(*parts: str) -> Path:
    """Return an absolute path to a resource bundled with the package.

    Works in editable installs and in PyInstaller onefile/onedir builds.
    """
    base = Path(__file__).resolve().parent
    return base.joinpath(*parts)
```

```python
from .resources import resource_path

icon_file = resource_path("assets", "icons", "app.png")
```

Two rules to live by:

- Every `open(...)`, `PhotoImage(file=...)`, `Image.open(...)` call
  goes through `resource_path` (or an analogous helper).
- The asset directory (`assets/` at project root, or
  `src/my_app/assets/`) is the *only* place files live. PyInstaller
  needs an explicit list to include them; the more centralized your
  asset dir, the simpler the include pattern.

Where your assets actually live (project root vs inside the package)
depends on whether you used `ttkb start` (root-level `assets/`) or
the manual layout (often `src/my_app/assets/`). Either works as long
as `resource_path` agrees.

---

## Building with the CLI

The recommended path is to use `ttkb build`, which wraps PyInstaller
behind a generated spec file:

```bash
ttkb promote --pyinstaller     # one-time: adds [build] to ttkb.toml
                                #           and generates app.spec
ttkb build                      # rebuilds dist/<AppName>
ttkb build --clean              # wipes dist/ first
```

This path produces a standard PyInstaller bundle (`dist/<AppName>`
on Linux/Windows, `dist/<AppName>.app` on macOS) using the asset-
include patterns from `[build.datas]`. See
[Build & Distribute](build-and-ship.md) for the full build /
sign / package pipeline including macOS notarization and Windows
code signing.

---

## Building with PyInstaller directly

If you'd rather drive PyInstaller yourself — to integrate with an
existing build system, or because your project predates the CLI —
use `--onedir` for early iteration (it's much easier to debug than
`--onefile`) and add explicit `--add-data` entries for every asset
directory:

```bash
# macOS / Linux (use ":" as the path separator)
pyinstaller -n MyApp --onedir --windowed -m my_app \
    --add-data "src/my_app/assets:my_app/assets" \
    --add-data "src/my_app/i18n:my_app/i18n"

# Windows (use ";" as the path separator)
pyinstaller -n MyApp --onedir --windowed -m my_app ^
    --add-data "src/my_app/assets;my_app/assets" ^
    --add-data "src/my_app/i18n;my_app/i18n"
```

A `.spec` file (`MyApp.spec`) generated on first run lets you
version-control the build configuration. Treat it like build-
system code.

When stable, switch to `--onefile` for a single-file distributable.
Make sure every asset access still goes through your
`resource_path` helper — it's the only thing that handles the
onefile temporary-extraction directory cleanly.

---

## PyInstaller-friendly checklist

Whichever path you take, structure the project so packaging stays
boring:

- **One entry point.** `python -m my_app` resolved via
  `__main__.py`, or `main.py` through `ttkb run` / the generated
  spec.
- **All assets inside `assets/`** (or `src/my_app/assets/`).
  PyInstaller needs an explicit include; sprawl makes it fragile.
- **No working-directory paths.** Always go through `resource_path`
  (or its equivalent).
- **No dynamic imports.** PyInstaller's static analysis can't see
  `importlib.import_module(name)` with a runtime-computed name. If
  you must, list the modules in `hiddenimports`.
- **Don't write next to the executable.** Use the platform state
  directory — see [App.state_path](../reference/app/App.md) and
  [Platform Differences → Application state directory](platform-differences.md#application-state-directory).

---

## Next steps

- [CLI (`ttkb`)](cli.md) — every CLI command and option
- [Build & Distribute](build-and-ship.md) — packaging, signing,
  notarization for macOS, Windows, and Linux
- [App Structure](../guides/app-structure.md) — how App, AppShell,
  views, and state fit together
- [App Settings](../guides/app-settings.md) — runtime configuration
  via `AppSettings`
- [Quick Start](../getting-started/quick-start.md) — first app from
  scratch
