"""Screenshot scenes for docs/widgets/frame.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Frame", size=(320, 140))

    header = ttk.Frame(app, padding=10, bootstyle="primary").pack(fill=X)
    ttk.Label(header, text="Dashboard", bootstyle="inverse-primary").pack()

    content = ttk.Frame(app, padding=20).pack(fill=BOTH, expand=YES)
    ttk.Label(content, text="Body goes here").pack()

    app._capture_full_window = True  # a composed layout — show the window chrome
    app.mainloop()


SCENES = {
    "hero": hero,
}
