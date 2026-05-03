"""Shot factories for action widget pages.

Covers ButtonGroup, MenuButton, DropdownButton. The ContextMenu page is
deferred along with the other popup-style widgets — its visual is a
floating Toplevel rather than an in-line widget, so it doesn't fit the
current capture model.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def buttongroup(parent: tkinter.Widget) -> None:
    """A clipboard-style ButtonGroup with three icon+text actions."""
    box = ttk.Frame(parent, padding=8)
    box.pack()
    bg = ttk.ButtonGroup(box, accent="primary")
    bg.pack()
    bg.add(text="Cut", icon="scissors")
    bg.add(text="Copy", icon="copy")
    bg.add(text="Paste", icon="clipboard")


def menubutton(parent: tkinter.Widget) -> None:
    """A MenuButton labeled "File" with a native Tk menu attached."""
    box = ttk.Frame(parent, padding=8)
    box.pack()
    menu = ttk.Menu(box, tearoff=0)
    menu.add_command(label="Open")
    menu.add_command(label="Save")
    menu.add_separator()
    menu.add_command(label="Exit")
    ttk.MenuButton(box, text="File", menu=menu, accent="primary").pack()


def dropdownbutton(parent: tkinter.Widget) -> None:
    """A DropdownButton labeled "Actions" with a small list of items."""
    box = ttk.Frame(parent, padding=8)
    box.pack()
    items = [
        ttk.ContextMenuItem(type="command", text="Open"),
        ttk.ContextMenuItem(type="command", text="Rename"),
        ttk.ContextMenuItem(type="separator"),
        ttk.ContextMenuItem(type="command", text="Delete"),
    ]
    ttk.DropdownButton(box, text="Actions", items=items, accent="primary").pack()
