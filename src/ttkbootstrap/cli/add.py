"""ttkb add command - Add views, dialogs, themes, and i18n to a project."""

from __future__ import annotations

import argparse
from pathlib import Path

from ttkbootstrap.cli.config import TtkbConfig, find_config
from ttkbootstrap.cli.templates import create_dialog, create_view


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the 'add' subcommand parser."""
    parser = subparsers.add_parser(
        "add",
        help="Add components to the project",
        description="Add views, dialogs, themes, or i18n support to the project.",
    )
    add_subparsers = parser.add_subparsers(dest="component")

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

    # Create view
    file_path = create_view(class_name, target_dir, container)

    print(f"Created view: {file_path.relative_to(project_root)}")


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
    print("To use this theme:")
    print(f"  1. Register it in your app: style.register_theme('{theme_name}')")
    print(f"  2. Apply it: style.theme_use('{theme_name}')")


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


def _get_light_theme_template(name: str) -> str:
    """Get a light theme template."""
    return f'''\
{{
    "name": "{name}",
    "type": "light",
    "colors": {{
        "primary": "#0d6efd",
        "secondary": "#6c757d",
        "success": "#198754",
        "info": "#0dcaf0",
        "warning": "#ffc107",
        "danger": "#dc3545",
        "light": "#f8f9fa",
        "dark": "#212529",
        "background": "#ffffff",
        "foreground": "#212529",
        "border": "#dee2e6",
        "inputBackground": "#ffffff",
        "inputForeground": "#212529"
    }}
}}
'''


def _get_dark_theme_template(name: str) -> str:
    """Get a dark theme template."""
    return f'''\
{{
    "name": "{name}",
    "type": "dark",
    "colors": {{
        "primary": "#0d6efd",
        "secondary": "#6c757d",
        "success": "#198754",
        "info": "#0dcaf0",
        "warning": "#ffc107",
        "danger": "#dc3545",
        "light": "#f8f9fa",
        "dark": "#212529",
        "background": "#212529",
        "foreground": "#f8f9fa",
        "border": "#495057",
        "inputBackground": "#343a40",
        "inputForeground": "#f8f9fa"
    }}
}}
'''


def _get_po_template(lang: str) -> str:
    """Get a .po file template."""
    return f'''\
# {lang.upper()} translations for the application.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
#
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2024-01-01 00:00+0000\\n"
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
