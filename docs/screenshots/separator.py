"""Screenshot scenes for docs/widgets/separator.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Separator", size=(280, 130))
    frm = ttk.Frame(app, padding=20).pack(fill=BOTH, expand=YES)
    ttk.Label(frm, text="Account").pack(anchor=W)
    ttk.Separator(frm, orient=HORIZONTAL).pack(fill=X, pady=10)
    ttk.Label(frm, text="Privacy").pack(anchor=W)
    app.mainloop()


SCENES = {
    "hero": hero,
}
