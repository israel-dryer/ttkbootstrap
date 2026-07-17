"""Screenshot scenes for docs/widgets/labelframe.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def hero():
    app = ttk.App(title="Labelframe", size=(300, 190))

    contact = ttk.Labelframe(app, text="Contact", padding=12)
    contact.pack(fill=X, padx=10, pady=10)

    ttk.Label(contact, text="Name").pack(anchor=W)
    ttk.Entry(contact).pack(fill=X)
    ttk.Label(contact, text="Email").pack(anchor=W, pady=(8, 0))
    ttk.Entry(contact).pack(fill=X)

    app.mainloop()


SCENES = {
    "hero": hero,
}
