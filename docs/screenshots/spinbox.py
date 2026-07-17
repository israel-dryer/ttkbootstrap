"""Screenshot scenes for docs/widgets/spinbox.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Spinbox")
    frm = ttk.Frame(app, padding=20).pack()
    ttk.Label(frm, text="Quantity").grid(row=0, column=0, padx=(0, 8), pady=4, sticky="e")
    quantity = ttk.IntVar(value=1)
    ttk.Spinbox(frm, from_=1, to=10, increment=1, textvariable=quantity,
                width=12).grid(row=0, column=1, pady=4)
    ttk.Label(frm, text="Size").grid(row=1, column=0, padx=(0, 8), pady=4, sticky="e")
    size = ttk.Spinbox(frm, values=["Small", "Medium", "Large"], wrap=True, width=12)
    size.grid(row=1, column=1, pady=4)
    size.set("Medium")
    app.mainloop()


SCENES = {
    "hero": hero,
}
