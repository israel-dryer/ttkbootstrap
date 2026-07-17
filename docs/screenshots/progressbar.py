"""Screenshot scenes for docs/widgets/progressbar.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Progressbar", size=(320, 100))
    frm = ttk.Frame(app, padding=20).pack(fill="both", expand=True)
    progress = ttk.IntVar(value=65)
    ttk.Progressbar(frm, variable=progress, maximum=100,
                    bootstyle="success").pack(fill="x")
    busy = ttk.Progressbar(frm, mode="indeterminate")
    busy.pack(fill="x", pady=(12, 0))
    busy.start()
    app.mainloop()


SCENES = {
    "hero": hero,
}
