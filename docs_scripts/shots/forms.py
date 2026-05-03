"""Shot factories for `docs/widgets/forms/*.md` widgets.

Currently Form only — additional form-related composites will live here.
"""

from __future__ import annotations

import tkinter

import ttkbootstrap as ttk


def form(parent: tkinter.Widget) -> None:
    """Form with three fields demonstrating the spec-driven layout."""
    from ttkbootstrap.widgets.composites.form import FieldItem, Form

    box = ttk.Frame(parent, padding=8, width=440)
    box.pack()
    Form(
        box,
        data={"name": "Alex Chen", "age": 34, "status": "In Progress"},
        items=[
            FieldItem(key="name", label="Name", editor="textentry"),
            FieldItem(key="age", label="Age", dtype="int", editor="numericentry"),
            FieldItem(
                key="status",
                label="Status",
                editor="selectbox",
                editor_options={"items": ["New", "In Progress", "Done"]},
            ),
        ],
    ).pack(fill="x")
