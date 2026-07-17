"""Screenshot scenes for docs/user-guide/feature-guides/icons.rst."""

import ttkbootstrap as ttk


def toolbar():
    app = ttk.App(title="Icons")
    bar = ttk.Frame(app, padding=10)
    bar.pack()
    for name, style in [("house-fill", "primary"),
                        ("gear-fill", "secondary"),
                        ("trash-fill", "danger")]:
        ttk.Button(bar, icon=name, icon_only=True, bootstyle=style).pack(
            side="left", padx=2)
    ttk.Button(bar, text="Save", icon="check-lg", bootstyle="success").pack(
        side="left", padx=(12, 0))
    app.mainloop()


SCENES = {
    "toolbar": toolbar,
}
