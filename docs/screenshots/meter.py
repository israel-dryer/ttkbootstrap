"""Screenshot scenes for docs/widgets/meter.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Meter


def hero():
    app = ttk.App(title="Meter")
    frm = ttk.Frame(app, padding=16).pack()
    Meter(frm, amount_used=65, amount_total=100, subtext="storage used",
          bootstyle="success").pack()
    app.mainloop()


def types():
    app = ttk.App(title="Meter — Full and Semi")
    frm = ttk.Frame(app, padding=16).pack()
    Meter(frm, amount_used=65, meter_size=170,
          subtext="full").pack(side=LEFT, padx=8)
    Meter(frm, amount_used=65, meter_type="semi", meter_size=170,
          subtext="semi").pack(side=LEFT, padx=8)
    app.mainloop()


def interactive():
    app = ttk.App(title="Meter — Interactive")
    frm = ttk.Frame(app, padding=16).pack()
    Meter(frm, amount_used=30, interactive=True, subtext="volume").pack()
    app.mainloop()


def striped():
    app = ttk.App(title="Meter — Striped")
    frm = ttk.Frame(app, padding=16).pack()
    Meter(frm, amount_used=65, stripe_thickness=10, meter_size=170,
          bootstyle="info", subtext="striped").pack(side=LEFT, padx=8)
    Meter(frm, amount_used=65, meter_size=170, bootstyle="info",
          subtext="solid").pack(side=LEFT, padx=8)
    app.mainloop()


def colors():
    app = ttk.App(title="Meter — Colors")
    frm = ttk.Frame(app, padding=16).pack()
    for color in ["primary", "success", "info", "warning", "danger"]:
        Meter(frm, amount_used=50, meter_size=120,
              bootstyle=color).pack(side=LEFT, padx=4)
    app.mainloop()


SCENES = {
    "hero": hero,
    "types": types,
    "interactive": interactive,
    "striped": striped,
    "colors": colors,
}
