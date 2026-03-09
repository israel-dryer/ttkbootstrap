"""Project templates for ttkb start command."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

ContainerType = Literal["grid", "pack"]
TemplateType = Literal["basic", "appshell"]


# =============================================================================
# Main entry point template
# =============================================================================

MAIN_PY_TEMPLATE = '''\
"""
{app_name} - A ttkbootstrap application.

Run with: python -m {module_name}
"""

import os

import ttkbootstrap as ttk

from {module_name}.views.main_view import MainView


def main() -> None:
    """Application entry point."""
    app = ttk.App(
        title="{app_name}",
        theme=os.environ.get("TTKB_THEME", "{theme}"),
        size=(800, 600),
    )

    # Create and display main view
    MainView(app).pack(fill="both", expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()
'''


# =============================================================================
# View templates (GridFrame vs PackFrame)
# =============================================================================

MAIN_VIEW_GRID_TEMPLATE = '''\
"""Main application view."""

import ttkbootstrap as ttk


class MainView(ttk.GridFrame):
    """Main view using GridFrame layout."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            columns=["auto", 1],
            gap=10,
            padding=20,
            **kwargs,
        )
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Header
        ttk.Label(
            self,
            text="Welcome to {app_name}",
            font=("TkDefaultFont", 18, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        # Example form layout
        ttk.Label(self, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(self, text="Email:").grid(row=2, column=0, sticky="e")
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=2, column=1, sticky="ew")

        # Action button
        ttk.Button(
            self,
            text="Get Started",
            bootstyle="primary",
            command=self._on_submit,
        ).grid(row=3, column=0, columnspan=2, pady=(20, 0))

    def _on_submit(self) -> None:
        """Handle form submission."""
        name = self.name_entry.get()
        email = self.email_entry.get()
        print(f"Name: {{name}}, Email: {{email}}")
'''


MAIN_VIEW_PACK_TEMPLATE = '''\
"""Main application view."""

import ttkbootstrap as ttk


class MainView(ttk.PackFrame):
    """Main view using PackFrame layout."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            direction="vertical",
            gap=10,
            padding=20,
            **kwargs,
        )
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Header
        header = ttk.Label(
            self,
            text="Welcome to {app_name}",
            font=("TkDefaultFont", 18, "bold"),
        )
        self.add(header)

        # Spacer
        self.add(ttk.Frame(self, height=10))

        # Name field
        name_frame = ttk.PackFrame(self, direction="horizontal", gap=10)
        ttk.Label(name_frame, text="Name:", width=10).pack(side="left")
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side="left", fill="x", expand=True)
        self.add(name_frame, fill_items="x")

        # Email field
        email_frame = ttk.PackFrame(self, direction="horizontal", gap=10)
        ttk.Label(email_frame, text="Email:", width=10).pack(side="left")
        self.email_entry = ttk.Entry(email_frame)
        self.email_entry.pack(side="left", fill="x", expand=True)
        self.add(email_frame, fill_items="x")

        # Action button
        self.add(ttk.Frame(self, height=10))
        btn = ttk.Button(
            self,
            text="Get Started",
            bootstyle="primary",
            command=self._on_submit,
        )
        self.add(btn)

    def _on_submit(self) -> None:
        """Handle form submission."""
        name = self.name_entry.get()
        email = self.email_entry.get()
        print(f"Name: {{name}}, Email: {{email}}")
'''


# =============================================================================
# View/Dialog add templates
# =============================================================================

VIEW_GRID_TEMPLATE = '''\
"""
{class_name} view.
"""

import ttkbootstrap as ttk


class {class_name}(ttk.GridFrame):
    """{class_name} using GridFrame layout."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            columns=["auto", 1],
            gap=10,
            padding=20,
            **kwargs,
        )
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        ttk.Label(
            self,
            text="{class_name}",
            font=("TkDefaultFont", 14, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        # Add your widgets here
'''


VIEW_PACK_TEMPLATE = '''\
"""
{class_name} view.
"""

import ttkbootstrap as ttk


class {class_name}(ttk.PackFrame):
    """{class_name} using PackFrame layout."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            direction="vertical",
            gap=10,
            padding=20,
            **kwargs,
        )
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        header = ttk.Label(
            self,
            text="{class_name}",
            font=("TkDefaultFont", 14, "bold"),
        )
        self.add(header)

        # Add your widgets here
'''


DIALOG_TEMPLATE = '''\
"""
{class_name} dialog.
"""

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Dialog


class {class_name}(Dialog):
    """{class_name} modal dialog."""

    def __init__(self, parent, title: str = "{class_name}", **kwargs):
        super().__init__(parent, title=title, **kwargs)

    def create_body(self, master) -> ttk.Frame:
        """Create the dialog body."""
        body = ttk.Frame(master, padding=20)

        ttk.Label(
            body,
            text="Dialog content goes here",
        ).pack(pady=10)

        return body

    def create_buttonbox(self, master) -> ttk.Frame:
        """Create the dialog buttons."""
        box = ttk.Frame(master, padding=(20, 10))

        ttk.Button(
            box,
            text="Cancel",
            command=self.cancel,
        ).pack(side="right", padx=5)

        ttk.Button(
            box,
            text="OK",
            bootstyle="primary",
            command=self.ok,
        ).pack(side="right")

        return box

    def validate(self) -> bool:
        """Validate dialog input before closing."""
        return True

    def apply(self) -> None:
        """Process dialog input after OK is clicked."""
        self.result = True
'''


# =============================================================================
# Package init template
# =============================================================================

INIT_PY_TEMPLATE = '''\
"""{app_name} package."""

__version__ = "0.1.0"
'''


# =============================================================================
# README template
# =============================================================================

README_TEMPLATE = '''\
# {app_name}

A ttkbootstrap application.

## Getting Started

### Development

```bash
# Run the application
python -m {module_name}

# Or use the CLI
ttkb run
```

### Building for Distribution

```bash
# Promote to packaging-ready (adds PyInstaller support)
ttkb promote --pyinstaller

# Build the executable
ttkb build
```

## Project Structure

```
{project_dir}/
├── src/{module_name}/
│   ├── __init__.py
│   ├── main.py
│   └── views/
│       └── main_view.py
├── assets/
├── ttkb.toml
└── README.md
```

## Configuration

Application settings are defined in `ttkb.toml`:

- `[app]` - Application metadata
- `[settings]` - Runtime settings (theme, language)
- `[layout]` - Default layout preferences
- `[build]` - Build/packaging configuration (after `ttkb promote`)
'''


# =============================================================================
# AppShell templates
# =============================================================================

APPSHELL_MAIN_PY_TEMPLATE = '''\
"""
{app_name} - A ttkbootstrap application.

Run with: python -m {module_name}
"""

import os

import ttkbootstrap as ttk

from {module_name}.pages.home_page import HomePage
from {module_name}.pages.settings_page import SettingsPage


def main() -> None:
    """Application entry point."""
    shell = ttk.AppShell(
        title="{app_name}",
        theme=os.environ.get("TTKB_THEME", "{theme}"),
        size=(1000, 650),
    )

    # Add a theme toggle button to the toolbar
    shell.toolbar.add_button(icon="sun", command=ttk.toggle_theme)

    # Navigation pages
    home = shell.add_page("home", text="Home", icon="house")
    HomePage(home)

    shell.add_separator()

    # Footer pages
    settings = shell.add_page("settings", text="Settings", icon="gear", is_footer=True)
    SettingsPage(settings)

    # Start on the home page
    shell.navigate("home")
    shell.mainloop()


if __name__ == "__main__":
    main()
'''


APPSHELL_HOME_PAGE_TEMPLATE = '''\
"""Home page."""

import ttkbootstrap as ttk


class HomePage:
    """Home page content.

    Pages in an AppShell are not widget subclasses. The ``parent`` frame
    is created by ``shell.add_page()`` and this class populates it.
    """

    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        ttk.Label(
            self.parent,
            text="Welcome to {app_name}",
            font="heading-xl",
        ).pack(anchor="w", padx=20, pady=(20, 10))

        ttk.Label(
            self.parent,
            text="This is your home page. Edit this file to get started.",
            wraplength=500,
        ).pack(anchor="w", padx=20, pady=(0, 20))

        content = ttk.LabelFrame(self.parent, text="Getting Started", padding=20)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        ttk.Label(
            content,
            text="Add your widgets here.\\n\\n"
            "Use shell.add_page() to create new pages,\\n"
            "and ttkb add page <PageName> to scaffold them.",
        ).pack(expand=True)
'''


APPSHELL_SETTINGS_PAGE_TEMPLATE = '''\
"""Settings page."""

import ttkbootstrap as ttk


class SettingsPage:
    """Settings page content.

    Pages in an AppShell are not widget subclasses. The ``parent`` frame
    is created by ``shell.add_page()`` and this class populates it.
    """

    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        ttk.Label(
            self.parent,
            text="Settings",
            font="heading-xl",
        ).pack(anchor="w", padx=20, pady=(20, 10))

        ttk.Label(
            self.parent,
            text="Configure your application preferences.",
            wraplength=500,
        ).pack(anchor="w", padx=20, pady=(0, 20))

        content = ttk.LabelFrame(self.parent, text="Preferences", padding=20)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Example settings
        theme_frame = ttk.Frame(content)
        theme_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(theme_frame, text="Theme:", width=15).pack(side="left")
        ttk.Button(
            theme_frame,
            text="Toggle Light/Dark",
            command=ttk.toggle_theme,
        ).pack(side="left")
'''


APPSHELL_PAGE_TEMPLATE = '''\
"""{page_title} page."""

import ttkbootstrap as ttk


class {class_name}:
    """{page_title} page content.

    Pages in an AppShell are not widget subclasses. The ``parent`` frame
    is created by ``shell.add_page()`` and this class populates it.
    """

    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        ttk.Label(
            self.parent,
            text="{page_title}",
            font="heading-xl",
        ).pack(anchor="w", padx=20, pady=(20, 10))

        content = ttk.LabelFrame(self.parent, text="Content", padding=20)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Add your widgets here
'''


APPSHELL_README_TEMPLATE = '''\
# {app_name}

A ttkbootstrap application using AppShell navigation.

## Getting Started

### Development

```bash
# Run the application
python -m {module_name}

# Or use the CLI
ttkb run
```

### Adding Pages

```bash
# Scaffold a new page
ttkb add page DashboardPage

# Then wire it up in main.py:
#   from {module_name}.pages.dashboard_page import DashboardPage
#   page = shell.add_page("dashboard", text="Dashboard", icon="speedometer2")
#   DashboardPage(page)
```

### Building for Distribution

```bash
# Promote to packaging-ready (adds PyInstaller support)
ttkb promote --pyinstaller

# Build the executable
ttkb build
```

## Project Structure

```
{project_dir}/
\u251c\u2500\u2500 src/{module_name}/
\u2502   \u251c\u2500\u2500 __init__.py
\u2502   \u251c\u2500\u2500 main.py
\u2502   \u2514\u2500\u2500 pages/
\u2502       \u251c\u2500\u2500 __init__.py
\u2502       \u251c\u2500\u2500 home_page.py
\u2502       \u2514\u2500\u2500 settings_page.py
\u251c\u2500\u2500 assets/
\u251c\u2500\u2500 ttkb.toml
\u2514\u2500\u2500 README.md
```

## Configuration

Application settings are defined in `ttkb.toml`:

- `[app]` - Application metadata
- `[settings]` - Runtime settings (theme, language)
- `[layout]` - Default layout preferences
- `[build]` - Build/packaging configuration (after `ttkb promote`)
'''


def create_page(
    class_name: str,
    target_dir: Path,
) -> Path:
    """Create a new AppShell page file.

    Args:
        class_name: Page class name (CamelCase).
        target_dir: Directory to create the page in.

    Returns:
        Path to the created file.
    """
    file_name = _camel_to_snake(class_name) + ".py"

    # Derive a readable title from the class name (e.g. "DashboardPage" -> "Dashboard")
    page_title = class_name
    if page_title.endswith("Page"):
        page_title = page_title[:-4]
    # Insert spaces before uppercase letters
    import re
    page_title = re.sub(r"([a-z])([A-Z])", r"\1 \2", page_title)

    content = APPSHELL_PAGE_TEMPLATE.format(
        class_name=class_name,
        page_title=page_title,
    )

    file_path = target_dir / file_name
    file_path.write_text(content, encoding="utf-8")

    return file_path


def create_project(
    name: str,
    target_dir: Path,
    container: ContainerType = "grid",
    theme: str = "cosmo",
    template: TemplateType = "basic",
    simple: bool = False,
) -> None:
    """Create a new ttkbootstrap project.

    Args:
        name: Application name.
        target_dir: Target directory for the project.
        container: Default container type ('grid' or 'pack').
        theme: Theme name for the application.
        template: Project template ('basic' or 'appshell').
        simple: If True, create minimal project without build config.
    """
    if template == "appshell":
        _create_appshell_project(name, target_dir, theme, simple)
    else:
        _create_basic_project(name, target_dir, container, theme, simple)


def _create_basic_project(
    name: str,
    target_dir: Path,
    container: ContainerType,
    theme: str,
    simple: bool,
) -> None:
    """Create a basic single-view project."""
    from ttkbootstrap.cli.config import write_config

    # Normalize names
    name_lower = name.lower().replace(" ", "_").replace("-", "_")
    module_name = name_lower

    # Create directory structure
    src_dir = target_dir / "src" / module_name
    views_dir = src_dir / "views"
    assets_dir = target_dir / "assets"

    src_dir.mkdir(parents=True, exist_ok=True)
    views_dir.mkdir(parents=True, exist_ok=True)
    if not simple:
        assets_dir.mkdir(parents=True, exist_ok=True)

    # Write main.py
    main_content = MAIN_PY_TEMPLATE.format(
        app_name=name,
        module_name=module_name,
        theme=theme,
    )
    (src_dir / "main.py").write_text(main_content, encoding="utf-8")

    # Write __init__.py
    init_content = INIT_PY_TEMPLATE.format(app_name=name)
    (src_dir / "__init__.py").write_text(init_content, encoding="utf-8")

    # Write views/__init__.py
    (views_dir / "__init__.py").write_text(
        '"""Views package."""\n', encoding="utf-8"
    )

    # Write main_view.py
    if container == "grid":
        view_template = MAIN_VIEW_GRID_TEMPLATE
    else:
        view_template = MAIN_VIEW_PACK_TEMPLATE

    view_content = view_template.format(app_name=name)
    (views_dir / "main_view.py").write_text(view_content, encoding="utf-8")

    # Write ttkb.toml
    write_config(
        path=target_dir / "ttkb.toml",
        name=name,
        entry=f"src/{module_name}/main.py",
        theme=theme,
        template="basic",
        include_build=False,
    )

    # Write README.md
    if not simple:
        readme_content = README_TEMPLATE.format(
            app_name=name,
            module_name=module_name,
            project_dir=target_dir.name,
        )
        (target_dir / "README.md").write_text(readme_content, encoding="utf-8")


def _create_appshell_project(
    name: str,
    target_dir: Path,
    theme: str,
    simple: bool,
) -> None:
    """Create an AppShell project with sidebar navigation and pages."""
    from ttkbootstrap.cli.config import write_config

    # Normalize names
    name_lower = name.lower().replace(" ", "_").replace("-", "_")
    module_name = name_lower

    # Create directory structure
    src_dir = target_dir / "src" / module_name
    pages_dir = src_dir / "pages"
    assets_dir = target_dir / "assets"

    src_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)
    if not simple:
        assets_dir.mkdir(parents=True, exist_ok=True)

    # Write main.py
    main_content = APPSHELL_MAIN_PY_TEMPLATE.format(
        app_name=name,
        module_name=module_name,
        theme=theme,
    )
    (src_dir / "main.py").write_text(main_content, encoding="utf-8")

    # Write __init__.py
    init_content = INIT_PY_TEMPLATE.format(app_name=name)
    (src_dir / "__init__.py").write_text(init_content, encoding="utf-8")

    # Write pages/__init__.py
    (pages_dir / "__init__.py").write_text(
        '"""Pages package."""\n', encoding="utf-8"
    )

    # Write home_page.py
    home_content = APPSHELL_HOME_PAGE_TEMPLATE.format(app_name=name)
    (pages_dir / "home_page.py").write_text(home_content, encoding="utf-8")

    # Write settings_page.py
    (pages_dir / "settings_page.py").write_text(
        APPSHELL_SETTINGS_PAGE_TEMPLATE, encoding="utf-8"
    )

    # Write ttkb.toml
    write_config(
        path=target_dir / "ttkb.toml",
        name=name,
        entry=f"src/{module_name}/main.py",
        theme=theme,
        template="appshell",
        include_build=False,
    )

    # Write README.md
    if not simple:
        readme_content = APPSHELL_README_TEMPLATE.format(
            app_name=name,
            module_name=module_name,
            project_dir=target_dir.name,
        )
        (target_dir / "README.md").write_text(readme_content, encoding="utf-8")


def create_view(
    class_name: str,
    target_dir: Path,
    container: ContainerType = "grid",
) -> Path:
    """Create a new view file.

    Args:
        class_name: View class name (CamelCase).
        target_dir: Directory to create the view in.
        container: Container type ('grid' or 'pack').

    Returns:
        Path to the created file.
    """
    # Convert CamelCase to snake_case
    file_name = _camel_to_snake(class_name) + ".py"

    if container == "grid":
        template = VIEW_GRID_TEMPLATE
    else:
        template = VIEW_PACK_TEMPLATE

    content = template.format(class_name=class_name)

    file_path = target_dir / file_name
    file_path.write_text(content, encoding="utf-8")

    return file_path


def create_dialog(
    class_name: str,
    target_dir: Path,
) -> Path:
    """Create a new dialog file.

    Args:
        class_name: Dialog class name (CamelCase).
        target_dir: Directory to create the dialog in.

    Returns:
        Path to the created file.
    """
    file_name = _camel_to_snake(class_name) + ".py"
    content = DIALOG_TEMPLATE.format(class_name=class_name)

    file_path = target_dir / file_name
    file_path.write_text(content, encoding="utf-8")

    return file_path


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    import re

    # Insert underscore before uppercase letters and lowercase
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
