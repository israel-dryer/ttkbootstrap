"""Screenshot scenes for docs/widgets/entry.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Entry")
    frm = ttk.Frame(app, padding=20).pack()
    ttk.Label(frm, text="Name").grid(row=0, column=0, padx=(0, 8), pady=4, sticky="e")
    name = ttk.StringVar(value="Ada Lovelace")
    ttk.Entry(frm, textvariable=name, width=24).grid(row=0, column=1, pady=4)
    ttk.Label(frm, text="Email").grid(row=1, column=0, padx=(0, 8), pady=4, sticky="e")
    email = ttk.StringVar(value="not-an-email")
    bad = ttk.Entry(frm, textvariable=email, width=24)
    bad.grid(row=1, column=1, pady=4)
    bad.state(["invalid", "focus"])  # a failed validation, field focused
    app.mainloop()


SCENES = {
    "hero": hero,
}
