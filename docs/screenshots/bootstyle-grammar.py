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


def value_tokens():
    app = ttk.App(title="bootstyle — value tokens")
    outer = ttk.Frame(app, padding=20).pack()
    # raw hex accents: each button IS that color, text auto-contrasted
    hexrow = ttk.Frame(outer).pack(anchor="w")
    for hexcode in ["#2f2f2f", "#e63946", "#2a9d8f", "#e9c46a"]:
        ttk.Button(hexrow, text=hexcode, bootstyle=hexcode).pack(side="left", padx=3)
    # ramp accents: the primary role stepped from a light tint to a dark shade
    ramprow = ttk.Frame(outer).pack(anchor="w", pady=(10, 0))
    for stop in [200, 400, 500, 600, 800]:
        token = f"primary[{stop}]"
        ttk.Button(ramprow, text=token, bootstyle=token).pack(side="left", padx=3)
    app.mainloop()


SCENES = {
    "colors": colors,
    "weights": weights,
    "value_tokens": value_tokens,
}
