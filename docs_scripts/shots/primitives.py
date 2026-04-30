"""Shot factories for `docs/widgets/primitives/*.md` widgets.

Covers Entry, Combobox, Spinbox, Text, Canvas.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def entry(parent: tkinter.Widget) -> None:
    """Three Entry instances showing typical states."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    e1 = ttk.Entry(column, width=24)
    e1.insert(0, "Active")
    e1.pack(pady=4)
    e2 = ttk.Entry(column, width=24)
    e2.insert(0, "Readonly")
    e2.configure(state="readonly")
    e2.pack(pady=4)
    e3 = ttk.Entry(column, width=24)
    e3.insert(0, "Disabled")
    e3.configure(state="disabled")
    e3.pack(pady=4)


def combobox(parent: tkinter.Widget) -> None:
    """A readonly Combobox showing the current value."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    ttk.Label(column, text="Priority").pack(anchor="w", pady=(0, 4))
    cb = ttk.Combobox(column, values=["Low", "Medium", "High"], state="readonly", width=20)
    cb.set("Medium")
    cb.pack(anchor="w")


def spinbox(parent: tkinter.Widget) -> None:
    """Two Spinbox instances: numeric range and value list."""
    column = ttk.Frame(parent, padding=8)
    column.pack()
    ttk.Label(column, text="Quantity").pack(anchor="w", pady=(0, 4))
    s1 = ttk.Spinbox(column, from_=0, to=10, increment=1, width=12)
    s1.set(5)
    s1.pack(anchor="w", pady=(0, 8))
    ttk.Label(column, text="Size").pack(anchor="w", pady=(0, 4))
    s2 = ttk.Spinbox(column, values=["Small", "Medium", "Large"], width=12)
    s2.set("Medium")
    s2.pack(anchor="w")


def text(parent: tkinter.Widget) -> None:
    """Plain Text widget with multi-line content."""
    box = ttk.Frame(parent, width=440, height=160, padding=4)
    box.pack_propagate(False)
    box.pack()
    t = ttk.Text(box, wrap="word", height=8, width=50)
    t.pack(fill="both", expand=True)
    t.insert(
        "end",
        "Text supports rich multi-line content.\n\n"
        "Use it for editors, log viewers, notes, and any place where "
        "users need to scroll through paragraphs of text.\n",
    )


def canvas(parent: tkinter.Widget) -> None:
    """Canvas with a few primitive shapes."""
    box = ttk.Frame(parent, padding=4)
    box.pack()
    c = ttk.Canvas(box, width=420, height=160, background="white", highlightthickness=0)
    c.pack()
    c.create_rectangle(20, 20, 180, 110, fill="#5b6cff", outline="")
    c.create_oval(200, 20, 320, 110, fill="#22c55e", outline="")
    c.create_polygon(360, 110, 400, 30, 410, 110, fill="#f59e0b", outline="")
    c.create_text(20, 130, anchor="w", text="Rectangle, Oval, Polygon", font=("Helvetica", 11))
