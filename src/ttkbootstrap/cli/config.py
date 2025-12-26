"""Configuration loader and writer for ttkb.toml."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# Python 3.11+ has tomllib built-in, earlier versions need tomli
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore

# Default ttkb.toml template
DEFAULT_CONFIG_TEMPLATE = """\
[app]
name = "{name}"
id = "{app_id}"
entry = "{entry}"

[settings]
theme = "cosmo"
language = "en"
appearance = "system"

[layout]
default_container = "grid"
"""

BUILD_CONFIG_TEMPLATE = """\

[build]
backend = "pyinstaller"
windowed = true
onefile = false

[build.icon]
# path = "assets/icon.ico"

[build.datas]
include = [
    "assets/**",
    "locales/**",
    "themes/**",
    "ttkb.toml",
]
"""


@dataclass
class AppConfig:
    """The [app] section of ttkb.toml."""

    name: str = "MyApp"
    id: str = "com.example.myapp"
    entry: str = "src/myapp/main.py"


@dataclass
class SettingsConfig:
    """The [settings] section of ttkb.toml."""

    theme: str = "cosmo"
    language: str = "en"
    appearance: str = "system"  # system | light | dark


@dataclass
class LayoutConfig:
    """The [layout] section of ttkb.toml."""

    default_container: str = "grid"  # grid | pack


@dataclass
class BuildIconConfig:
    """The [build.icon] section of ttkb.toml."""

    path: Optional[str] = None


@dataclass
class BuildDatasConfig:
    """The [build.datas] section of ttkb.toml."""

    include: list[str] = field(default_factory=list)


@dataclass
class BuildConfig:
    """The [build] section of ttkb.toml."""

    backend: str = "pyinstaller"
    windowed: bool = True
    onefile: bool = False
    icon: BuildIconConfig = field(default_factory=BuildIconConfig)
    datas: BuildDatasConfig = field(default_factory=BuildDatasConfig)


@dataclass
class TtkbConfig:
    """Complete ttkb.toml configuration."""

    app: AppConfig = field(default_factory=AppConfig)
    settings: SettingsConfig = field(default_factory=SettingsConfig)
    layout: LayoutConfig = field(default_factory=LayoutConfig)
    build: Optional[BuildConfig] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TtkbConfig:
        """Create TtkbConfig from a dictionary (parsed TOML)."""
        app_data = data.get("app", {})
        settings_data = data.get("settings", {})
        layout_data = data.get("layout", {})
        build_data = data.get("build")

        app = AppConfig(
            name=app_data.get("name", "MyApp"),
            id=app_data.get("id", "com.example.myapp"),
            entry=app_data.get("entry", "src/myapp/main.py"),
        )

        settings = SettingsConfig(
            theme=settings_data.get("theme", "cosmo"),
            language=settings_data.get("language", "en"),
            appearance=settings_data.get("appearance", "system"),
        )

        layout = LayoutConfig(
            default_container=layout_data.get("default_container", "grid"),
        )

        build = None
        if build_data is not None:
            icon_data = build_data.get("icon", {})
            datas_data = build_data.get("datas", {})

            build = BuildConfig(
                backend=build_data.get("backend", "pyinstaller"),
                windowed=build_data.get("windowed", True),
                onefile=build_data.get("onefile", False),
                icon=BuildIconConfig(path=icon_data.get("path")),
                datas=BuildDatasConfig(include=datas_data.get("include", [])),
            )

        return cls(app=app, settings=settings, layout=layout, build=build)

    @classmethod
    def load(cls, path: Path | str = "ttkb.toml") -> TtkbConfig:
        """Load configuration from a ttkb.toml file.

        Args:
            path: Path to the configuration file.

        Returns:
            TtkbConfig instance.

        Raises:
            FileNotFoundError: If the file does not exist.
            RuntimeError: If TOML parsing is not available.
        """
        if tomllib is None:
            raise RuntimeError(
                "TOML parsing not available. Install 'tomli' package: pip install tomli"
            )
        path = Path(path)
        with path.open("rb") as f:
            data = tomllib.load(f)
        return cls.from_dict(data)

    @classmethod
    def load_or_default(cls, path: Path | str = "ttkb.toml") -> TtkbConfig:
        """Load configuration from file, or return defaults if not found.

        Args:
            path: Path to the configuration file.

        Returns:
            TtkbConfig instance (loaded or default).
        """
        path = Path(path)
        if path.exists():
            return cls.load(path)
        return cls()


def find_config(start_dir: Path | str | None = None) -> Path | None:
    """Find ttkb.toml by walking up from start_dir.

    Args:
        start_dir: Starting directory (defaults to current working directory).

    Returns:
        Path to ttkb.toml if found, None otherwise.
    """
    if start_dir is None:
        start_dir = Path.cwd()
    else:
        start_dir = Path(start_dir)

    current = start_dir.resolve()
    while current != current.parent:
        config_path = current / "ttkb.toml"
        if config_path.exists():
            return config_path
        current = current.parent

    # Check root
    config_path = current / "ttkb.toml"
    if config_path.exists():
        return config_path

    return None


def generate_config(
    name: str,
    app_id: Optional[str] = None,
    entry: Optional[str] = None,
    include_build: bool = False,
) -> str:
    """Generate ttkb.toml content.

    Args:
        name: Application name.
        app_id: Application identifier (defaults to com.example.<name>).
        entry: Entry point path (defaults to src/<name>/main.py).
        include_build: Whether to include [build] section.

    Returns:
        TOML configuration string.
    """
    name_lower = name.lower().replace(" ", "_").replace("-", "_")
    if app_id is None:
        app_id = f"com.example.{name_lower}"
    if entry is None:
        entry = f"src/{name_lower}/main.py"

    content = DEFAULT_CONFIG_TEMPLATE.format(
        name=name,
        app_id=app_id,
        entry=entry,
    )

    if include_build:
        content += BUILD_CONFIG_TEMPLATE

    return content


def write_config(
    path: Path | str,
    name: str,
    app_id: Optional[str] = None,
    entry: Optional[str] = None,
    include_build: bool = False,
) -> None:
    """Write ttkb.toml to disk.

    Args:
        path: Path to write the configuration file.
        name: Application name.
        app_id: Application identifier.
        entry: Entry point path.
        include_build: Whether to include [build] section.
    """
    path = Path(path)
    content = generate_config(name, app_id, entry, include_build)
    path.write_text(content, encoding="utf-8")
