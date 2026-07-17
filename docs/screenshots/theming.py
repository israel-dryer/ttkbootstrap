"""Screenshot scenes for docs/user-guide/feature-guides/theming.rst."""

import ttkbootstrap as ttk


def sample():
    # A small representative window; the harness captures it once per theme
    # (bootstrap-light / bootstrap-dark), and the page shows the pair side by
    # side to compare a family's matched light/dark surfaces. Auto-sized (no
    # explicit size) so the content fills it -- no dead space under the buttons.
    app = ttk.App(title="Accounts")
    app.minsize(300, 1)
    ttk.Label(app, text="  Dashboard", bootstyle="@primary").pack(fill="x", ipady=8)

    body = ttk.Frame(app, padding=16)
    body.pack(fill="both", expand=True)
    ttk.Label(body, text="Balance").pack(anchor="w")
    ttk.Entry(body).pack(fill="x", pady=(2, 12))

    row = ttk.Frame(body)
    row.pack(fill="x", pady=(0, 12))
    for color in ["primary", "success", "danger"]:
        ttk.Button(row, text=color.title(), bootstyle=color).pack(side="left", padx=(0, 6))

    ttk.Checkbutton(body, text="Email me updates",
                    bootstyle="success round toggle").pack(anchor="w", pady=(0, 12))
    pb = ttk.Progressbar(body, value=66, bootstyle="info")
    pb.pack(fill="x")

    app._capture_full_window = True
    app.mainloop()


SCENES = {
    "sample": sample,
}
