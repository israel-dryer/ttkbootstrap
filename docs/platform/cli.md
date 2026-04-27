---
title: Command Line Interface
---

# Command Line Interface (`ttkb`)

The `ttkb` command-line interface is an **optional productivity tool** that
helps you scaffold, develop, diagnose, and distribute ttkbootstrap
applications. You can use ttkbootstrap with or without it — the CLI exists to
reduce boilerplate, encourage a consistent project layout, and provide a
smooth path from prototype to distributable application.

---

## When to use the CLI

The CLI is most useful when:

- starting a new application
- maintaining a consistent project layout
- adding views, pages, or dialogs incrementally
- preparing an app for [distribution](build-and-ship.md)
- diagnosing project or environment issues

For one-off scripts or experiments, manual setup may be simpler.

---

## Top-level options

```
ttkb [--version] [--verbose] <command> [args]
```

| Option | Description |
|---|---|
| `--version` | Print the installed `ttkbootstrap` version and exit |
| `-v`, `--verbose` | Print full Python tracebacks on error (default: one-line message) |
| `-h`, `--help` | Show help; works on every subcommand too (e.g. `ttkb add --help`) |

---

## Commands

### `ttkb start`

Scaffold a new project.

```
ttkb start <name> [--template basic|appshell] [--theme <name>]
                   [--container grid|pack] [--simple] [--dir <path>]
```

| Option | Default | Description |
|---|---|---|
| `--template` | `basic` | `basic` for a single-view `App`, `appshell` for an `AppShell` with sidebar nav |
| `--theme` | `cosmo` | Starting theme — see `ttkb list themes` |
| `--container` | `grid` | `grid` or `pack` (the geometry manager used by the generated view; ignored for `appshell`) |
| `--simple` | off | Skip the `assets/` directory and `README.md` |
| `--dir` | `./<name_lowercased>` | Target directory |

The two templates produce different layouts:

```
# basic                              # appshell
my_app/                               my_app/
├── src/my_app/                       ├── src/my_app/
│   ├── __init__.py                   │   ├── __init__.py
│   ├── main.py                       │   ├── main.py
│   └── views/                        │   └── pages/
│       ├── __init__.py               │       ├── __init__.py
│       └── main_view.py              │       ├── home_page.py
├── assets/                           │       └── settings_page.py
├── ttkb.toml                         ├── assets/
└── README.md                         ├── ttkb.toml
                                      └── README.md
```

The chosen template is recorded in `ttkb.toml` as `[app].template` so other
commands (like `ttkb add page` and `ttkb add view`) know which scaffolds are
appropriate.

---

### `ttkb run`

Run the application defined in `ttkb.toml`, or a specific Python file.

```
ttkb run [path]
```

- With no argument, walks up from the current directory until it finds a
  `ttkb.toml`, then runs `[app].entry`.
- With a directory, looks for `ttkb.toml` there.
- With a `.py` file, runs that file directly.

`ttkb run` adds `<project>/src` to `PYTHONPATH` and exports `TTKB_THEME` from
`[settings].theme` so generated `main.py` files can pick the configured theme
without hard-coding it.

---

### `ttkb add`

Scaffold components inside an existing project.

```
ttkb add page <ClassName>      [--scrollable] [--dir <path>]   # appshell only
ttkb add view <ClassName>      [--container grid|pack] [--dir <path>]   # basic only
ttkb add dialog <ClassName>    [--dir <path>]
ttkb add theme <name>          [--mode light|dark]
ttkb add i18n                  [--languages <lang> ...]
```

`add page` and `add view` are gated by `[app].template` — running the wrong
one in the wrong project type prints a clear error directing you to the
other.

#### `ttkb add page`

Scaffolds a class-based page module under `src/<module>/pages/`. The command
**only creates the file** — it does *not* modify `main.py`. After scaffolding
it prints the three lines you need to paste in to register the page with the
sidebar:

```
from <module>.pages.dashboard_page import DashboardPage
page = shell.add_page("dashboard", text="Dashboard", icon="speedometer2")
DashboardPage(page)
```

`--scrollable` adjusts the printed hint so the suggested `add_page()` call
includes `scrollable=True`.

#### `ttkb add theme`

Writes `themes/<name>.json` using the v2 theme schema (`mode`, `shades`,
`semantic`, top-level `foreground`/`background`). To use the theme:

```python
from ttkbootstrap.style.theme_provider import register_user_theme

register_user_theme("mytheme", "themes/mytheme.json")
app = ttk.App(theme="mytheme")
```

#### `ttkb add i18n`

Creates `locales/<lang>/LC_MESSAGES/messages.po` files for each language
listed in `--languages` (defaults to `en`). Compile them with `msgfmt` before
shipping.

---

### `ttkb list`

Discover resources known to the framework.

```
ttkb list themes
```

Prints a table of every theme bundled with `ttkbootstrap` (canonical and
legacy), including its display name and mode. Useful for picking a value to
pass to `ttkb start --theme` or to set in `[settings].theme`.

---

### `ttkb promote --pyinstaller`

Add packaging support to an existing project.

```
ttkb promote --pyinstaller [--force]
```

This step:

1. Adds a `[build]` section to `ttkb.toml` (backend, windowed/console mode,
   onefile vs. onedir, icon path, asset-include patterns).
2. Generates `build/pyinstaller/app.spec` — a PyInstaller spec file that
   reads `ttkb.toml` at build time.

If PyInstaller isn't installed in the current interpreter, `promote` prints a
note pointing at `pip install pyinstaller`. The promote step itself only
writes config — it doesn't need PyInstaller to run.

`--force` overwrites existing build configuration.

---

### `ttkb build`

Build the application.

```
ttkb build [--clean]
```

Runs PyInstaller against the spec generated by `promote`. `--clean` wipes
`dist/` and the PyInstaller work directory first.

The default Windows launch icon (visible in Explorer and on the taskbar) is
the bundled `ttkbootstrap` icon. To override it, set `[build.icon].path` in
`ttkb.toml` to a `.ico` (Windows) or `.icns` (macOS) file.

!!! note "macOS distribution"
    `ttkb build` produces a `.app` bundle on macOS, but it is **not yet
    distributable** — modern macOS requires code-signing, notarization, and
    stapling, none of which `ttkb build` performs. See
    [Build & Ship → Shipping to macOS](build-and-ship.md#shipping-to-macos)
    for the recommended Briefcase handoff.

---

### `ttkb doctor`

Diagnose project and environment health.

```
ttkb doctor
```

Reports:

- Python and Tcl/Tk versions
- ttkbootstrap version
- Whether `ttkb.toml` exists and parses
- Whether the entry point file exists
- Whether the directory layout matches `[app].template` (`pages/` for
  appshell, `views/` for basic)
- PyInstaller availability (always — even before `promote`, so users know
  whether they have a `pip install` ahead of them)

Returns exit code 1 if any checks fail; warnings (e.g. PyInstaller not
installed) never fail the command.

---

### `ttkb demo`

Launch the AppShell-based widget gallery.

```
ttkb demo
```

Useful for browsing every widget category, trying themes, and seeing example
spec values for buttons, forms, tables, and dialogs.

---

## Configuration: `ttkb.toml`

When present, the CLI reads configuration from `ttkb.toml` at the project
root. The default layout produced by `ttkb start`:

```toml
[app]
name = "MyApp"
id = "com.example.myapp"
entry = "src/myapp/main.py"
template = "basic"           # or "appshell"

[settings]
theme = "cosmo"
language = "en"
appearance = "system"        # system | light | dark

[layout]
default_container = "grid"   # grid | pack

# Added by `ttkb promote --pyinstaller`:
[build]
backend = "pyinstaller"
windowed = true
onefile = false

[build.icon]
# path = "assets/icon.ico"

[build.datas]
include = ["assets/**", "locales/**", "themes/**", "ttkb.toml"]
```

If no `ttkb.toml` exists, the CLI uses defaults and your application code
remains authoritative at runtime via `AppSettings`.

!!! link "See [Guides → App Settings](../guides/app-settings.md) for the runtime configuration model."

---

## What the CLI is not

- **Not required** to use ttkbootstrap.
- **Not a runtime dependency** — your built application doesn't import the
  CLI.
- **Not a replacement** for learning the framework. Everything the CLI
  generates is plain Python you can read, modify, or replace.

If you prefer a fully manual setup, you can ignore the CLI entirely.

---

## Next steps

- [Quick Start](../getting-started/quick-start.md) — build your first app
- [Project Structure](project-structure.md) — file organization and packaging
- [Build & Ship](build-and-ship.md) — distribution workflow
- [App Settings](../guides/app-settings.md) — runtime configuration
