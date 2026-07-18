"""Screenshot scenes for docs/user-guide/feature-guides/icons.rst."""

import ttkbootstrap as ttk


def matrix():
    # A matrix of varied glyphs -- an icon is a visual idea, so the page opens on
    # the breadth of the set (2,000+ glyphs) in the semantic colors.
    app = ttk.App(title="Bootstrap Icons")
    grid = ttk.Frame(app, padding=16)
    grid.pack()
    cells = [
        ("house-fill", "primary"), ("search", "secondary"), ("bell-fill", "warning"),
        ("envelope-fill", "info"), ("heart-fill", "danger"), ("star-fill", "warning"),
        ("gear-fill", "secondary"), ("person-fill", "primary"),
        ("folder-fill", "warning"), ("file-earmark-text", "info"), ("calendar-event", "danger"),
        ("clock-fill", "secondary"), ("camera-fill", "primary"), ("music-note-beamed", "success"),
        ("cloud-fill", "info"), ("geo-alt-fill", "danger"),
        ("check-circle-fill", "success"), ("exclamation-triangle-fill", "warning"),
        ("trash-fill", "danger"), ("download", "success"), ("upload", "info"),
        ("pencil-fill", "primary"), ("lock-fill", "dark"), ("lightning-fill", "warning"),
    ]
    cols = 8
    for i, (name, style) in enumerate(cells):
        ttk.Button(grid, icon=name, icon_only=True, bootstyle=style).grid(
            row=i // cols, column=i % cols, padx=3, pady=3)
    app.mainloop()


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
    "matrix": matrix,
    "toolbar": toolbar,
}
