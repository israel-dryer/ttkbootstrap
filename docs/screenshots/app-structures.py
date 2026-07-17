"""Screenshot scenes for docs/user-guide/getting-started/app-structures.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Sidebar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8, bootstyle="card")
        ttk.Button(self, text="Home").pack(fill=X, pady=2)
        ttk.Button(self, text="Settings").pack(fill=X, pady=2)


class Content(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        ttk.Label(self, text="Content area", font="-size 16").pack(anchor=NW)


class MyApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        Sidebar(self).pack(side=LEFT, fill=Y)
        Content(self).pack(side=LEFT, fill=BOTH, expand=YES)


def skeleton():
    app = ttk.App(title="My App", size=(460, 280))
    MyApp(app)
    app._capture_full_window = True  # a composed app — show the window chrome
    app.mainloop()


SCENES = {
    "skeleton": skeleton,
}
