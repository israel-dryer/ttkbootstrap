"""Generate API reference pages for ttkbootstrap widgets."""

from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

REF_DIR = Path("reference")
WIDGETS_DIR = REF_DIR / "widgets"

# Map widget names to their full module paths for mkdocstrings
# This avoids issues with lazy loading in ttkbootstrap.__init__
WIDGET_MODULES = {
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
    "Separator": "ttkbootstrap.widgets.primitives.separator.Separator",
    "SizeGrip": "ttkbootstrap.widgets.primitives.sizegrip.SizeGrip",
    "Spinbox": "ttkbootstrap.widgets.primitives.spinbox.Spinbox",
    "TreeView": "ttkbootstrap.widgets.primitives.treeview.TreeView",
    # Composites
    "ButtonGroup": "ttkbootstrap.widgets.composites.buttongroup.ButtonGroup",
    "Calendar": "ttkbootstrap.widgets.composites.calendar.Calendar",
    "ContextMenu": "ttkbootstrap.widgets.composites.contextmenu.ContextMenu",
    "DateEntry": "ttkbootstrap.widgets.composites.dateentry.DateEntry",
    "DropdownButton": "ttkbootstrap.widgets.composites.dropdownbutton.DropdownButton",
    "Field": "ttkbootstrap.widgets.composites.field.Field",
    "FloodGauge": "ttkbootstrap.widgets.composites.floodgauge.FloodGauge",
    "Form": "ttkbootstrap.widgets.composites.form.Form",
    "LabeledScale": "ttkbootstrap.widgets.composites.labeledscale.LabeledScale",
    "ListItem": "ttkbootstrap.widgets.composites.list.listitem.ListItem",
    "ListView": "ttkbootstrap.widgets.composites.list.listview.ListView",
    "Meter": "ttkbootstrap.widgets.composites.meter.Meter",
    "NumericEntry": "ttkbootstrap.widgets.composites.numericentry.NumericEntry",
    "PageStack": "ttkbootstrap.widgets.composites.pagestack.PageStack",
    "PasswordEntry": "ttkbootstrap.widgets.composites.passwordentry.PasswordEntry",
    "PathEntry": "ttkbootstrap.widgets.composites.pathentry.PathEntry",
    "RadioGroup": "ttkbootstrap.widgets.composites.radiogroup.RadioGroup",
    "ScrolledText": "ttkbootstrap.widgets.composites.scrolledtext.ScrolledText",
    "ScrollView": "ttkbootstrap.widgets.composites.scrollview.ScrollView",
    "SelectBox": "ttkbootstrap.widgets.composites.selectbox.SelectBox",
    "SpinnerEntry": "ttkbootstrap.widgets.composites.spinnerentry.SpinnerEntry",
    "TableView": "ttkbootstrap.widgets.composites.tableview.TableView",
    "TextEntry": "ttkbootstrap.widgets.composites.textentry.TextEntry",
    "TimeEntry": "ttkbootstrap.widgets.composites.timeentry.TimeEntry",
    "Toast": "ttkbootstrap.widgets.composites.toast.Toast",
    "ToggleGroup": "ttkbootstrap.widgets.composites.togglegroup.ToggleGroup",
    "ToolTip": "ttkbootstrap.widgets.composites.tooltip.ToolTip",
    # Dialogs
    "Dialog": "ttkbootstrap.dialogs.dialog.Dialog",
    "MessageDialog": "ttkbootstrap.dialogs.message.MessageDialog",
    "MessageBox": "ttkbootstrap.dialogs.message.MessageBox",
    "QueryDialog": "ttkbootstrap.dialogs.query.QueryDialog",
    "QueryBox": "ttkbootstrap.dialogs.query.QueryBox",
    "ColorChooser": "ttkbootstrap.dialogs.colorchooser.ColorChooser",
    "ColorChooserDialog": "ttkbootstrap.dialogs.colorchooser.ColorChooserDialog",
    "ColorDropperDialog": "ttkbootstrap.dialogs.colordropper.ColorDropperDialog",
    "DateDialog": "ttkbootstrap.dialogs.datedialog.DateDialog",
    "FontDialog": "ttkbootstrap.dialogs.fontdialog.FontDialog",
    "FilterDialog": "ttkbootstrap.dialogs.filterdialog.FilterDialog",
    "FormDialog": "ttkbootstrap.dialogs.formdialog.FormDialog",
    # Core
    "App": "ttkbootstrap.runtime.app.App",
    "Toplevel": "ttkbootstrap.runtime.toplevel.Toplevel",
    "Style": "ttkbootstrap.style.style.Style",
}


def write_ref_page(path: Path, identifier: str, title: str | None = None):
    """Write a reference page for a single symbol."""
    with mkdocs_gen_files.open(path, "w") as f:
        if title:
            f.write(f"# {title}\n\n")
        f.write(f"::: {identifier}\n")


# Generate individual widget pages
items = sorted(WIDGET_MODULES.keys())
print(f"Generating API docs for {len(items)} symbols: {items}")

for name in items:
    identifier = WIDGET_MODULES[name]
    write_ref_page(WIDGETS_DIR / f"{name}.md", identifier, title=name)

# Generate widgets index page
with mkdocs_gen_files.open(WIDGETS_DIR / "index.md", "w") as f:
    f.write("# API Reference - Widgets\n\n")
    f.write("Auto-generated API reference for ttkbootstrap widgets.\n\n")

    # Group by category
    f.write("## Primitives\n\n")
    for name in sorted(n for n in items if "primitives" in WIDGET_MODULES[n]):
        f.write(f"- [{name}]({name}.md)\n")

    f.write("\n## Composites\n\n")
    for name in sorted(n for n in items if "composites" in WIDGET_MODULES[n]):
        f.write(f"- [{name}]({name}.md)\n")

    f.write("\n## Dialogs\n\n")
    for name in sorted(n for n in items if "dialogs" in WIDGET_MODULES[n]):
        f.write(f"- [{name}]({name}.md)\n")

    f.write("\n## Core\n\n")
    for name in sorted(n for n in items if "runtime" in WIDGET_MODULES[n] or "style.style" in WIDGET_MODULES[n]):
        f.write(f"- [{name}]({name}.md)\n")