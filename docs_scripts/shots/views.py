"""Shot factories for tabbed/multi-page widget pages.

Covers Tabs (navigation/tabs.md), Notebook, PageStack, TabView (views/*.md).
"""

from __future__ import annotations

import tkinter
from typing import Callable

import ttkbootstrap as ttk


def tabs(parent: tkinter.Widget) -> Callable[[], None]:
    """Single Tabs bar with Home/Files/Settings; Files selected."""
    column = ttk.Frame(parent, width=380)
    column.pack()
    bar = ttk.Tabs(column)
    bar.pack(fill="x")
    bar.add(text="Home", icon="house")
    bar.add(text="Files", icon="folder2")
    bar.add(text="Settings", icon="gear")

    def finalize() -> None:
        # Select the middle tab so the screenshot shows non-default selection.
        bar.set("Files")

    return finalize


def notebook(parent: tkinter.Widget) -> None:
    """Notebook with Home / Settings / About; Home active."""
    box = ttk.Frame(parent, width=440, height=200)
    box.pack_propagate(False)
    box.pack()
    nb = ttk.Notebook(box)
    nb.pack(fill="both", expand=True)
    home = nb.add(text="Home", key="home")
    settings = nb.add(text="Settings", key="settings")
    about = nb.add(text="About", key="about")
    ttk.Label(home, text="Welcome", font="heading[16]").pack(anchor="w", padx=12, pady=(12, 4))
    ttk.Label(home, text="Pick a section to begin.").pack(anchor="w", padx=12)
    ttk.CheckButton(settings, text="Auto-save").pack(anchor="w", padx=12, pady=12)
    ttk.Label(about, text="Version 1.0").pack(padx=12, pady=12)


def pagestack(parent: tkinter.Widget) -> None:
    """PageStack on the "details" page with forward/back actions visible."""
    box = ttk.Frame(parent, width=440, height=180)
    box.pack_propagate(False)
    box.pack()
    stack = ttk.PageStack(box, padding=12)
    stack.pack(fill="both", expand=True)

    page1 = stack.add("start", padding=12)
    page2 = stack.add("details", padding=12)
    page3 = stack.add("confirm", padding=12)

    ttk.Label(page1, text="Start page").pack()
    ttk.Label(page2, text="Details", font="heading[14]").pack(anchor="w")
    ttk.Label(page2, text="Step 2 of 3 — review the request").pack(anchor="w", pady=(4, 12))
    row = ttk.Frame(page2)
    row.pack(fill="x")
    ttk.Button(row, text="Back", bootstyle="secondary").pack(side="left")
    ttk.Button(row, text="Next").pack(side="right")
    ttk.Label(page3, text="Confirm page").pack()
    stack.navigate("details")


def tabview(parent: tkinter.Widget) -> None:
    """TabView with Home / Files / Settings tabs and content for the active one."""
    box = ttk.Frame(parent, width=440, height=200)
    box.pack_propagate(False)
    box.pack()
    tv = ttk.TabView(box)
    tv.pack(fill="both", expand=True)
    home = tv.add("home", text="Home", icon="house")
    files = tv.add("files", text="Files", icon="folder2")
    settings = tv.add("settings", text="Settings", icon="gear")
    ttk.Label(home, text="Welcome to the Home page!").pack(padx=20, pady=20)
    ttk.Label(files, text="Browse your files here.").pack(padx=20, pady=20)
    ttk.Label(settings, text="Configure your settings.").pack(padx=20, pady=20)
