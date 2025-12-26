---
title: Project Structure
---

# Project Structure

ttkbootstrap is designed to be used like a **framework**, not a loose collection of widgets.
A good project structure makes it easy to:

- grow from a prototype into a real application
- keep UI code maintainable (views, state, services)
- package reliably with **PyInstaller** (assets, icons, translations)

This guide shows a structure that works well for ttkbootstrap apps and avoids the most common packaging pitfalls.

---

## A practical default layout

This is a solid “start here” structure for most apps:

```
my_app/
  pyproject.toml
  README.md
  src/
    my_app/
      __init__.py
      __main__.py
      app.py                 # App entry + wiring
      settings.py            # AppSettings / configuration defaults
      state.py               # Signals and shared app state
      views/
        __init__.py
        main_window.py       # Top-level UI composition
      widgets/               # Optional: custom composite widgets
        __init__.py
      services/              # Optional: IO, data, network, persistence
        __init__.py
      assets/
        icons/               # App icon files + brand assets
        images/              # App images
      i18n/
        en.po                # Optional: source translations
        en.mo                # Optional: compiled translations
  tests/
  scripts/
    build.py                 # Optional: helper scripts
  build/                     # PyInstaller work dir (ignored)
  dist/                      # PyInstaller output (ignored)
```

Why this works:

- `src/` layout prevents accidental imports from your repo root.
- `app.py` owns framework wiring (theme, settings, menu, app state).
- `views/` is where you compose screens from widgets and containers.
- `assets/` and `i18n/` are *explicit* so packaging can include them reliably.

!!! link "See [Guides → App Structure](../guides/app-structure.md) for how windows, layout, and state fit together."

---

## Entry points

### `__main__.py`

Use `python -m my_app` for development and to give PyInstaller a clear entry.

```python
# src/my_app/__main__.py
from .app import main

if __name__ == "__main__":
    main()
```

---

### `app.py`

Keep `main()` small and explicit.

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

---

## Where ttkbootstrap concepts live

### Settings

Put framework-level defaults in one place.

- theme choice
- localization defaults
- behavior toggles (if you expose them)

```python
# src/my_app/settings.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    title: str = "My App"
    theme: str = "cosmo"

settings = Settings()
```

!!! link "See [Guides → App Settings](../guides/app-settings.md) for using `AppSettings` and framework configuration."

---

### State (signals)

Signals represent shared state and keep UI reactive without tangled callbacks.

```python
# src/my_app/state.py
import ttkbootstrap as ttk

status = ttk.Signal("Ready")
```

!!! link "See [Guides → Reactivity](../guides/reactivity.md) and [Capabilities → Signals](../capabilities/signals/signals.md)."

---

### Views (composition)

Views assemble widgets into real screens. Think “page” or “window content”.

```python
# src/my_app/views/main_window.py
import ttkbootstrap as ttk

class MainWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)

        ttk.Label(self, text="Welcome").pack(anchor="w")
        ttk.Button(self, text="Continue", bootstyle="primary").pack(pady=(12, 0))
```

!!! link "See [Guides → Layout](../guides/layout.md) for recommended containers and structure."

---

## Assets and packaging strategy (PyInstaller)

Packaging is where structure matters most.

### Keep assets in your package

Put images/icons under `src/my_app/assets/...` so they can be included as package data.

At runtime, avoid hardcoding filesystem paths relative to the working directory.

Instead, resolve assets via a single helper (so dev + PyInstaller behave the same).

```python
# src/my_app/resources.py
from __future__ import annotations

from pathlib import Path

def resource_path(*parts: str) -> Path:
    # Works in editable installs and in PyInstaller onefile/onedir builds.
    base = Path(__file__).resolve().parent
    return base.joinpath(*parts)
```

Use it:

```python
from .resources import resource_path

icon_file = resource_path("assets", "icons", "app.png")
```

!!! note
    PyInstaller extraction paths differ between **onefile** and **onedir** builds.
    Keeping all asset access behind `resource_path()` makes this painless later.

---

### Prefer “onedir” during development

For early packaging work, `--onedir` is simpler to debug.

- easy to inspect bundled files
- quicker iteration
- fewer surprises

When stable, you can switch to `--onefile`.

---

## A PyInstaller-friendly build checklist

When you plan to distribute, structure with these in mind:

- **One entry point** (`python -m my_app` / `my_app.__main__`)
- All assets stored under your package (`src/my_app/assets`)
- Localization files in a predictable location (`src/my_app/i18n`)
- No dynamic imports that depend on working directory
- Avoid writing files next to the executable (use user data dirs)

!!! link "See [Build → App Runtime](../build/app-runtime.md) for runtime behavior and distribution patterns."
!!! link "See [Build → App Configuration](../build/app-configuration.md) for configuration and environment-aware settings."

---

## Suggested PyInstaller command (starter)

A minimal starter command (adjust paths for your project):

```bash
pyinstaller -n MyApp --onedir --windowed -m my_app
```

To include assets and translations, you typically add `--add-data` entries, or a `.spec` file.

Example (Windows-style separator shown; on macOS/Linux use `:` instead of `;`):

```bash
pyinstaller -n MyApp --onedir --windowed -m my_app ^
  --add-data "src/my_app/assets;my_app/assets" ^
  --add-data "src/my_app/i18n;my_app/i18n"
```

!!! tip
    If you use a `.spec` file, treat it as part of your build system and keep it in version control.

---

## What about “framework” modules?

As your app grows, you can introduce higher-level organization without changing the basics:

- `views/` → screens and navigation
- `widgets/` → reusable composite widgets
- `services/` → IO and integration points
- `state.py` → shared signals and state
- `settings.py` → AppSettings / defaults

Start simple. Add structure when you feel friction.

---

## Next steps

- [Quick Start](../getting-started/quick-start.md) — build your first app
- [App Structure](../guides/app-structure.md) — windows, layout, and state
- [Layout](../guides/layout.md) — containers and composition
- [CLI](cli.md) — scaffolding and build commands
- [Build & Distribute](build-and-ship.md) — packaging for distribution
