"""Screenshot scenes for docs/user-guide/foundations/bootstyle-grammar.rst."""

import ttkbootstrap as ttk


def colors():
    app = ttk.App(title="bootstyle — colors")
    row = ttk.Frame(app, padding=20).pack()
    for color in ["primary", "secondary", "success", "info", "warning", "danger"]:
        ttk.Button(row, text=color.title(), bootstyle=color).pack(side="left", padx=3)
    app.mainloop()


def weights():
    app = ttk.App(title="bootstyle — weights")
    row = ttk.Frame(app, padding=20).pack()
    ttk.Button(row, text="Solid", bootstyle="primary").pack(side="left", padx=4)
    ttk.Button(row, text="Outline", bootstyle="primary outline").pack(side="left", padx=4)
    ttk.Button(row, text="Link", bootstyle="primary link").pack(side="left", padx=4)
    ttk.Button(row, text="Ghost", bootstyle="primary ghost").pack(side="left", padx=4)
    app.mainloop()


SCENES = {
    "colors": colors,
    "weights": weights,
}
