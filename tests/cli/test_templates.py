"""Tests for the ttkb CLI templating mechanism.

These tests exercise create_project / create_view / create_page /
create_dialog plus the theme JSON templates. Each generated file is
parsed (Python via ast, TOML via tomllib, JSON via json.loads) so that
broken format strings or schema drift fail loudly.

Tests do NOT execute the generated apps — that would require Tk and is
covered (manually) by the editable-install workflow in
``analysis/cli-testing.md``.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore

from ttkbootstrap.cli.add import (
    _get_dark_theme_template,
    _get_light_theme_template,
)
from ttkbootstrap.cli.config import TtkbConfig
from ttkbootstrap.cli.pyinstaller import SPEC_TEMPLATE, generate_spec
from ttkbootstrap.cli.templates import (
    create_dialog,
    create_page,
    create_project,
    create_view,
)
from ttkbootstrap.style.theme_provider import load_user_defined_theme


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _assert_python_parses(path: Path) -> ast.Module:
    """Parse a .py file with ast and return the module node."""
    src = path.read_text(encoding="utf-8")
    return ast.parse(src, filename=str(path))


def _load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# create_project: basic template
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("container", ["grid", "pack"])
@pytest.mark.parametrize("simple", [False, True])
def test_create_basic_project(tmp_path: Path, container: str, simple: bool) -> None:
    target = tmp_path / "myapp"
    create_project(
        name="MyApp",
        target_dir=target,
        container=container,
        theme="cosmo",
        template="basic",
        simple=simple,
    )

    # Required files
    assert (target / "src" / "myapp" / "main.py").is_file()
    assert (target / "src" / "myapp" / "__init__.py").is_file()
    assert (target / "src" / "myapp" / "views" / "main_view.py").is_file()
    assert (target / "src" / "myapp" / "views" / "__init__.py").is_file()
    assert (target / "ttkb.toml").is_file()

    # Simple flag controls README and assets/
    assert (target / "README.md").is_file() != simple
    assert (target / "assets").is_dir() != simple

    # Generated Python parses
    for py in (target / "src" / "myapp").rglob("*.py"):
        _assert_python_parses(py)

    # ttkb.toml round-trips and carries the right fields
    cfg = _load_toml(target / "ttkb.toml")
    assert cfg["app"]["name"] == "MyApp"
    assert cfg["app"]["template"] == "basic"
    assert cfg["app"]["entry"] == "src/myapp/main.py"
    assert cfg["settings"]["theme"] == "cosmo"
    assert "build" not in cfg  # promote adds it later

    # main.py respects TTKB_THEME (env override path) and references the
    # right view subclass for the chosen container.
    main_src = (target / "src" / "myapp" / "main.py").read_text(encoding="utf-8")
    assert 'os.environ.get("TTKB_THEME", "cosmo")' in main_src
    assert "from myapp.views.main_view import MainView" in main_src

    view_src = (target / "src" / "myapp" / "views" / "main_view.py").read_text(encoding="utf-8")
    if container == "grid":
        assert "ttk.GridFrame" in view_src
    else:
        assert "ttk.PackFrame" in view_src


# ---------------------------------------------------------------------------
# create_project: appshell template
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("simple", [False, True])
def test_create_appshell_project(tmp_path: Path, simple: bool) -> None:
    target = tmp_path / "myshell"
    create_project(
        name="MyShell",
        target_dir=target,
        theme="superhero",
        template="appshell",
        simple=simple,
    )

    assert (target / "src" / "myshell" / "main.py").is_file()
    assert (target / "src" / "myshell" / "pages" / "home_page.py").is_file()
    assert (target / "src" / "myshell" / "pages" / "settings_page.py").is_file()
    assert (target / "src" / "myshell" / "pages" / "__init__.py").is_file()

    # Basic-template artifacts must not appear
    assert not (target / "src" / "myshell" / "views").exists()

    for py in (target / "src" / "myshell").rglob("*.py"):
        _assert_python_parses(py)

    cfg = _load_toml(target / "ttkb.toml")
    assert cfg["app"]["template"] == "appshell"
    assert cfg["settings"]["theme"] == "superhero"

    main_src = (target / "src" / "myshell" / "main.py").read_text(encoding="utf-8")
    assert "ttk.AppShell" in main_src
    assert 'os.environ.get("TTKB_THEME", "superhero")' in main_src
    assert "HomePage" in main_src and "SettingsPage" in main_src


# ---------------------------------------------------------------------------
# Name normalization
# ---------------------------------------------------------------------------


def test_create_project_normalizes_hyphenated_name(tmp_path: Path) -> None:
    target = tmp_path / "out"
    create_project(
        name="My-Cool App",
        target_dir=target,
        template="basic",
        simple=True,
    )
    # Module dir uses snake_case derived from the name
    assert (target / "src" / "my_cool_app" / "main.py").is_file()
    cfg = _load_toml(target / "ttkb.toml")
    assert cfg["app"]["entry"] == "src/my_cool_app/main.py"


# ---------------------------------------------------------------------------
# Component scaffolders
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("container", ["grid", "pack"])
def test_create_view(tmp_path: Path, container: str) -> None:
    out = create_view("ProfileView", tmp_path, container=container)
    assert out.name == "profile_view.py"
    mod = _assert_python_parses(out)
    classes = [n.name for n in ast.walk(mod) if isinstance(n, ast.ClassDef)]
    assert "ProfileView" in classes
    src = out.read_text(encoding="utf-8")
    assert ("ttk.GridFrame" if container == "grid" else "ttk.PackFrame") in src


def test_create_dialog(tmp_path: Path) -> None:
    out = create_dialog("ConfirmDialog", tmp_path)
    assert out.name == "confirm_dialog.py"
    mod = _assert_python_parses(out)
    classes = [n.name for n in ast.walk(mod) if isinstance(n, ast.ClassDef)]
    assert "ConfirmDialog" in classes


def test_create_page_camel_to_snake(tmp_path: Path) -> None:
    out = create_page("DashboardPage", tmp_path)
    assert out.name == "dashboard_page.py"
    mod = _assert_python_parses(out)
    classes = [n.name for n in ast.walk(mod) if isinstance(n, ast.ClassDef)]
    assert "DashboardPage" in classes
    # Page title strips trailing 'Page' for the heading
    src = out.read_text(encoding="utf-8")
    assert 'text="Dashboard"' in src


# ---------------------------------------------------------------------------
# Theme JSON templates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "renderer,expected_mode,expected_step",
    [
        (_get_light_theme_template, "light", "600"),
        (_get_dark_theme_template, "dark", "400"),
    ],
)
def test_theme_template_matches_v2_schema(
    tmp_path: Path, renderer, expected_mode: str, expected_step: str
) -> None:
    rendered = renderer("acme")
    data = json.loads(rendered)

    # Required v2 schema keys
    for key in ("name", "display_name", "mode", "foreground", "background", "shades", "semantic"):
        assert key in data, f"missing top-level key: {key}"

    assert data["name"] == "acme"
    assert data["mode"] == expected_mode
    assert isinstance(data["shades"], dict) and "blue" in data["shades"]
    assert isinstance(data["semantic"], dict)
    # Semantic accents reference shade tokens with the mode-appropriate step
    assert data["semantic"]["primary"].endswith(f"[{expected_step}]")

    # Round-trip through the user-theme loader
    path = tmp_path / "acme.json"
    path.write_text(rendered, encoding="utf-8")
    loaded = load_user_defined_theme(path)
    assert loaded == data


# ---------------------------------------------------------------------------
# PyInstaller spec template
# ---------------------------------------------------------------------------


def test_spec_template_format_is_safe() -> None:
    """SPEC_TEMPLATE.format(...) must render without KeyError on stray
    f-string braces (regression: {CONFIG_PATH} was once unescaped)."""
    rendered = SPEC_TEMPLATE.format(app_name="Demo")
    # Generated spec is parseable Python
    ast.parse(rendered)
    # Spot-check that the literal Python f-string survived as f-string
    assert "f\"ttkb.toml not found at {CONFIG_PATH}\"" in rendered


def test_default_launch_icon_is_packaged() -> None:
    """The spec template falls back to ttkbootstrap/assets/ttkbootstrap.ico
    when no [build.icon] is set; the file must ship with the package."""
    import ttkbootstrap
    icon = Path(ttkbootstrap.__file__).parent / "assets" / "ttkbootstrap.ico"
    assert icon.is_file(), f"missing default launch icon: {icon}"
    rendered = SPEC_TEMPLATE.format(app_name="Demo")
    assert "ttkbootstrap.ico" in rendered, (
        "spec template no longer references the bundled default icon — "
        "the previous path 'assets/icons/app.ico' silently failed because "
        "that file never existed in the package"
    )


def test_spec_template_bundles_icon_package_assets() -> None:
    """Until ttkbootstrap-icons publishes its pyinstaller40 entry point and
    a hook for the _bs provider, the spec must bundle icon assets directly,
    or frozen apps fail with ``No module named 'ttkbootstrap_icons_bs.assets'``.

    Tracked: https://github.com/israel-dryer/ttkbootstrap-icons (upstream).
    """
    rendered = SPEC_TEMPLATE.format(app_name="Demo")
    assert "collect_data_files" in rendered
    for pkg in ("ttkbootstrap_icons", "ttkbootstrap_icons_bs"):
        assert pkg in rendered, f"spec must reference {pkg} for the icon-bundle workaround"


def test_spec_template_uses_specpath_not_dunder_file() -> None:
    """Spec files are exec'd by PyInstaller without ``__file__`` in the
    namespace; ``SPECPATH`` is the supported way to locate the spec dir.

    ``module.__file__`` references (e.g. ``ttkbootstrap.__file__``) are
    fine — only a bare ``__file__`` lookup is broken.
    """
    rendered = SPEC_TEMPLATE.format(app_name="Demo")
    # Bare __file__ references look like Path(__file__), not foo.__file__
    assert "Path(__file__)" not in rendered, (
        "spec template references bare __file__ which is undefined when "
        "PyInstaller exec's the spec — use SPECPATH instead"
    )
    assert "SPECPATH" in rendered


def test_generate_spec_writes_parseable_file(tmp_path: Path) -> None:
    target = tmp_path / "proj"
    create_project(name="SpecApp", target_dir=target, template="basic", simple=True)
    cfg = TtkbConfig.load(target / "ttkb.toml")
    spec_path = target / "build" / "pyinstaller" / "app.spec"
    generate_spec(cfg, target, spec_path)
    assert spec_path.is_file()
    ast.parse(spec_path.read_text(encoding="utf-8"))
