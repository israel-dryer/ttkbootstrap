"""Shot factories for `docs/widgets/selection/checkbutton.md`."""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def states(parent: tkinter.Widget) -> None:
    # unchecked
    b1 = ttk.CheckButton(parent)
    b1.pack(side="left", padx=10)
    b1.invoke()
    b1.invoke()
    # checked
    b2 = ttk.CheckButton(parent)
    b2.pack(side="left", padx=10)
    b2.invoke()
    # unchecked disabled
    b3 = ttk.CheckButton(parent)
    b3.pack(side="left", padx=10)
    b3.invoke()
    b3.invoke()
    b3["state"] = "disabled"
    # checked disabled
    b4 = ttk.CheckButton(parent)
    b4.pack(side="left", padx=10)
    b4.invoke()
    b4["state"] = "disabled"


def indeterminate(parent: tkinter.Widget) -> None:
    b1 = ttk.CheckButton(parent)
    b1.pack(side="left", padx=10)
    b2 = ttk.CheckButton(parent)
    b2.pack(side="left", padx=10)
    b2["state"] = "disabled"


def toggle(parent: tkinter.Widget) -> None:
    off = ttk.CheckButton(parent, bootstyle="toggle")
    off.pack(side="left", padx=10)
    off.state(["!selected"])
    on = ttk.CheckButton(parent, bootstyle="toggle")
    on.pack(side="left", padx=10)
    on.state(["selected"])


def labeled(parent: tkinter.Widget) -> None:
    cb = ttk.CheckButton(parent, text="checkbutton")
    cb.pack(side="left", padx=10)
    cb.state(["!selected"])
    tg = ttk.CheckButton(parent, text="toggle", bootstyle="toggle")
    tg.pack(side="left", padx=10)
    tg.state(["selected"])


def colors(parent: tkinter.Widget) -> None:
    """Two rows: standard CheckButtons (top), toggle variants (bottom)."""
    top = ttk.Frame(parent)
    top.pack(side="top", anchor="w")
    for color in ["primary", "secondary", "success", "info", "warning", "danger", "light", "dark"]:
        b = ttk.CheckButton(top, bootstyle=color)
        b.pack(side="left", padx=8)
        b.invoke()
    bottom = ttk.Frame(parent)
    bottom.pack(side="top", anchor="w", pady=(8, 0))
    for color in ["primary", "secondary", "success", "info", "warning", "danger", "light", "dark"]:
        b = ttk.CheckButton(bottom, bootstyle=color + "-toggle")
        b.pack(side="left")
        b.invoke()
