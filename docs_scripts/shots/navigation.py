"""Shot factories for navigation widget pages.

Covers Toolbar, SideNav, AppShell. The Tabs widget shot lives in
`views.py` next to Notebook/PageStack/TabView since they share a
visual theme (tabbed content panes).
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def toolbar(parent: tkinter.Widget) -> None:
    """Toolbar with menu/title/spacer/action layout."""
    box = ttk.Frame(parent, width=520)
    box.pack()
    bar = ttk.Toolbar(box, surface="chrome")
    bar.pack(fill="x")
    bar.add_button(icon="list")
    bar.add_separator()
    bar.add_label(text="My App", font="heading[14]")
    bar.add_spacer()
    bar.add_button(icon="bell")
    bar.add_button(icon="gear")


def sidenav(parent: tkinter.Widget) -> None:
    """SideNav with title, three nav items, a header, and a footer item."""
    box = ttk.Frame(parent, width=300, height=420)
    box.pack_propagate(False)
    box.pack()
    nav = ttk.SideNav(box, title="My App")
    nav.pack(side="left", fill="y")
    nav.add_item("home", text="Home", icon="house")
    nav.add_item("docs", text="Documents", icon="file-earmark-text")
    nav.add_item("inbox", text="Inbox", icon="inbox")
    nav.add_separator()
    nav.add_header("Favorites")
    nav.add_item("photos", text="Photos", icon="image")
    nav.add_footer_item("settings", text="Settings", icon="gear")
    nav.select("home")


def appshell(parent: tkinter.Widget) -> None:
    """Toolbar + SideNav + content area mock — illustrates AppShell layout.

    AppShell extends App (a window), so it can't be embedded directly.
    This composition reproduces the AppShell layout using its constituent
    widgets so the screenshot still conveys the shape it gives an app.
    """
    box = ttk.Frame(parent, width=720, height=400)
    box.pack_propagate(False)
    box.pack()

    bar = ttk.Toolbar(box, surface="chrome")
    bar.pack(fill="x")
    bar.add_button(icon="list")
    bar.add_separator()
    bar.add_label(text="My App", font="heading[14]")
    bar.add_spacer()
    bar.add_button(icon="bell")
    bar.add_button(icon="gear")

    body = ttk.Frame(box)
    body.pack(fill="both", expand=True)

    nav = ttk.SideNav(body, title="", show_header=False, collapsible=False)
    nav.pack(side="left", fill="y")
    nav.add_item("home", text="Home", icon="house")
    nav.add_item("docs", text="Documents", icon="file-earmark-text")
    nav.add_item("inbox", text="Inbox", icon="inbox")
    nav.add_separator()
    nav.add_item("settings", text="Settings", icon="gear")
    nav.select("home")

    content = ttk.Frame(body, padding=24)
    content.pack(side="left", fill="both", expand=True)
    ttk.Label(content, text="Home", font="heading[20]").pack(anchor="w")
    ttk.Label(
        content,
        text="Welcome back. Pick a section from the sidebar to get started.",
        bootstyle="secondary",
    ).pack(anchor="w", pady=(4, 16))
    ttk.Button(content, text="Open dashboard", accent="primary").pack(anchor="w")
