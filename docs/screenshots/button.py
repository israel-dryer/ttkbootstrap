"""Screenshot scenes for docs/widgets/button.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Button")
    row = ttk.Frame(app, padding=20).pack()
    ttk.Button(row, text="Save", bootstyle="primary").pack(side=LEFT, padx=4)
    ttk.Button(row, text="Edit", bootstyle="outline").pack(side=LEFT, padx=4)
    ttk.Button(row, text="Learn more", bootstyle="link").pack(side=LEFT, padx=4)
    ttk.Button(row, icon="trash", icon_only=True, bootstyle="danger").pack(side=LEFT, padx=4)
    app.mainloop()


def icons():
    app = ttk.App(title="Button — Icons")
    row = ttk.Frame(app, padding=20).pack()
    ttk.Button(row, text="Save", icon="save", bootstyle="success").pack(side=LEFT, padx=4)
    ttk.Button(row, text="Next", icon="arrow-right", compound=RIGHT, bootstyle="primary").pack(side=LEFT, padx=4)
    ttk.Button(row, icon="trash", icon_only=True, bootstyle="danger").pack(side=LEFT, padx=4)
    app.mainloop()


def colors():
    app = ttk.App(title="Button — Colors")
    row = ttk.Frame(app, padding=20).pack()
    for color in ["neutral", "primary", "secondary", "success", "info",
                  "warning", "danger", "light", "dark"]:
        ttk.Button(row, text=color.title(), bootstyle=color).pack(side=LEFT, padx=3)
    app.mainloop()


SCENES = {
    "hero": hero,
    "icons": icons,
    "colors": colors,
}
