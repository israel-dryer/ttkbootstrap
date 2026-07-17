"""Screenshot scenes for docs/widgets/checkbutton.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Checkbutton")
    frm = ttk.Frame(app, padding=20).pack()
    keep = []

    def make(row, col, text, style, value):
        var = ttk.BooleanVar(value=value)
        keep.append(var)
        ttk.Checkbutton(frm, text=text, variable=var, bootstyle=style).grid(
            row=row, column=col, padx=10, pady=6, sticky="w")

    make(0, 0, "I agree", "", True)
    make(1, 0, "I agree", "", False)
    make(0, 1, "Wi-Fi", "round toggle", True)
    make(1, 1, "Wi-Fi", "round toggle", False)
    make(0, 2, "Bold", "toolbutton", True)
    make(1, 2, "Bold", "toolbutton", False)
    app.mainloop()


def looks():
    app = ttk.App(title="Checkbutton — Looks")
    frm = ttk.Frame(app, padding=20).pack()
    keep = []

    def make(row, col, text, style, value):
        var = ttk.BooleanVar(value=value)
        keep.append(var)
        ttk.Checkbutton(frm, text=text, variable=var, bootstyle=style).grid(
            row=row, column=col, padx=10, pady=6, sticky="w")

    make(0, 0, "Wi-Fi", "round toggle", True)
    make(1, 0, "Wi-Fi", "round toggle", False)
    make(0, 1, "Wi-Fi", "square toggle", True)
    make(1, 1, "Wi-Fi", "square toggle", False)
    make(0, 2, "Bold", "toolbutton", True)
    make(1, 2, "Bold", "toolbutton", False)
    app.mainloop()


SCENES = {
    "hero": hero,
    "looks": looks,
}
