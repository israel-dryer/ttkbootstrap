"""Screenshot scenes for docs/widgets/notebook.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Notebook", size=(340, 160))

    notebook = ttk.Notebook(app)
    notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for name in ["General", "Display", "Advanced"]:
        page = ttk.Frame(notebook, padding=16)
        ttk.Label(page, text=f"{name} settings").pack()
        notebook.add(page, text=name)

    notebook.select(1)  # middle tab selected

    app._capture_full_window = True  # a tabbed container fills the window
    app.mainloop()


SCENES = {
    "hero": hero,
}
