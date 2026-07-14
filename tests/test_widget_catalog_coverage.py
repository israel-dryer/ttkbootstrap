"""No-gaps sync test for the Widgets catalog (docs Workstream H).

The visual catalog (`docs/widgets/`) has one usage page per public widget. This
test enforces that no public widget can be added to the API without either a
catalog page or an explicit "covered elsewhere" allowlist entry -- so a new
widget can't silently ship undocumented.

The widget set is derived live from `ttkbootstrap.__all__`: every exported
`tkinter.Widget` subclass, plus the two shipped helpers that are catalog widgets
without being tk widgets (`ToastNotification`, `ToolTip`). Each must map to a
`docs/widgets/<page>.rst` file or appear in `COVERED_ELSEWHERE`.

The allowlists are themselves checked (`test_*_are_public_widgets`) so they
can't rot: every key must still name a real public widget.
"""
import pathlib
import tkinter

import ttkbootstrap as ttk

_REPO = pathlib.Path(__file__).resolve().parents[1]
_WIDGETS_DIR = _REPO / "docs" / "widgets"

# Shipped helpers that ARE catalog widgets but don't subclass tkinter.Widget.
_EXTRA_WIDGETS = {"ToastNotification", "ToolTip"}

# class name -> catalog page basename, where it isn't just the lowercased name.
_PAGE_ALIASES = {
    "ToastNotification": "toast",
    "ScrolledFrame": "scrolled",
    "ScrolledText": "scrolled",
}

# Public widget classes documented OUTSIDE the visual catalog, by design.
_COVERED_ELSEWHERE = {
    "Menu": "Menus feature guide",
    "TkFrame": "window/infrastructure, not a catalog widget",
    "TkLabel": "window/infrastructure, not a catalog widget",
    "LabelFrame": "the tk LabelFrame; the catalog documents the ttk Labelframe",
    "ColorChooser": "Dialogs & overlays reference",
    "Listbox": "API reference; superseded for most uses by Treeview/Combobox",
    "FloodgaugeLegacy": "deprecated alias, removed in 3.0",
}


def _public_widgets():
    names = set(_EXTRA_WIDGETS)
    for name in ttk.__all__:
        obj = getattr(ttk, name)
        if isinstance(obj, type) and issubclass(obj, tkinter.Widget):
            names.add(name)
    return names


def test_every_public_widget_has_catalog_page_or_allowlist():
    missing = []
    for name in sorted(_public_widgets()):
        if name in _COVERED_ELSEWHERE:
            continue
        page = _PAGE_ALIASES.get(name, name.lower())
        if not (_WIDGETS_DIR / f"{page}.rst").exists():
            missing.append(f"{name} (expected docs/widgets/{page}.rst)")
    assert not missing, (
        "Public widgets with no catalog page and no COVERED_ELSEWHERE entry:\n  "
        + "\n  ".join(missing)
        + "\n\nAuthor a docs/widgets/<name>.rst page, add a _PAGE_ALIASES entry, "
        "or (if documented elsewhere by design) a _COVERED_ELSEWHERE entry."
    )


def test_allowlist_keys_are_public_widgets():
    widgets = _public_widgets()
    stale = sorted(
        name
        for name in (*_COVERED_ELSEWHERE, *_PAGE_ALIASES)
        if name not in widgets
    )
    assert not stale, (
        "Allowlist names that are no longer public widgets (remove them):\n  "
        + "\n  ".join(stale)
    )
