---
title: Installation
icon: fontawesome/solid/download
---

# Installation

ttkbootstrap v2 targets **modern Python environments** and builds directly on Tkinter, which is included with most
Python distributions.

This page walks through the requirements, installation options, optional extras, and verification steps so you can
install ttkbootstrap confidently and consistently.

---

## Requirements

Before installing, make sure your environment meets the following requirements:

- **Python 3.10 or newer**  
  Run `python --version` to confirm your interpreter version.

- **Tk support (8.6+)**  
  Most official Python installers already include Tk.  
  On Linux, you may need to install it separately (for example `python3-tk` or `tk-dev`).

- **Updated pip**  
  Keeping pip current helps ensure prebuilt wheels are used when available:

  ```bash
  python -m pip install --upgrade pip
  ```

---

## Installing with pip

The recommended way to install ttkbootstrap is via pip:

```bash
python -m pip install ttkbootstrap
```

You may optionally pin a specific release:

```bash
python -m pip install ttkbootstrap==2.0.0
```

For isolated installs, tools such as `pipx` or virtual environments work well and are fully supported.

---

## Optional Extras

ttkbootstrap provides optional extras that enable additional tooling:

- **CLI tools**  
  Includes project generators and developer utilities:
  ```bash
  python -m pip install ttkbootstrap[cli]
  ```

- **Full feature set**  
  Adds extended theming utilities, palette assets, and typography support:
  ```bash
  python -m pip install ttkbootstrap[full]
  ```

Extras can be combined:

```bash
python -m pip install "ttkbootstrap[cli,full]"
```

These extras are optional and not required for most applications.

---

## Verifying the Installation

After installation, you can verify that ttkbootstrap is available:

```python
>> > import ttkbootstrap
>> > ttkbootstrap.__version__
```

If CLI tools are installed, you can also run:

```bash
python -m ttkbootstrap --version
```

If these commands succeed, your installation is complete.

---

## Platform Notes & Troubleshooting

### Missing `_tkinter`

If you see errors related to `_tkinter`, Tk is not installed or not visible to your Python interpreter.

Common fixes include:

- **Debian / Ubuntu**: `sudo apt install python3-tk`
- **macOS (Homebrew)**: `brew install tcl-tk`
- **Windows**: Reinstall Python using the official installer and ensure Tcl/Tk is selected

After installing Tk, reinstall ttkbootstrap.

---

### Virtual Environments

If you are using a virtual environment:

- activate it before installing,
- ensure it was created using a Python interpreter with Tk support.

---

### Permission Errors

If you encounter permission errors:

- avoid system-wide installs,
- use a virtual environment or the `--user` flag.

---

## Where to Go Next

Once installed, you can:

- Build your **first application** to see ttkbootstrap in action
- Explore available **widgets**
- Learn how themes and styling work in the **Design System**

Installation is intentionally simple so you can focus on building interfaces, not fighting setup.
