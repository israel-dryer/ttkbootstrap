"""Screenshot scenes for docs/widgets/floodgauge.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets import Floodgauge


def hero():
    app = ttk.App(title="Floodgauge", size=(320, 90))
    frm = ttk.Frame(app, padding=20).pack(fill="both", expand=True)
    progress = ttk.IntVar(value=75)
    Floodgauge(frm, variable=progress, maximum=100, mask="{}% complete",
               bootstyle="info").pack(fill="x")
    app.mainloop()


SCENES = {
    "hero": hero,
}
