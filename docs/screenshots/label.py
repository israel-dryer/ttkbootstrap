"""Screenshot scenes for docs/widgets/label.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Label")
    frm = ttk.Frame(app, padding=20).pack()
    ttk.Label(frm, text="Quarterly report", font="-size 16 -weight bold").pack(anchor="w")
    ttk.Label(frm, text="Ready", bootstyle="success").pack(anchor="w", pady=(6, 0))
    app.mainloop()


SCENES = {
    "hero": hero,
}
