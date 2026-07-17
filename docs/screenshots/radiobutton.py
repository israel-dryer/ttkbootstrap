"""Screenshot scenes for docs/widgets/radiobutton.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Radiobutton")
    frm = ttk.Frame(app, padding=20).pack()

    size = ttk.StringVar(value="medium")
    stack = ttk.Frame(frm).pack(side=LEFT, padx=(0, 24))
    for label in ["small", "medium", "large"]:
        ttk.Radiobutton(stack, text=label.title(), variable=size,
                        value=label).pack(anchor="w", pady=2)

    view = ttk.StringVar(value="list")
    group = ttk.Frame(frm).pack(side=LEFT)
    for label in ["list", "grid", "columns"]:
        ttk.Radiobutton(group, text=label.title(), variable=view, value=label,
                        bootstyle="toolbutton").pack(side=LEFT)

    app.mainloop()


def toolbutton():
    app = ttk.App(title="Radiobutton — Toolbutton")
    frm = ttk.Frame(app, padding=20).pack()
    view = ttk.StringVar(value="grid")  # middle option selected
    for label in ["list", "grid", "columns"]:
        ttk.Radiobutton(frm, text=label.title(), variable=view, value=label,
                        bootstyle="toolbutton").pack(side=LEFT)
    app.mainloop()


SCENES = {
    "hero": hero,
    "toolbutton": toolbutton,
}
