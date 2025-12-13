---
icon: fontawesome/solid/download
---

# Installation

ttkbootstrap 2 installs on Python 3.10+ interpreters that include Tk (standard in most desktop distributions). This page shows the recommended commands plus notes about optional extras and compatibility.

## Supported platforms

- Windows 10/11 (Tk ships with official Python installers).
- macOS (use the official Python installer or Homebrew).
- Linux desktops (Tk is available via system packages like `python3-tk` or `tk-dev`).

## Installing with pip

Before installing, confirm your interpreter meets the minimum requirement:

```bash
python --version
```

If the version is lower than 3.10, upgrade your interpreter or use a pyenv/virtual environment before proceeding.

```bash
python -m pip install ttkbootstrap
```

For quicker installs, pin the version or use `pipx` to isolate the CLI tools:

```bash
python -m pip install ttkbootstrap==2.0.0
# or
pipx install ttkbootstrap
```

## Optional dependencies

- **ttkbootstrap[cli]** includes CLI scaffolding helpers for faster projects (`python -m pip install "ttkbootstrap[cli]"`).
- **ttkbootstrap[full]** bundles optional theming utilities if you plan to ship advanced palettes or custom fonts.

## Verification

Run `python -m ttkbootstrap --version` to ensure the CLI is on your path, or import the package interactively:

```python
>>> import ttkbootstrap
>>> ttkbootstrap.__version__
'2.0.0'
```

If you see errors about missing `_tkinter`, install your system’s Tk dependencies (e.g., `sudo apt install python3-tk` on Ubuntu).
