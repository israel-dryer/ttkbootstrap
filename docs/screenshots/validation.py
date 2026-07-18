"""Screenshot scenes for docs/user-guide/feature-guides/validation.rst."""

import ttkbootstrap as ttk


def _age(app, value):
    frm = ttk.Frame(app, padding=20)
    frm.pack(fill="both", expand=True)
    ttk.Label(frm, text="Age (0–120)").pack(anchor="w", pady=(0, 4))
    age = ttk.Entry(frm, width=18)
    age.insert(0, value)
    age.pack()
    ttk.Validation.range(age, 0, 120)
    app.after(300, age.validate)   # run the rule once -> flags on failure
    app.mainloop()


def valid():
    _age(ttk.App(title="Validation"), "42")


def invalid():
    _age(ttk.App(title="Validation"), "200")


SCENES = {
    "valid": valid,
    "invalid": invalid,
}
