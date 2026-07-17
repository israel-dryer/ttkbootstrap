"""Screenshot scenes for docs/user-guide/feature-guides/theming.rst."""

import ttkbootstrap as ttk


def sample():
    # A small representative window; the harness captures it once per theme
    # (bootstrap-light / bootstrap-dark), and the page shows the pair side by
    # side to compare a family's matched light/dark surfaces.
    app = ttk.App(title="Dashboard", size=(280, 210))
    ttk.Label(app, text="  Dashboard", bootstyle="@primary").pack(fill="x", ipady=8)
    body = ttk.Frame(app, padding=16)
    body.pack(fill="both", expand=True)
    ttk.Label(body, text="Balance").pack(anchor="w")
    ttk.Entry(body).pack(fill="x", pady=(2, 10))
    row = ttk.Frame(body)
    row.pack(anchor="w")
    ttk.Button(row, text="Save", bootstyle="primary").pack(side="left", padx=(0, 6))
    ttk.Button(row, text="Cancel", bootstyle="secondary outline").pack(side="left")
    app._capture_full_window = True
    app.mainloop()


SCENES = {
    "sample": sample,
}
