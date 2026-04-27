"""ttkb add command - Add views, dialogs, themes, and i18n to a project."""

from __future__ import annotations

import argparse
from pathlib import Path

from ttkbootstrap.cli.config import TtkbConfig, find_config
from ttkbootstrap.cli.templates import create_dialog, create_page, create_view


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'add' subcommand parser."""
    parser = subparsers.add_parser(
        "add",
        help="Add components to the project",
        description="Add views, pages, dialogs, themes, or i18n support to the project.",
    )
    add_subparsers = parser.add_subparsers(dest="component")

    # ttkb add page <ClassName>
    page_parser = add_subparsers.add_parser(
        "page",
        help="Add a new page (for AppShell projects)",
    )
    page_parser.add_argument(
        "class_name",
        help="Page class name (CamelCase, e.g., 'DashboardPage')",
    )
    page_parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="Target directory (default: src/<app>/pages/)",
    )
    page_parser.add_argument(
        "--scrollable",
        action="store_true",
        help="Make the page scrollable (wraps content in a ScrollView)",
    )
    page_parser.set_defaults(func=run_add_page)

    # ttkb add view <ClassName>
    view_parser = add_subparsers.add_parser(
        "view",
        help="Add a new view",
    )
    view_parser.add_argument(
        "class_name",
        help="View class name (CamelCase, e.g., 'SettingsView')",
    )
    view_parser.add_argument(
        "--container",
        choices=["grid", "pack"],
        default=None,
        help="Container type (default: from ttkb.toml or 'grid')",
    )
    view_parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="Target directory (default: src/<app>/views/)",
    )
    view_parser.set_defaults(func=run_add_view)

    # ttkb add dialog <ClassName>
    dialog_parser = add_subparsers.add_parser(
        "dialog",
        help="Add a new dialog",
    )
    dialog_parser.add_argument(
        "class_name",
        help="Dialog class name (CamelCase, e.g., 'ConfirmDialog')",
    )
    dialog_parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        help="Target directory (default: src/<app>/dialogs/)",
    )
    dialog_parser.set_defaults(func=run_add_dialog)

    # ttkb add theme <name>
    theme_parser = add_subparsers.add_parser(
        "theme",
        help="Add a custom theme",
    )
    theme_parser.add_argument(
        "name",
        help="Theme name (e.g., 'mytheme')",
    )
    theme_parser.add_argument(
        "--mode",
        choices=["light", "dark"],
        default="light",
        help="Theme mode (default: light)",
    )
    theme_parser.set_defaults(func=run_add_theme)

    # ttkb add i18n
    i18n_parser = add_subparsers.add_parser(
        "i18n",
        help="Add internationalization support",
    )
    i18n_parser.add_argument(
        "--languages",
        nargs="+",
        default=["en"],
        help="Languages to support (default: en)",
    )
    i18n_parser.set_defaults(func=run_add_i18n)

    parser.set_defaults(func=lambda args: parser.print_help())


def run_add_view(args: argparse.Namespace) -> None:
    """Add a new view to the project."""
    class_name = args.class_name

    # Validate class name
    if not class_name[0].isupper():
        print("Error: Class name should be CamelCase (e.g., 'SettingsView')")
        return

    # Find project configuration
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found. Are you in a ttkbootstrap project?")
        return

    project_root = config_path.parent
    config = TtkbConfig.load(config_path)

    # Reject in AppShell projects — views belong to the basic template
    if config.app.template == "appshell":
        print("Error: 'ttkb add view' is for basic-template projects.")
        print("This project uses the 'appshell' template. Use 'ttkb add page' instead.")
        return

    # Determine container type
    container = args.container
    if container is None:
        container = config.layout.default_container

    # Determine target directory
    if args.dir:
        target_dir = args.dir
    else:
        # Parse entry point to find source directory
        entry_path = Path(config.app.entry)
        if entry_path.parts[0] == "src" and len(entry_path.parts) >= 2:
            module_name = entry_path.parts[1]
            target_dir = project_root / "src" / module_name / "views"
        else:
            target_dir = project_root / "views"

    target_dir.mkdir(parents=True, exist_ok=True)

    # Ensure __init__.py exists
    init_file = target_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""Views package."""\n', encoding="utf-8")

    # Create view
    file_path = create_view(class_name, target_dir, container)

    print(f"Created view: {file_path.relative_to(project_root)}")


def run_add_page(args: argparse.Namespace) -> None:
    """Add a new page to an AppShell project."""
    class_name = args.class_name

    # Validate class name
    if not class_name[0].isupper():
        print("Error: Class name should be CamelCase (e.g., 'DashboardPage')")
        return

    # Find project configuration
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found. Are you in a ttkbootstrap project?")
        return

    project_root = config_path.parent
    config = TtkbConfig.load(config_path)

    # Check that this is an AppShell project
    if config.app.template != "appshell":
        print("Error: 'ttkb add page' is for AppShell projects.")
        print("This project uses the 'basic' template. Use 'ttkb add view' instead.")
        return

    # Determine target directory and module name for the import hint
    entry_path = Path(config.app.entry)
    if entry_path.parts[0] == "src" and len(entry_path.parts) >= 2:
        module_name = entry_path.parts[1]
        default_target = project_root / "src" / module_name / "pages"
    else:
        module_name = None
        default_target = project_root / "pages"

    target_dir = args.dir if args.dir else default_target

    target_dir.mkdir(parents=True, exist_ok=True)

    # Ensure __init__.py exists
    init_file = target_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""Pages package."""\n', encoding="utf-8")

    # Create page
    scrollable = args.scrollable
    file_path = create_page(class_name, target_dir, scrollable=scrollable)

    print(f"Created page: {file_path.relative_to(project_root)}")
    print()
    print("This created the file only — it is NOT yet shown in the sidebar.")
    print("To register it with the AppShell, paste these lines into main.py:")
    print()
    import_module = f"{module_name}.pages" if module_name else "<module>.pages"
    print(f"  from {import_module}.{file_path.stem} import {class_name}")
    scrollable_arg = ", scrollable=True" if scrollable else ""
    print(f'  page = shell.add_page("<id>", text="<Label>", icon="<icon>"{scrollable_arg})')
    print(f"  {class_name}(page)")


def run_add_dialog(args: argparse.Namespace) -> None:
    """Add a new dialog to the project."""
    class_name = args.class_name

    # Validate class name
    if not class_name[0].isupper():
        print("Error: Class name should be CamelCase (e.g., 'ConfirmDialog')")
        return

    # Find project configuration
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found. Are you in a ttkbootstrap project?")
        return

    project_root = config_path.parent
    config = TtkbConfig.load(config_path)

    # Determine target directory
    if args.dir:
        target_dir = args.dir
    else:
        # Parse entry point to find source directory
        entry_path = Path(config.app.entry)
        if entry_path.parts[0] == "src" and len(entry_path.parts) >= 2:
            module_name = entry_path.parts[1]
            target_dir = project_root / "src" / module_name / "dialogs"
        else:
            target_dir = project_root / "dialogs"

    target_dir.mkdir(parents=True, exist_ok=True)

    # Ensure __init__.py exists
    init_file = target_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""Dialogs package."""\n', encoding="utf-8")

    # Create dialog
    file_path = create_dialog(class_name, target_dir)

    print(f"Created dialog: {file_path.relative_to(project_root)}")


def run_add_theme(args: argparse.Namespace) -> None:
    """Add a custom theme to the project."""
    theme_name = args.name.lower()
    mode = args.mode

    # Find project configuration
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found. Are you in a ttkbootstrap project?")
        return

    project_root = config_path.parent

    # Create themes directory
    themes_dir = project_root / "themes"
    themes_dir.mkdir(exist_ok=True)

    # Create theme file
    theme_file = themes_dir / f"{theme_name}.json"
    if theme_file.exists():
        print(f"Error: Theme '{theme_name}' already exists.")
        return

    # Theme template based on mode
    if mode == "light":
        theme_content = _get_light_theme_template(theme_name)
    else:
        theme_content = _get_dark_theme_template(theme_name)

    theme_file.write_text(theme_content, encoding="utf-8")

    print(f"Created theme: {theme_file.relative_to(project_root)}")
    print()
    print("To use this theme, register the JSON file before creating your App:")
    print()
    print("  from ttkbootstrap.style.theme_provider import register_user_theme")
    print(f'  register_user_theme("{theme_name}", "themes/{theme_name}.json")')
    print(f'  app = ttk.App(theme="{theme_name}")')


def run_add_i18n(args: argparse.Namespace) -> None:
    """Add internationalization support to the project."""
    languages = args.languages

    # Find project configuration
    config_path = find_config()
    if config_path is None:
        print("Error: No ttkb.toml found. Are you in a ttkbootstrap project?")
        return

    project_root = config_path.parent

    # Create locales directory structure
    locales_dir = project_root / "locales"

    for lang in languages:
        lang_dir = locales_dir / lang / "LC_MESSAGES"
        lang_dir.mkdir(parents=True, exist_ok=True)

        # Create .po file template
        po_file = lang_dir / "messages.po"
        if not po_file.exists():
            po_content = _get_po_template(lang)
            po_file.write_text(po_content, encoding="utf-8")
            print(f"Created: {po_file.relative_to(project_root)}")

    print()
    print("Internationalization support added!")
    print()
    print("Next steps:")
    print("  1. Add translatable strings to your .po files")
    print("  2. Compile with: msgfmt locales/<lang>/LC_MESSAGES/messages.po -o locales/<lang>/LC_MESSAGES/messages.mo")
    print("  3. Use translations in code: ttk.mc('Hello')")


_BASE_SHADES = {
    "blue": "#0d6efd",
    "indigo": "#6610f2",
    "purple": "#6f42c1",
    "red": "#dc3545",
    "orange": "#fd7e14",
    "yellow": "#ffc107",
    "green": "#198754",
    "teal": "#20c997",
    "cyan": "#0dcaf0",
    "gray": "#adb5bd",
    "pink": "#d63384",
}


def _theme_display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.replace("_", "-").split("-") if part)


def _render_theme(name: str, mode: str) -> str:
    """Render a v2 theme JSON template.

    Light themes use the [600] step for semantic accents (so text on white
    has good contrast); dark themes use [400] (lighter accents on a dark
    background). Both schemas match the format consumed by
    ``ttkbootstrap.style.theme_provider``.
    """
    if mode == "light":
        foreground, background, step = "#212529", "#ffffff", "600"
    else:
        foreground, background, step = "#f8f9fa", "#212529", "400"

    payload = {
        "name": name,
        "display_name": _theme_display_name(name),
        "mode": mode,
        "foreground": foreground,
        "background": background,
        "white": "#ffffff",
        "black": "#000000",
        "shades": _BASE_SHADES,
        "semantic": {
            "primary": f"blue[{step}]",
            "secondary": f"gray[{step}]",
            "success": f"green[{step}]",
            "info": f"cyan[{step}]",
            "warning": f"yellow[{step}]",
            "danger": f"red[{step}]",
            "light": "gray[100]",
            "dark": "gray[900]",
        },
    }
    import json as _json
    return _json.dumps(payload, indent=2) + "\n"


def _get_light_theme_template(name: str) -> str:
    """Get a v2 light-mode theme template."""
    return _render_theme(name, "light")


def _get_dark_theme_template(name: str) -> str:
    """Get a v2 dark-mode theme template."""
    return _render_theme(name, "dark")


def _get_po_template(lang: str) -> str:
    """Get a .po file template."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M%z")

    return f'''\
# {lang.upper()} translations for the application.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
#
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: {now}\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: {lang.upper()} <LL@li.org>\\n"
"Language: {lang}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

# Example translation
# msgid "Hello"
# msgstr "Hello"
'''
