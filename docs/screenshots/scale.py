"""Screenshot scenes for docs/widgets/scale.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Scale")
    frm = ttk.Frame(app, padding=20).pack()
    volume = ttk.DoubleVar(value=30)
    ttk.Scale(frm, from_=0, to=100, variable=volume, length=240).pack()
    app.mainloop()


SCENES = {
    "hero": hero,
}
