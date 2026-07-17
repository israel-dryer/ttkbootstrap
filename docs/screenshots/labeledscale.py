"""Screenshot scenes for docs/widgets/labeledscale.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets import LabeledScale


def hero():
    app = ttk.App(title="LabeledScale", size=(300, 100))
    frm = ttk.Frame(app, padding=20).pack(fill="both", expand=True)
    level = ttk.IntVar(value=40)
    ls = LabeledScale(frm, variable=level, from_=0, to=100,
                      bootstyle="info").pack(fill="x")
    ls.value = 40
    app.mainloop()


SCENES = {
    "hero": hero,
}
