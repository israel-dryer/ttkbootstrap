# CLI Testing Strategy

How to test the `ttkb` CLI without putting generated files into this project.

---

## Recommended: Editable Install in a Separate Virtualenv

This is the fastest iteration loop — change CLI code, immediately test, no reinstall needed.

```bash
# 1. Create a test workspace anywhere OUTSIDE the project
mkdir D:/ttkb-test
cd D:/ttkb-test

# 2. Create a fresh virtual environment
python -m venv .venv

# 3. Activate it
# Windows (cmd):
.venv\Scripts\activate
# Windows (Git Bash / MSYS2):
source .venv/Scripts/activate
# Linux/macOS:
source .venv/bin/activate

# 4. Install ttkbootstrap in editable mode from the dev folder
pip install -e D:/Development/ttkbootstrap

# 5. Test CLI commands
ttkb --version
ttkb start MyApp
cd myapp
ttkb run
ttkb add view SettingsView
ttkb add page Dashboard        # (after implementing)
ttkb promote --pyinstaller
ttkb build
```

### Why editable mode works well

- `pip install -e` creates a symlink — your CLI code changes take effect immediately
- No files are created inside `D:/Development/ttkbootstrap`
- Generated projects land in `D:/ttkb-test/`
- You can blow away `D:/ttkb-test/` anytime and start fresh

### Caveats

- If you add new files/modules to the CLI package, you may need to re-run `pip install -e .`
- If dependencies change in `pyproject.toml`, re-run `pip install -e .`

---

## Alternative: Build a Wheel

Useful for testing the actual install experience (closer to what users get).

```bash
# Build from the project
cd D:/Development/ttkbootstrap
python -m build --wheel

# Install in a separate venv
mkdir D:/ttkb-test && cd D:/ttkb-test
python -m venv .venv
source .venv/Scripts/activate
pip install D:/Development/ttkbootstrap/dist/ttkbootstrap-2.0.0a1-py3-none-any.whl

# Test
ttkb start MyApp
```

### When to use this

- Final smoke test before publishing
- Testing that package data (themes, assets) is bundled correctly
- Verifying the console_scripts entry point resolves

### Downside

- Must rebuild the wheel after every code change

---

## Alternative: Publish to TestPyPI

Useful for testing the full install-from-registry experience.

```bash
# Build
cd D:/Development/ttkbootstrap
python -m build

# Upload to TestPyPI (requires a TestPyPI account + token)
twine upload --repository testpypi dist/*

# Install from TestPyPI in a fresh env
mkdir D:/ttkb-test && cd D:/ttkb-test
python -m venv .venv
source .venv/Scripts/activate
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ttkbootstrap==2.0.0a1
```

### When to use this

- Testing that the package installs correctly from a registry
- Sharing a pre-release with others for feedback
- Verifying metadata (description, classifiers, etc.)

### Downside

- Slowest iteration loop
- Requires TestPyPI credentials
- Dependencies must either be on TestPyPI or you need `--extra-index-url`

---

## Quick Reference

| Method | Iteration Speed | Fidelity | Best For |
|--------|----------------|----------|----------|
| Editable install | Instant | Good | Day-to-day development |
| Wheel install | Rebuild per change | High | Pre-release smoke test |
| TestPyPI | Rebuild + upload | Exact | Sharing with others |

---

## Tips

- **Always `cd` out of the ttkbootstrap project** before running `ttkb start` — otherwise the generated project lands inside the repo.
- **Keep a cleanup script** in your test folder:
  ```bash
  # reset.sh — wipe all generated projects
  cd D:/ttkb-test
  rm -rf myapp/ another_app/ dist/ build/
  ```
- **Test on a clean venv periodically** to catch missing dependencies.
- **Run `ttkb --help` and `ttkb <command> --help`** to verify help text renders correctly after changes.
