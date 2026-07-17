"""Screenshot scenes for docs/widgets/scrollbar.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

LINES = [
    "Chapter 1 — Getting started",
    "Install the package, create an App, and",
    "add your first widgets. Themes apply to",
    "every widget automatically.",
    "",
    "Chapter 2 — Layout",
    "Arrange widgets with pack and grid, and",
    "group them in frames.",
    "",
    "Chapter 3 — Styling",
    "Use bootstyle to color any widget from",
    "the semantic palette.",
]


def hero():
    app = ttk.App(title="Scrollbar")
    frm = ttk.Frame(app, padding=10).pack(fill=BOTH, expand=YES)

    text = ttk.Text(frm, height=8, width=40)
    scroll = ttk.Scrollbar(frm, orient=VERTICAL, command=text.yview)
    text.configure(yscrollcommand=scroll.set)

    text.pack(side=LEFT, fill=BOTH, expand=YES)
    scroll.pack(side=RIGHT, fill=Y)

    text.insert("1.0", "\n".join(LINES))
    text.yview_scroll(3, "units")  # scrolled partway so the thumb is mid-track

    app.mainloop()


SCENES = {
    "hero": hero,
}
