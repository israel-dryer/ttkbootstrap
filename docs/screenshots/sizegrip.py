"""Screenshot scenes for docs/widgets/sizegrip.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Sizegrip", size=(300, 120))
    ttk.Label(app, text="Drag the corner to resize").pack(padx=20, pady=20)
    # a little padding keeps the grip clear of the macOS rounded corner
    ttk.Sizegrip(app).pack(side=BOTTOM, anchor=SE, padx=4, pady=4)
    app._capture_full_window = True  # the grip lives in the window's corner
    app.mainloop()


SCENES = {
    "hero": hero,
}
