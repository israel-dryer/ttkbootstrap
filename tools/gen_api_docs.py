#!/usr/bin/env python
"""Generate API reference markdown files for ttkbootstrap.

Run this script before building docs with Zensical:
    python tools/gen_api_docs.py
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
REF_DIR = DOCS_DIR / "reference"

# API structure matching ttkbootstrap.api modules
API_MODULES = {
    "app": {
        "title": "App",
        "description": "Application, window management, and menus",
        "exports": {
            "App": "ttkbootstrap.runtime.app.App",
            "Window": "ttkbootstrap.runtime.app.App",  # Alias
            "Toplevel": "ttkbootstrap.runtime.toplevel.Toplevel",
            "AppSettings": "ttkbootstrap.runtime.app.AppSettings",
            "get_current_app": "ttkbootstrap.runtime.app.get_current_app",
            "get_app_settings": "ttkbootstrap.runtime.app.get_app_settings",
            "MenuManager": "ttkbootstrap.runtime.menu.MenuManager",
            "create_menu": "ttkbootstrap.runtime.menu.create_menu",
        },
    },
    "style": {
        "title": "Style",
        "description": "Theme and style management",
        "exports": {
            "Style": "ttkbootstrap.style.style.Style",
            "Bootstyle": "ttkbootstrap.style.bootstyle.Bootstyle",
            "BootstrapIcon": "ttkbootstrap_icons_bs.BootstrapIcon",
            "get_style": "ttkbootstrap.style.style.get_style",
            "get_style_builder": "ttkbootstrap.style.style.get_style_builder",
            "get_theme": "ttkbootstrap.style.style.get_theme",
            "get_theme_provider": "ttkbootstrap.style.style.get_theme_provider",
            "set_theme": "ttkbootstrap.style.style.set_theme",
            "toggle_theme": "ttkbootstrap.style.style.toggle_theme",
            "get_theme_color": "ttkbootstrap.style.style.get_theme_color",
            "get_themes": "ttkbootstrap.style.style.get_themes",
        },
    },
    "widgets": {
        "title": "Widgets",
        "description": "UI components",
        "exports": {
            # Primitives
            "Badge": "ttkbootstrap.widgets.primitives.badge.Badge",
            "Button": "ttkbootstrap.widgets.primitives.button.Button",
            "CheckButton": "ttkbootstrap.widgets.primitives.checkbutton.CheckButton",
            "CheckToggle": "ttkbootstrap.widgets.primitives.checktoggle.CheckToggle",
            "Combobox": "ttkbootstrap.widgets.primitives.combobox.Combobox",
            "Entry": "ttkbootstrap.widgets.primitives.entry.Entry",
            "Frame": "ttkbootstrap.widgets.primitives.frame.Frame",
            "Label": "ttkbootstrap.widgets.primitives.label.Label",
            "LabelFrame": "ttkbootstrap.widgets.primitives.labelframe.LabelFrame",
            "MenuButton": "ttkbootstrap.widgets.primitives.menubutton.MenuButton",
            "Notebook": "ttkbootstrap.widgets.primitives.notebook.Notebook",
            "OptionMenu": "ttkbootstrap.widgets.primitives.optionmenu.OptionMenu",
            "PanedWindow": "ttkbootstrap.widgets.primitives.panedwindow.PanedWindow",
            "Progressbar": "ttkbootstrap.widgets.primitives.progressbar.Progressbar",
            "RadioButton": "ttkbootstrap.widgets.primitives.radiobutton.RadioButton",
            "RadioToggle": "ttkbootstrap.widgets.primitives.radiotoggle.RadioToggle",
            "Scale": "ttkbootstrap.widgets.primitives.scale.Scale",
            "Scrollbar": "ttkbootstrap.widgets.primitives.scrollbar.Scrollbar",
            "SelectBox": "ttkbootstrap.widgets.primitives.selectbox.SelectBox",
            "Separator": "ttkbootstrap.widgets.primitives.separator.Separator",
            "SizeGrip": "ttkbootstrap.widgets.primitives.sizegrip.SizeGrip",
            "Spinbox": "ttkbootstrap.widgets.primitives.spinbox.Spinbox",
            "TreeView": "ttkbootstrap.widgets.primitives.treeview.TreeView",
            # Composites
            "ButtonGroup": "ttkbootstrap.widgets.composites.buttongroup.ButtonGroup",
            "Calendar": "ttkbootstrap.widgets.composites.calendar.Calendar",
            "ContextMenu": "ttkbootstrap.widgets.composites.contextmenu.ContextMenu",
            "ContextMenuItem": "ttkbootstrap.widgets.composites.contextmenu.ContextMenuItem",
            "DateEntry": "ttkbootstrap.widgets.composites.dateentry.DateEntry",
            "DropdownButton": "ttkbootstrap.widgets.composites.dropdownbutton.DropdownButton",
            "Field": "ttkbootstrap.widgets.composites.field.Field",
            "FieldOptions": "ttkbootstrap.widgets.composites.field.FieldOptions",
            "FloodGauge": "ttkbootstrap.widgets.composites.floodgauge.FloodGauge",
            "Form": "ttkbootstrap.widgets.composites.form.Form",
            "LabeledScale": "ttkbootstrap.widgets.composites.labeledscale.LabeledScale",
            "Meter": "ttkbootstrap.widgets.composites.meter.Meter",
            "NumericEntry": "ttkbootstrap.widgets.composites.numericentry.NumericEntry",
            "PageStack": "ttkbootstrap.widgets.composites.pagestack.PageStack",
            "PasswordEntry": "ttkbootstrap.widgets.composites.passwordentry.PasswordEntry",
            "PathEntry": "ttkbootstrap.widgets.composites.pathentry.PathEntry",
            "RadioGroup": "ttkbootstrap.widgets.composites.radiogroup.RadioGroup",
            "ScrolledText": "ttkbootstrap.widgets.composites.scrolledtext.ScrolledText",
            "ScrollView": "ttkbootstrap.widgets.composites.scrollview.ScrollView",
            "SpinnerEntry": "ttkbootstrap.widgets.composites.spinnerentry.SpinnerEntry",
            "TableView": "ttkbootstrap.widgets.composites.tableview.TableView",
            "TextEntry": "ttkbootstrap.widgets.composites.textentry.TextEntry",
            "TimeEntry": "ttkbootstrap.widgets.composites.timeentry.TimeEntry",
            "Toast": "ttkbootstrap.widgets.composites.toast.Toast",
            "ToggleGroup": "ttkbootstrap.widgets.composites.togglegroup.ToggleGroup",
            "ToolTip": "ttkbootstrap.widgets.composites.tooltip.ToolTip",
        },
    },
    "dialogs": {
        "title": "Dialogs",
        "description": "Dialog windows for common interactions",
        "exports": {
            "Dialog": "ttkbootstrap.dialogs.dialog.Dialog",
            "DialogButton": "ttkbootstrap.dialogs.dialog.DialogButton",
            "FilterDialog": "ttkbootstrap.dialogs.filterdialog.FilterDialog",
            "FormDialog": "ttkbootstrap.dialogs.formdialog.FormDialog",
            "MessageDialog": "ttkbootstrap.dialogs.message.MessageDialog",
            "MessageBox": "ttkbootstrap.dialogs.message.MessageBox",
            "QueryDialog": "ttkbootstrap.dialogs.query.QueryDialog",
            "QueryBox": "ttkbootstrap.dialogs.query.QueryBox",
            "DateDialog": "ttkbootstrap.dialogs.datedialog.DateDialog",
            "FontDialog": "ttkbootstrap.dialogs.fontdialog.FontDialog",
            "ColorChooser": "ttkbootstrap.dialogs.colorchooser.ColorChooser",
            "ColorChooserDialog": "ttkbootstrap.dialogs.colorchooser.ColorChooserDialog",
            "ColorDropperDialog": "ttkbootstrap.dialogs.colordropper.ColorDropperDialog",
        },
    },
    "data": {
        "title": "Data",
        "description": "Data sources for widgets",
        "exports": {
            "BaseDataSource": "ttkbootstrap.datasource.base.BaseDataSource",
            "MemoryDataSource": "ttkbootstrap.datasource.memory_source.MemoryDataSource",
            "SqliteDataSource": "ttkbootstrap.datasource.sqlite_source.SqliteDataSource",
            "FileDataSource": "ttkbootstrap.datasource.file_source.FileDataSource",
            "FileSourceConfig": "ttkbootstrap.datasource.file_source.FileSourceConfig",
            "DataSourceProtocol": "ttkbootstrap.datasource.types.DataSourceProtocol",
            "Record": "ttkbootstrap.datasource.types.Record",
            "Primitive": "ttkbootstrap.datasource.types.Primitive",
        },
    },
    "i18n": {
        "title": "i18n",
        "description": "Internationalization and localization",
        "exports": {
            "MessageCatalog": "ttkbootstrap.core.localization.msgcat.MessageCatalog",
            "L": "ttkbootstrap.core.localization.specs.L",
            "LV": "ttkbootstrap.core.localization.specs.LV",
            "IntlFormatter": "ttkbootstrap.core.localization.intl_format.IntlFormatter",
        },
    },
    "utils": {
        "title": "Utils",
        "description": "Core utilities for reactive programming and validation",
        "exports": {
            "Signal": "ttkbootstrap.core.signals.signal.Signal",
            "TraceOperation": "ttkbootstrap.core.signals.signal.TraceOperation",
            "ValidationRule": "ttkbootstrap.core.validation.ValidationRule",
            "ValidationResult": "ttkbootstrap.core.validation.ValidationResult",
            "SetVar": "ttkbootstrap.core.variables.SetVar",
        },
    },
}


def write_ref_page(path: Path, identifier: str, title: str):
    """Write a reference page for a single symbol."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"# {title}\n\n::: {identifier}\n"
    path.write_text(content, encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}")


def write_module_index(module_name: str, module_info: dict):
    """Generate index page for a module."""
    module_dir = REF_DIR / module_name
    module_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {module_info['title']}",
        "",
        module_info['description'],
        "",
        "## Exports",
        "",
        "| Name | Description |",
        "|------|-------------|",
    ]

    for name in sorted(module_info['exports'].keys()):
        lines.append(f"| [{name}]({name}.md) | |")

    index_path = module_dir / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  {index_path.relative_to(ROOT)}")


def write_main_index():
    """Generate the main API reference index."""
    lines = [
        "# API Reference",
        "",
        "Auto-generated API documentation for ttkbootstrap.",
        "",
        "## Modules",
        "",
        "| Module | Description |",
        "|--------|-------------|",
    ]

    for module_name, module_info in API_MODULES.items():
        lines.append(f"| [{module_info['title']}]({module_name}/index.md) | {module_info['description']} |")

    lines.extend([
        "",
        "## Usage",
        "",
        "All exports are available from the top-level package:",
        "",
        "```python",
        "import ttkbootstrap as ttk",
        "",
        "# App",
        "app = ttk.App(title=\"My App\", theme=\"darkly\")",
        "",
        "# Widgets",
        "button = ttk.Button(app, text=\"Click\", bootstyle=\"success\")",
        "",
        "# Style",
        "ttk.set_theme(\"cosmo\")",
        "",
        "# Localization",
        "from ttkbootstrap import L",
        "label = ttk.Label(app, text=L(\"Hello\"))",
        "",
        "app.mainloop()",
        "```",
    ])

    index_path = REF_DIR / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  {index_path.relative_to(ROOT)}")


def main():
    print("Generating API reference docs...")
    print()

    total = 0

    for module_name, module_info in API_MODULES.items():
        print(f"[{module_info['title']}]")
        module_dir = REF_DIR / module_name

        # Generate individual pages
        for name, identifier in sorted(module_info['exports'].items()):
            write_ref_page(module_dir / f"{name}.md", identifier, title=name)
            total += 1

        # Generate module index
        write_module_index(module_name, module_info)
        print()

    # Generate main index
    print("[Main Index]")
    write_main_index()

    print(f"\nGenerated {total} API reference pages across {len(API_MODULES)} modules.")


if __name__ == "__main__":
    main()