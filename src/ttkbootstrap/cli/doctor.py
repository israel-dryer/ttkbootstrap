"""ttkb doctor command - Validate project structure and environment."""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

from ttkbootstrap.cli.config import TtkbConfig, find_config


_OK = "  [OK]   "
_WARN = "  [WARN] "
_FAIL = "  [FAIL] "


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'doctor' subcommand parser."""
    parser = subparsers.add_parser(
        "doctor",
        help="Diagnose project and environment health",
        description=(
            "Validate ttkb.toml, check the project layout, and report "
            "environment versions relevant to building and running."
        ),
    )
    parser.set_defaults(func=run_doctor)


def run_doctor(args: argparse.Namespace) -> None:
    """Run the diagnostic checks."""
    failures = 0
    warnings = 0

    # ---- Environment -------------------------------------------------------
    print("Environment:")
    print(f"{_OK}Python {platform.python_version()} ({sys.executable})")

    tk_version, tk_error = _probe_tk()
    if tk_version:
        print(f"{_OK}Tcl/Tk {tk_version}")
    else:
        print(f"{_FAIL}Tcl/Tk: {tk_error}")
        failures += 1

    ttkb_version = _probe_ttkbootstrap()
    print(f"{_OK}ttkbootstrap {ttkb_version}")

    print()

    # ---- Project -----------------------------------------------------------
    config_path = find_config()
    if config_path is None:
        print("Project:")
        print(f"{_WARN}No ttkb.toml found in current directory or parents.")
        print("         (Run 'ttkb start <name>' to create a project, or 'cd' into one.)")
        return

    project_root = config_path.parent
    print(f"Project: {project_root}")

    try:
        config = TtkbConfig.load(config_path)
    except Exception as e:
        print(f"{_FAIL}ttkb.toml failed to parse: {e}")
        sys.exit(1)
    print(f"{_OK}ttkb.toml parses ([app] name={config.app.name!r}, template={config.app.template!r})")

    # Entry point exists
    entry_path = project_root / config.app.entry
    if entry_path.exists():
        print(f"{_OK}entry point: {config.app.entry}")
    else:
        print(f"{_FAIL}entry point missing: {config.app.entry}")
        failures += 1

    # Layout matches template
    if entry_path.parts and "src" in entry_path.parts:
        idx = list(entry_path.parts).index("src")
        if idx + 1 < len(entry_path.parts):
            module_dir = project_root.joinpath(*entry_path.parts[: idx + 2])
            failures += _check_template_layout(config.app.template, module_dir)
    else:
        # Non-src layout: skip the views/pages check
        pass

    # Packaging — always reported. If [build] exists we run the full check;
    # otherwise we still flag a missing PyInstaller as a heads-up so users
    # discover it before they reach 'ttkb build'.
    if config.build is not None:
        warnings += _check_build(config, project_root)
    else:
        warnings += _check_packaging_readiness()

    # ---- Summary -----------------------------------------------------------
    print()
    if failures:
        print(f"{failures} failure(s), {warnings} warning(s).")
        sys.exit(1)
    if warnings:
        print(f"All checks passed with {warnings} warning(s).")
    else:
        print("All checks passed.")


def _check_template_layout(template: str, module_dir: Path) -> int:
    """Verify the project's component directory matches its template type.

    Returns the number of failures recorded.
    """
    expected = "pages" if template == "appshell" else "views"
    other = "views" if template == "appshell" else "pages"

    expected_dir = module_dir / expected
    other_dir = module_dir / other

    failures = 0
    if expected_dir.exists():
        print(f"{_OK}layout: found {expected}/ (matches template={template!r})")
    else:
        print(f"{_FAIL}layout: expected {expected_dir.relative_to(module_dir.parent.parent)}/ for template={template!r}")
        failures += 1

    if other_dir.exists():
        print(f"{_WARN}layout: unexpected {other}/ directory for template={template!r}")
    return failures


def _check_packaging_readiness() -> int:
    """Report packaging-tool availability for un-promoted projects.

    Never fails — just warns if PyInstaller is missing so users know
    they have an install ahead of them before 'ttkb build' will work.
    Returns the number of warnings.
    """
    print()
    print("Packaging (project not yet promoted):")
    try:
        import PyInstaller  # noqa: F401
        print(f"{_OK}PyInstaller is available (run 'ttkb promote --pyinstaller' to enable builds)")
        return 0
    except ImportError:
        print(f"{_WARN}PyInstaller is not installed")
        print("         Install it before 'ttkb build': pip install pyinstaller")
        return 1


def _check_build(config: TtkbConfig, project_root: Path) -> int:
    """Verify build-time prerequisites. Returns the number of warnings."""
    warnings = 0
    backend = config.build.backend if config.build else None
    print()
    print(f"Build (backend={backend!r}):")

    if backend == "pyinstaller":
        spec = project_root / "build" / "pyinstaller" / "app.spec"
        if spec.exists():
            print(f"{_OK}spec file: {spec.relative_to(project_root)}")
        else:
            print(f"{_WARN}spec file missing — run 'ttkb promote --pyinstaller --force'")
            warnings += 1
        try:
            import PyInstaller  # noqa: F401
            print(f"{_OK}PyInstaller is importable")
        except ImportError:
            print(f"{_WARN}PyInstaller is not installed (pip install pyinstaller)")
            warnings += 1
    else:
        print(f"{_WARN}unknown build backend: {backend!r}")
        warnings += 1

    return warnings


def _probe_tk() -> tuple[str | None, str | None]:
    """Return (version, None) on success, (None, error_message) on failure.

    Uses `_tkinter` module constants directly so the probe does not have
    to instantiate a Tk interpreter (ttkbootstrap monkey-patches
    `Tk.__init__` to require an App, which would trip the probe).
    """
    try:
        import _tkinter
        return f"{_tkinter.TCL_VERSION} / Tk {_tkinter.TK_VERSION}", None
    except Exception as e:
        return None, str(e)


def _probe_ttkbootstrap() -> str:
    try:
        import ttkbootstrap
        return getattr(ttkbootstrap, "__version__", "(unknown)")
    except Exception:
        return "(import failed)"
