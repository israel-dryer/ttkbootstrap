---
title: Installation
---

# Installation

ttkbootstrap is a **framework** for building Tkinter applications with a modern design system and convenience APIs
(reactive state, icons, layout containers, localization, and more).

It runs anywhere Tk runs — Windows, macOS, and Linux — and installs like any other Python package.

---

## Requirements

- **Python 3.10 or newer**

- **Tk / Tcl**

  Tkinter ships with most Python distributions, but some minimal Linux installs omit Tk.

!!! tip "On Linux, install Tk if Tkinter is missing"
    - Debian/Ubuntu: `sudo apt-get install python3-tk`
    - Fedora: `sudo dnf install python3-tkinter`
    - Arch: `sudo pacman -S tk`

---

## Install with pip

```bash
python -m pip install ttkbootstrap
```

If you’re upgrading:

```bash
python -m pip install --upgrade ttkbootstrap
```

---

## Verify your installation

Create a quick smoke test:

```python
import ttkbootstrap as ttk

app = ttk.App()
ttk.Label(app, text="Hello ttkbootstrap").pack(padx=20, pady=20)
app.mainloop()
```

If a window appears, you’re ready.

!!! link "Next: follow the [Quick Start](quick-start.md) to build your first small app."

---

## Included image support (Pillow)

ttkbootstrap includes Pillow as a dependency to support modern image workflows, including
theme-aware icons, DPI scaling, caching, and recoloring.

No additional installation is required.

!!! link "See [Icons & Imagery](../capabilities/icons-and-imagery.md) for details on image handling and icon behavior."

---

## Optional: Command-line tooling

ttkbootstrap includes an optional CLI that can scaffold projects, add views or dialogs, and help with
building and distribution.

You do **not** need the CLI to use ttkbootstrap, but it can simplify larger projects.

!!! link "See [Platform → CLI](../platform/cli.md) for available commands."

---

## Troubleshooting

### `_tkinter` / Tk not found

If you see errors like:

- `ModuleNotFoundError: No module named '_tkinter'`
- `TclError: ...`

then Tk is not installed or not visible to your Python interpreter.

Common fixes:

- **Windows**: reinstall Python using the official installer and ensure Tcl/Tk is selected.
- **macOS**: use the official Python installer from python.org or a distribution that bundles Tk support.
- **Linux**: install the Tk package for your distro (see the Linux tip above).

### Virtual environments

If Tk works in system Python but not in a venv, ensure:

- the venv was created from an interpreter that has Tk support.

---

## Next steps

- [Quick Start](quick-start.md) — build a minimal app
- [Guides](../guides/index.md) — recommended patterns and workflows
- [Widgets](../widgets/index.md) — available UI components
- [Platform](../platform/index.md) — Tk/ttk foundations (optional)
- [Capabilities](../capabilities/index.md) — framework features like signals and localization
