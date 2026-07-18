"""Screenshot scenes for docs/widgets/panedwindow.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Panedwindow", size=(360, 150))

    paned = ttk.Panedwindow(app, orient=HORIZONTAL)
    paned.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    sidebar = ttk.Frame(paned, padding=10)
    ttk.Label(sidebar, text="Sidebar").pack()
    paned.add(sidebar, weight=1)

    content = ttk.Frame(paned, padding=10)
    ttk.Label(content, text="Content").pack()
    paned.add(content, weight=4)

    def split():
        paned.sashpos(0, 110)

    app.after(300, split)
    app._capture_full_window = True  # panes fill the window — show the chrome
    app.mainloop()


SCENES = {
    "hero": hero,
}
