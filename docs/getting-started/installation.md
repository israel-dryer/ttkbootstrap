---
icon: fontawesome/solid/download
---

# Installation

ttkbootstrap 2 targets Python 3.10 and newer interpreters that already include Tk (8.6 or later). This page walks through the platform notes, pip commands, optional extras, and verification steps you need for a repeatable install.

![Installation hero](https://placehold.co/800x800/FFFFFF/333333.webp?text=Installation&font=lato)

## Requirements

- **Python 3.10+**: Run `python --version` to confirm and upgrade the interpreter if it reports an earlier release.
- **Tk support**: Most official installers already ship Tk. On Linux, install the system package (`python3-tk`, `tk-dev`, etc.) before the first launch.
- **Up-to-date pip**: Keep wheels current via `python -m pip install --upgrade pip` so the install pulls prebuilt binaries.

## Installing with pip

```bash
python -m pip install ttkbootstrap
```

Pin a release (`ttkbootstrap==2.0.0`) or use `pipx install ttkbootstrap` to isolate the CLI helpers while leaving other environments untouched.

## Optional extras

- `ttkbootstrap[cli]` bundles project generators, linting helpers, and template scaffolding.
- `ttkbootstrap[full]` adds advanced theming utilities, palette assets, and extended typography controls.
- Combine extras as needed: `python -m pip install "ttkbootstrap[cli,full]"`.

## Verify the install

```python
>>> import ttkbootstrap
>>> ttkbootstrap.__version__
'2.0.0'
```

Or run `python -m ttkbootstrap --version` to ensure the CLI tools are on your PATH.

## Troubleshooting

- **Missing `_tkinter`**: Install the relevant Tk package (for example, `sudo apt install python3-tk` on Debian/Ubuntu or `brew install tcl-tk` on macOS) before rerunning the pip install.
- **Virtual environments**: Activate the venv before installing so Tk and the package bind to the correct interpreter.
- **Permission errors**: Use `--user` or a virtual environment instead of a system-wide install when permissions are restricted.
